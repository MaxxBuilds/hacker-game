# Hacker Game Package Manifest

This folder is intended to be a complete shareable package for Hacker Game.

## Top-level files

```text
README.md               Full usage, safety, install, run, sharing, and troubleshooting guide
DEPENDENCIES.md         Dependency and package-manager notes
MANIFEST.md             This package inventory
install.sh              Current-user installer/updater/uninstaller
uninstall.sh            Uninstaller wrapper
hacker_terminal.py      Main Python/Tkinter game
hacker-game-blue.png    Desktop/app icon
assets/                 Music, voice, and attribution assets
```

## Asset files

```text
assets/music/SOURCES.md
assets/music/adult-insistent.ogg
assets/music/cyber-pynchon.mp3
assets/music/office-upbeat.ogg
assets/voice/voice-action.wav
assets/voice/voice-counter.wav
assets/voice/voice-mission.wav
assets/voice/voice-objective.wav
assets/voice/voice-optimal.wav
assets/voice/voice-stealth.wav
```

## Installed paths

The installer writes only into the current user account:

```text
~/.local/bin/hacker-game
~/.local/share/hacker-game/hacker_terminal.py
~/.local/share/hacker-game/assets/
~/.local/share/icons/hacker-game-blue.png
~/.local/share/applications/hacker-game.desktop
~/.config/hacker-game/config.json
~/Desktop/Hacker Game.desktop        if a Desktop folder exists and --no-desktop is not used
```

The installer may also remove exact legacy files from an earlier app id, `hacker-terminal-game`, during install/uninstall cleanup.

## Uninstall

```bash
./uninstall.sh
```

or:

```bash
./install.sh --uninstall
```

Uninstall removes installed app files, launchers, icons, bundled assets, and saved app settings/data in `~/.config/hacker-game`.

## Pre-share checks

Run these from this folder before sharing:

```bash
python3 -m py_compile hacker_terminal.py
bash -n install.sh
bash -n uninstall.sh
./install.sh --name "Test" --mode cyber --no-desktop
hacker-game --windowed --no-music
```

## Safety summary

Hacker Game is a simulation with in-game command parsing and fake tool output. Settings are saved in `~/.config/hacker-game/config.json`.
