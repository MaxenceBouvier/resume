#!/bin/bash
docker run --rm -i -v "$PWD":/data -w /data blang/latex pdflatex maxence_bouvier_resume.tex