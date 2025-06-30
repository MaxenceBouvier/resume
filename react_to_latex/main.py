import json
import re
import ast
import subprocess
import os
from pathlib import Path

def extract_experiences(js_code):
    """
    Extracts the experiences array from the React file string.
    """
    # Find the experiences = [ ... ]; block (non-greedy match for nested []s)
    match = re.search(r"experiences\s*=\s*(\[[\s\S]*?\]);", js_code)
    if not match:
        raise ValueError("Could not find experiences array in file.")
    array_str = match.group(1)
    return array_str

def js_to_py(js_str):
    """
    Converts minimal JS object/array syntax to Python-compatible syntax for ast.literal_eval.
    (Assumes only keys/values as shown in your data; not full JS parser.)
    """
    # Replace JS null/true/false
    js_str = re.sub(r'\bnull\b', 'None', js_str)
    js_str = re.sub(r'\btrue\b', 'True', js_str, flags=re.IGNORECASE)
    js_str = re.sub(r'\bfalse\b', 'False', js_str, flags=re.IGNORECASE)
    # Ensure all keys are quoted
    js_str = re.sub(r'(\w+)\s*:', r'"\1":', js_str)
    # Replace single quotes with double quotes
    js_str = js_str.replace("'", '"')
    # Escape double quotes inside string values (not at start/end)
    def escape_inner_quotes(match):
        s = match.group(1)
        # Only escape unescaped double quotes inside the string
        s_escaped = re.sub(r'(?<!\\)\"', r'\\"', s)  # already escaped
        s_escaped = re.sub(r'(?<!\\)"', r'\\"', s_escaped)
        return '"' + s_escaped + '"'
    js_str = re.sub(r'"((?:[^"\\]|\\.)*)"', escape_inner_quotes, js_str)
    # Remove trailing commas (object/array)
    js_str = re.sub(r',([\s\n]*[}}\]])', r'\1', js_str)
    return js_str


def escape_latex(text):
    # Simple LaTeX escaping
    text = text.replace('&', '\\&')
    text = text.replace('%', '\\%')
    text = text.replace('#', '\\#')
    text = text.replace('_', '\\_')
    text = text.replace('$', '\\$')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    text = text.replace('~', '\\textasciitilde{}')
    text = text.replace('^', '\\^{}')
    text = text.replace('\\', '\\textbackslash{}')
    return text

def render_achievements(achievements, indent="      "):
    out = []
    for ach in achievements:
        ach = escape_latex(ach)
        out.append(f"{indent}\\item {ach}")
    return "\n".join(out)

def render_position(company, loc, title, period, achievements, indent="    "):
    latex = f"""{indent}\\resumeSubSubheading
{indent}  {{{escape_latex(title)}}}{{{escape_latex(period)}}}
{indent}  \\resumeItemListStart
{render_achievements(achievements, indent+'    ')}
{indent}  \\resumeItemListEnd
"""
    return latex

def render_experience(exp):
    output = ""
    company = exp["company"]
    loc = exp["location"]
    if "positions" in exp:
        # Multi-position case (e.g., Sony)
        output += f"    \\resumeSubheading\n"
        output += f"      {{{escape_latex(company)}}}{{{escape_latex(loc)}}}{{}}{{}}\n"
        for i, pos in enumerate(exp["positions"]):
            output += render_position(company, loc, pos["title"], pos["period"], pos["achievements"])
    else:
        title = exp["position"]
        period = exp["period"]
        achievements = exp["achievements"]
        output += f"    \\resumeSubheading\n"
        output += f"      {{{escape_latex(company)}}}{{{escape_latex(loc)}}}{{{escape_latex(title)}}}{{{escape_latex(period)}}}\n"
        output += f"      \\resumeItemListStart\n"
        output += render_achievements(achievements, "        ")
        output += f"\n      \\resumeItemListEnd\n"
    return output

def write_latex_experience(experiences, output_filename):
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("%-----------EXPERIENCE-----------------\n")
        f.write("\\section{Experience}\n")
        f.write("  \\resumeSubHeadingListStart\n")
        for exp in experiences:
            f.write(render_experience(exp))
        f.write("  \\resumeSubHeadingListEnd\n")


def main():
    # --- Part 1: Use Node.js (acorn) to extract experiences array as JSON ---
    react_filename = Path(os.environ["WEBSITE_REPO_PATH"]) / "src/components/Experience.tsx"
    node_script = Path(__file__).parent / "extract_experiences_acorn.js"
    result = subprocess.run([
        "node", str(node_script), str(react_filename)
    ], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error extracting experiences:", result.stderr)
        exit(1)
    experiences = json.loads(result.stdout)

    # --- Output to file ---
    output_filename = "experience.tex"
    write_latex_experience(experiences, output_filename)
    print(f"LaTeX written to {output_filename}")

if __name__ == "__main__":
    main()
