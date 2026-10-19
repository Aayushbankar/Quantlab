#!/usr/bin/env python3
"""
Compiles the GTU DI05000341 Pramaan project reports using pdflatex.
Generates:
1. docs/Pramaan_Report.pdf (Master report)
2. docs/Pramaan_Report_Aayush_Avinash_Bankar.pdf (Team copy 1 of 2)
3. docs/Pramaan_Report_Meet_Jayeshbhai_Patel.pdf (Team copy 2 of 2)
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


def main():
    print("[1/4] Reading base Pramaan_Report.tex...")
    with open(TEX_FILE, "r") as f:
        content = f.read()

    # 1. Compile Copy 1 (Aayush)
    print("[2/4] Compiling Copy 1 (Aayush Avinash Bankar)...")
    compile_latex()
    compile_latex()  # second pass for TOC / references
    shutil.copy(os.path.join(DOCS_DIR, "Pramaan_Report.pdf"),
                os.path.join(DOCS_DIR, "Pramaan_Report_Aayush_Avinash_Bankar.pdf"))

    # 2. Compile Copy 2 (Meet)
    print("[3/4] Compiling Copy 2 (Meet Jayeshbhai Patel)...")
    meet_content = content.replace(
        r"\texttt{Team copy \copyNo\ of 2 --- deposited by \memberLead}",
        r"\texttt{Team copy 2 of 2 --- deposited by \otherName}"
    )
    with open(TEX_FILE, "w") as f:
        f.write(meet_content)

    compile_latex()
    compile_latex()
    shutil.copy(os.path.join(DOCS_DIR, "Pramaan_Report.pdf"),
                os.path.join(DOCS_DIR, "Pramaan_Report_Meet_Jayeshbhai_Patel.pdf"))

    # 3. Restore original content for Master / Copy 1
    print("[4/4] Restoring Master Pramaan_Report.tex and Pramaan_Report.pdf...")
    with open(TEX_FILE, "w") as f:
        f.write(content)
    compile_latex()
    print("All 3 report PDFs compiled and verified successfully.")


if __name__ == "__main__":
    main()
