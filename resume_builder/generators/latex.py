"""LaTeX CV generator using Jinja2 templates."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from ..filters import filter_by_tags
from ..loader import CVDataLoader
from ..models import CVData, Patent, Publication
from ..utils import escape_latex, format_period_latex
from .base import group_experiences, group_skills, sort_by_weight


class LaTeXGenerator:
    """Generate LaTeX CV from CSV data with tag-based filtering."""

    def __init__(
        self,
        data_dir: Path | str,
        template_dir: Path | str | None = None,
        template_name: str = "resume.tex.j2",
    ):
        """
        Initialize LaTeX generator.

        Args:
            data_dir: Path to cv_data/ directory
            template_dir: Path to templates/ directory (defaults to sibling of data_dir)
            template_name: Name of Jinja2 template file
        """
        self.data_dir = Path(data_dir)
        self.template_dir = (
            Path(template_dir) if template_dir else self.data_dir.parent / "templates"
        )
        self.template_name = template_name
        self.loader = CVDataLoader(self.data_dir)

        # Set up Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=select_autoescape(disabled_extensions=["tex", "j2"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["escape_tex"] = escape_latex
        self.env.filters["format_period"] = format_period_latex

    def generate(
        self,
        tags: list[str] | None = None,
        summary_variant: str = "default",
    ) -> str:
        """
        Generate LaTeX content with optional tag filtering.

        Args:
            tags: List of tags to filter by (None = include all)
            summary_variant: Which summary variant to use

        Returns:
            Generated LaTeX content as string
        """
        # Load and process data
        cv_data = self._load_and_process_data(tags or [], summary_variant)

        # Render template
        template = self.env.get_template(self.template_name)
        return template.render(cv=cv_data)

    def generate_to_file(
        self,
        output_path: Path | str,
        tags: list[str] | None = None,
        summary_variant: str = "default",
    ) -> Path:
        """
        Generate LaTeX and write to file.

        Args:
            output_path: Path for output .tex file
            tags: List of tags to filter by
            summary_variant: Which summary variant to use

        Returns:
            Path to generated file
        """
        output_path = Path(output_path)
        content = self.generate(tags, summary_variant)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)
        return output_path

    def _load_and_process_data(self, tags: list[str], summary_variant: str) -> CVData:
        """Load, filter, and group CV data."""
        # Load contact (always included)
        contact = self.loader.load_contact()

        # Load summary
        summary = self.loader.load_summary(summary_variant)

        # Load and filter experiences
        exp_df = self.loader.load_experiences()
        if tags:
            exp_df = filter_by_tags(exp_df, tags)
        experiences = group_experiences(exp_df)

        # Load and filter skills
        skills_df = self.loader.load_skills()
        if tags:
            skills_df = filter_by_tags(skills_df, tags)
        skills = group_skills(skills_df)

        # Load education (always included)
        education = self.loader.load_education()

        # Load and filter patents
        patents_df = self.loader.load_patents()
        if tags:
            patents_df = filter_by_tags(patents_df, tags)
        patents_df = sort_by_weight(patents_df)
        patents = [Patent(**row.to_dict()) for _, row in patents_df.iterrows()]

        # Load and filter publications
        pubs_df = self.loader.load_publications()
        if tags:
            pubs_df = filter_by_tags(pubs_df, tags)
        pubs_df = sort_by_weight(pubs_df)
        publications = [Publication(**row.to_dict()) for _, row in pubs_df.iterrows()]

        return CVData(
            contact=contact,
            summary=summary,
            experiences=experiences,
            skills=skills,
            education=education,
            patents=patents,
            publications=publications,
        )
