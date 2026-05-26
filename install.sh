#!/usr/bin/env bash
set -euo pipefail

DISPLAY_NAME="${USER:-Agent}"
THEME=""
MODE="cyber"
INSTALL_DEPS=0
CREATE_DESKTOP=1

usage() {
  cat <<'EOF'
Hacker Game installer

Usage:
  ./install.sh --name "Alex"
  ./install.sh --name "Alex" --theme matrix --mode cyber
  ./install.sh --install-deps
  ./install.sh --uninstall

Options:
  --name NAME       Name shown inside the terminal.
  --theme NAME      blue, matrix, red, purple, amber. Defaults to the selected mode color.
  --mode NAME       cyber, office, adult.
  --no-desktop      Do not create a desktop shortcut.
  --install-deps    Try to install missing Linux packages. Off by default.
  --uninstall       Remove the app from this user account.
  -h, --help        Show this help.

By default this installer does not install packages. If Tkinter is missing,
install it manually or rerun with --install-deps.
EOF
}

UNINSTALL=0
while [ $# -gt 0 ]; do
  case "$1" in
    --name)
      shift
      [ $# -gt 0 ] || { echo "Missing value for --name" >&2; exit 1; }
      DISPLAY_NAME="$1"
      ;;
    --theme)
      shift
      [ $# -gt 0 ] || { echo "Missing value for --theme" >&2; exit 1; }
      THEME="$1"
      ;;
    --mode)
      shift
      [ $# -gt 0 ] || { echo "Missing value for --mode" >&2; exit 1; }
      MODE="$1"
      ;;
    --no-desktop)
      CREATE_DESKTOP=0
      ;;
    --install-deps)
      INSTALL_DEPS=1
      ;;
    --uninstall)
      UNINSTALL=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
  shift
done

case "$MODE" in cyber|office|adult) ;; *) echo "Unknown mode: $MODE" >&2; exit 1 ;; esac
if [ -z "$THEME" ]; then
  case "$MODE" in
    cyber) THEME="blue" ;;
    office) THEME="matrix" ;;
    adult) THEME="red" ;;
  esac
fi
case "$THEME" in blue|matrix|red|purple|amber) ;; *) echo "Unknown theme: $THEME" >&2; exit 1 ;; esac

SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
APPDIR="$HOME/.local/share/hacker-game"
BINDIR="$HOME/.local/bin"
ICONDIR="$HOME/.local/share/icons"
APPDESKTOPDIR="$HOME/.local/share/applications"
CONFIGDIR="$HOME/.config/hacker-game"
DESKTOP_FILE="$APPDESKTOPDIR/hacker-game.desktop"
ICON_FILE="$ICONDIR/hacker-game-blue.png"
BIN_FILE="$BINDIR/hacker-game"
APP_FILE="$APPDIR/hacker_terminal.py"
ASSET_SRC="$SRC_DIR/assets"
ASSET_DEST="$APPDIR/assets"
CONFIG_FILE="$CONFIGDIR/config.json"

find_desktop_dir() {
  if command -v xdg-user-dir >/dev/null 2>&1; then
    xdg-user-dir DESKTOP 2>/dev/null || true
  else
    printf '%s\n' "$HOME/Desktop"
  fi
}

if [ "$UNINSTALL" -eq 1 ]; then
  rm -rf "$APPDIR" "$CONFIGDIR"
  rm -f "$BIN_FILE" "$DESKTOP_FILE" "$ICON_FILE" "$ICONDIR/hacker-game.svg"
  OLD_ID="hacker-""terminal-game"
  OLD_DESKTOP_NAME="Hacker ""Terminal ""Game.desktop"
  rm -rf "$HOME/.local/share/$OLD_ID" "$HOME/.config/$OLD_ID"
  rm -f "$HOME/.local/bin/$OLD_ID" "$APPDESKTOPDIR/$OLD_ID.desktop" "$ICONDIR/$OLD_ID.svg" "$ICONDIR/$OLD_ID.png" "$ICONDIR/hacker-game.svg"
  DDIR="$(find_desktop_dir)"
  if [ -n "$DDIR" ]; then
    rm -f "$DDIR/Hacker Game.desktop" "$DDIR/$OLD_DESKTOP_NAME" 2>/dev/null || true
  fi
  echo "Removed Hacker Game for user: ${USER:-unknown}"
  exit 0
