# terraform/main.tf
# GEESP-Angola Terraform Configuration - Production Ready

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket         = "geesp-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = "GEESP-Angola"
      Environment = var.environment
      ManagedBy   = "Terraform"
      CreatedAt   = timestamp()
    }
  }
}

# ============================================================================
# DATA SOURCES
# ============================================================================

data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical
  
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

data "aws_caller_identity" "current" {}

# ============================================================================
# VPC & NETWORKING
# ============================================================================

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"
  
  name = "geesp-vpc-${var.environment}"
  cidr = "10.0.0.0/16"
  
  azs             = data.aws_availability_zones.available.names
  private_subnets = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  
  enable_nat_gateway = true
  single_nat_gateway = var.environment != "production" ? true : false
  one_nat_gateway_per_az = var.environment == "production" ? true : false
  
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  public_subnet_tags = {
    Type = "Public"
  }
  
  private_subnet_tags = {
    Type = "Private"
  }
  
  tags = {
    Name = "geesp-vpc-${var.environment}"
  }
}

# ============================================================================
# SECURITY GROUPS
# ============================================================================

resource "aws_security_group" "bastion" {
  name_prefix = "geesp-bastion-"
  description = "Bastion host security group"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "SSH from anywhere"
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "All outbound traffic"
  }
  
  tags = {
    Name = "geesp-bastion-sg-${var.environment}"
  }
}

resource "aws_security_group" "app" {
  name_prefix = "geesp-app-"
  description = "Application server security group"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion.id]
    description     = "SSH from bastion"
  }
  
  ingress {
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
    description     = "FastAPI from ALB"
  }
  
  ingress {
    from_port       = 8501
    to_port         = 8501
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
    description     = "Streamlit from ALB"
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "geesp-app-sg-${var.environment}"
  }
}

resource "aws_security_group" "alb" {
  name_prefix = "geesp-alb-"
  description = "ALB security group"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP"
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS"
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "geesp-alb-sg-${var.environment}"
  }
}

resource "aws_security_group" "rds" {
  name_prefix = "geesp-rds-"
  description = "RDS security group"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
    description     = "PostgreSQL from app servers"
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "geesp-rds-sg-${var.environment}"
  }
}

# ============================================================================
# RDS DATABASE
# ============================================================================

resource "aws_db_subnet_group" "geesp" {
  name_prefix = "geesp-"
  subnet_ids  = module.vpc.private_subnets
  
  tags = {
    Name = "geesp-db-subnet-${var.environment}"
  }
}

resource "random_password" "db_password" {
  length  = 32
  special = true
}

resource "aws_rds_cluster_parameter_group" "geesp" {
  family      = "aurora-postgresql14"
  name_prefix = "geesp-"
  
  parameter {
    name  = "log_statement"
    value = "all"
  }
  
  tags = {
    Name = "geesp-db-param-group-${var.environment}"
  }
}

resource "aws_rds_cluster" "geesp" {
  cluster_identifier      = "geesp-db-${var.environment}"
  engine                  = "aurora-postgresql"
  engine_version          = "14.7"
  database_name           = "geesp_db"
  master_username         = "admin"
  master_password         = random_password.db_password.result
  db_subnet_group_name    = aws_db_subnet_group.geesp.name
  vpc_security_group_ids  = [aws_security_group.rds.id]
  
  backup_retention_period = var.environment == "production" ? 30 : 7
  preferred_backup_window = "02:00-03:00"
  preferred_maintenance_window = "sun:03:00-sun:04:00"
  
  enabled_cloudwatch_logs_exports = ["postgresql"]
  storage_encrypted               = var.environment == "production" ? true : false
  
  skip_final_snapshot = var.environment == "production" ? false : true
  
  tags = {
    Name = "geesp-cluster-${var.environment}"
  }
}

