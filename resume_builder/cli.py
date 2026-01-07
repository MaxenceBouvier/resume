"""Command-line interface for CV generation and building."""

from __future__ import annotations

import subprocess
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from .filters import collect_all_tags_from_loader
from .generators import LaTeXGenerator, WebsiteGenerator
from .loader import CVDataLoader

console = Console()

# Default paths relative to package
DEFAULT_DATA_DIR = Path(__file__).parent.parent / "cv_data"
DEFAULT_TEMPLATE_DIR = Path(__file__).parent.parent / "templates"
DEFAULT_OUTPUT_DIR = Path(__file__).parent.parent / "output"
DEFAULT_WEBSITE_DATA_DIR = Path(__file__).parent.parent / "ext" / "bio-website-launch" / "src" / "data"


@click.group()
@click.version_option()
def cli() -> None:
    """CV Generator - Build tailored CVs and website data from CSV sources."""
    pass


@cli.command()
@click.option(
    "--tags",
    "-t",
    multiple=True,
    help="Tags to filter by (OR logic). Can be repeated or comma-separated.",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default=None,
    help="Output file path (default: output/maxence_bouvier_resume.tex)",
)
@click.option(
    "--data-dir",
    type=click.Path(exists=True, file_okay=False),
    default=None,
    help="Path to cv_data/ directory",
)
@click.option(
    "--template-dir",
    type=click.Path(exists=True, file_okay=False),
    default=None,
    help="Path to templates/ directory",
)
@click.option(
    "--summary",
    "-s",
    default="default",
    help="Summary variant to use",
)
def latex(
    tags: tuple[str, ...],
    output: str | None,
    data_dir: str | None,
    template_dir: str | None,
    summary: str,
) -> None:
    """Generate LaTeX CV with optional tag filtering."""
    # Parse tags (support both repeated -t and comma-separated)
    all_tags = []
    for tag_str in tags:
        all_tags.extend(t.strip() for t in tag_str.split(",") if t.strip())

    # Set up paths
    data_path = Path(data_dir) if data_dir else DEFAULT_DATA_DIR
    template_path = Path(template_dir) if template_dir else DEFAULT_TEMPLATE_DIR
    output_path = Path(output) if output else DEFAULT_OUTPUT_DIR / "maxence_bouvier_resume.tex"

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    console.print(f"[bold blue]Generating LaTeX CV...[/bold blue]")
    if all_tags:
        console.print(f"  Tags: {', '.join(all_tags)}")
    console.print(f"  Data: {data_path}")
    console.print(f"  Output: {output_path}")

    generator = LaTeXGenerator(data_path, template_path)
    result_path = generator.generate_to_file(output_path, all_tags or None, summary)

    console.print(f"[bold green]Generated:[/bold green] {result_path}")


@cli.command()
@click.option(
    "--tags",
    "-t",
    multiple=True,
    help="Tags to filter by (OR logic). Usually not needed for website.",
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(),
    default=None,
    help="Output directory for JSON files",
)
@click.option(
    "--data-dir",
    type=click.Path(exists=True, file_okay=False),
    default=None,
    help="Path to cv_data/ directory",
)
def website(
    tags: tuple[str, ...],
    output_dir: str | None,
    data_dir: str | None,
) -> None:
    """Generate JSON data files for React website."""
    # Parse tags
    all_tags = []
    for tag_str in tags:
        all_tags.extend(t.strip() for t in tag_str.split(",") if t.strip())

    # Set up paths
    data_path = Path(data_dir) if data_dir else DEFAULT_DATA_DIR
    out_path = Path(output_dir) if output_dir else DEFAULT_WEBSITE_DATA_DIR

    console.print(f"[bold blue]Generating website data...[/bold blue]")
    console.print(f"  Data: {data_path}")
    console.print(f"  Output: {out_path}")

    generator = WebsiteGenerator(data_path, out_path)
    generated = generator.generate_all(all_tags or None)

    console.print(f"[bold green]Generated {len(generated)} files:[/bold green]")
    for filename, path in generated.items():
        console.print(f"  - {filename}: {path}")


@cli.command(name="all")
@click.option(
    "--tags",
    "-t",
    multiple=True,
    help="Tags to filter by for LaTeX output (website usually unfiltered).",
)
@click.option(
    "--latex-output",
    type=click.Path(),
    default=None,
    help="LaTeX output file path",
)
@click.option(
    "--website-output-dir",
    type=click.Path(),
    default=None,
    help="Website JSON output directory",
)
@click.option(
    "--data-dir",
    type=click.Path(exists=True, file_okay=False),
    default=None,
    help="Path to cv_data/ directory",
)
@click.pass_context
def generate_all(
    ctx: click.Context,
    tags: tuple[str, ...],
    latex_output: str | None,
    website_output_dir: str | None,
    data_dir: str | None,
) -> None:
    """Generate both LaTeX CV and website JSON data."""
    console.print("[bold blue]Generating all outputs...[/bold blue]\n")

    # Generate LaTeX with tags
    ctx.invoke(
        latex,
        tags=tags,
        output=latex_output,
        data_dir=data_dir,
        template_dir=None,
        summary="default",
    )

    console.print()

    # Generate website (usually without tags)
    ctx.invoke(
        website,
        tags=(),
        output_dir=website_output_dir,
        data_dir=data_dir,
    )


