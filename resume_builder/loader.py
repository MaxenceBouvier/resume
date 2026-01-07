"""CSV data loader with validation."""

from pathlib import Path

import pandas as pd
from pydantic import ValidationError

from .models import Contact, Education, Experience, Patent, Publication, Skill


class CVDataLoader:
    """Load and validate CV data from CSV files."""

    def __init__(self, data_dir: Path | str):
        """
        Initialize loader with data directory.

        Args:
            data_dir: Path to cv_data/ directory containing CSV files
        """
        self.data_dir = Path(data_dir)
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")

    def _read_csv(self, filename: str) -> pd.DataFrame:
        """Read a CSV file from the data directory."""
        filepath = self.data_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"CSV file not found: {filepath}")
        return pd.read_csv(filepath)

    def load_contact(self) -> Contact:
        """Load contact information."""
        df = self._read_csv("contact.csv")
        if df.empty:
            raise ValueError("contact.csv is empty")
        row = df.iloc[0].to_dict()
        return Contact(**row)

    def load_summary(self, variant: str = "default") -> str:
        """Load summary text for a specific variant."""
        try:
            df = self._read_csv("summary.csv")
            summaries = {row["variant"]: row["text"] for _, row in df.iterrows()}
            return summaries.get(variant, summaries.get("default", ""))
        except FileNotFoundError:
            return ""

    def load_experiences(self) -> pd.DataFrame:
        """Load experiences as DataFrame (for filtering/grouping)."""
        df = self._read_csv("experiences.csv")
        # Fill NaN values
        df["achievement_group"] = df["achievement_group"].fillna("")
        df["tags"] = df["tags"].fillna("")
        df["weight"] = df["weight"].fillna(0).astype(int)
        df["papers"] = df["papers"].fillna(0).astype(int)
        df["patents"] = df["patents"].fillna(0).astype(int)
        return df

    def load_skills(self) -> pd.DataFrame:
        """Load skills as DataFrame (for filtering/grouping)."""
        df = self._read_csv("skills.csv")
        df["tags"] = df["tags"].fillna("")
        df["icon"] = df["icon"].fillna("Code")
        df["weight"] = df["weight"].fillna(0).astype(int)
        return df

    def load_education(self) -> list[Education]:
        """Load education entries (always included, no filtering)."""
        df = self._read_csv("education.csv")
        return [Education(**row.to_dict()) for _, row in df.iterrows()]

    def load_patents(self) -> pd.DataFrame:
        """Load patents as DataFrame (for filtering)."""
        df = self._read_csv("patents.csv")
        df["tags"] = df["tags"].fillna("")
        df["weight"] = df["weight"].fillna(0).astype(int)
        return df

    def load_publications(self) -> pd.DataFrame:
        """Load publications as DataFrame (for filtering)."""
        df = self._read_csv("publications.csv")
        df["tags"] = df["tags"].fillna("")
        df["weight"] = df["weight"].fillna(0).astype(int)
        return df

    def validate_all(self) -> dict[str, list[str]]:
        """
        Validate all CSV files and return any errors.

        Returns:
            Dictionary mapping filename to list of validation errors
        """
        errors: dict[str, list[str]] = {}

        # Validate contact
        try:
            self.load_contact()
        except (FileNotFoundError, ValidationError, ValueError) as e:
            errors["contact.csv"] = [str(e)]

        # Validate experiences
        try:
            df = self.load_experiences()
            for idx, row in df.iterrows():
                try:
                    Experience(**row.to_dict())
                except ValidationError as e:
                    errors.setdefault("experiences.csv", []).append(f"Row {idx}: {e}")
        except FileNotFoundError as e:
            errors["experiences.csv"] = [str(e)]

        # Validate skills
        try:
            df = self.load_skills()
            for idx, row in df.iterrows():
                try:
                    Skill(**row.to_dict())
                except ValidationError as e:
                    errors.setdefault("skills.csv", []).append(f"Row {idx}: {e}")
        except FileNotFoundError as e:
            errors["skills.csv"] = [str(e)]

        # Validate education
        try:
            self.load_education()
        except (FileNotFoundError, ValidationError) as e:
            errors["education.csv"] = [str(e)]

        # Validate patents
        try:
            df = self.load_patents()
            for idx, row in df.iterrows():
                try:
                    Patent(**row.to_dict())
                except ValidationError as e:
                    errors.setdefault("patents.csv", []).append(f"Row {idx}: {e}")
        except FileNotFoundError as e:
            errors["patents.csv"] = [str(e)]

        # Validate publications
        try:
            df = self.load_publications()
            for idx, row in df.iterrows():
                try:
                    Publication(**row.to_dict())
                except ValidationError as e:
                    errors.setdefault("publications.csv", []).append(f"Row {idx}: {e}")
        except FileNotFoundError as e:
            errors["publications.csv"] = [str(e)]

        return errors