resource "aws_rds_cluster_instance" "geesp" {
  count              = var.environment == "production" ? 2 : 1
  cluster_identifier = aws_rds_cluster.geesp.id
  instance_class     = var.db_instance_class
  engine             = aws_rds_cluster.geesp.engine
  engine_version     = aws_rds_cluster.geesp.engine_version
  
  performance_insights_enabled = var.environment == "production" ? true : false
  
  tags = {
    Name = "geesp-db-instance-${count.index}-${var.environment}"
  }
}

# Store database password in Secrets Manager
resource "aws_secretsmanager_secret" "db_password" {
  name                    = "geesp-db-password-${var.environment}"
  recovery_window_in_days = 0
  
  tags = {
    Name = "geesp-db-password-${var.environment}"
  }
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = jsonencode({
    username = "admin"
    password = random_password.db_password.result
    engine   = "postgres"
    host     = aws_rds_cluster.geesp.endpoint
    port     = 5432
    dbname   = "geesp_db"
  })
}

# ============================================================================
# BASTION HOST (EC2)
# ============================================================================

resource "aws_iam_role" "bastion" {
  name_prefix = "geesp-bastion-"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
  
  tags = {
    Name = "geesp-bastion-role-${var.environment}"
  }
}

resource "aws_iam_role_policy_attachment" "bastion_cloudwatch" {
  role       = aws_iam_role.bastion.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

resource "aws_iam_instance_profile" "bastion" {
  name_prefix = "geesp-bastion-"
  role        = aws_iam_role.bastion.name
}

resource "aws_instance" "bastion" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.micro"
  key_name               = var.key_pair_name
  subnet_id              = module.vpc.public_subnets[0]
  iam_instance_profile   = aws_iam_instance_profile.bastion.name
  vpc_security_group_ids = [aws_security_group.bastion.id]
  
  associate_public_ip_address = true
  
  user_data = base64encode(templatefile("${path.module}/scripts/bastion-init.sh", {
    environment = var.environment
  }))
  
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }
  
  root_block_device {
    volume_type           = "gp3"
    volume_size           = 30
    delete_on_termination = true
    encrypted             = true
  }
  
  tags = {
    Name = "geesp-bastion-${var.environment}"
  }
  
  depends_on = [module.vpc]
}

resource "aws_eip" "bastion" {
  instance = aws_instance.bastion.id
  domain   = "vpc"
  
  tags = {
    Name = "geesp-bastion-eip-${var.environment}"
  }
  
  depends_on = [module.vpc]
}

# ============================================================================
# APPLICATION LOAD BALANCER
# ============================================================================

resource "aws_lb" "geesp" {
  name_prefix = "gesp"
  internal    = false
  load_balancer_type = "application"
  subnets     = module.vpc.public_subnets
  security_groups = [aws_security_group.alb.id]
  
  enable_deletion_protection = var.environment == "production" ? true : false
  enable_http2               = true
  enable_cross_zone_load_balancing = true
  
  tags = {
    Name = "geesp-alb-${var.environment}"
  }
}

resource "aws_lb_target_group" "app" {
  name_prefix = "app"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = module.vpc.vpc_id
  target_type = "instance"
  
  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 30
    path                = "/health"
    matcher             = "200-299"
  }
  
  tags = {
    Name = "geesp-app-tg-${var.environment}"
  }
}

resource "aws_lb_listener" "app" {
  load_balancer_arn = aws_lb.geesp.arn
  port              = 80
  protocol          = "HTTP"
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# ============================================================================
# AUTO SCALING GROUP
# ============================================================================

resource "aws_iam_role" "app" {
  name_prefix = "geesp-app-"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "app_ecr" {
  name_prefix = "ecr-"
  role        = aws_iam_role.app.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "ecr:GetAuthorizationToken",
        "ecr:BatchGetImage",
        "ecr:GetDownloadUrlForLayer"
      ]
      Resource = "*"
    }]
  })
}

