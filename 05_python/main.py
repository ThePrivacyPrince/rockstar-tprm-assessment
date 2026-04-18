# 05_python/main.py

import os
import sys

from src.loader import load_controls, load_vendor_responses, load_saq_responses
from src.scorer import calculate_vendor_risk
from src.gap_analyzer import find_gaps, summarize_gaps
from src.saq_evaluator import evaluate_saq, get_critical_summary
from src.report_generator import generate_pdf_report

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.rule import Rule
from rich import box

console = Console()


def print_header():
    console.print()
    console.print(Panel.fit(
        "[bold red]TPRM Assessment Engine[/bold red]\n"
        "[white]Vendor: Anodot  |  Client: Rockstar Games[/white]\n"
        "[dim]Framework: ISO 27001:2022  |  Date: 2026-04-14[/dim]\n"
        "[dim]Case Study: ShinyHunters Breach — 78.6M Records Leaked[/dim]"
    ))
    console.print()


def print_risk_summary(risk_summary: dict):
    console.print(Rule("[bold yellow]VENDOR RISK SUMMARY[/bold yellow]"))
    console.print()

    rating = risk_summary["risk_rating"]
    color = "red" if rating == "CRITICAL" else "yellow" if rating == "HIGH" else "green"

    console.print(Panel.fit(
        f"[bold]Overall Risk Rating:  [{color}]{rating}[/{color}][/bold]\n"
        f"Weighted Average Score:   "
        f"[yellow]{risk_summary['weighted_average_score']}[/yellow] / 5.0\n"
        f"Total Controls Assessed:  {risk_summary['total_controls_assessed']}\n"
        f"Failed Controls:          "
        f"[red]{risk_summary['failed_controls']}[/red]\n"
        f"Not Implemented:          "
        f"[bold red]{risk_summary['not_implemented_count']}[/bold red]"
    ))
    console.print()


def print_gap_table(gaps: list, gap_summary: dict):
    console.print(Rule("[bold yellow]CONTROL GAP ANALYSIS[/bold yellow]"))
    console.print()

    # Summary counts
    console.print(
        f"  Critical Gaps: [bold red]{gap_summary.get('CRITICAL', 0)}[/bold red]  "
        f"High Gaps: [yellow]{gap_summary.get('HIGH', 0)}[/yellow]  "
        f"Medium Gaps: [green]{gap_summary.get('MEDIUM', 0)}[/green]"
    )
    console.print()

    # Gap table
    table = Table(
        box=box.ROUNDED,
        show_lines=True,
        header_style="bold white"
    )

    table.add_column("Control", style="cyan", width=10)
    table.add_column("Name", style="white", width=35)
    table.add_column("Score", style="yellow", width=7)
    table.add_column("Severity", style="red", width=10)
    table.add_column("Recommendation", style="green", width=45)

    for gap in gaps:
        severity = gap["severity"]
        sev_color = (
            "bold red" if severity == "CRITICAL"
            else "yellow" if severity == "HIGH"
            else "white"
        )

        table.add_row(
            gap["control_id"],
            gap["control_name"],
            f"{gap['score']}/5",
            f"[{sev_color}]{severity}[/{sev_color}]",
            gap["recommendation"][:55] + "..."
        )

    console.print(table)
    console.print()


def print_saq_results(saq_results: dict):
    console.print(Rule("[bold yellow]SAQ EVALUATION RESULTS[/bold yellow]"))
    console.print()

    escalate_text = (
        "[bold red]YES — ESCALATE IMMEDIATELY[/bold red]"
        if saq_results["auto_escalate"]
        else "[green]NO[/green]"
    )

    console.print(Panel.fit(
        f"Total Questions:     {saq_results['total_questions']}\n"
        f"Passed:              [green]{saq_results['passed']}[/green]\n"
        f"Failed:              [red]{saq_results['failed']}[/red]\n"
        f"Critical Failures:   "
        f"[bold red]{saq_results['critical_failures']}[/bold red]\n"
        f"Auto-Escalate:       {escalate_text}"
    ))
    console.print()

    if saq_results["critical_findings"]:
        console.print(
            "[bold red]CRITICAL SAQ FINDINGS — REQUIRES IMMEDIATE ACTION[/bold red]"
        )
        console.print()
        for finding in saq_results["critical_findings"]:
            console.print(
                f"  [red]●[/red] [bold][{finding['question_id']}][/bold] "
                f"{finding['question']}"
            )
            console.print(
                f"    [dim]→ {finding['escalation_reason']}[/dim]"
            )
            console.print()


def print_footer():
    console.print(Rule())
    console.print()
    console.print(
        "  [bold green]Assessment complete.[/bold green]\n"
        "  [dim]Next step: run report_generator.py to produce PDF output.[/dim]\n"
        "  [dim]Push results to GitHub when complete.[/dim]"
    )
    console.print()


def run_assessment():
    # Set working directory to 05_python
    # so relative paths to data/ work correctly
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    print_header()

    # Load all data
    console.print("[dim]Loading data...[/dim]")
    controls = load_controls()
    vendor_data = load_vendor_responses()
    saq_data = load_saq_responses()

    responses = vendor_data["responses"]
    saq_responses = saq_data["responses"]
    console.print(f"[dim]Loaded {len(controls)} controls, "
                  f"{len(responses)} vendor responses, "
                  f"{len(saq_responses)} SAQ responses.[/dim]")
    console.print()

    # Run scoring engine
    risk_summary = calculate_vendor_risk(responses, controls)

    # Run gap analysis
    gaps = find_gaps(controls, responses)
    gap_summary = summarize_gaps(gaps)

    # Run SAQ evaluation
    saq_results = evaluate_saq(saq_responses)

    # Print everything
    print_risk_summary(risk_summary)
    print_gap_table(gaps, gap_summary)
    print_saq_results(saq_results)
    print_footer()
    generate_pdf_report(risk_summary, gaps, saq_results)

if __name__ == "__main__":
    run_assessment()