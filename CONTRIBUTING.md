# Contributing to dconv

Thanks for taking the time to contribute! 🎉

---

## Getting Started

1. **Fork** the repository
2. **Clone** your fork:
   ```bash
   git clone https://github.com/your-username/dconv.git
   cd dconv
   ```
3. **Create a branch** for your change:
   ```bash
   git checkout -b feat/your-feature-name
   ```
4. **Install in editable mode**:
   ```bash
   pip install -e .
   ```
5. Make your changes, then **commit**:
   ```bash
   git commit -m "feat: describe your change"
   ```
6. **Push** and open a **Pull Request** against `main`

---

## Commit Message Format

Use short, descriptive prefixes:

| Prefix | When to use |
|---|---|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation only |
| `refactor:` | Code restructure, no behavior change |
| `test:` | Adding or fixing tests |
| `chore:` | Tooling, deps, CI |

Example: `fix: handle missing LibreOffice on Windows`

---

## Project Structure

```
docx2pdf_cli/
├── main.py          # Entry point
├── cli.py           # CLI subcommands (argparse)
├── utils.py         # Shared helpers
└── converter/
    ├── to_pdf.py    # DOCX/DOC → PDF logic
    └── to_docx.py  # PDF → DOCX logic
```

- **New conversion format?** Add a file in `converter/` and wire it up in `cli.py`
- **New CLI flag?** Add it in `cli.py` → `_add_common_args()` or the relevant subcommand

---

## Reporting Bugs

Please use the [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) issue template and include:

- Your OS and Python version
- Whether LibreOffice is installed and its version
- The exact command you ran
- Full error output

---

## Suggesting Features

Use the [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) template. Describe the use case, not just the solution.

---

## Code Style

- Follow existing code conventions (no linter enforced yet)
- Keep functions small and focused
- Add a comment when the logic isn't obvious

---

## Questions?

Open a [Discussion](https://github.com/your-username/dconv/discussions) or just file an issue — no question is too small.
