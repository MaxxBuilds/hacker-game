# Hacker Game Dependencies

Hacker Game is a local Python/Tkinter desktop game with simulated terminal/security-tool output.

## Required

- Linux desktop session
- Python 3
- Python Tkinter

## Optional audio helpers

The app uses the first available audio helper:

1. `ffplay` from FFmpeg / Fedora `ffmpeg-free` — best option; supports volume control well
2. `paplay` from PulseAudio/PipeWire Pulse tools
3. `aplay` from ALSA tools

If none are installed, the game still runs without audio.

## Manual install commands

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

## Installer behavior

Package installation is available through the explicit `install.sh --install-deps` option.

To let it try installing dependencies, run:

```bash
./install.sh --install-deps
```

That may use bandwidth and system package manager changes, so it should only be used with approval from the computer owner.

## Runtime safety

Normal play uses in-game simulated commands and fake tool output. Local settings are saved in:

```text
~/.config/hacker-game/config.json
```
