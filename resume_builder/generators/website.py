"""Website JSON generator for React components."""

import json
from pathlib import Path


from ..filters import filter_by_tags
from ..loader import CVDataLoader
from .base import group_skills, sort_by_weight


class WebsiteGenerator:
    """Generate JSON data files for React website."""

    def __init__(self, data_dir: Path | str, output_dir: Path | str):
        """
        Initialize website generator.

        Args:
            data_dir: Path to cv_data/ directory
            output_dir: Path to website's src/data/ directory
        """
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.loader = CVDataLoader(self.data_dir)

    def generate_all(self, tags: list[str] | None = None) -> dict[str, Path]:
        """
        Generate all JSON data files for the website.

        Args:
            tags: Optional tag filter (usually None for website)

        Returns:
            Dictionary mapping filename to output path
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)
        generated = {}

        generated["experiences.json"] = self._generate_experiences(tags)
        generated["skills.json"] = self._generate_skills(tags)
        generated["publications.json"] = self._generate_publications(tags)
        generated["contact.json"] = self._generate_contact()

        return generated

    def _generate_experiences(self, tags: list[str] | None) -> Path:
        """Generate experiences.json for website."""
        df = self.loader.load_experiences()
        if tags:
            df = filter_by_tags(df, tags)

        # Group by job but handle multi-position companies like SONY
        experiences = []

        # First group by company to detect multi-position entries
        company_groups = df.groupby("company", sort=False)

        for company, company_df in company_groups:
            # Check if company has multiple positions
            positions = company_df[["position", "period"]].drop_duplicates()

            if len(positions) > 1:
                # Multi-position company (like SONY)
                location = company_df.iloc[0]["location"]
                positions_list = []

                for _, pos_row in positions.iterrows():
                    pos_df = company_df[
                        (company_df["position"] == pos_row["position"])
                        & (company_df["period"] == pos_row["period"])
                    ].sort_values("weight", ascending=False)

                    positions_list.append(
                        {
                            "title": pos_row["position"],
                            "period": pos_row["period"],
                            "achievements": pos_df["achievement_text"].tolist(),
                        }
                    )

                experiences.append(
                    {
                        "company": company,
                        "location": location,
                        "positions": positions_list,
                    }
                )
            else:
                # Single position company
                sorted_df = company_df.sort_values("weight", ascending=False)
                experiences.append(
                    {
                        "company": company,
                        "position": sorted_df.iloc[0]["position"],
                        "location": sorted_df.iloc[0]["location"],
                        "period": sorted_df.iloc[0]["period"],
                        "achievements": sorted_df["achievement_text"].tolist(),
                    }
                )

        output_path = self.output_dir / "experiences.json"
        output_path.write_text(json.dumps(experiences, indent=2))
        return output_path

    def _generate_skills(self, tags: list[str] | None) -> Path:
        """Generate skills.json for website."""
        df = self.loader.load_skills()
        if tags:
            df = filter_by_tags(df, tags)

        grouped = group_skills(df)

        # Convert to website format with icon mapping
        skills_data = [
            {
                "icon": skill.icon,
                "title": skill.category,
                "skills": skill.skills,
            }
            for skill in grouped
        ]

        output_path = self.output_dir / "skills.json"
        output_path.write_text(json.dumps(skills_data, indent=2))
        return output_path

    def _generate_publications(self, tags: list[str] | None) -> Path:
        """Generate publications.json for website."""
        df = self.loader.load_publications()
        if tags:
            df = filter_by_tags(df, tags)
        df = sort_by_weight(df)

        publications = []
        for _, row in df.iterrows():
            publications.append(
                {
                    "authors": row["authors"],
                    "title": row["title"],
                    "venue": row["venue"],
                    "year": int(row["year"]),
                    "url": row["url"],
                }
            )

        output_path = self.output_dir / "publications.json"
        output_path.write_text(json.dumps(publications, indent=2))
        return output_path

    def _generate_contact(self) -> Path:
        """Generate contact.json for website."""
        contact = self.loader.load_contact()

        contact_data = {
            "name": contact.name,
            "email": contact.email,
            "phone": contact.phone,
            "linkedin": contact.linkedin,
            "scholar": contact.scholar,
        }

        output_path = self.output_dir / "contact.json"
        output_path.write_text(json.dumps(contact_data, indent=2))
        return output_path
