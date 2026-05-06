"""
PDF Financial Report Generator for GEESP-Angola
Generates comprehensive multi-page financial reports with LCOE analysis, sensitivity charts, and projections

Usage:
    python generate_financial_report.py --site-name "Site A" --output report.pdf
    python generate_financial_report.py --config analysis_config.json --output report.pdf
"""

import sys
from pathlib import Path
from datetime import datetime
import logging
import json
from typing import Dict, List, Tuple, Optional

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server environments
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont

# For PDF generation
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image as RLImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY


# ============================================================================
# CONFIGURATION
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s"
)
logger = logging.getLogger(__name__)

# Color scheme for charts
COLOR_PALETTE = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'success': '#06A77D',
    'warning': '#F18F01',
    'danger': '#C73E1D',
    'light_gray': '#F0F0F0',
    'dark_gray': '#333333',
}

sns.set_palette("husl")


# ============================================================================
# LCOE & FINANCIAL CALCULATIONS
# ============================================================================

class FinancialAnalyzer:
    """Calculate LCOE, financial metrics, and projections"""
    
    def __init__(self, site_config: Dict):
        """Initialize with site configuration"""
        self.config = site_config
        self.results = {}
    
    def calculate_lcoe(self) -> float:
        """
        Calculate Levelized Cost of Energy (LCOE)
        
        LCOE = (CapEx + Sum(OpEx_t / (1+r)^t)) / Sum(Energy_t / (1+r)^t)
        
        Returns:
            lcoe: $/kWh
        """
        capex = self.config.get('capex', 0)
        annual_opex = self.config.get('annual_opex', 0)
        discount_rate = self.config.get('discount_rate', 0.08)
        project_lifetime = self.config.get('project_lifetime', 25)
        annual_energy_kwh = self.config.get('annual_energy_kwh', 0)
        
        # Calculate NPV of costs and energy
        npv_costs = capex
        npv_energy = 0
        
        for year in range(1, project_lifetime + 1):
            discount_factor = (1 + discount_rate) ** year
            npv_costs += annual_opex / discount_factor
            npv_energy += annual_energy_kwh / discount_factor
        
        lcoe = npv_costs / npv_energy if npv_energy > 0 else float('inf')
        self.results['lcoe'] = lcoe
        return lcoe
    
    def calculate_irr(self) -> float:
        """Calculate Internal Rate of Return using Newton-Raphson method"""
        capex = self.config.get('capex', 0)
        annual_revenue = self.config.get('annual_revenue', 0)
        annual_opex = self.config.get('annual_opex', 0)
        project_lifetime = self.config.get('project_lifetime', 25)
        residual_value = self.config.get('residual_value', 0)
        
        def npv(rate):
            npv_value = -capex
            for year in range(1, project_lifetime + 1):
                cf = annual_revenue - annual_opex
                npv_value += cf / (1 + rate) ** year
            npv_value += residual_value / (1 + rate) ** project_lifetime
            return npv_value
        
        # Newton-Raphson
        rate = 0.1
        for _ in range(100):
            f = npv(rate)
            df_rate = rate * 0.001
            df = (npv(rate + df_rate) - f) / df_rate
            if abs(f) < 0.01 or abs(df) < 1e-10:
                break
            rate = rate - f / df
        
        self.results['irr'] = rate
        return rate
    
    def calculate_payback_period(self) -> float:
        """Calculate simple payback period"""
        capex = self.config.get('capex', 0)
        annual_cash_flow = self.config.get('annual_revenue', 0) - self.config.get('annual_opex', 0)
        
        if annual_cash_flow <= 0:
            return float('inf')
        
        payback = capex / annual_cash_flow
        self.results['payback_period'] = payback
        return payback
    
    def sensitivity_analysis(self, variable: str, range_pct: float = 0.3) -> Dict:
        """
        Perform sensitivity analysis on key variables
        
        Args:
            variable: Variable to test (e.g., 'annual_energy_kwh', 'capex', 'discount_rate')
            range_pct: Range to test as fraction of base (default 30%)
        
        Returns:
            Dictionary with sensitivity results
        """
        base_value = self.config.get(variable)
        variations = np.linspace(base_value * (1 - range_pct), 
                                base_value * (1 + range_pct), 
                                11)
        
        results = {'variation': [], 'lcoe': [], 'irr': []}
        
        for variation in variations:
            # Temporarily update config
            original = self.config[variable]
            self.config[variable] = variation
            
            results['variation'].append(variation / base_value if base_value != 0 else 0)
            results['lcoe'].append(self.calculate_lcoe())
            results['irr'].append(self.calculate_irr())
            
            # Restore original
            self.config[variable] = original
        
        return results
    
    def npv_projection(self) -> Tuple[np.ndarray, np.ndarray]:
        """Generate year-by-year NPV projection"""
        capex = self.config.get('capex', 0)
        annual_revenue = self.config.get('annual_revenue', 0)
        annual_opex = self.config.get('annual_opex', 0)
        discount_rate = self.config.get('discount_rate', 0.08)
        project_lifetime = self.config.get('project_lifetime', 25)
        
        years = np.arange(0, project_lifetime + 1)
        npv_cumulative = np.zeros(project_lifetime + 1)
        npv_cumulative[0] = -capex
        
        for year in range(1, project_lifetime + 1):
            cf = annual_revenue - annual_opex
            npv_cumulative[year] = npv_cumulative[year-1] + (cf / (1 + discount_rate) ** year)
        
        return years, npv_cumulative


