#!/usr/bin/env python3
"""
Compiles the GTU DI05000341 Pramaan project reports using pdflatex.
Generates:
1. docs/Pramaan_Report_Team.pdf & docs/Pramaan_Report.pdf (Team submission copy)
2. docs/Pramaan_Report_Aayush_Avinash_Bankar.pdf (Individual student copy - Aayush)
3. docs/Pramaan_Report_Meet_Jayeshbhai_Patel.pdf (Individual student copy - Meet)
"""

import os
import subprocess
import shutil

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
TEX_FILE = os.path.join(DOCS_DIR, "Pramaan_Report.tex")


def compile_latex():
    cmd = ["pdflatex", "-interaction=nonstopmode", "Pramaan_Report.tex"]
    res = subprocess.run(cmd, cwd=DOCS_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("LaTeX compilation failed:")
        for line in res.stdout.splitlines():
            if line.startswith("!"):
                print(line)
        raise RuntimeError("pdflatex compilation failed")


def set_copy_mode(content: str, mode: int) -> str:
    import re
    return re.sub(r"\\newcommand\{\\copyMode\}\{\d+\}", rf"\\newcommand{{\\copyMode}}{{{mode}}}", content)


def main():
    print("[1/5] Reading base Pramaan_Report.tex...")
    with open(TEX_FILE, "r") as f:
        base_content = f.read()

    # 1. Compile Copy 0 (Team Submission Copy)
    print("[2/5] Compiling Team Copy (Master / Department submission)...")
    with open(TEX_FILE, "w") as f:
        f.write(set_copy_mode(base_content, 0))
    compile_latex()
    compile_latex()  # second pass for TOC / references
    shutil.copy(os.path.join(DOCS_DIR, "Pramaan_Report.pdf"),
                os.path.join(DOCS_DIR, "Pramaan_Report_Team.pdf"))

    # 2. Compile Copy 1 (Aayush Avinash Bankar Individual Copy)
    print("[3/5] Compiling Individual Copy (Aayush Avinash Bankar)...")
    with open(TEX_FILE, "w") as f:
        f.write(set_copy_mode(base_content, 1))
    compile_latex()
    compile_latex()
    shutil.copy(os.path.join(DOCS_DIR, "Pramaan_Report.pdf"),
                os.path.join(DOCS_DIR, "Pramaan_Report_Aayush_Avinash_Bankar.pdf"))

    # 3. Compile Copy 2 (Meet Jayeshbhai Patel Individual Copy)
    print("[4/5] Compiling Individual Copy (Meet Jayeshbhai Patel)...")
    with open(TEX_FILE, "w") as f:
        f.write(set_copy_mode(base_content, 2))
    compile_latex()
    compile_latex()
    shutil.copy(os.path.join(DOCS_DIR, "Pramaan_Report.pdf"),
                os.path.join(DOCS_DIR, "Pramaan_Report_Meet_Jayeshbhai_Patel.pdf"))

    # 4. Restore original base content (Mode 0)
    print("[5/5] Restoring base Pramaan_Report.tex and master Pramaan_Report.pdf...")
    with open(TEX_FILE, "w") as f:
        f.write(set_copy_mode(base_content, 0))
    compile_latex()
    print("All 3 report versions compiled and verified successfully:")
    print("  1. Team Copy:       docs/Pramaan_Report_Team.pdf (and docs/Pramaan_Report.pdf)")
    print("  2. Individual Copy: docs/Pramaan_Report_Aayush_Avinash_Bankar.pdf")
    print("  3. Individual Copy: docs/Pramaan_Report_Meet_Jayeshbhai_Patel.pdf")


if __name__ == "__main__":
    main()
