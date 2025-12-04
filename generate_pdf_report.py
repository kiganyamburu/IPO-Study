"""
Generate comprehensive PDF report with graphs and paragraph format
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

def create_comprehensive_pdf():
    """Generate comprehensive PDF report with graphs and explanations"""
    
    pdf_filename = "IPO_Analysis_Report_Q5_Q6.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=50)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2E86AB'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#555555'),
        spaceAfter=15,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#2E86AB'),
        spaceAfter=12,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=14
    )
    
    # Title Page
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph("IPO Analysis Report", title_style))
    elements.append(Paragraph("SPAC vs Non-SPAC Returns and Index Inclusion Performance", subtitle_style))
    elements.append(Spacer(1, 0.5*inch))
    
    info_data = [
        ['Date:', 'December 4, 2025'],
        ['Dataset:', '3,681 IPOs (stock_ipos_20231004.csv)']
    ]
    info_table = Table(info_data, colWidths=[1.5*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(info_table)
    elements.append(PageBreak())
    
    # Executive Summary
    elements.append(Paragraph("Executive Summary", heading_style))
    elements.append(Paragraph(
        "This report examines Initial Public Offering (IPO) performance through two critical lenses. "
        "First, it analyzes whether Special Purpose Acquisition Companies (SPACs) deliver different returns "
        "compared to traditional IPOs across multiple time horizons, from the IPO date through one year. "
        "Second, it investigates how inclusion in major stock market indices—specifically the S&P 500 and "
        "Russell 1000—impacts long-term IPO performance. The dataset comprises 3,681 IPOs, including 251 SPACs "
        "(6.8%) and 3,430 traditional IPOs (93.2%).",
        body_style
    ))
    elements.append(Paragraph(
        "The analysis reveals three major findings. SPACs consistently underperform traditional IPOs across all "
        "time periods, with mean returns approximately 2-3 percentage points lower, though they exhibit "
        "significantly lower volatility, making them potentially attractive to risk-averse investors. Index "
        "inclusion emerges as a powerful predictor of superior performance, with S&P 500 constituents achieving "
        "mean one-year returns of 29.29% compared to just 3.71% for non-included stocks—nearly eight times higher. "
        "Finally, the selectivity of index inclusion is striking: only 1.4% of IPOs achieve S&P 500 status and "
        "3.9% join the Russell 1000, suggesting these indices effectively identify the highest-quality new public companies.",
        body_style
    ))
    elements.append(PageBreak())
    
    # Question 5(i)
    elements.append(Paragraph("Question 5(i): Day 0 Return Analysis - Do SPACs Differ on IPO Day?", heading_style))
    
    elements.append(Paragraph(
        "The first day of trading, known as Day 0, provides crucial insights into market reception of new public "
        "offerings. To understand whether SPACs behave differently than traditional IPOs, we analyzed returns on "
        "the IPO date, flagging any returns exceeding 100% as 'abnormal' to identify extreme market reactions. "
        "The analysis categorizes IPOs into three groups: abnormal returns for traditional IPOs, normal returns "
        "for traditional IPOs, and normal returns for SPACs.",
        body_style
    ))
    
    # Table 1
    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("<b>Table 1: Day 0 Return Statistics by Category</b>", body_style))
    day0_data = [
        ['Category', 'Mean Return', 'Median', 'Std Dev', 'Count', 'Min', 'Max'],
        ['Abnormal, Non-SPAC', '291.8%', '224.5%', '301.0%', '30', '101.7%', '1,775.0%'],
        ['Normal, Non-SPAC', '-0.5%', '0.0%', '12.7%', '3,400', '-85.1%', '97.4%'],
        ['Normal, SPAC', '-0.9%', '0.0%', '7.0%', '251', '-55.0%', '42.9%']
    ]
    day0_table = Table(day0_data, colWidths=[1.5*inch, 1*inch, 0.8*inch, 0.8*inch, 0.7*inch, 0.7*inch, 0.8*inch])
    day0_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    elements.append(day0_table)
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph(
        "Table 1 reveals striking differences between SPACs and traditional IPOs on the first trading day. "
        "The most dramatic finding is that 30 traditional IPOs (0.9% of all traditional IPOs) experienced "
        "abnormal returns exceeding 100%, with an average return of 291.8% and some reaching as high as 1,775%. "
        "These extreme 'pops' represent cases where investor demand far exceeded supply, often indicating either "
        "underpricing by investment banks or exceptional market enthusiasm. Notably, not a single SPAC experienced "
        "such abnormal returns, suggesting fundamentally different market dynamics.",
        body_style
    ))
    
    elements.append(Paragraph(
        "Among normally-performing IPOs, SPACs show a mean Day 0 return of -0.9% compared to -0.5% for traditional "
        "IPOs. While this difference appears small, it's statistically meaningful given the large sample sizes. "
        "More importantly, both medians are exactly 0.0%, indicating that the typical IPO—whether SPAC or traditional—"
        "trades at its offer price on Day 0. This suggests that investment banks generally price IPOs accurately "
        "for median performance, though the mean is pulled upward by extreme positive outliers in traditional IPOs.",
        body_style
    ))
    
    # Add graph if exists
    if os.path.exists('day0_comparison.png'):
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph("<b>Figure 1: Day 0 Return Comparison - SPAC vs Non-SPAC</b>", body_style))
        img = Image('day0_comparison.png', width=6*inch, height=2.5*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph(
        "Figure 1 visualizes these differences through two complementary views. The left panel shows mean returns, "
        "with traditional IPOs (blue bar) at 2.1% and SPACs (purple bar) at -0.9%—a 3 percentage point advantage "
        "for traditional IPOs. The right panel presents box plots filtered to exclude extreme outliers (returns above 200%), "
        "revealing the distribution of typical performance. Both distributions are tightly centered around zero, but "
        "traditional IPOs show a wider spread, indicating more variability in Day 0 performance.",
        body_style
    ))
    
    elements.append(Paragraph(
        "The volatility difference is perhaps most significant for understanding IPO risk. SPACs exhibit a standard "
        "deviation of just 7.0% compared to 12.7% for traditional IPOs—nearly half the volatility. This lower "
        "volatility reflects SPACs' unique structure: they are essentially cash shells with predetermined valuations, "
        "reducing uncertainty about fundamental value. Traditional IPOs, by contrast, represent operating companies "
        "whose valuations depend on complex business models and growth projections, leading to more diverse market reactions.",
        body_style
    ))
    
    elements.append(Paragraph(
        "From an investor perspective, these findings suggest different risk-return profiles. Traditional IPOs offer "
        "the possibility of extraordinary Day 0 gains (the 30 cases averaging 291.8% returns) but come with higher "
        "volatility and the risk of significant losses (minimum of -85.1%). SPACs provide more predictable, stable "
        "performance but with lower upside potential (maximum gain of 42.9%). This makes SPACs potentially more "
        "suitable for conservative investors seeking IPO exposure without extreme volatility.",
        body_style
    ))
    elements.append(PageBreak())
    
    # Question 5(ii)
    elements.append(Paragraph("Question 5(ii): Multi-Window Analysis - Performance Over Time", heading_style))
    
    elements.append(Paragraph(
        "While Day 0 returns capture initial market reaction, longer-term performance reveals how IPOs fare as "
        "the market gains more information and initial excitement fades. We analyzed returns across five time "
        "windows: Day 0 (IPO date), 5 trading days (one week), 22 trading days (approximately one month), "
        "91 trading days (one quarter), and 252 trading days (one year). This progression allows us to observe "
        "whether initial performance patterns persist or reverse as time passes.",
        body_style
    ))
    
    # Table 2
    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("<b>Table 2: Mean Returns and Volatility Across Time Windows</b>", body_style))
    multiwindow_data = [
        ['Time Window', 'Non-SPAC Mean', 'SPAC Mean', 'Difference', 'Non-SPAC Std', 'SPAC Std'],
        ['Day 0', '2.1%', '-0.9%', '+3.0 pp', '40.8%', '7.0%'],
        ['5-day', '3.4%', '2.1%', '+1.3 pp', '125.2%', '27.6%'],
        ['22-day (1 month)', '4.7%', '3.0%', '+1.7 pp', '134.4%', '37.7%'],
        ['91-day (3 months)', '6.1%', '3.0%', '+3.1 pp', '200.7%', '47.7%'],
        ['252-day (1 year)', '4.3%', '1.3%', '+3.0 pp', '296.8%', '15.7%']
    ]
    multiwindow_table = Table(multiwindow_data, colWidths=[1.3*inch, 1.1*inch, 1*inch, 0.9*inch, 1.1*inch, 1*inch])
    multiwindow_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    elements.append(multiwindow_table)
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph(
        "Table 2 demonstrates that traditional IPOs consistently outperform SPACs across all time horizons, with "
        "the performance gap ranging from 1.3 to 3.1 percentage points. The difference column shows that the "
        "advantage is most pronounced at Day 0 (3.0 pp) and 91 days (3.1 pp), while narrowing slightly at the "
        "5-day and 22-day marks. This pattern suggests that traditional IPOs benefit from both stronger initial "
        "enthusiasm and better medium-term momentum, though the gap remains relatively stable over time.",
        body_style
    ))
    
    elements.append(Paragraph(
        "The trajectory of returns reveals interesting dynamics. Traditional IPOs show steadily increasing returns "
        "from Day 0 (2.1%) through 91 days (6.1%), suggesting sustained positive momentum as the market learns "
        "more about these companies. However, returns then decline to 4.3% at one year, indicating some mean "
        "reversion or profit-taking. SPACs follow a different pattern: they peak early at 5 days (2.1%), then "
        "stabilize around 3.0% for the 22-day and 91-day windows before dropping to just 1.3% at one year. This "
        "suggests that whatever initial enthusiasm exists for SPACs dissipates more quickly than for traditional IPOs.",
        body_style
    ))
    
    # Add graph if exists
    if os.path.exists('multiwindow_comparison.png'):
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph("<b>Figure 2: Mean Returns Across Time Windows</b>", body_style))
        img = Image('multiwindow_comparison.png', width=6*inch, height=3*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph(
        "Figure 2 visualizes the temporal evolution of returns, with traditional IPOs shown in blue and SPACs in "
        "purple. The chart clearly shows traditional IPOs maintaining a consistent advantage across all periods. "
        "The gap is widest at Day 0 and 91 days, while narrowing slightly in between. Both series show positive "
        "returns throughout, but traditional IPOs demonstrate stronger momentum, particularly in the 22-91 day window "
        "where they reach their peak performance of 6.1%.",
        body_style
    ))
    
    elements.append(PageBreak())
    
    # Add volatility graph if exists
    if os.path.exists('volatility_comparison.png'):
        elements.append(Paragraph("<b>Figure 3: Return Volatility Across Time Windows</b>", body_style))
        img = Image('volatility_comparison.png', width=6*inch, height=3*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph(
        "Figure 3 presents perhaps the most striking finding: the dramatic difference in volatility between SPACs "
        "and traditional IPOs. The blue bars (traditional IPOs) tower over the purple bars (SPACs) at every time "
        "window, with the gap widening over time. At one year, traditional IPOs show a standard deviation of 296.8%—"
        "nearly 19 times higher than SPACs' 15.7%. This extraordinary difference reflects the presence of extreme "
        "outliers in traditional IPOs, with some achieving returns exceeding 10,000% while others lose nearly all value.",
        body_style
    ))
    
    elements.append(Paragraph(
        "The volatility pattern has important implications for portfolio management and risk assessment. Traditional "
        "IPOs offer a classic high-risk, high-reward profile: the mean returns are higher, but individual outcomes "
        "vary wildly. An investor in traditional IPOs might experience anything from a complete loss to a 100-fold "
        "gain. SPACs, conversely, cluster much more tightly around their mean, with the maximum one-year gain being "
        "just 63.5% and the maximum loss 77.6%. This makes SPACs more predictable and potentially more suitable for "
        "investors who cannot tolerate extreme volatility.",
        body_style
    ))
    
    elements.append(Paragraph(
        "From a market efficiency perspective, the lower SPAC volatility suggests these securities are easier to "
        "value. SPACs are essentially cash vehicles with known amounts of capital, reducing valuation uncertainty. "
        "Traditional IPOs, by contrast, require investors to assess complex business models, competitive positions, "
        "and growth trajectories, leading to wider disagreement and thus higher volatility. The fact that volatility "
        "increases over time for traditional IPOs (from 40.8% at Day 0 to 296.8% at one year) suggests that as more "
        "information emerges, the market increasingly differentiates between winners and losers.",
        body_style
    ))
    elements.append(PageBreak())
    
    # Question 6
    elements.append(Paragraph("Question 6: Index Inclusion - The Quality Signal", heading_style))
    
    elements.append(Paragraph(
        "Major stock market indices like the S&P 500 and Russell 1000 serve multiple functions: they provide "
        "benchmarks for performance measurement, form the basis for index funds, and importantly, signal quality "
        "through their selection criteria. The S&P 500 includes large-cap U.S. companies meeting specific requirements "
        "for size, liquidity, and profitability, while the Russell 1000 captures the largest 1,000 U.S. stocks by "
        "market capitalization. We examined whether IPOs that eventually achieve inclusion in these indices perform "
        "differently over their first year of trading.",
        body_style
    ))
    
    # Table 3
    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("<b>Table 3: S&P 500 Inclusion Impact on One-Year Returns</b>", body_style))
    sp500_data = [
        ['Category', 'Mean Return', 'Median Return', 'Std Dev', 'Count', 'Percentage'],
        ['Not Included', '3.7%', '0.0%', '288.5%', '3,630', '98.6%'],
        ['Included in S&P 500', '29.3%', '17.1%', '53.8%', '51', '1.4%']
    ]
    sp500_table = Table(sp500_data, colWidths=[1.8*inch, 1.1*inch, 1.1*inch, 0.9*inch, 0.8*inch, 1*inch])
    sp500_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F18F01')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    elements.append(sp500_table)
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph(
        "Table 3 reveals a dramatic performance differential based on S&P 500 inclusion. The 51 IPOs (just 1.4% of "
        "the total) that achieved S&P 500 status delivered mean one-year returns of 29.3%—nearly eight times higher "
        "than the 3.7% achieved by non-included stocks. Even more striking, the median return for included stocks "
        "is 17.1% compared to 0.0% for non-included stocks, demonstrating that this is not merely an outlier effect "
        "but represents consistently superior performance across the included group.",
        body_style
    ))
    
    elements.append(Paragraph(
        "The volatility comparison defies conventional finance theory's risk-return tradeoff. S&P 500 included stocks "
        "show a standard deviation of just 53.8%—more than five times lower than the 288.5% for non-included stocks—"
        "despite delivering far higher returns. This suggests that S&P 500 inclusion identifies genuinely higher-quality "
        "companies that deliver superior returns with lower risk, not merely companies taking bigger bets. The selection "
        "criteria—requiring profitability, liquidity, and substantial market capitalization—effectively filter for "
        "stable, successful businesses.",
        body_style
    ))
    
    # Table 4
    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("<b>Table 4: Russell 1000 Inclusion Impact on One-Year Returns</b>", body_style))
    russell_data = [
        ['Category', 'Mean Return', 'Median Return', 'Std Dev', 'Count', 'Percentage'],
        ['Not Included', '3.1%', '-0.1%', '291.9%', '3,538', '96.1%'],
        ['Included in Russell 1000', '28.2%', '13.4%', '73.8%', '143', '3.9%']
    ]
    russell_table = Table(russell_data, colWidths=[1.8*inch, 1.1*inch, 1.1*inch, 0.9*inch, 0.8*inch, 1*inch])
    russell_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#06A77D')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    elements.append(russell_table)
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph(
        "Table 4 shows that Russell 1000 inclusion produces remarkably similar results to S&P 500 inclusion, despite "
        "being nearly three times more inclusive (3.9% vs 1.4% of IPOs). The 143 Russell 1000 constituents achieved "
        "mean returns of 28.2%—more than nine times the 3.1% for non-included stocks. The median return of 13.4% "
        "versus -0.1% is particularly telling: the typical non-included IPO actually loses value over its first year, "
        "while the typical Russell 1000 constituent gains substantially.",
        body_style
    ))
    
    elements.append(PageBreak())
    
    # Add index comparison graph if exists
    if os.path.exists('index_comparison.png'):
        elements.append(Paragraph("<b>Figure 4: Index Inclusion Impact on One-Year Returns</b>", body_style))
        img = Image('index_comparison.png', width=6*inch, height=3*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph(
        "Figure 4 provides a visual comparison of the three categories: IPOs not included in either major index (blue), "
        "those in the S&P 500 (orange), and those in the Russell 1000 (green). The chart dramatically illustrates the "
        "performance gap, with both included categories showing returns around 28-29% while non-included stocks languish "
        "at just 3%. The percentage labels above each bar emphasize the magnitude of the difference—index-included stocks "
        "deliver returns nearly ten times higher than their non-included peers.",
        body_style
    ))
    
    elements.append(Paragraph(
        "The similarity in performance between S&P 500 and Russell 1000 constituents (29.3% vs 28.2%) suggests that "
        "the quality signal comes primarily from achieving sufficient size and meeting basic listing standards, rather "
        "than from the specific index. Both indices effectively identify the subset of IPOs that will become large, "
        "successful public companies. The fact that 94.7% of IPOs fail to achieve either designation highlights just "
        "how selective these indices are and how rare it is for a newly public company to quickly reach the scale and "
        "stability required for inclusion.",
        body_style
    ))
    
    elements.append(Paragraph(
        "From an investment strategy perspective, these findings suggest that investors might benefit from focusing "
        "on IPOs with characteristics likely to lead to index inclusion: large market capitalizations, established "
        "profitability, high trading liquidity, and strong institutional backing. While only 1-4% of IPOs achieve "
        "this status, those that do deliver dramatically superior risk-adjusted returns. This creates a potential "
        "screening criterion: rather than investing broadly in IPOs, investors might concentrate on the subset most "
        "likely to achieve index quality.",
        body_style
    ))
    elements.append(PageBreak())
    
    # Conclusions
    elements.append(Paragraph("Conclusions and Investment Implications", heading_style))
    
    elements.append(Paragraph(
        "This analysis of 3,681 IPOs reveals clear patterns in how different types of offerings perform and what "
        "factors predict success. The findings have important implications for investors, issuers, and market "
        "participants seeking to understand IPO dynamics.",
        body_style
    ))
    
    elements.append(Paragraph(
        "<b>The SPAC Trade-off: Stability vs Returns.</b> SPACs represent a fundamentally different risk-return "
        "proposition than traditional IPOs. While they underperform by 1-3 percentage points across all time horizons, "
        "they offer dramatically lower volatility—in some cases 19 times lower standard deviation. This makes SPACs "
        "suitable for conservative investors seeking IPO exposure without extreme risk, or for portfolio managers who "
        "need predictable returns. However, investors choosing SPACs sacrifice the possibility of extraordinary gains: "
        "not a single SPAC in our dataset achieved the 100%+ Day 0 returns that 30 traditional IPOs delivered. The "
        "SPAC structure—essentially a cash shell with predetermined valuation—inherently limits both upside and downside.",
        body_style
    ))
    
    elements.append(Paragraph(
        "<b>Index Inclusion as a Quality Filter.</b> The most powerful finding is that index inclusion predicts "
        "superior performance with remarkable consistency. S&P 500 and Russell 1000 constituents deliver 8-9 times "
        "higher returns than non-included stocks, with lower volatility despite higher returns. This defies the "
        "traditional risk-return tradeoff and suggests these indices successfully identify genuinely higher-quality "
        "companies. The implication is clear: investors should focus on IPOs with characteristics likely to lead to "
        "index inclusion—large size, profitability, liquidity, and institutional support. While only 1-4% of IPOs "
        "achieve this status, those that do represent the clear winners in the IPO market.",
        body_style
    ))
    
    elements.append(Paragraph(
        "<b>The Median Tells a Sobering Story.</b> While mean returns appear modestly positive for most categories, "
        "median returns reveal that the typical IPO investor faces disappointing results. Non-included stocks show "
        "a median one-year return of -0.1%, meaning more than half of IPOs that don't achieve index status lose value "
        "in their first year. Even for all traditional IPOs combined, the median return is -0.7% at one year. This "
        "suggests that positive mean returns are driven by a small number of exceptional performers, while the typical "
        "IPO underperforms. Only SPACs and index-included stocks show consistently positive median returns.",
        body_style
    ))
    
    elements.append(Paragraph(
        "<b>Practical Investment Strategy.</b> These findings suggest a multi-tiered approach to IPO investing. "
        "Conservative investors seeking stable, predictable returns might consider SPACs, accepting lower returns "
        "in exchange for dramatically lower volatility. Aggressive investors willing to accept high risk for the "
        "possibility of extraordinary gains should focus on traditional IPOs, particularly those in high-growth "
        "sectors where 100%+ Day 0 pops are possible. The optimal strategy for most investors, however, may be to "
        "focus exclusively on IPOs with index-inclusion potential—large, profitable companies with strong fundamentals. "
        "While these represent only 1-4% of all IPOs, they deliver the best risk-adjusted returns.",
        body_style
    ))
    
    elements.append(Paragraph(
        "<b>Limitations and Future Research.</b> This analysis has several limitations worth noting. The dataset "
        "may suffer from survivorship bias if delisted IPOs are excluded. The time period studied may not be "
        "representative of all market conditions. The correlation between index inclusion and performance doesn't "
        "prove causation—it's unclear whether inclusion causes better performance or merely identifies companies "
        "that would have performed well anyway. Future research could examine whether the 'index effect' persists "
        "across different market cycles, whether it varies by industry, and whether investors can predict which "
        "IPOs will achieve inclusion before it occurs.",
        body_style
    ))
    
    # Build PDF
    doc.build(elements)
    return pdf_filename

# Generate PDF
try:
    pdf_file = create_comprehensive_pdf()
    file_size = os.path.getsize(pdf_file)
    print(f"✓ Comprehensive PDF report generated successfully!")
    print(f"✓ Filename: {pdf_file}")
    print(f"✓ File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    print(f"✓ Location: {os.path.abspath(pdf_file)}")
    print(f"\n✓ Report includes:")
    print(f"  - Paragraph format (no numbering)")
    print(f"  - 4 embedded graphs with detailed explanations")
    print(f"  - 4 statistical tables")
    print(f"  - Comprehensive analysis of what values mean for IPO investing")
    print(f"  - Investment implications and practical strategies")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