# ============================================================================
# CHART GENERATION
# ============================================================================

def create_lcoe_sensitivity_chart(analyzer: FinancialAnalyzer) -> str:
    """Create LCOE sensitivity chart"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Test sensitivity to key variables
    variables = ['annual_energy_kwh', 'capex', 'annual_opex']
    colors = [COLOR_PALETTE['primary'], COLOR_PALETTE['secondary'], COLOR_PALETTE['warning']]
    
    for var, color in zip(variables, colors):
        results = analyzer.sensitivity_analysis(var)
        variation_pct = (np.array(results['variation']) - 1) * 100
        
        ax1.plot(variation_pct, results['lcoe'], marker='o', label=var.replace('_', ' '), 
                color=color, linewidth=2, markersize=6)
    
    ax1.set_xlabel('Variable Change (%)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('LCOE ($/kWh)', fontsize=11, fontweight='bold')
    ax1.set_title('LCOE Sensitivity Analysis', fontsize=12, fontweight='bold')
    ax1.legend(loc='best', framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    
    # Tornado chart
    base_lcoe = analyzer.calculate_lcoe()
    tornado_data = []
    
    for var in variables:
        results = analyzer.sensitivity_analysis(var, range_pct=0.3)
        min_lcoe = min(results['lcoe'])
        max_lcoe = max(results['lcoe'])
        tornado_data.append({
            'variable': var.replace('_', ' ').title(),
            'low': base_lcoe - max_lcoe if max_lcoe != min_lcoe else 0,
            'high': min_lcoe - base_lcoe if max_lcoe != min_lcoe else 0,
        })
    
    tornado_df = pd.DataFrame(tornado_data)
    y_pos = np.arange(len(tornado_df))
    
    ax2.barh(y_pos, tornado_df['high'], left=0, color=COLOR_PALETTE['success'], label='Decrease LCOE')
    ax2.barh(y_pos, -tornado_df['low'], color=COLOR_PALETTE['danger'], label='Increase LCOE')
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(tornado_df['variable'])
    ax2.set_xlabel('Change in LCOE ($/kWh)', fontsize=11, fontweight='bold')
    ax2.set_title('Tornado Diagram', fontsize=12, fontweight='bold')
    ax2.legend(loc='best')
    ax2.axvline(x=0, color='black', linestyle='-', linewidth=1)
    ax2.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    
    # Save chart
    chart_path = Path('temp_lcoe_sensitivity.png')
    plt.savefig(chart_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return str(chart_path)


def create_npv_projection_chart(analyzer: FinancialAnalyzer) -> str:
    """Create NPV projection over project lifetime"""
    years, npv = analyzer.npv_projection()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Fill between payback and positive NPV
    ax.fill_between(years, npv, 0, where=(npv >= 0), alpha=0.3, color=COLOR_PALETTE['success'], 
                    label='Positive NPV')
    ax.fill_between(years, npv, 0, where=(npv < 0), alpha=0.3, color=COLOR_PALETTE['danger'], 
                    label='Negative NPV (Payback)')
    
    # Plot line
    ax.plot(years, npv, marker='o', color=COLOR_PALETTE['primary'], linewidth=2.5, 
           markersize=4, label='Cumulative NPV')
    
    # Payback point
    payback_idx = np.where(npv >= 0)[0]
    if len(payback_idx) > 0:
        payback_year = years[payback_idx[0]]
        ax.axvline(x=payback_year, color=COLOR_PALETTE['warning'], linestyle='--', linewidth=2, 
                  label=f'Payback Year: {payback_year:.1f}')
        ax.scatter([payback_year], [0], s=100, color=COLOR_PALETTE['warning'], zorder=5)
    
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax.set_xlabel('Year', fontsize=11, fontweight='bold')
    ax.set_ylabel('Net Present Value ($)', fontsize=11, fontweight='bold')
    ax.set_title('Project NPV Projection (25-Year Lifetime)', fontsize=12, fontweight='bold')
    ax.legend(loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3)
    
    # Format y-axis as currency
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.0f}M'))
    
    plt.tight_layout()
    
    chart_path = Path('temp_npv_projection.png')
    plt.savefig(chart_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return str(chart_path)


def create_financial_metrics_chart(analyzer: FinancialAnalyzer) -> str:
    """Create dashboard with key financial metrics"""
    fig = plt.figure(figsize=(10, 6))
    gs = GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.3)
    
    lcoe = analyzer.calculate_lcoe()
    irr = analyzer.calculate_irr()
    payback = analyzer.calculate_payback_period()
    capex = analyzer.config.get('capex', 0)
    
    # LCOE gauge
    ax1 = fig.add_subplot(gs[0, 0])
    lcoe_ranges = [0, 0.05, 0.1, 0.15, 0.2, 0.3]
    colors_lcoe = [COLOR_PALETTE['success'], COLOR_PALETTE['success'], 
                  COLOR_PALETTE['warning'], COLOR_PALETTE['danger'], COLOR_PALETTE['danger']]
    
    for i, (start, end, color) in enumerate(zip(lcoe_ranges[:-1], lcoe_ranges[1:], colors_lcoe)):
        theta = np.linspace(0, np.pi, 100)
        r_inner, r_outer = 1, 1.5
        x_inner = r_inner * np.cos(theta) + (start / lcoe_ranges[-1]) * 2 - 1
        x_outer = r_outer * np.cos(theta) + (start / lcoe_ranges[-1]) * 2 - 1
        ax1.fill_between(x_inner, 0, 1, color=color, alpha=0.7)
    
    ax1.text(0, -0.3, f'${lcoe:.3f}/kWh', ha='center', fontsize=14, fontweight='bold')
    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-0.5, 1.5)
    ax1.axis('off')
    ax1.set_title('LCOE', fontsize=11, fontweight='bold')
    
    # IRR metric
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.bar(['IRR'], [irr * 100], color=COLOR_PALETTE['primary'], width=0.4)
    ax2.set_ylabel('Percent (%)', fontsize=10, fontweight='bold')
    ax2.set_ylim(0, 20)
    ax2.set_title('Internal Rate of Return', fontsize=11, fontweight='bold')
    ax2.text(0, irr * 100 + 1, f'{irr*100:.1f}%', ha='center', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Payback period
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.bar(['Payback'], [payback], color=COLOR_PALETTE['secondary'], width=0.4)
    ax3.set_ylabel('Years', fontsize=10, fontweight='bold')
    ax3.set_ylim(0, 25)
    ax3.set_title('Payback Period', fontsize=11, fontweight='bold')
    ax3.text(0, payback + 1, f'{payback:.1f} yrs', ha='center', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Capex breakdown
    ax4 = fig.add_subplot(gs[1, 1])
    capex_breakdown = {
        'Equipment': capex * 0.6,
        'Installation': capex * 0.25,
        'Contingency': capex * 0.15
    }
    ax4.pie(capex_breakdown.values(), labels=capex_breakdown.keys(), autopct='%1.0f%%',
           colors=[COLOR_PALETTE['primary'], COLOR_PALETTE['secondary'], COLOR_PALETTE['warning']])
    ax4.set_title('Capital Expenditure Breakdown', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    
    chart_path = Path('temp_financial_metrics.png')
    plt.savefig(chart_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return str(chart_path)


# ============================================================================
# PDF REPORT GENERATION
# ============================================================================

class FinancialReportGenerator:
    """Generate comprehensive PDF financial report"""
    
    def __init__(self, site_config: Dict, output_path: str = "financial_report.pdf"):
        """Initialize report generator"""
        self.config = site_config
        self.output_path = Path(output_path)
        self.analyzer = FinancialAnalyzer(site_config)
        self.doc = SimpleDocTemplate(str(self.output_path), pagesize=letter,
                                    rightMargin=0.5*inch, leftMargin=0.5*inch,
                                    topMargin=0.75*inch, bottomMargin=0.75*inch)
        self.story = []
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='TitleStyle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor(COLOR_PALETTE['primary']),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='HeadingStyle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor(COLOR_PALETTE['primary']),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
    
    def add_title_page(self):
        """Add title/cover page"""
        self.story.append(Spacer(1, 2*inch))
        
        title = Paragraph("GEESP-Angola", self.styles['TitleStyle'])
        self.story.append(title)
        
        subtitle = Paragraph("Financial Analysis Report", self.styles['HeadingStyle'])
        self.story.append(subtitle)
        
        self.story.append(Spacer(1, 0.5*inch))
        
        # Site information
        site_name = self.config.get('site_name', 'Unknown Site')
        info_text = f"""
        <b>Site:</b> {site_name}<br/>
        <b>Date:</b> {datetime.now().strftime('%B %d, %Y')}<br/>
        <b>Analyst:</b> GEESP-Angola Energy Team
        """
        self.story.append(Paragraph(info_text, self.styles['BodyText']))
        self.story.append(PageBreak())
    
    def add_executive_summary(self):
        """Add executive summary"""
        self.story.append(Paragraph("Executive Summary", self.styles['HeadingStyle']))
        
        lcoe = self.analyzer.calculate_lcoe()
        irr = self.analyzer.calculate_irr()
        payback = self.analyzer.calculate_payback_period()
        
        summary_text = f"""
        This report presents a comprehensive financial analysis for {self.config.get('site_name', 'the proposed site')}.
        <br/><br/>
        <b>Key Findings:</b><br/>
        • <b>LCOE:</b> ${lcoe:.4f}/kWh - Competitive cost of energy<br/>
        • <b>IRR:</b> {irr*100:.2f}% - Strong financial returns<br/>
        • <b>Payback Period:</b> {payback:.1f} years - Reasonable investment recovery<br/>
        • <b>Project Lifetime:</b> {self.config.get('project_lifetime', 25)} years<br/>
        <br/>
        The analysis demonstrates strong financial viability with acceptable risk profile.
        """
        
        self.story.append(Paragraph(summary_text, self.styles['BodyText']))
        self.story.append(Spacer(1, 0.3*inch))
        self.story.append(PageBreak())
    
    def add_financial_metrics_section(self):
        """Add financial metrics section with chart"""
        self.story.append(Paragraph("Financial Metrics Dashboard", self.styles['HeadingStyle']))
        
        chart_path = create_financial_metrics_chart(self.analyzer)
        if Path(chart_path).exists():
            self.story.append(RLImage(chart_path, width=6*inch, height=4.5*inch))
            self.story.append(Spacer(1, 0.2*inch))
        
        # Metrics table
        metrics_data = [
            ['Metric', 'Value', 'Unit'],
            ['LCOE', f"${self.analyzer.calculate_lcoe():.4f}", '$/kWh'],
            ['IRR', f"{self.analyzer.calculate_irr()*100:.2f}", '%'],
            ['Payback Period', f"{self.analyzer.calculate_payback_period():.1f}", 'years'],
            ['Capital Expenditure', f"${self.config.get('capex', 0):,.0f}", '$'],
            ['Annual O&M', f"${self.config.get('annual_opex', 0):,.0f}", '$/year'],
            ['Annual Energy Output', f"{self.config.get('annual_energy_kwh', 0):,.0f}", 'kWh/year'],
        ]
        
        metrics_table = Table(metrics_data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLOR_PALETTE['primary'])),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        self.story.append(metrics_table)
        self.story.append(PageBreak())
    
    def add_sensitivity_analysis(self):
        """Add sensitivity analysis section"""
        self.story.append(Paragraph("Sensitivity Analysis", self.styles['HeadingStyle']))
        
        self.story.append(Paragraph(
            "The following charts demonstrate how LCOE and project returns vary with key input parameters.",
            self.styles['BodyText']
        ))
        self.story.append(Spacer(1, 0.2*inch))
        
        chart_path = create_lcoe_sensitivity_chart(self.analyzer)
        if Path(chart_path).exists():
            self.story.append(RLImage(chart_path, width=7*inch, height=4*inch))
        
        self.story.append(PageBreak())
    
    def add_npv_projection(self):
        """Add NPV projection section"""
        self.story.append(Paragraph("Project NPV Projection", self.styles['HeadingStyle']))
        
        self.story.append(Paragraph(
            "Cumulative Net Present Value over the 25-year project lifetime:",
            self.styles['BodyText']
        ))
        self.story.append(Spacer(1, 0.2*inch))
        
        chart_path = create_npv_projection_chart(self.analyzer)
        if Path(chart_path).exists():
            self.story.append(RLImage(chart_path, width=6.5*inch, height=3.9*inch))
        
        self.story.append(PageBreak())
    
    def add_assumptions_section(self):
        """Add assumptions and methodology"""
        self.story.append(Paragraph("Assumptions & Methodology", self.styles['HeadingStyle']))
        
        assumptions_text = f"""
        <b>Financial Assumptions:</b><br/>
        • Discount Rate: {self.config.get('discount_rate', 0.08)*100:.1f}%<br/>
        • Project Lifetime: {self.config.get('project_lifetime', 25)} years<br/>
        • Inflation Rate: {self.config.get('inflation_rate', 0.03)*100:.1f}%<br/>
        <br/>
        <b>Technical Assumptions:</b><br/>
        • Annual Energy Output: {self.config.get('annual_energy_kwh', 0):,.0f} kWh<br/>
        • Capacity Factor: {(self.config.get('annual_energy_kwh', 0) / (365*24*self.config.get('capacity_mw', 1))):.1%}<br/>
        • Degradation Rate: {self.config.get('degradation_rate', 0.005)*100:.2f}%/year<br/>
        <br/>
        <b>Methodology:</b><br/>
        LCOE is calculated using the discounted cash flow approach per NREL guidelines.<br/>
        IRR is computed via Newton-Raphson iterative method.<br/>
        Sensitivity analysis includes ±30% variation in key parameters.
        """
        
        self.story.append(Paragraph(assumptions_text, self.styles['BodyText']))
    
    def generate(self):
        """Generate complete report"""
        logger.info(f"Generating financial report to {self.output_path}")
        
        self.add_title_page()
        self.add_executive_summary()
        self.add_financial_metrics_section()
        self.add_sensitivity_analysis()
        self.add_npv_projection()
        self.add_assumptions_section()
        
        # Build PDF
        self.doc.build(self.story)
        logger.info(f"✓ Report generated: {self.output_path}")
        
        # Cleanup temp charts
        for temp_file in ['temp_lcoe_sensitivity.png', 'temp_npv_projection.png', 
                         'temp_financial_metrics.png']:
            Path(temp_file).unlink(missing_ok=True)


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate financial analysis PDF report")
    parser.add_argument('--site-name', default='Sample Site', help='Site name')
    parser.add_argument('--capex', type=float, default=1000000, help='Capital expenditure ($)')
    parser.add_argument('--opex', type=float, default=50000, help='Annual O&M ($)')
    parser.add_argument('--annual-energy', type=float, default=500000, help='Annual energy output (kWh)')
    parser.add_argument('--discount-rate', type=float, default=0.08, help='Discount rate')
    parser.add_argument('--output', default='financial_report.pdf', help='Output file path')
    
    args = parser.parse_args()
    
    # Create configuration
    config = {
        'site_name': args.site_name,
        'capex': args.capex,
        'annual_opex': args.opex,
        'annual_energy_kwh': args.annual_energy,
        'discount_rate': args.discount_rate,
        'project_lifetime': 25,
        'inflation_rate': 0.03,
        'degradation_rate': 0.005,
        'capacity_mw': args.annual_energy / (365 * 24 * 0.25),  # Assume 25% capacity factor
        'annual_revenue': args.annual_energy * 0.08,  # $0.08/kWh revenue
        'residual_value': 0,
    }
    
    # Generate report
    generator = FinancialReportGenerator(config, args.output)
    generator.generate()
    
    print(f"\n✓ Report saved to: {args.output}")


if __name__ == "__main__":
    main()
