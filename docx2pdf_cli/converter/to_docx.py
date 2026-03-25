"""PDF → DOCX конвертація"""

from pathlib import Path

try:
    from tqdm import tqdm
    _HAS_TQDM = True
except ImportError:
    _HAS_TQDM = False

from ..utils import make_output_path, should_skip, ok, err, info


def convert_to_docx(
    files: list[Path],
    output_dir: str | None = None,
    skip_existing: bool = False,
    force: bool = False,
    verbose: bool = False,
) -> list[dict]:
    """
    Конвертує список PDF файлів у DOCX.
    Повертає список результатів {src, dest, ok, error}.
    """
    results = []
    iterator = tqdm(files, desc="Конвертація → DOCX", unit="файл") if _HAS_TQDM else files

    for src in iterator:
        dest = make_output_path(src, output_dir, ".docx")

        if should_skip(dest, skip_existing, force, verbose):
            results.append({"src": src, "dest": dest, "ok": True, "error": None})
            continue

        if verbose:
            print(info(f"{src}  →  {dest}"))

        error = _do_convert(src, dest)

        if error:
            print(err(f"{src.name}: {error}"))
            results.append({"src": src, "dest": dest, "ok": False, "error": error})
        else:
            if verbose:
                print(ok(f"Готово: {dest}"))
            results.append({"src": src, "dest": dest, "ok": True, "error": None})

    return results


# ── конвертація: pdf2docx ─────────────────────────────────────────────────────

def _do_convert(src: Path, dest: Path) -> str | None:
    """
    Повертає None при успіху або рядок з помилкою.
    Використовує бібліотеку pdf2docx.
    """
    try:
        from pdf2docx import Converter
    except ImportError:
        return (
            "Бібліотека pdf2docx не встановлена. "
            "Виконайте: pip install pdf2docx"
        )

    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        cv = Converter(str(src))
        cv.convert(str(dest), start=0, end=None)
        cv.close()
        if dest.exists():
            return None
        return "pdf2docx не створив файл"
    except Exception as e:
        return str(e)
