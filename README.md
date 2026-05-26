# Hacker Game

A flashy movie-style operations console. It accepts Kali-like command input, prints realistic-looking terminal flows, plays music and voice cues, and runs terminal games. It does **not** execute real shell commands, does **not** connect to networks, and does **not** run real Kali tools.

The terminal UI intentionally omits a version number.

## Copy/paste Linux install commands

These commands download Hacker Game into `~/Desktop/MaxxBuilds/hacker-game`, install required dependencies, make the installer executable, and install or update the game for the current user. They use the GitHub source archive for the downloaded app folder.

### Linux Mint / Ubuntu / Debian

```bash
bash -lc 'set -e; sudo apt update; sudo apt install -y curl tar python3 python3-tk ffmpeg pulseaudio-utils alsa-utils; REPO=hacker-game; URL=https://github.com/MaxxBuilds/hacker-game/archive/refs/heads/main.tar.gz; BASE="$HOME/Desktop/MaxxBuilds"; DEST="$BASE/$REPO"; TMP="$(mktemp -d)"; mkdir -p "$BASE" "$DEST"; curl -L "$URL" -o "$TMP/app.tar.gz"; tar -xzf "$TMP/app.tar.gz" -C "$TMP"; SRC="$TMP/hacker-game-main"; rm -rf "$DEST/.git"; cp -a "$SRC"/. "$DEST"/; rm -rf "$DEST/.git" "$DEST/__pycache__"; chmod +x "$DEST/install.sh"; "$DEST/install.sh" --name "${USER:-Player}"; rm -rf "$TMP"'
```

### Fedora

```bash
bash -lc 'set -e; sudo dnf install -y curl tar python3 python3-tkinter ffmpeg-free pulseaudio-utils alsa-utils; REPO=hacker-game; URL=https://github.com/MaxxBuilds/hacker-game/archive/refs/heads/main.tar.gz; BASE="$HOME/Desktop/MaxxBuilds"; DEST="$BASE/$REPO"; TMP="$(mktemp -d)"; mkdir -p "$BASE" "$DEST"; curl -L "$URL" -o "$TMP/app.tar.gz"; tar -xzf "$TMP/app.tar.gz" -C "$TMP"; SRC="$TMP/hacker-game-main"; rm -rf "$DEST/.git"; cp -a "$SRC"/. "$DEST"/; rm -rf "$DEST/.git" "$DEST/__pycache__"; chmod +x "$DEST/install.sh"; "$DEST/install.sh" --name "${USER:-Player}"; rm -rf "$TMP"'
```

### Arch Linux / Manjaro

```bash
bash -lc 'set -e; sudo pacman -Sy --noconfirm curl tar python tk ffmpeg libpulse alsa-utils; REPO=hacker-game; URL=https://github.com/MaxxBuilds/hacker-game/archive/refs/heads/main.tar.gz; BASE="$HOME/Desktop/MaxxBuilds"; DEST="$BASE/$REPO"; TMP="$(mktemp -d)"; mkdir -p "$BASE" "$DEST"; curl -L "$URL" -o "$TMP/app.tar.gz"; tar -xzf "$TMP/app.tar.gz" -C "$TMP"; SRC="$TMP/hacker-game-main"; rm -rf "$DEST/.git"; cp -a "$SRC"/. "$DEST"/; rm -rf "$DEST/.git" "$DEST/__pycache__"; chmod +x "$DEST/install.sh"; "$DEST/install.sh" --name "${USER:-Player}"; rm -rf "$TMP"'
```

### openSUSE

```bash
bash -lc 'set -e; sudo zypper --non-interactive refresh; sudo zypper --non-interactive install curl tar python3 python3-tk ffmpeg pulseaudio-utils alsa-utils; REPO=hacker-game; URL=https://github.com/MaxxBuilds/hacker-game/archive/refs/heads/main.tar.gz; BASE="$HOME/Desktop/MaxxBuilds"; DEST="$BASE/$REPO"; TMP="$(mktemp -d)"; mkdir -p "$BASE" "$DEST"; curl -L "$URL" -o "$TMP/app.tar.gz"; tar -xzf "$TMP/app.tar.gz" -C "$TMP"; SRC="$TMP/hacker-game-main"; rm -rf "$DEST/.git"; cp -a "$SRC"/. "$DEST"/; rm -rf "$DEST/.git" "$DEST/__pycache__"; chmod +x "$DEST/install.sh"; "$DEST/install.sh" --name "${USER:-Player}"; rm -rf "$TMP"'
```

## Quick start

From this folder:

```bash
./install.sh --name "Alex" --theme matrix --mode cyber
hacker-game
```

Run without installing:

```bash
python3 ./hacker_terminal.py --windowed --no-music
```

## Safety notes

Everything happens inside the app. Typed text is interpreted by the Python/Tkinter program only.

