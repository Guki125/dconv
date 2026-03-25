# dconv — DOCX/DOC ↔ PDF Converter

A fast, headless CLI tool for batch converting `.docx` / `.doc` files to PDF and back — no GUI, no Microsoft Word pop-ups.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)

---

## Features

- 📄 **DOCX / DOC → PDF** via LibreOffice headless (no Word required)
- 📝 **PDF → DOCX** via `pdf2docx`
- 📦 **Batch conversion** — pass multiple files or glob patterns (`*.docx`, `**/*.docx`)
- 📁 **Custom output directory** with `-o`
- ⚡ **Progress bar** with `tqdm`
- 🎨 **Colored output** with `colorama`
- 🔁 **Conflict handling** — `--skip-existing` or `--force`
- 🖥️ **Cross-platform** — macOS, Linux, Windows

---

## Requirements

- Python 3.10+
- [LibreOffice](https://www.libreoffice.org/download/download/) (for DOCX/DOC → PDF)

### Install LibreOffice

| OS | Command |
|---|---|
| macOS | `brew install --cask libreoffice` |
| Ubuntu / Debian | `sudo apt install libreoffice` |
| Windows | [Download installer](https://www.libreoffice.org/download/download/) |

---

## Installation

### macOS & Linux — one command

```bash
git clone https://github.com/Guki125/dconv.git
cd dconv
chmod +x install.sh && ./install.sh
```

The script automatically:
- Checks for Python 3.10+
- Installs LibreOffice if not present (via `brew` on macOS, `apt` / `dnf` / `pacman` on Linux)
- Runs `pip install -e .` to register the `dconv` command

### Windows

```bat
git clone https://github.com/Guki125/dconv.git
cd dconv
install.bat
```

The script automatically:
- Checks for Python 3.10+
- Installs LibreOffice via `winget` if not present
- Runs `pip install -e .`

### Manual install (any OS)

```bash
pip install -e .
```

> LibreOffice is required for DOCX/DOC → PDF:
>
> | OS | Command |
> |---|---|
> | macOS | `brew install --cask libreoffice` |
> | Ubuntu / Debian | `sudo apt install libreoffice` |
> | Windows | [Download installer](https://www.libreoffice.org/download/download/) |

---

## Usage

### DOCX / DOC → PDF

```bash
# Single file
dconv to-pdf report.docx

# Multiple files
dconv to-pdf file1.docx file2.doc file3.docx

# Glob pattern
dconv to-pdf "*.docx"
dconv to-pdf "**/*.docx"        # recursive

# Custom output directory
dconv to-pdf *.docx -o ./pdfs

# Skip already converted files
dconv to-pdf *.docx --skip-existing

# Overwrite without prompting
dconv to-pdf *.docx --force

# Verbose output
dconv to-pdf *.docx -v
```

### PDF → DOCX

```bash
dconv to-docx scan.pdf
dconv to-docx *.pdf -o ./word_files --skip-existing -v
```

---

## Options

| Flag | Description |
|---|---|
| `-o`, `--output DIR` | Directory to save converted files |
| `--skip-existing` | Skip files that already have a converted version |
| `--force` | Overwrite existing files without prompting |
| `-v`, `--verbose` | Show detailed output for each file |
| `-h`, `--help` | Show help message |

---

## Project Structure

```
dconv/
├── docx2pdf_cli/
│   ├── __init__.py
│   ├── main.py             # Entry point
│   ├── cli.py              # argparse + subcommands
│   ├── utils.py            # Glob, colors, summary
│   └── converter/
│       ├── __init__.py
│       ├── to_pdf.py       # DOCX/DOC → PDF (LibreOffice)
│       └── to_docx.py      # PDF → DOCX (pdf2docx)
├── pyproject.toml
├── requirements.txt
├── LICENSE
├── CONTRIBUTING.md
└── README.md
```

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.

---

## License

MIT — see [LICENSE](LICENSE) for details.
