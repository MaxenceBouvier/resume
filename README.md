### Build Using `make_cv`

Install the package in editable mode using [uv](https://docs.astral.sh/uv/):

```sh
uv pip install -e .
```

Then build a CV PDF by supplying the path to the LaTeX source file:

```sh
make_cv --cv_filepath maxence_bouvier_resume.tex
```

### Build using Docker

If you prefer to invoke Docker directly, you can run:

```sh
docker build -t latex .
docker run --rm -i -v "$PWD":/data latex pdflatex maxence_bouvier_resume.tex
```

### Preview

![Resume Screenshot](/resume_preview.png)

## Setup Guidelines for JavaScript Parser Integration

To extract the `experiences` array from your React/TypeScript file and convert it to LaTeX, this project uses a Node.js script as a parser. Follow these steps to set up and use the parser:

### 1. Install Node.js

Make sure Node.js is installed on your system. You can check by running:

```bash
node --version
```
If not installed, download it from https://nodejs.org/ or use your package manager:

```bash
# Ubuntu/Debian
sudo apt-get install nodejs npm
cd react_to_latex
npm install acorn
```

### 2. Usage

The Python script will automatically call the Node.js parser. However, you can also run it manually for debugging:

```bash
cd react_to_latex
node extract_experiences_acorn.js /absolute/path/to/Experience.tsx
```

This will print the extracted `experiences` array as JSON to stdout.

### 3. Environment Variable

Set the `WEBSITE_REPO_PATH` environment variable to the root of your website repository, so the script can find `src/components/Experience.tsx`:

```bash
export WEBSITE_REPO_PATH=/absolute/path/to/your/website/repo
```

### 4. Run the Python Script

From the project root:

```bash
python3 react_to_latex/main.py
```

This will generate `experience.tex` from your website's experience data.

---

If you encounter issues with Node.js or the parser, ensure your `Experience.tsx` file uses only data (no functions or complex JS expressions) in the `experiences` array.
