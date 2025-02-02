from pathlib import Path
import typst
import os
import sys
import subprocess

CWD = Path.cwd()


def generate_note(topic: str):
    typst.compile(
        str(CWD / "typst" / "main.typ"),
        str(CWD / "typst" / f"{topic}.pdf"),
        str(CWD / "typst"),
    )
    open_pdf(str(CWD / "typst" / f"{topic}.pdf"))

def open_pdf(location: str):
    if sys.platform.startswith('win'):
        subprocess.call(['start', location], shell=True)
    elif sys.platform.startswith('darwin'):
        subprocess.call(['open', location])
