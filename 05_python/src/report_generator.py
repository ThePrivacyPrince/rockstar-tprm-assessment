# 05_python/src/report_generator.py

import os
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable
)


# ── Color Palette ──────────────────────────────────────────
DARK_BG     = colors.HexColor("#1a1a2e")
RED         = colors.HexColor("#e63946")
YELLOW      = colors.HexColor("#f4a261")
GREEN       = colors.HexColor("#2a9d8f")
WHITE       = colors.white
LIGHT_GRAY  = colors.HexColor("#f0f0f0")
MID_GRAY    = colors.HexColor("#cccccc")
DARK_GRAY   = colors.HexColor("#444444")


def build_styles():
    """Returns a dictionary of paragraph styles."""
    base = getSampleStyleSheet()

    styles = {
        "title": ParagraphStyle(
            "title",
            fontSize=16,
            textColor=WHITE,
            fontName="Helvetica-Bold",
            spaceAfter=6
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            fontSize=11,
            textColor=MID_GRAY,
            fontName="Helvetica",
            spaceAfter=4
        ),
        "section_header": ParagraphStyle(
            "section_header",
            fontSize=13,
            textColor=YELLOW,
            fontName="Helvetica-Bold",
            spaceBefore=16,
            spaceAfter=8
        ),
        "body": ParagraphStyle(
            "body",
            fontSize=9,
            textColor=DARK_GRAY,
            fontName="Helvetica",
            spaceAfter=4,
            leading=14
        ),
        "body_bold": ParagraphStyle(
            "body_bold",
            fontSize=9,
            textColor=DARK_GRAY,
            fontName="Helvetica-Bold",
            spaceAfter=4
        ),
        "critical": ParagraphStyle(
            "critical",
            fontSize=9,
            textColor=RED,
            fontName="Helvetica-Bold",
            spaceAfter=4
        ),
        "finding": ParagraphStyle(
            "finding",
            fontSize=8,
            textColor=DARK_GRAY,
            fontName="Helvetica",
            spaceAfter=3,
            leading=12,
            leftIndent=12
        )
    }
    return styles


def build_header(styles) -> list:
    """Builds the report header block."""
    elements = []

    # Dark header background using a table
    header_data = [[
        Paragraph("TPRM Assessment Report", styles["title"]),
    ]]
    header_table = Table(header_data, colWidths=[7 * inch])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_BG),
        ("TOPPADDING", (0, 0), (-1, -1), 20),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
    ]))
    elements.append(header_table)

    # Metadata bar
    meta_data = [[
        Paragraph("Vendor: Anodot", styles["subtitle"]),
        Paragraph("Client: Rockstar Games", styles["subtitle"]),
        Paragraph("Framework: ISO 27001:2022", styles["subtitle"]),
        Paragraph(f"Date: {date.today()}", styles["subtitle"]),
    ]]
    meta_table = Table(meta_data, colWidths=[1.75 * inch] * 4)
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_BG),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 16))

    return elements


def build_executive_summary(risk_summary: dict, styles: dict) -> list:
    """Builds the executive summary section."""
    elements = []

    elements.append(Paragraph("Executive Summary", styles["section_header"]))
    elements.append(HRFlowable(width="100%", thickness=1, color=YELLOW))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph(
        "It started with a vendor nobody was watching...",
        styles["body_bold"]
    ))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        "Anodot. A cloud analytics platform. The kind of tool that sits quietly "
        "in the background of a large organization, monitoring costs, tracking "
        "infrastructure metrics, connected to everything and scrutinized by nobody.",
        styles["body"]
    ))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        "Somewhere along the way, ShinyHunters got in. They didn't need to break "
        "anything. They just needed the keys and Anodot had them. Long-lived "
        "authentication tokens, sitting in Anodot's systems, with a direct line "
        "into Rockstar's Snowflake data warehouse. Once those tokens were stolen, "
        "the attackers didn't look like attackers anymore. They looked like Anodot. "
        "They looked legitimate. And for 10 days, nobody knew the difference.",
        styles["body"]
    ))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        "By the time Rockstar found out, not from Anodot, not from their own "
        "security team, but from a post on a dark web leak site. 78.6 million "
        "records were already gone. The ransom deadline came and went. The data "
        "was published. And Rockstar was left explaining to the world how a vendor "
        "they trusted became the door someone else walked through.",
        styles["body"]
    ))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        "This assessment exists to answer one question: what would a proper "
        "third-party risk assessment of Anodot have found before any of this happened?",
        styles["body_bold"]
    ))

    # Risk rating box
    rating = risk_summary["risk_rating"]
    rating_color = RED if rating == "CRITICAL" else YELLOW if rating == "HIGH" else GREEN

    summary_data = [
        ["Overall Risk Rating", "Weighted Avg Score", "Controls Assessed", "Failed Controls"],
        [
            Paragraph(f'<font color="#{rating_color.hexval()[2:]}"><b>{rating}</b></font>',
                      styles["body_bold"]),
            str(risk_summary["weighted_average_score"]) + " / 5.0",
            str(risk_summary["total_controls_assessed"]),
            str(risk_summary["failed_controls"])
        ]
    ]

    summary_table = Table(summary_data, colWidths=[1.5*inch, 1.5*inch, 2*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LIGHT_GRAY, WHITE]),
        ("GRID", (0, 0), (-1, -1), 0.5, MID_GRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 16))

    return elements