fi

check_tkinter() {
  python3 - <<'PY' >/dev/null 2>&1
import tkinter
PY
}

install_deps() {
  if [ "$INSTALL_DEPS" -ne 1 ]; then
    return 0
  fi
  echo "Installing dependencies if missing..."
  if command -v dnf >/dev/null 2>&1; then
    sudo dnf install -y python3-tkinter ffmpeg-free pulseaudio-utils alsa-utils || true
  elif command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update || true
    sudo apt-get install -y python3-tk ffmpeg pulseaudio-utils alsa-utils || true
  elif command -v pacman >/dev/null 2>&1; then
    sudo pacman -Sy --noconfirm tk ffmpeg libpulse alsa-utils || true
  elif command -v zypper >/dev/null 2>&1; then
    sudo zypper --non-interactive install python3-tk ffmpeg pulseaudio-utils alsa-utils || true
  elif command -v apk >/dev/null 2>&1; then
    sudo apk add python3 py3-tkinter ffmpeg alsa-utils pulseaudio-utils || true
  else
    echo "No supported package manager found. Install Python Tkinter manually."
  fi
}

install_deps

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required but was not found." >&2
  exit 1
fi

if ! check_tkinter; then
  cat >&2 <<'EOF'
Python Tkinter is missing.
Install it, then rerun this installer:
  Fedora:        sudo dnf install -y python3-tkinter
  Ubuntu/Debian: sudo apt install -y python3-tk
  Arch:          sudo pacman -S tk
  openSUSE:      sudo zypper install python3-tk

Or rerun this installer with --install-deps if you approve package changes.
EOF
  exit 1
fi

mkdir -p "$APPDIR" "$BINDIR" "$ICONDIR" "$APPDESKTOPDIR" "$CONFIGDIR"
OLD_ID="hacker-""terminal-game"
OLD_DESKTOP_NAME="Hacker ""Terminal ""Game.desktop"
rm -f "$HOME/.local/bin/$OLD_ID" "$APPDESKTOPDIR/$OLD_ID.desktop" "$ICONDIR/$OLD_ID.svg" "$ICONDIR/$OLD_ID.png" "$ICONDIR/hacker-game.svg"
DDIR="$(find_desktop_dir)"
[ -n "$DDIR" ] && rm -f "$DDIR/$OLD_DESKTOP_NAME" 2>/dev/null || true
cp -f "$SRC_DIR/hacker_terminal.py" "$APP_FILE"
if [ -d "$ASSET_SRC" ]; then
  rm -rf "$ASSET_DEST"
  mkdir -p "$ASSET_DEST"
  cp -R "$ASSET_SRC/." "$ASSET_DEST/"
fi
cp -f "$SRC_DIR/hacker-game-blue.png" "$ICON_FILE"
chmod 755 "$APP_FILE"
chmod 644 "$ICON_FILE"

cat > "$BIN_FILE" <<EOF
#!/usr/bin/env sh
exec /usr/bin/env python3 "$APP_FILE" "\$@"
EOF
chmod 755 "$BIN_FILE"

python3 - <<PY
import json
from pathlib import Path
path = Path("$CONFIG_FILE")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps({
    "name": "$DISPLAY_NAME",
    "theme": "$THEME",
    "mode": "$MODE",
    "music": True,
    "fullscreen": True,
    "volume": 75,
}, indent=2) + "\n")
PY

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=Hacker Game
Exec=$BIN_FILE
Icon=$ICON_FILE
Terminal=false
Categories=Game;
StartupNotify=false
EOF
chmod 755 "$DESKTOP_FILE"

if [ "$CREATE_DESKTOP" -eq 1 ]; then
  DDIR="$(find_desktop_dir)"
  if [ -n "$DDIR" ]; then
    mkdir -p "$DDIR"
    cp -f "$DESKTOP_FILE" "$DDIR/Hacker Game.desktop"
    chmod 755 "$DDIR/Hacker Game.desktop"
  fi
fi

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$APPDESKTOPDIR" >/dev/null 2>&1 || true
fi

echo "Installed Hacker Game for user: ${USER:-unknown}"
echo "Display name: $DISPLAY_NAME"
echo "Theme: $THEME"
echo "Mode: $MODE"
echo "Run it with: hacker-game"