@cli.command()
@click.option(
    "--data-dir",
    type=click.Path(exists=True, file_okay=False),
    default=None,
    help="Path to cv_data/ directory",
)
def tags(data_dir: str | None) -> None:
    """List all available tags from CV data."""
    data_path = Path(data_dir) if data_dir else DEFAULT_DATA_DIR

    loader = CVDataLoader(data_path)
    tags_by_section = collect_all_tags_from_loader(loader)

    # Collect all unique tags
    all_tags: set[str] = set()
    for section_tags in tags_by_section.values():
        all_tags.update(section_tags)

    # Create table
    table = Table(title="Available Tags")
    table.add_column("Section", style="cyan")
    table.add_column("Tags", style="green")

    for section, section_tags in sorted(tags_by_section.items()):
        table.add_row(section, ", ".join(sorted(section_tags)))

    console.print(table)
    console.print(f"\n[bold]All unique tags ({len(all_tags)}):[/bold]")
    console.print(", ".join(sorted(all_tags)))


@cli.command()
@click.option(
    "--data-dir",
    type=click.Path(exists=True, file_okay=False),
    default=None,
    help="Path to cv_data/ directory",
)
def validate(data_dir: str | None) -> None:
    """Validate CSV data files."""
    data_path = Path(data_dir) if data_dir else DEFAULT_DATA_DIR

    console.print(f"[bold blue]Validating CV data in {data_path}...[/bold blue]\n")

    loader = CVDataLoader(data_path)
    errors: list[str] = []

    # Validate contact
    try:
        contact = loader.load_contact()
        console.print("[green]contact.csv[/green]: OK")
    except Exception as e:
        errors.append(f"contact.csv: {e}")
        console.print(f"[red]contact.csv[/red]: {e}")

    # Validate experiences
    try:
        exp_df = loader.load_experiences()
        console.print(f"[green]experiences.csv[/green]: OK ({len(exp_df)} rows)")
    except Exception as e:
        errors.append(f"experiences.csv: {e}")
        console.print(f"[red]experiences.csv[/red]: {e}")

    # Validate skills
    try:
        skills_df = loader.load_skills()
        console.print(f"[green]skills.csv[/green]: OK ({len(skills_df)} rows)")
    except Exception as e:
        errors.append(f"skills.csv: {e}")
        console.print(f"[red]skills.csv[/red]: {e}")

    # Validate education
    try:
        edu = loader.load_education()
        console.print(f"[green]education.csv[/green]: OK ({len(edu)} rows)")
    except Exception as e:
        errors.append(f"education.csv: {e}")
        console.print(f"[red]education.csv[/red]: {e}")

    # Validate patents
    try:
        patents_df = loader.load_patents()
        console.print(f"[green]patents.csv[/green]: OK ({len(patents_df)} rows)")
    except Exception as e:
        errors.append(f"patents.csv: {e}")
        console.print(f"[red]patents.csv[/red]: {e}")

    # Validate publications
    try:
        pubs_df = loader.load_publications()
        console.print(f"[green]publications.csv[/green]: OK ({len(pubs_df)} rows)")
    except Exception as e:
        errors.append(f"publications.csv: {e}")
        console.print(f"[red]publications.csv[/red]: {e}")

    if errors:
        console.print(f"\n[bold red]Validation failed with {len(errors)} error(s)[/bold red]")
        raise SystemExit(1)
    else:
        console.print("\n[bold green]All files validated successfully![/bold green]")


@cli.command()
@click.argument("tex_file", type=click.Path(exists=True))
def build(tex_file: str) -> None:
    """Build PDF from LaTeX file using Docker."""
    path = Path(tex_file).expanduser().resolve()
    directory = path.parent
    file_name = path.name

    console.print(f"[bold blue]Building PDF from {path}...[/bold blue]")

    cmd = [
        "docker",
        "run",
        "--rm",
        "-i",
        "-v",
        f"{directory}:/data",
        "-w",
        "/data",
        "blang/latex",
        "pdflatex",
        file_name,
    ]

    try:
        subprocess.run(cmd, check=True)
        pdf_path = path.with_suffix(".pdf")
        console.print(f"[bold green]Built:[/bold green] {pdf_path}")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Build failed:[/bold red] {e}")
        raise SystemExit(1)


def main() -> None:
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