User input is parsed inside the simulation rather than passed to:

- a shell
- real Kali tools
- network sockets
- wireless adapters
- password tools
- system commands

The only subprocesses during runtime are local audio playback through `ffplay`, `paplay`, or `aplay`. Closing the app terminates those audio subprocesses.

## Current features

- Modes: cyber, office, adult.
- Themes: blue, matrix, red, purple, amber.
- Mode-specific missions, vocabulary, colors, visual rain, signal map, animated background, crack sequences, and audio.
- Kali-style tool flows with purpose descriptions, per-tool help, output fields, error states, and guided scenarios.
- Real downloaded voice cues for tool starts, hits, mission accomplishments, and games.
- Downloaded free/open source music for each mode, stored in `assets/music`.
- Volume controls inside the terminal: `volume up`, `volume down`, or `volume 0-100`. The `-`, `+`, and `=` keys type normally.
- Games: cipher, firewall, breach, snake, adventure, and a current-mode special game.
- Boss mini-event: press X to defeat a trace.
- Command history with Up/Down arrows.
- Settings saved per user.
- Safer installer: package installation is off by default.

## Files in this folder

```text
hacker_terminal.py              Main Python/Tkinter app
install.sh                      Current-user installer/updater
uninstall.sh                    Full uninstaller wrapper
hacker-game-blue.png        Blue app icon
README.md                       This file
assets/music/                   Mode music and attribution notes
assets/voice/                   Voice cue assets
```

## Dependencies

Required:

- Python 3
- Python Tkinter

Optional for audio:

- `ffplay` from FFmpeg for best playback and volume support
- or `paplay` from PulseAudio/PipeWire Pulse tools
- or `aplay` from ALSA tools

Manual dependency commands:

```bash
# Fedora
sudo dnf install -y python3-tkinter ffmpeg-free pulseaudio-utils alsa-utils

# Ubuntu / Debian
sudo apt install -y python3-tk ffmpeg pulseaudio-utils alsa-utils

# Arch
sudo pacman -S tk ffmpeg libpulse alsa-utils

# openSUSE
sudo zypper install python3-tk ffmpeg pulseaudio-utils alsa-utils
```

## Install

From this folder:

```bash
./install.sh --name "Alex"
```

Install with a theme and mode:

```bash
./install.sh --name "Alex" --theme matrix --mode cyber
```

If you pass `--mode office` without `--theme`, the installer uses the green `matrix` theme.

Install in adult after-hours mode:

```bash
./install.sh --name "Alex" --theme red --mode adult
```

If dependencies are missing and you approve package changes:

```bash
./install.sh --install-deps --name "Alex"
```

## What gets installed

Current-user only:

```text
~/.local/bin/hacker-game
~/.local/share/hacker-game/hacker_terminal.py
~/.local/share/hacker-game/assets/music/*
~/.local/share/hacker-game/assets/voice/*
~/.local/share/icons/hacker-game-blue.png
~/.local/share/applications/hacker-game.desktop
~/.config/hacker-game/config.json
```

If a Desktop folder exists, it also creates:

```text
~/Desktop/Hacker Game.desktop
```

## Run

After install:

```bash
hacker-game
```

Run without installing:

```bash
python3 ./hacker_terminal.py --windowed --no-music
```

Run windowed:

```bash
hacker-game --windowed
```

Run without audio:

```bash
hacker-game --no-music
```

Run with one-time name/theme/mode:

```bash
hacker-game --name "Sam" --theme purple --mode cyber
```

## Exit

- Press `Escape`
- or press `Ctrl+Q`
- or type `quit`

## Learning-focused behavior

The app now explains what is happening instead of only printing output. Tool runs include:

- `PURPOSE` — what the tool is for
- `WHY` — why that step matters
- `REASONING` — what the operator should be thinking about
- `WATCH` — the important evidence field
- `PITFALL` — common mistake to avoid
- `DEFENSE` — how the finding maps to remediation

This keeps the terminal feeling realistic while making each flow easier to understand.

## Main commands

Unknown keyboard input returns a help hint. Type a listed command to continue.


```text
help
tools
kalihelp TOOL
scenario TOOL
scan
decrypt
trace
mission
crack
effects
boss
matrix
cipher
firewall
breach
snake
adventure
modegame
clear
theme blue|matrix|red|purple|amber
mode cyber|office|adult
sound on|off
volume up|down
volume 0-100
+ / -
fullscreen on|off
profile NAME
settings
quit
```

## Simulated tool commands

Use `tools` inside the app to list them. Use `kalihelp TOOL` for per-tool syntax. Use `scenario TOOL` for a guided workflow outline.

Included tool profiles:

```text
nmap
msfconsole
burpsuite
wireshark
tshark
sqlmap
hydra
john
hashcat
aircrack-ng
wifite
gobuster
dirb
nikto
searchsploit
enum4linux
smbclient
wpscan
```

