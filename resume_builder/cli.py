"""Command-line interface to build a CV PDF from a LaTeX source."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def build_cv(cv_filepath: str) -> None:
    """Build a CV PDF using Docker and pdflatex.

    Parameters
    ----------
    cv_filepath: str
        Path to the LaTeX file describing the CV.
    """
    path = Path(cv_filepath).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist")

    directory = path.parent
    file_name = path.name

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
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a CV PDF from a LaTeX file using Docker."
    )
    parser.add_argument(
        "--cv_filepath",
        required=True,
        help="Path to the LaTeX file for the CV",
    )
    args = parser.parse_args()
    build_cv(args.cv_filepath)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