resource "aws_iam_role_policy" "app_s3" {
  name_prefix = "s3-"
  role        = aws_iam_role.app.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ]
      Resource = [
        aws_s3_bucket.data.arn,
        "${aws_s3_bucket.data.arn}/*"
      ]
    }]
  })
}

resource "aws_iam_role_policy_attachment" "app_cloudwatch" {
  role       = aws_iam_role.app.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

resource "aws_iam_instance_profile" "app" {
  name_prefix = "geesp-app-"
  role        = aws_iam_role.app.name
}

resource "aws_launch_template" "app" {
  name_prefix   = "geesp-app-"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  key_name      = var.key_pair_name
  
  iam_instance_profile {
    arn = aws_iam_instance_profile.app.arn
  }
  
  vpc_security_group_ids = [aws_security_group.app.id]
  
  user_data = base64encode(templatefile("${path.module}/scripts/app-init.sh", {
    db_endpoint = aws_rds_cluster.geesp.endpoint
    db_password = random_password.db_password.result
    db_name     = "geesp_db"
    environment = var.environment
  }))
  
  block_device_mappings {
    device_name = "/dev/sda1"
    ebs {
      volume_size           = 50
      volume_type           = "gp3"
      delete_on_termination = true
      encrypted             = true
    }
  }
  
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }
  
  monitoring {
    enabled = true
  }
  
  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "geesp-app-instance-${var.environment}"
    }
  }
}

resource "aws_autoscaling_group" "app" {
  name_prefix         = "geesp-app-"
  vpc_zone_identifier = module.vpc.private_subnets
  target_group_arns   = [aws_lb_target_group.app.arn]
  health_check_type   = "ELB"
  health_check_grace_period = 300
  
  min_size         = var.environment == "production" ? 2 : 1
  max_size         = var.environment == "production" ? 6 : 2
  desired_capacity = var.environment == "production" ? 2 : 1
  
  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }
  
  enabled_metrics = [
    "GroupDesiredCapacity",
    "GroupInServiceInstances",
    "GroupTotalInstances"
  ]
  
  tag {
    key                 = "Name"
    value               = "geesp-app-asg-${var.environment}"
    propagate_at_launch = true
  }
}

# CPU-based scaling policy
resource "aws_autoscaling_policy" "app_scale_up" {
  name                   = "geesp-scale-up"
  autoscaling_group_name = aws_autoscaling_group.app.name
  adjustment_type        = "ChangeInCapacity"
  scaling_adjustment     = 1
  cooldown               = 300
}

resource "aws_autoscaling_policy" "app_scale_down" {
  name                   = "geesp-scale-down"
  autoscaling_group_name = aws_autoscaling_group.app.name
  adjustment_type        = "ChangeInCapacity"
  scaling_adjustment     = -1
  cooldown               = 300
}

resource "aws_cloudwatch_metric_alarm" "app_cpu_high" {
  alarm_name          = "geesp-app-cpu-high-${var.environment}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = 70
  alarm_actions       = [aws_autoscaling_policy.app_scale_up.arn]
}

resource "aws_cloudwatch_metric_alarm" "app_cpu_low" {
  alarm_name          = "geesp-app-cpu-low-${var.environment}"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = 30
  alarm_actions       = [aws_autoscaling_policy.app_scale_down.arn]
}

# ============================================================================
# S3 STORAGE
# ============================================================================

resource "aws_s3_bucket" "data" {
  bucket_prefix = "geesp-data-${var.environment}-"
  
  tags = {
    Name = "geesp-data-${var.environment}"
  }
}

resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket = aws_s3_bucket.data.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ============================================================================
# CLOUDWATCH LOGGING
# ============================================================================

resource "aws_cloudwatch_log_group" "geesp" {
  name              = "/geesp-angola/${var.environment}"
  retention_in_days = var.environment == "production" ? 30 : 7
  
  tags = {
    Name = "geesp-logs-${var.environment}"
  }
}
