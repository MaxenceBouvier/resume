# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Critical Rule

**NEVER manually edit the LaTeX file or website JSON files directly.** Always use the `make_cv` CLI to generate outputs from the CSV data sources in `cv_data/`.

## Commands

```bash
# Install in development mode
uv pip install -e .

# Generate LaTeX CV (auto-excludes 'private' by default)
make_cv latex
make_cv latex --tags ml,hardware

# Generate website JSON data (auto-excludes 'private,sensitive' by default)
make_cv website

# Generate both outputs
make_cv all

# List available tags across all CSV files
make_cv tags

# Validate all CSV data files
make_cv validate

# Build PDF from LaTeX (uses Docker)
make_cv build-pdf

# Linting and type checking (run automatically by pre-commit)
uv run ruff check --fix .
uv run ty check
```

## Architecture

This is a data-driven CV/website generator that builds tailored outputs from CSV data with tag-based filtering.

**Data Flow:** CSV files → Pydantic validation → Tag filtering → Grouping transformation → LaTeX or JSON output

### Key Directories

- `cv_data/` - CSV data sources (contact, experiences, skills, education, patents, publications, summary)
- `templates/resume.tex.j2` - Jinja2 template for LaTeX output
- `ext/bio-website-launch/src/data/` - Target directory for website JSON files (git submodule)

### resume_builder/ Module Structure

- `cli.py` - Click-based CLI with 6 commands (latex, website, all, tags, validate, build-pdf)
- `loader.py` - CVDataLoader: CSV parsing and Pydantic validation
- `filters.py` - Tag filtering functions (filter_by_tags, exclude_by_tags)
- `models.py` - Pydantic models for each CSV type
- `generators/latex.py` - LaTeXGenerator: Jinja2 template rendering
- `generators/website.py` - WebsiteGenerator: JSON output for React site

### Tag System

Tags in CSV are pipe-separated (e.g., `"ai|ml|python|always"`). The special `always` tag forces inclusion regardless of filter. Filter uses OR logic; exclude uses AND logic (runs after include filter).

## Code Style

- Line length: 100 characters
- Python 3.10+
- Pre-commit hooks run ruff formatting and ty type checking