Examples:

```text
scenario nmap
scenario burpsuite
nmap -sV -sC 192.0.2.10
gobuster dir -u http://192.0.2.10 -w common.txt
nikto -h http://demo.ops.local
sqlmap -u 'http://demo.ops.local/item?id=1' --batch
hydra -l admin -P rockyou.txt ssh://192.0.2.10
msfconsole
burpsuite
wireshark lab-http.pcap
tshark -r lab-http.pcap -Y http
wifite
aircrack-ng capture.cap -w wordlist.txt
```

Targets are handled inside the console. The app uses documentation/demo IP ranges and local generated output only.

## Interactive tool sessions

Tool commands now open a staged session instead of running every phase automatically. Password cracking stages run a random number of displayed attempts and then stop at success within a short runtime window. After launching a tool, follow the prompts and enter the next action.

Examples:

```text
wifite
scan
target 3
options
capture
crack
crack
show
finish

msfconsole
search
use 0
options
set RHOSTS 192.0.2.10
run
notes

burpsuite
proxy
repeater
intruder
report

wireshark lab-http.pcap
open
filter http
conversations
stream
report
```

Use `stop`, `back`, `quit`, or `exit` to leave a tool session.

## Tool scenarios

Use this command pattern inside the app:

```text
scenario nmap
scenario burpsuite
scenario wireshark
scenario sqlmap
scenario hydra
scenario john
scenario hashcat
scenario aircrack-ng
scenario wifite
```

Every tool run now starts with a purpose line and ends with evidence/defense notes.

## Games

```text
cipher     Decode shifted payloads.
firewall   Type the displayed firewall key exactly.
breach     Type node numbers to keep the route alive.
snake      Use w/a/s/d then Enter to steer.
adventure  Branching operation. Choose numbered actions.
modegame   Special challenge using the current mode vocabulary.
```

Stop a game with:

```text
stop
```

## Modes

- `cyber` — mainframe, proxy, vault, auth, and route operations.
- `office` — printer, VPN, badge, ticket, coffee, and spreadsheet operations. Office mode uses the green `matrix` theme by default.
- `adult` — after-hours lounge mode with raunchy innuendo.

## Audio sources

Music and voice files are stored in:

```text
assets/music/
assets/voice/
```

Attribution and license notes are in:

```text
assets/music/SOURCES.md
```

Current sources are free/open assets from OpenGameArt.

## Sharing / release notes

Private/casual sharing is ready from this folder. For a public release, handle these items first:

- Add a project code license file if you want others to modify or redistribute the Python/shell code. Without one, the code has no explicit open-source license.
- Keep `assets/music/SOURCES.md` with the package. The voice pack requires VoiceBosch attribution and is listed as CC-BY-SA 4.0.
- Adult mode contains innuendo. If sharing broadly, mention that clearly or remove/disable that mode for a clean package.
- The app uses documentation/demo target ranges such as `192.0.2.0/24`, `198.51.100.0/24`, and `203.0.113.0/24`. These are intentionally reserved example ranges.
- Do not remove the safety notes unless the implementation changes. The app is designed as a local game/learning console, not a real security tool.

Suggested package contents:

```text
Hacker Game/
  README.md
  install.sh
  uninstall.sh
  hacker_terminal.py
  hacker-game-blue.png
  assets/
```

Before sharing, run:

```bash
python3 -m py_compile hacker_terminal.py
bash -n install.sh
bash -n uninstall.sh
./install.sh --name "Test" --mode cyber
hacker-game --windowed --no-music
```

## Updating from GitHub

Run the same copy/paste install command again. It downloads the current GitHub source archive, refreshes `~/Desktop/MaxxBuilds/hacker-game`, and reinstalls the app files. Saved settings/data live in `~/.config/hacker-game`.

## Uninstall

From this folder:

```bash
./uninstall.sh
```

The uninstaller removes the installed app files, launchers, icons, bundled assets, and saved app settings/data in `~/.config/hacker-game`.

Equivalent command:

```bash
./install.sh --uninstall
```

This removes the current-user install, launcher, icon, desktop file, and saved config. The downloaded source folder remains separate.

## Troubleshooting

### App launch troubleshooting

```bash
python3 - <<'PY'
import tkinter
print('tkinter ok')
PY
```

If missing, install Python Tkinter for your distro.

### Sound keeps playing

Current builds terminate audio subprocesses on close. If a stale old process remains:

```bash
pkill -f 'hacker-game|audio-.*wav|voice-.*wav'
```

### Fullscreen is annoying

```bash
hacker-game --windowed
```

or inside the app:

```text
fullscreen off
```

### Reset settings

```bash
rm -rf ~/.config/hacker-game
```

Then rerun the installer.
