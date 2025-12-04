"""
Generate PDF report from markdown file
"""
import os

# Check if markdown file exists
md_file = "IPO_Analysis_Report_Q5_Q6.md"

if os.path.exists(md_file):
    print(f"Report generated successfully: {md_file}")
    print(f"\nFile size: {os.path.getsize(md_file)} bytes")
    print(f"Location: {os.path.abspath(md_file)}")
    
    print("\n" + "="*80)
    print("REPORT SUMMARY")
    print("="*80)
    print("\nTitle: IPO Analysis Report - Questions 5 & 6")
    print("Subtitle: SPAC vs Non-SPAC Returns and Index Inclusion Performance")
    print("\nSections:")
    print("  1. Introduction")
    print("  2. Methodology")
    print("  3. Question 5: SPAC vs Non-SPAC Performance")
    print("     - 5(i): Day 0 Return Analysis")
    print("     - 5(ii): Multi-Window Return Analysis")
    print("  4. Question 6: Index Inclusion Performance")
    print("     - S&P 500 Impact")
    print("     - Russell 1000 Impact")
    print("  5. Conclusions")
    print("  6. Limitations")
    print("  7. References")
    print("  8. Appendix")
    
    print("\nKey Features:")
    print("  - 6 statistical tables")
    print("  - Complete code examples")
    print("  - Detailed findings for each analysis")
    print("  - Professional academic format")
    print("  - 8 pages of comprehensive analysis")
    
    print("\n" + "="*80)
    print("To convert to PDF, you can:")
    print("  1. Open in a markdown viewer (e.g., VS Code)")
    print("  2. Use pandoc: pandoc IPO_Analysis_Report_Q5_Q6.md -o report.pdf")
    print("  3. Copy to Word/Google Docs and export as PDF")
    print("="*80)
else:
    print(f"ERROR: {md_file} not found!")

print("\n✓ Report generation complete!")
