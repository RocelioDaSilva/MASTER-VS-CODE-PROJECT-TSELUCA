# terraform/outputs.tf

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "bastion_public_ip" {
  description = "Bastion host public IP"
  value       = aws_eip.bastion.public_ip
}

output "bastion_public_dns" {
  description = "Bastion host public DNS name"
  value       = aws_instance.bastion.public_dns
}

output "alb_dns_name" {
  description = "Application Load Balancer DNS name"
  value       = aws_lb.geesp.dns_name
}

output "alb_arn" {
  description = "Application Load Balancer ARN"
  value       = aws_lb.geesp.arn
}

output "rds_endpoint" {
  description = "RDS cluster endpoint"
  value       = aws_rds_cluster.geesp.endpoint
  sensitive   = true
}

output "rds_reader_endpoint" {
  description = "RDS cluster reader endpoint"
  value       = aws_rds_cluster.geesp.reader_endpoint
  sensitive   = true
}

output "rds_port" {
  description = "RDS port"
  value       = aws_rds_cluster.geesp.port
}

output "db_secret_arn" {
  description = "Secrets Manager secret ARN for database credentials"
  value       = aws_secretsmanager_secret.db_password.arn
}

output "s3_bucket_name" {
  description = "S3 data bucket name"
  value       = aws_s3_bucket.data.id
}

output "s3_bucket_arn" {
  description = "S3 data bucket ARN"
  value       = aws_s3_bucket.data.arn
}

output "autoscaling_group_name" {
  description = "Auto Scaling Group name"
  value       = aws_autoscaling_group.app.name
}

output "autoscaling_group_arn" {
  description = "Auto Scaling Group ARN"
  value       = aws_autoscaling_group.app.arn
}

output "cloudwatch_log_group" {
  description = "CloudWatch log group name"
  value       = aws_cloudwatch_log_group.geesp.name
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = module.vpc.private_subnets
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = module.vpc.public_subnets
}

output "app_security_group_id" {
  description = "Application server security group ID"
  value       = aws_security_group.app.id
}

output "bastion_security_group_id" {
  description = "Bastion host security group ID"
  value       = aws_security_group.bastion.id
}

output "rds_security_group_id" {
  description = "RDS security group ID"
  value       = aws_security_group.rds.id
}

output "alb_security_group_id" {
  description = "ALB security group ID"
  value       = aws_security_group.alb.id
}

output "deployment_guide" {
  description = "Quick deployment guide"
  value = <<-EOT
    ╔════════════════════════════════════════════════════════╗
    ║         GEESP-Angola Terraform Deployment              ║
    ╚════════════════════════════════════════════════════════╝
    
    1. Run Terraform:
       terraform init
       terraform plan -var-file="environments/${var.environment}.tfvars"
       terraform apply -var-file="environments/${var.environment}.tfvars"
    
    2. Connect to Bastion:
       ssh -i ~/.ssh/id_ed25519 ubuntu@${aws_eip.bastion.public_ip}
    
    3. Access Application:
       http://${aws_lb.geesp.dns_name}
    
    4. Database Credentials:
       aws secretsmanager get-secret-value --secret-id ${aws_secretsmanager_secret.db_password.name}
    
    5. CloudWatch Logs:
       aws logs tail ${aws_cloudwatch_log_group.geesp.name} --follow
    
    6. Auto Scaling Status:
       aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names ${aws_autoscaling_group.app.name}
  EOT
}
