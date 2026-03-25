#!/usr/bin/env python3
"""docx2pdf-cli — пакетний конвертер DOCX/DOC ↔ PDF"""

from docx2pdf_cli.cli import build_parser, run


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return

    run(args)


if __name__ == "__main__":
    main()
