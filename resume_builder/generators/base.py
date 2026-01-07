"""Base grouping logic for transforming flat CSV data into hierarchical structures."""

from typing import Any, cast

import pandas as pd

from ..models import GroupedExperience, GroupedSkill


def group_experiences(df: pd.DataFrame) -> list[GroupedExperience]:
    """
    Transform flat filtered DataFrame into hierarchical experience structure.

    Groups achievements by (company, location, position, period) and sorts
    bullets by weight within each group.

    Args:
        df: Filtered DataFrame from experiences.csv

    Returns:
        List of GroupedExperience objects ready for template rendering
    """
    if df.empty:
        return []

    experiences = []

    # Group by job context (preserves CSV order for jobs via sort=False)
    grouped = df.groupby(["company", "location", "position", "period"], sort=False)

    for key, group in grouped:
        # Cast key to tuple for type safety (pandas returns tuple for multi-column groupby)
        key_tuple = cast(tuple[Any, Any, Any, Any], key)
        company, loc, pos, period = (
            str(key_tuple[0]),
            str(key_tuple[1]),
            str(key_tuple[2]),
            str(key_tuple[3]),
        )
        # Sort bullets by weight within the job (descending = highest first)
        sorted_group = group.sort_values("weight", ascending=False)

        # Group achievements by achievement_group if present
        achievement_groups: dict[str, list[str]] = {}
        ungrouped_achievements: list[str] = []

        for _, row in sorted_group.iterrows():
            text = row["achievement_text"]
            group_name = row.get("achievement_group", "")

            if group_name and pd.notna(group_name) and group_name.strip():
                achievement_groups.setdefault(group_name, []).append(text)
            else:
                ungrouped_achievements.append(text)

        # Flatten all achievements for simple rendering
        all_achievements = ungrouped_achievements.copy()
        for group_achievements in achievement_groups.values():
            all_achievements.extend(group_achievements)

        experiences.append(
            GroupedExperience(
                company=company,
                location=loc,
                position=pos,
                period=period,
                achievements=sorted_group["achievement_text"].tolist(),
                achievement_groups=achievement_groups,
            )
        )

    return experiences


def group_skills(df: pd.DataFrame) -> list[GroupedSkill]:
    """
    Transform flat filtered DataFrame into grouped skills by category.

    Groups skills by category, preserving icon and sorting by weight.

    Args:
        df: Filtered DataFrame from skills.csv

    Returns:
        List of GroupedSkill objects ready for template rendering
    """
    if df.empty:
        return []

    skills = []

    # Group by category (preserves order)
    grouped = df.groupby("category", sort=False)

    for cat_key, group in grouped:
        category = str(cat_key)
        # Sort skills by weight within category (descending)
        sorted_group = group.sort_values("weight", ascending=False)

        # Get icon from first row (all rows in category should have same icon)
        icon = sorted_group.iloc[0]["icon"] if "icon" in sorted_group.columns else "Code"

        skills.append(
            GroupedSkill(
                category=category,
                icon=icon,
                skills=sorted_group["skill"].tolist(),
            )
        )

    return skills


def sort_by_weight(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sort DataFrame by weight column (descending).

    Args:
        df: DataFrame with weight column

    Returns:
        Sorted DataFrame
    """
    if "weight" in df.columns:
        return df.sort_values("weight", ascending=False)
    return df
