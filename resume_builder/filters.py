"""Tag-based filtering for CV data."""

import pandas as pd

from .utils import parse_tags


def filter_by_tags(df: pd.DataFrame, tags: list[str], tags_column: str = "tags") -> pd.DataFrame:
    """
    Filter DataFrame rows by tags using OR logic.

    Include row if ANY of the selected tags match OR if 'always' tag is present.
    Empty tags list means include everything.

    Args:
        df: DataFrame with a tags column
        tags: List of tags to filter by (OR logic)
        tags_column: Name of the column containing pipe-separated tags

    Returns:
        Filtered DataFrame
    """
    if not tags:
        return df  # No filter = include all

    filter_tags = {t.lower() for t in tags}

    def row_matches(row_tags: str) -> bool:
        item_tags = parse_tags(row_tags)
        # Include if 'always' tag present OR any tag matches
        return "always" in item_tags or bool(item_tags & filter_tags)

    mask = df[tags_column].apply(row_matches)
    return df[mask]


def exclude_by_tags(
    df: pd.DataFrame, exclude_tags: list[str], tags_column: str = "tags"
) -> pd.DataFrame:
    """
    Exclude DataFrame rows that have ANY of the specified tags.

    Args:
        df: DataFrame with a tags column
        exclude_tags: List of tags to exclude (if ANY match, row is excluded)
        tags_column: Name of the column containing pipe-separated tags

    Returns:
        Filtered DataFrame with matching rows removed
    """
    if not exclude_tags:
        return df  # No exclusions = include all

    exclude_set = {t.lower() for t in exclude_tags}

    def row_excluded(row_tags: str) -> bool:
        item_tags = parse_tags(row_tags)
        # Exclude if ANY tag matches
        return bool(item_tags & exclude_set)

    mask = ~df[tags_column].apply(row_excluded)
    return df[mask]


def get_all_tags(df: pd.DataFrame, tags_column: str = "tags") -> set[str]:
    """
    Extract all unique tags from a DataFrame.

    Args:
        df: DataFrame with a tags column
        tags_column: Name of the column containing pipe-separated tags

    Returns:
        Set of all unique tags
    """
    all_tags: set[str] = set()
    for tags_str in df[tags_column].dropna():
        all_tags.update(parse_tags(tags_str))
    return all_tags


def collect_all_tags_from_loader(loader) -> dict[str, set[str]]:
    """
    Collect all tags from all filterable sections.

    Args:
        loader: CVDataLoader instance

    Returns:
        Dictionary mapping section name to set of tags
    """
    tags_by_section = {}

    try:
        df = loader.load_experiences()
        tags_by_section["experiences"] = get_all_tags(df)
    except FileNotFoundError:
        pass

    try:
        df = loader.load_skills()
        tags_by_section["skills"] = get_all_tags(df)
    except FileNotFoundError:
        pass

    try:
        df = loader.load_patents()
        tags_by_section["patents"] = get_all_tags(df)
    except FileNotFoundError:
        pass

    try:
        df = loader.load_publications()
        tags_by_section["publications"] = get_all_tags(df)
    except FileNotFoundError:
        pass

    return tags_by_section
