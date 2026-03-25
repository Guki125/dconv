#!/usr/bin/env bash
# ─────────────────────────────────────────────
#  dconv — one-shot installer (macOS & Linux)
# ─────────────────────────────────────────────
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

info()    { echo -e "${CYAN}[dconv]${RESET} $*"; }
success() { echo -e "${GREEN}[dconv] ✓${RESET} $*"; }
warn()    { echo -e "${YELLOW}[dconv] ⚠${RESET}  $*"; }
error()   { echo -e "${RED}[dconv] ✗${RESET} $*"; exit 1; }

echo -e "${BOLD}"
echo "  ╔══════════════════════════════╗"
echo "  ║     dconv installer          ║"
echo "  ║  DOCX/DOC ↔ PDF converter   ║"
echo "  ╚══════════════════════════════╝"
echo -e "${RESET}"

# ── Detect OS ────────────────────────────────
OS="$(uname -s)"
case "$OS" in
  Darwin) PLATFORM="macos" ;;
  Linux)  PLATFORM="linux" ;;
  *)      error "Unsupported OS: $OS" ;;
esac
info "Detected platform: $PLATFORM"

# ── Check Python 3.10+ ───────────────────────
PYTHON=""
for cmd in python3 python; do
  if command -v "$cmd" &>/dev/null; then
    VERSION=$("$cmd" -c 'import sys; print(sys.version_info >= (3,10))')
    if [ "$VERSION" = "True" ]; then
      PYTHON="$cmd"
      break
    fi
  fi
done

if [ -z "$PYTHON" ]; then
  error "Python 3.10+ is required but not found.\nInstall it from https://www.python.org/downloads/"
fi
success "Python found: $($PYTHON --version)"

# ── Check / Install LibreOffice ───────────────
install_libreoffice_macos() {
  if [ -x "/Applications/LibreOffice.app/Contents/MacOS/soffice" ]; then
    success "LibreOffice already installed"
    return
  fi
  info "Installing LibreOffice via Homebrew..."
  if ! command -v brew &>/dev/null; then
    error "Homebrew not found. Install it first:\n  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
  fi
  brew install --cask libreoffice
  success "LibreOffice installed"
}

install_libreoffice_linux() {
  if command -v libreoffice &>/dev/null || command -v soffice &>/dev/null; then
    success "LibreOffice already installed"
    return
  fi
  info "Installing LibreOffice..."
  if command -v apt-get &>/dev/null; then
    sudo apt-get update -q && sudo apt-get install -y libreoffice
  elif command -v dnf &>/dev/null; then
    sudo dnf install -y libreoffice
  elif command -v pacman &>/dev/null; then
    sudo pacman -Sy --noconfirm libreoffice-fresh
  else
    error "Cannot detect package manager. Install LibreOffice manually:\n  https://www.libreoffice.org/download/download/"
  fi
  success "LibreOffice installed"
}

if [ "$PLATFORM" = "macos" ]; then
  install_libreoffice_macos
else
  install_libreoffice_linux
fi

# ── Install dconv ─────────────────────────────
info "Installing dconv..."
$PYTHON -m pip install --upgrade pip -q
$PYTHON -m pip install -e . -q
success "dconv installed"

# ── Verify ────────────────────────────────────
echo ""
if command -v dconv &>/dev/null; then
  success "All done! Run:  dconv --help"
else
  warn "dconv not found in PATH. Try restarting your terminal or run:"
  echo "       $PYTHON -m docx2pdf_cli.main --help"
fi
