"""Утиліти: glob, кольори, summary"""

import glob as _glob
import sys
from pathlib import Path

# ── кольори ───────────────────────────────────────────────────────────────────

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    _HAS_COLOR = True
except ImportError:
    _HAS_COLOR = False

def _c(text: str, color: str) -> str:
    if not _HAS_COLOR:
        return text
    colors = {
        "green":  Fore.GREEN,
        "red":    Fore.RED,
        "yellow": Fore.YELLOW,
        "cyan":   Fore.CYAN,
        "bold":   Style.BRIGHT,
        "reset":  Style.RESET_ALL,
    }
    return f"{colors.get(color, '')}{text}{Style.RESET_ALL}"

def ok(msg: str)   -> str: return _c(f"✅  {msg}", "green")
def err(msg: str)  -> str: return _c(f"❌  {msg}", "red")
def warn(msg: str) -> str: return _c(f"⚠️   {msg}", "yellow")
def info(msg: str) -> str: return _c(f"ℹ️   {msg}", "cyan")


# ── glob resolver ─────────────────────────────────────────────────────────────

def resolve_files(patterns: list[str], exts: list[str]) -> list[Path]:
    """
    Розгортає glob-патерни та фільтрує за розширеннями.
    Повертає унікальний впорядкований список Path.
    """
    found: list[Path] = []
    exts_lower = [e.lower() for e in exts]

    for pattern in patterns:
        # спочатку пробуємо як glob
        matches = _glob.glob(pattern, recursive=True)
        if matches:
            for m in matches:
                p = Path(m)
                if p.is_file() and p.suffix.lower() in exts_lower:
                    found.append(p)
        else:
            # може бути конкретний файл
            p = Path(pattern)
            if p.is_file() and p.suffix.lower() in exts_lower:
                found.append(p)
            elif p.is_file():
                print(warn(f"Пропущено (невірне розширення): {p}"))
            else:
                print(warn(f"Файл не знайдено: {pattern}"))

    # дедуплікація зі збереженням порядку
    seen: set[Path] = set()
    unique: list[Path] = []
    for p in found:
        resolved = p.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(p)

    return unique


# ── output path ───────────────────────────────────────────────────────────────

def make_output_path(src: Path, output_dir: str | None, new_suffix: str) -> Path:
    """Будує шлях до вихідного файлу."""
    stem = src.stem
    filename = stem + new_suffix
    if output_dir:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        return out_dir / filename
    return src.parent / filename


# ── conflict resolution ───────────────────────────────────────────────────────

def should_skip(dest: Path, skip_existing: bool, force: bool, verbose: bool) -> bool:
    """Повертає True якщо файл треба пропустити."""
    if not dest.exists():
        return False
    if skip_existing:
        if verbose:
            print(warn(f"Пропущено (вже існує): {dest}"))
        return True
    if force:
        return False
    # інтерактивний запит
    try:
        answer = input(_c(f"  Файл вже існує: {dest}. Перезаписати? [y/N] ", "yellow")).strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)
    return answer not in ("y", "yes", "т", "так")


# ── summary ───────────────────────────────────────────────────────────────────

def print_summary(results: list[dict]):
    """Виводить підсумок після конвертації."""
    success = [r for r in results if r["ok"]]
    failed  = [r for r in results if not r["ok"]]

    print()
    print(_c("─" * 48, "bold"))
    print(_c("📊  Результат:", "bold"))
    print(f"  {ok(f'Успішно:  {len(success)}/{len(results)}')}  ")
    if failed:
        print(f"  {err(f'Помилки:  {len(failed)}/{len(results)}')}")
        for r in failed:
            print(f"    • {r['src']}  →  {r['error']}")
    print(_c("─" * 48, "bold"))
