"""CLI — argparse + субкоманди to-pdf / to-docx"""

import argparse
from .utils import resolve_files, print_summary
from .converter.to_pdf import convert_to_pdf
from .converter.to_docx import convert_to_docx


# ── builder ──────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="converter",
        description="📄  Пакетний конвертер DOCX/DOC ↔ PDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Приклади:
  converter to-pdf report.docx
  converter to-pdf *.docx -o ./output
  converter to-pdf doc1.docx doc2.doc --force
  converter to-docx scan.pdf invoice.pdf -o ./word_files
  converter to-docx *.pdf --skip-existing -v
        """,
    )

    sub = parser.add_subparsers(title="Команди", metavar="<команда>")

    # ── to-pdf ────────────────────────────────────────────────────────────────
    p_pdf = sub.add_parser(
        "to-pdf",
        help="Конвертувати DOCX/DOC → PDF",
        description="Конвертує один або кілька .docx / .doc файлів у PDF.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Приклади:
  converter to-pdf file.docx
  converter to-pdf *.docx -o ./pdfs --force
        """,
    )
    _add_common_args(p_pdf, exts=[".docx", ".doc"])
    p_pdf.set_defaults(func=_cmd_to_pdf)

    # ── to-docx ───────────────────────────────────────────────────────────────
    p_docx = sub.add_parser(
        "to-docx",
        help="Конвертувати PDF → DOCX",
        description="Конвертує один або кілька .pdf файлів у DOCX.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Приклади:
  converter to-docx file.pdf
  converter to-docx *.pdf -o ./docs --skip-existing
        """,
    )
    _add_common_args(p_docx, exts=[".pdf"])
    p_docx.set_defaults(func=_cmd_to_docx)

    return parser


def _add_common_args(p: argparse.ArgumentParser, exts: list[str]):
    p.add_argument(
        "files",
        nargs="+",
        metavar="FILE",
        help=f"Файли або glob-патерни ({', '.join(exts)})",
    )
    p.add_argument(
        "-o", "--output",
        metavar="DIR",
        help="Директорія для збереження результатів (за замовчуванням — поруч з оригіналом)",
    )
    p.add_argument(
        "--skip-existing",
        action="store_true",
        help="Пропускати вже існуючі файли",
    )
    p.add_argument(
        "--force",
        action="store_true",
        help="Перезаписувати існуючі файли без питань",
    )
    p.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Детальний вивід",
    )


# ── runners ───────────────────────────────────────────────────────────────────

def run(args):
    args.func(args)


def _cmd_to_pdf(args):
    files = resolve_files(args.files, exts=[".docx", ".doc"])
    if not files:
        print("❌  Файлів для конвертації не знайдено.")
        return
    results = convert_to_pdf(files, output_dir=args.output,
                             skip_existing=args.skip_existing,
                             force=args.force, verbose=args.verbose)
    print_summary(results)


def _cmd_to_docx(args):
    files = resolve_files(args.files, exts=[".pdf"])
    if not files:
        print("❌  Файлів для конвертації не знайдено.")
        return
    results = convert_to_docx(files, output_dir=args.output,
                              skip_existing=args.skip_existing,
                              force=args.force, verbose=args.verbose)
    print_summary(results)