def build_gap_table(gaps: list, styles: dict) -> list:
    """Builds the control gap analysis table."""
    elements = []

    elements.append(Paragraph("Control Gap Analysis", styles["section_header"]))
    elements.append(HRFlowable(width="100%", thickness=1, color=YELLOW))
    elements.append(Spacer(1, 8))

    headers = ["Control", "Name", "Score", "Severity", "Recommendation"]
    rows = [headers]

    for gap in gaps:
        rows.append([
            Paragraph(gap["control_id"], styles["body"]),
            Paragraph(gap["control_name"], styles["body"]),
            Paragraph(f"{gap['score']}/5", styles["body"]),
            Paragraph(gap["severity"], styles["body"]),
            Paragraph(gap["recommendation"][:80] + "...", styles["body"])
        ])

    col_widths = [0.6*inch, 2.0*inch, 0.5*inch, 0.8*inch, 3.1*inch]
    gap_table = Table(rows, colWidths=col_widths, repeatRows=1)

    table_style = [
        ("BACKGROUND", (0, 0), (-1, 0), DARK_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, MID_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LIGHT_GRAY, WHITE]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]

    # Color severity cells
    for i, gap in enumerate(gaps, start=1):
        if gap["severity"] == "CRITICAL":
            table_style.append(("TEXTCOLOR", (3, i), (3, i), RED))
            table_style.append(("FONTNAME", (3, i), (3, i), "Helvetica-Bold"))
        elif gap["severity"] == "HIGH":
            table_style.append(("TEXTCOLOR", (3, i), (3, i), YELLOW))

    gap_table.setStyle(TableStyle(table_style))
    elements.append(gap_table)
    elements.append(Spacer(1, 16))

    return elements


def build_saq_section(saq_results: dict, styles: dict) -> list:
    """Builds the SAQ evaluation section."""
    elements = []

    elements.append(Paragraph("SAQ Evaluation Results", styles["section_header"]))
    elements.append(HRFlowable(width="100%", thickness=1, color=YELLOW))
    elements.append(Spacer(1, 8))

    # SAQ summary table
    saq_summary = [
        ["Total Questions", "Passed", "Failed", "Critical Failures", "Auto-Escalate"],
        [
            str(saq_results["total_questions"]),
            str(saq_results["passed"]),
            str(saq_results["failed"]),
            str(saq_results["critical_failures"]),
            "YES" if saq_results["auto_escalate"] else "NO"
        ]
    ]

    saq_table = Table(saq_summary, colWidths=[1.4 * inch] * 5)
    saq_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, MID_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LIGHT_GRAY]),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TEXTCOLOR", (4, 1), (4, 1), RED),
        ("FONTNAME", (4, 1), (4, 1), "Helvetica-Bold"),
    ]))
    elements.append(saq_table)
    elements.append(Spacer(1, 12))

    # Critical findings
    if saq_results["critical_findings"]:
        elements.append(Paragraph(
            "Critical SAQ Findings — Requires Immediate Action",
            styles["critical"]
        ))
        elements.append(Spacer(1, 6))

        for finding in saq_results["critical_findings"]:
            elements.append(Paragraph(
                f"[{finding['question_id']}] {finding['question']}",
                styles["body_bold"]
            ))
            elements.append(Paragraph(
                f"→ {finding['escalation_reason']}",
                styles["finding"]
            ))
            elements.append(Spacer(1, 4))

    elements.append(Spacer(1, 16))
    return elements


def build_footer(styles: dict) -> list:
    """Builds the report footer."""
    elements = []

    elements.append(HRFlowable(width="100%", thickness=1, color=MID_GRAY))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        "This assessment was conducted as a portfolio project demonstrating GRC engineering "
        "fundamentals using the Rockstar Games / Anodot breach as a real-world case study. "
        "Framework: ISO 27001:2022 Annex A. All findings are based on publicly available "
        "breach reporting and inferred control gaps.",
        styles["body"]
    ))
    return elements


def generate_pdf_report(
    risk_summary: dict,
    gaps: list,
    saq_results: dict,
    output_path: str = "../06_report/anodot_tprm_report.pdf"
):
    """
    Master function. Assembles all sections and builds the PDF.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )

    styles = build_styles()
    elements = []

    elements += build_header(styles)
    elements += build_executive_summary(risk_summary, styles)
    elements += build_gap_table(gaps, styles)
    elements += build_saq_section(saq_results, styles)
    elements += build_footer(styles)

    doc.build(elements)
    print(f"\nPDF report saved to: {output_path}")