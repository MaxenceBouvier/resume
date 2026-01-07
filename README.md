## CV Generator

A data-driven CV and website generator that builds tailored CVs from CSV data sources with tag-based filtering.

### Installation

Install the package in editable mode using [uv](https://docs.astral.sh/uv/):

```sh
uv pip install -e .
```

### CLI Usage

The `make_cv` command provides several subcommands:

```sh
# Generate LaTeX CV (optionally filtered by tags)
make_cv latex --tags ml,hardware

# Generate website JSON data
make_cv website

# Generate both outputs
make_cv all --tags ml

# List available tags
make_cv tags

# Validate CV data files
make_cv validate

# Build PDF from LaTeX file (uses Docker, temp files in tex_tmp/)
make_cv build-pdf                              # defaults to maxence_bouvier_resume.tex
make_cv build-pdf path/to/other.tex            # or specify a file
```

#### Options

- `-t, --tags`: Filter by tags (OR logic). Can be repeated or comma-separated.
- `-o, --output`: Output file/directory path.
- `--data-dir`: Path to `cv_data/` directory.
- `--template-dir`: Path to `templates/` directory.
- `-s, --summary`: Summary variant to use (default: "default").

### Project Structure

```
cv_data/           # CSV data sources
templates/         # Jinja2 LaTeX templates
output/            # Generated outputs
ext/bio-website-launch/  # Website submodule (JSON data destination)
```

### Legacy: Build Using Docker

If you prefer to invoke Docker directly:

```sh
docker build -t latex .
docker run --rm -i -v "$PWD":/data latex pdflatex maxence_bouvier_resume.tex
```

### Preview

![Resume Screenshot](/resume_preview.png)
