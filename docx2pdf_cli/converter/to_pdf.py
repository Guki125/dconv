"""DOCX / DOC → PDF конвертація"""

from pathlib import Path

try:
    from tqdm import tqdm
    _HAS_TQDM = True
except ImportError:
    _HAS_TQDM = False

from ..utils import make_output_path, should_skip, ok, err, info


def convert_to_pdf(
    files: list[Path],
    output_dir: str | None = None,
    skip_existing: bool = False,
    force: bool = False,
    verbose: bool = False,
) -> list[dict]:
    """
    Конвертує список DOCX/DOC файлів у PDF.
    Повертає список результатів {src, dest, ok, error}.
    """
    results = []
    iterator = tqdm(files, desc="Конвертація → PDF", unit="файл") if _HAS_TQDM else files

    for src in iterator:
        dest = make_output_path(src, output_dir, ".pdf")

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


# ── конвертація: тільки LibreOffice headless (без GUI) ───────────────────────

def _do_convert(src: Path, dest: Path) -> str | None:
    """Конвертація через LibreOffice --headless. Без Word, без GUI."""
    import subprocess, shutil

    # macOS: LibreOffice встановлений як .app
    lo = (
        shutil.which("libreoffice")
        or shutil.which("soffice")
        or "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    )

    if not lo or not Path(lo).exists():
        return (
            "Не знайдено LibreOffice. Встановіть через Homebrew:\n"
            "    brew install --cask libreoffice"
        )

    out_dir = dest.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        subprocess.run(
            [lo, "--headless", "--convert-to", "pdf",
             "--outdir", str(out_dir), str(src)],
            capture_output=True, text=True, timeout=120,
            check=True,
        )
        lo_dest = out_dir / (src.stem + ".pdf")
        if lo_dest.exists():
            if lo_dest != dest:
                lo_dest.rename(dest)
            return None
        return "LibreOffice не створив PDF"
    except subprocess.CalledProcessError as e:
        return e.stderr.strip() or "LibreOffice завершився з помилкою"
    except subprocess.TimeoutExpired:
        return "Таймаут LibreOffice (>120 с)"
    except Exception as e:
        return str(e)
