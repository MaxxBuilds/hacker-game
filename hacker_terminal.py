#!/usr/bin/env python3
import argparse
import json
import math
import os
import random
import shlex
import shutil
import struct
import subprocess
import threading
import time
import wave
from pathlib import Path
import tkinter as tk
from tkinter import font

APP_NAME = "Hacker Game"
CONFIG_DIR = Path.home() / ".config" / "hacker-game"
CONFIG_FILE = CONFIG_DIR / "config.json"
DATA_DIR = Path.home() / ".local" / "share" / "hacker-game"
SOURCE_ASSET_DIR = Path(__file__).resolve().parent / "assets"
MUSIC_FILES = {"cyber": "cyber-pynchon.mp3", "office": "office-upbeat.ogg", "adult": "adult-insistent.ogg"}
VOICE_FILES = {"tool": "voice-action.wav", "game": "voice-action.wav", "hit": "voice-objective.wav", "success": "voice-mission.wav", "counter": "voice-counter.wav", "stealth": "voice-stealth.wav", "optimal": "voice-optimal.wav"}

THEMES = {
    "blue": {"bg": "#071019", "panel": "#0d1620", "text_bg": "#09131d", "fg": "#5ecbff", "dim": "#1d4b66", "accent": "#9ee7ff", "danger": "#ff5e7a"},
    "matrix": {"bg": "#020b04", "panel": "#061407", "text_bg": "#021006", "fg": "#33ff77", "dim": "#0d6b32", "accent": "#b8ffd0", "danger": "#ff4d4d"},
    "red": {"bg": "#120406", "panel": "#21070b", "text_bg": "#160609", "fg": "#ff4d6d", "dim": "#7a1b2e", "accent": "#ffd1dc", "danger": "#ffcc00"},
    "purple": {"bg": "#0d0618", "panel": "#170b2e", "text_bg": "#100820", "fg": "#c084fc", "dim": "#5b2a86", "accent": "#f0d9ff", "danger": "#ff6bcb"},
    "amber": {"bg": "#140d02", "panel": "#221605", "text_bg": "#1a1103", "fg": "#ffbf47", "dim": "#735016", "accent": "#ffe2a3", "danger": "#ff6b35"},
}

MODES = {
    "cyber": {
        "label": "CYBER OPS",
        "tag": "BLACKGRID",
        "theme": "blue",
        "status": ["STEALTH CHANNEL: STABLE", "QUANTUM ROUTER: LOCKED", "FIREWALL PRESSURE: RISING", "DARKNET HANDSHAKE: LIVE", "KEYSPACE MAP: ACTIVE"],
        "missions": ["financial mainframe", "offshore vault", "satellite proxy", "zero-trust gateway", "cold-storage node"],
        "verbs": ["spoofing handshake", "rotating identity", "hashing token", "injecting decoy", "mirroring packet stream", "pivoting route"],
        "crack": ["enumerating auth surface", "capturing salted hash", "building mask attack", "testing hybrid wordlist", "checking MFA drift", "replaying Kerberos ticket", "validating session cookie"],
        "keys": ["SYN", "ACK", "RSA", "SHA", "JWT", "AES", "OTP", "VPN"],
        "extras": ["Root tunnel stabilized", "Session ghosted", "Vault index mounted", "Audit trail displaced", "Operator clearance elevated"],
        "sound": {"base": 74, "lead": 148, "pulse": 0.23, "noise": 0.03, "tempo": 9},
    },
    "office": {
        "label": "CORP IT",
        "tag": "HELPDESK HELL",
        "theme": "matrix",
        "status": ["COFFEE SERVER: ONLINE", "PRINTER QUEUE: ANGRY", "SPREADSHEET SHIELD: UP", "MEETING DETECTOR: ACTIVE", "VPN HAMSTER: SWEATING"],
        "missions": ["coffee server", "printer queue", "spreadsheet vault", "conference-room tablet", "smart-fridge admin panel"],
        "verbs": ["rebooting printer", "dodging meeting invite", "patching spreadsheet", "caffeinating server", "flushing ticket queue", "rerouting office gossip"],
        "crack": ["enumerating sticky-note passwords", "bypassing printer rage-lock", "decrypting spreadsheet macro", "replaying badge reader token", "guessing conference PIN", "bribing coffee daemon", "closing ticket without comment"],
        "keys": ["COFFEE", "PRINTER", "BADGE", "MACRO", "VPN", "TICKET", "FRIDGE", "MEETING"],
        "extras": ["Printer tantrum contained", "Coffee daemon promoted", "Spreadsheet vault opened", "Meeting invite neutralized", "Ticket queue suppressed"],
        "sound": {"base": 70, "lead": 176, "pulse": 0.19, "noise": 0.05, "tempo": 6},
    },
    "adult": {
        "label": "AFTER HOURS",
        "tag": "BAD IDEAS LAB",
        "theme": "red",
        "status": ["BAD DECISIONS: ONLINE", "HR FILTER: DISABLED", "BOOTY CACHE: INDEXED", "MARTINI PROTOCOL: ARMED", "COUGAR RADAR: ACTIVE"],
        "missions": ["VIP lounge", "black-card vault", "booty cache", "walk-of-shame relay", "thirst-trap firewall", "hotel minibar node"],
        "verbs": ["pouring martini packet", "masking regret logs", "arming booty cache", "spoofing room key", "dodging HR scanner", "routing through velvet rope"],
        "crack": ["indexing booty cache", "bypassing velvet-rope auth", "decrypting black-card hash", "spoofing room-service token", "quarantining regret logs", "testing walk-of-shame relay", "arming champagne payload"],
        "keys": ["VIP", "BOOTY", "MARTINI", "VELVET", "COUGAR", "MINIBAR", "REGRET", "LOUNGE"],
        "extras": ["Black-card handshake approved", "Regret logs quarantined", "Minibar node drained", "Champagne payload staged", "Velvet-rope firewall bypassed"],
        "sound": {"base": 49, "lead": 196, "pulse": 0.16, "noise": 0.02, "tempo": 8},
    },
}

HELP = [
    "COMMANDS",
    "  help              show this help",
    "  tools             list tool profiles",
    "  kalihelp TOOL     show syntax for one tool",
    "  scenario TOOL     guided workflow for one tool",
    "",
    "OPERATIONS",
    "  scan              mode-specific scan",
    "  decrypt           decrypt current target",
    "  trace             trace countermeasure",
    "  mission           full mission chain",
    "  crack             credential/keyspace sequence",
    "  effects           visual surge",
    "  boss              keyboard boss battle",
    "  matrix            data-rain burst",
    "",
    "TOOLS",
    "  nmap TARGET       reconnaissance scan",
    "  wifite            wireless workflow",
    "  gobuster ...      content discovery",
    "  nikto ...         web assessment",
    "  sqlmap ...        injection workflow",
    "  hydra ...         credential audit",
    "  msfconsole        framework console flow",
    "  burpsuite         web proxy workspace",
    "  wireshark         packet analyzer",
    "  tshark            packet CLI analyzer",
    "",
    "GAMES",
    "  cipher            cipher challenge",
    "  firewall          firewall reflex",
    "  breach            breach-route",
    "  snake             terminal snake",
    "  adventure         branching operation",
    "  modegame          current-mode special",
    "",
    "SETTINGS",
    "  volume up/down    adjust volume",
    "  volume 0-100      set volume",
    "  sound on/off      toggle audio",
    "  fullscreen on/off toggle fullscreen",
    "  theme NAME        blue, matrix, red, purple, amber",
    "  mode NAME         cyber, office, adult",
    "  profile NAME      change agent name",
    "  settings          show current settings",
    "  clear             clear terminal",
    "  quit              close app",
    "",
]
CRACK_WORDS = ["dragon", "ninja123", "pizza9000", "moonlaser", "candycannon", "t_rex_king", "ultra_bonk", "coffee_admin", "parrot_gold", "orbital_zero", "velvet_admin"]


SIM_TARGETS = ["192.0.2.10", "192.0.2.25", "198.51.100.42", "203.0.113.77", "demo.ops.local", "vault.example.test"]
SIM_TOOLS = {
    "nmap": {
        "title": "Nmap reconnaissance",
        "syntax": [
            "nmap 192.0.2.10",
            "nmap -sV -sC 192.0.2.10",
            "nmap -A -p- 192.0.2.25",
            "nmap --script vuln 198.51.100.42",
        ],
        "notes": ["Parses scan flags, builds a host profile, and prints service/version output."],
    },
    "gobuster": {
        "title": "Gobuster content discovery",
        "syntax": [
            "gobuster dir -u http://192.0.2.10 -w common.txt",
            "gobuster dir -u http://demo.ops.local -x php,txt,bak",
        ],
        "notes": ["Runs wordlist discovery, status codes, sizes, redirects, and interesting paths."],
    },
    "dirb": {
        "title": "DIRB content discovery",
        "syntax": ["dirb http://192.0.2.10", "dirb http://demo.ops.local common.txt"],
        "notes": ["Runs classic web directory brute-force output."],
    },
    "nikto": {
        "title": "Nikto web assessment",
        "syntax": ["nikto -h http://192.0.2.10", "nikto -h https://demo.ops.local -Tuning x"],
        "notes": ["Checks server headers, outdated components, risky files, and findings."],
    },
    "sqlmap": {
        "title": "sqlmap injection workflow",
        "syntax": [
            "sqlmap -u 'http://demo.ops.local/item?id=1' --batch",
            "sqlmap -u 'http://192.0.2.10/login.php?id=2' --dbs",
        ],
        "notes": ["Runs parameter testing, DBMS fingerprinting, database listing, and dump-style flow."],
    },
    "hydra": {
        "title": "Hydra credential audit",
        "syntax": [
            "hydra -l admin -P rockyou.txt ssh://192.0.2.10",
            "hydra -L users.txt -P passwords.txt 192.0.2.25 http-post-form '/login:username=^USER^&password=^PASS^:Invalid'",
        ],
        "notes": ["Shows rate limits, failed attempts, lockout warnings, and credential results."],
    },
    "john": {
        "title": "John hash audit",
        "syntax": ["john hashes.txt --wordlist=rockyou.txt", "john --show hashes.txt"],
        "notes": ["Shows hash loading, format detection, cracking progress, and show output."],
    },
    "hashcat": {
        "title": "Hashcat keyspace audit",
        "syntax": ["hashcat -m 0 hashes.txt rockyou.txt", "hashcat -m 1000 ntlm.txt wordlist.txt --status"],
        "notes": ["Shows device status, speed, recovered count, and candidate progress."],
    },
    "msfconsole": {
        "title": "Framework console flow",
        "syntax": ["msfconsole", "msfconsole -q", "msfconsole exploit/multi/http/demo_module"],
        "notes": ["Runs search/use/options/check/run/session handling in one console sequence."],
    },
    "searchsploit": {
        "title": "Exploit database search",
        "syntax": ["searchsploit apache 2.4", "searchsploit openssh 7.2"],
        "notes": ["Searches the local exploit index and prints matching entries."],
    },
    "enum4linux": {
        "title": "SMB enumeration",
        "syntax": ["enum4linux -a 192.0.2.25"],
        "notes": ["Enumerates SMB shares, users, password policy, and OS banner."],
    },
    "smbclient": {
        "title": "SMB client",
        "syntax": ["smbclient -L //192.0.2.25 -N", "smbclient //192.0.2.25/backups -N"],
        "notes": ["Lists shares and performs read-only directory browsing."],
    },
    "wpscan": {
        "title": "WordPress assessment",
        "syntax": ["wpscan --url http://demo.ops.local", "wpscan --url http://192.0.2.10 --enumerate u,p"],
        "notes": ["Enumerates plugins, themes, users, and finding summaries."],
    },
    "wifite": {
        "title": "Wireless audit workflow",
        "syntax": ["wifite", "wifite --wps", "wifite --kill --dict wordlist.txt"],
        "notes": ["Runs interface discovery, AP selection, handshake capture, PMKID/WPS-style progress, and offline key recovery."],
    },
    "burpsuite": {
        "title": "Burp Suite web proxy workspace",
        "syntax": ["burpsuite", "burpsuite --use-defaults", "burp proxy", "burp repeater", "burp intruder"],
        "notes": ["Opens a web proxy workspace with Target, Proxy, Repeater, Intruder, Decoder, Comparer, Logger, and findings views."],
    },
    "wireshark": {
        "title": "Wireshark packet analyzer",
        "syntax": ["wireshark lab-http.pcap", "wireshark dns-lab.pcap", "wireshark --display-filter dns"],
        "notes": ["Loads packet captures, shows packet list/detail/bytes panes, conversations, protocol hierarchy, and stream follow output."],
    },
    "tshark": {
        "title": "TShark packet analyzer",
        "syntax": ["tshark -r lab-http.pcap -Y http", "tshark -r dns-lab.pcap -T fields -e ip.src -e dns.qry.name"],
        "notes": ["Reads capture files and prints display-filtered packet summaries or field output."],
    },
    "aircrack-ng": {
        "title": "Wireless audit replay",
        "syntax": ["aircrack-ng capture.cap -w wordlist.txt"],
        "notes": ["Runs offline capture analysis and reports handshake/key status."],
    },
}

TOOL_SCENARIOS = {
    "nmap": ["Confirm scope", "Select target 192.0.2.10", "Run discovery", "Run -sV -sC", "Review open/closed/filtered states", "Export service table", "Recommend closing unused services"],
    "msfconsole": ["Open console", "search scanner/http", "info module", "use auxiliary/scanner/http/title", "show options", "set RHOSTS 192.0.2.10", "run", "review notes/services"],
    "burpsuite": ["Start project", "Set browser proxy", "Capture login request", "Send to Repeater", "Change parameter", "Compare response", "Mark finding", "Export note"],
    "wireshark": ["Open lab capture", "Apply display filter", "Inspect TCP handshake", "Follow stream", "Open conversations", "Review protocol hierarchy", "Write packet summary"],
    "tshark": ["Read capture with -r", "Apply -Y display filter", "Print -T fields", "Extract endpoints", "Summarize protocol counts"],
    "sqlmap": ["Load target request", "Select id parameter", "Run detection", "Identify technique", "Fingerprint DBMS", "List synthetic databases", "Write remediation"],
    "hydra": ["Select service", "Set username source", "Set password source", "Limit attempts", "Observe lockout/rate-limit", "Record valid result", "Recommend MFA/rate limits"],
    "john": ["Load toy hashes", "Detect format", "Choose wordlist/rules", "Watch progress", "Show recovered", "Classify weak passwords", "Recommend password manager"],
    "hashcat": ["Choose hash mode", "Choose attack mode", "Load candidates", "Monitor speed/progress", "Show recovered/left", "Review candidate pattern", "Recommend slow salted hashing"],
    "aircrack-ng": ["Select prerecorded capture", "Inspect AP table", "Confirm handshake", "Run offline analysis", "Compare weak/strong passphrases", "Recommend WPA3/WPS off"],
    "wifite": ["Select wireless interface", "Scan AP table", "Apply filters", "Select target", "Capture artifact", "Run offline check", "Review cracked/ignored DB", "Recommend wireless controls"],
}


TOOL_DETAILS = {
    "nmap": {
        "purpose": "Discovers hosts, ports, service versions, script findings, and OS fingerprints.",
        "menu": ["Target specification", "Host discovery", "Scan techniques", "Port selection", "Service/version detection", "Script engine", "OS detection", "Timing", "Output formats"],
        "fields": ["Host", "Port", "Protocol", "State", "Reason", "Service", "Version", "Confidence"],
        "errors": ["invalid target format", "host appears down", "DNS resolution failure", "scan profile too broad", "permission warning"],
        "defense": "Close unused services, patch exposed software, restrict administrative ports, monitor unexpected listeners.",
    },
    "msfconsole": {
        "purpose": "Provides a modular console for finding modules, setting options, running scanners/checkers, and recording findings.",
        "menu": ["help", "search", "info", "use", "show options", "set/setg", "check", "run", "hosts", "services", "notes", "creds", "sessions"],
        "fields": ["Module", "Type", "Rank", "Required options", "Target", "Result", "References", "Remediation"],
        "errors": ["required option missing", "module incompatible", "target timeout", "session expired"],
        "defense": "Validate exposure with safe checks first, document evidence, and remediate the underlying vulnerable service.",
    },
    "burpsuite": {
        "purpose": "Acts as a web testing proxy to inspect, edit, replay, compare, and document HTTP traffic.",
        "menu": ["Dashboard", "Target site map", "Proxy intercept", "HTTP history", "Repeater", "Intruder", "Decoder", "Comparer", "Logger"],
        "fields": ["Method", "URL", "Status", "Length", "MIME", "Parameters", "Cookies", "Headers", "Response time"],
        "errors": ["browser not proxied", "target out of scope", "intercept left on", "malformed body", "rate limit reached"],
        "defense": "Fix authorization, validation, cookie flags, error handling, and server-side request controls.",
    },
    "wireshark": {
        "purpose": "Analyzes packet captures with packet list, detail tree, bytes pane, filters, streams, endpoints, and statistics.",
        "menu": ["Open capture", "Display filter", "Packet details", "Follow stream", "Conversations", "Endpoints", "Protocol hierarchy", "Expert info"],
        "fields": ["No.", "Time", "Source", "Destination", "Protocol", "Length", "Info"],
        "errors": ["invalid filter", "no packets match", "truncated capture", "unsupported link layer", "encrypted payload"],
        "defense": "Use captures to support conclusions, identify exposed protocols, and avoid overclaiming encrypted traffic.",
    },
    "tshark": {
        "purpose": "Provides Wireshark-style capture analysis from a terminal using read files, filters, fields, and verbose packet output.",
        "menu": ["-r capture", "-Y display filter", "-f capture filter", "-T fields", "-e field", "-V verbose", "-z statistics"],
        "fields": ["Frame", "Time", "ip.src", "ip.dst", "protocol", "field values", "summary"],
        "errors": ["bad display filter", "missing capture", "field not found", "no matching packets"],
        "defense": "Automate repeatable packet review and extract evidence fields for reports.",
    },
    "sqlmap": {
        "purpose": "Tests request parameters for SQL injection behavior and fingerprints the backend DBMS.",
        "menu": ["Target", "Request", "Detection", "Techniques", "Enumeration", "Output/session", "Batch mode"],
        "fields": ["Target URL", "Parameter", "Technique", "DBMS", "Confidence", "Evidence", "Risk"],
        "errors": ["parameter not found", "dynamic page unstable", "WAF-like behavior", "false-positive warning", "session cache conflict"],
        "defense": "Use parameterized queries, least privilege, input validation, safe errors, and regression testing.",
    },
    "hydra": {
        "purpose": "Audits login controls by exercising credential combinations against selected services.",
        "menu": ["-l/-L users", "-p/-P passwords", "-s port", "-S TLS", "-t tasks", "-f stop", "-o output", "-U module help"],
        "fields": ["Service", "Host", "Port", "Attempts", "Threads", "Rate limit", "Lockout", "Result"],
        "errors": ["too many attempts", "account locked", "unsupported module", "service unavailable", "invalid list format"],
        "defense": "Deploy MFA, rate limiting, lockouts, monitoring, and stronger password policy.",
    },
    "john": {
        "purpose": "Audits offline password hashes with wordlists, rules, masks, incremental search, and pot-file review.",
        "menu": ["--wordlist", "--rules", "--incremental", "--mask", "--format", "--show", "--status", "--restore", "--test"],
        "fields": ["Hash label", "Format", "Mode", "Candidates", "Speed", "Recovered", "Session", "Pot status"],
        "errors": ["unknown format", "malformed hash", "empty wordlist", "session restore unavailable"],
        "defense": "Use long unique passwords, password managers, salted slow hashes, and breach monitoring.",
    },
    "hashcat": {
        "purpose": "Runs offline hash recovery strategies and reports device, speed, progress, recovered, left, and candidate status.",
        "menu": ["-m hash mode", "-a attack mode", "--status", "--show", "--left", "--session", "--restore", "--runtime", "--potfile-path"],
        "fields": ["Status", "Hash mode", "Attack mode", "Speed", "Recovered", "Progress", "Rejected", "Candidates"],
        "errors": ["wrong hash mode", "separator unmatched", "device unavailable", "thermal warning", "candidate space exhausted"],
        "defense": "Prefer Argon2/bcrypt/scrypt/PBKDF2, unique salts, password managers, and strong reset controls.",
    },
    "aircrack-ng": {
        "purpose": "Reviews wireless capture artifacts and performs offline WPA/WEP-style capture analysis.",
        "menu": ["aircrack-ng", "airmon-ng concept", "airodump-ng AP/client table", "airdecap-ng", "wpaclean", "airgraph-ng"],
        "fields": ["BSSID", "ESSID", "Channel", "Encryption", "Signal", "Clients", "Handshake", "Result"],
        "errors": ["no handshake", "capture corrupted", "wrong passphrase list", "target not in capture", "unsupported encryption"],
        "defense": "Use WPA3 where possible, strong passphrases, WPS disabled, and wireless monitoring.",
    },
    "wifite": {
        "purpose": "Coordinates wireless audit workflow: interface selection, AP scan, target filtering, capture checks, and offline analysis.",
        "menu": ["settings", "WEP", "WPA", "WPS", "PMKID", "--clients-only", "--skip-crack", "--cracked", "--ignored", "--check"],
        "fields": ["ESSID", "BSSID", "Channel", "Power", "Encryption", "WPS", "Clients", "PMKID", "Handshake"],
        "errors": ["no interface", "no AP matches", "no clients", "PMKID not present", "WPS locked", "target ignored"],
        "defense": "Disable WPS, use WPA3/strong WPA2, monitor rogue APs, and rotate weak passphrases.",
    },
}



def default_config():
    return {"name": os.environ.get("USER", "Agent") or "Agent", "theme": "blue", "mode": "cyber", "music": True, "fullscreen": True}


def load_config(cli):
    cfg = default_config()
    if CONFIG_FILE.exists():
        try:
            saved = json.loads(CONFIG_FILE.read_text())
            if isinstance(saved, dict):
                cfg.update(saved)
        except Exception:
            pass
    if cli.name:
        cfg["name"] = cli.name
    if cli.theme:
        cfg["theme"] = cli.theme
    if cli.mode:
        cfg["mode"] = cli.mode
        if not cli.theme and cli.mode in MODES:
            cfg["theme"] = MODES[cli.mode]["theme"]
    if cli.no_music:
        cfg["music"] = False
    if cli.windowed:
        cfg["fullscreen"] = False
    if cfg.get("theme") not in THEMES:
        cfg["theme"] = MODES.get(cfg.get("mode", "cyber"), MODES["cyber"])["theme"]
    if cfg.get("mode") not in MODES:
        cfg["mode"] = "cyber"
        cfg["theme"] = MODES["cyber"]["theme"]
    return cfg


def save_config(cfg):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2) + "\n")


def clean_name(name):
    cleaned = "".join(c.lower() if c.isalnum() else "" for c in str(name))
    return cleaned or "agent"


class App:
    def __init__(self, root, cfg):
        self.root = root
        self.cfg = cfg
        self.mode = MODES[cfg["mode"]]
        self.theme = THEMES[cfg["theme"]]
        self.agent_name = str(cfg.get("name") or "Agent").strip() or "Agent"
        self.prompt_user = clean_name(self.agent_name)
        self.cmd_buffer = ""
        self.history = []
        self.history_pos = None
        self.busy = False
        self.music_enabled = bool(cfg.get("music", True))
        self.volume = int(cfg.get("volume", 75))
        self.volume = max(0, min(100, self.volume))
        self.music_alive = True
        self.music_proc = None
        self.voice_proc = None
        self.music_mode = None
        self.columns = []
        self.nodes = []
        self.scan_tick = 0
        self.bg_tick = 0
        self.glitch_until = 0
        self.boss_active = False
        self.boss_hits = 0
        self.game = None
        self.tool_session = None

        self.root.title(APP_NAME)
        self.root.configure(bg=self.theme["bg"])
        self.root.attributes("-fullscreen", bool(cfg.get("fullscreen", True)))

        self.title_font = font.Font(family="Courier New", size=16, weight="bold")
        self.main_font = font.Font(family="Courier New", size=18)
        self.small_font = font.Font(family="Courier New", size=12)
        self.big_font = font.Font(family="Courier New", size=24, weight="bold")

        self.build_ui()
        self.root.bind("<Escape>", lambda e: self.close_app())
        self.root.bind("<Control-q>", lambda e: self.close_app())
        self.root.bind("<Button-1>", lambda e: self.force_focus())
        self.root.bind_all("<KeyPress>", self.global_keypress, add="+")

        self.animate_background()
        self.animate_matrix()
        self.animate_status()
        self.animate_scanbar()
        self.animate_cursor()
        self.animate_graph()
        if self.music_enabled:
            self.start_music()
        self.force_focus()
        self.boot_sequence()

    def colors(self):
        return self.theme

    def build_ui(self):
        c = self.colors()
        top = tk.Frame(self.root, bg=c["panel"], height=46)
        top.pack(fill="x")
        self.title_label = tk.Label(top, text=f"{self.mode['label']} // AGENT {self.agent_name.upper()}", bg=c["panel"], fg=c["fg"], font=self.title_font)
        self.title_label.pack(side="left", padx=12, pady=8)
        self.sim_label = tk.Label(top, text="TRAINING RANGE", bg=c["panel"], fg=c["accent"], font=self.small_font)
        self.sim_label.pack(side="left", padx=16, pady=10)
        self.status_var = tk.StringVar(value=random.choice(self.mode["status"]))
        self.status_label = tk.Label(top, textvariable=self.status_var, bg=c["panel"], fg=c["accent"], font=self.small_font)
        self.status_label.pack(side="right", padx=12, pady=10)

        body = tk.Frame(self.root, bg=c["bg"])
        body.pack(fill="both", expand=True)
        self.bg_canvas = tk.Canvas(body, bg=c["bg"], highlightthickness=0)
        self.bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        left = tk.Frame(body, bg=c["bg"])
        left.pack(side="left", fill="both", expand=True)
        right = tk.Frame(body, bg=c["bg"], width=330)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)
        left.lift()
        right.lift()

        self.text = tk.Text(left, bg=c["text_bg"], fg=c["fg"], insertbackground=c["fg"], relief="flat", wrap="word", font=self.main_font, padx=16, pady=16, state="disabled", takefocus=0)
        self.text.pack(fill="both", expand=True, padx=(8, 0), pady=8)
        self.text.tag_configure("danger", foreground=c["danger"])
        self.text.tag_configure("accent", foreground=c["accent"])

        bottom = tk.Frame(left, bg=c["bg"])
        bottom.pack(fill="x", padx=16, pady=(0, 16))
        tk.Label(bottom, text="COMMAND:", bg=c["bg"], fg=c["accent"], font=self.small_font).pack(anchor="w")
        self.cmd_frame = tk.Frame(bottom, bg=c["text_bg"], highlightbackground=c["fg"], highlightthickness=2)
        self.cmd_frame.pack(fill="x", pady=(4, 0))
        self.prompt_var = tk.StringVar(value=self.random_prompt())
        self.prompt_label = tk.Label(self.cmd_frame, textvariable=self.prompt_var, bg=c["text_bg"], fg=c["fg"], font=self.main_font)
        self.prompt_label.pack(side="left", padx=(8, 0), pady=6)
        self.command_var = tk.StringVar(value="")
        self.command_label = tk.Label(self.cmd_frame, textvariable=self.command_var, bg=c["text_bg"], fg=c["accent"], font=self.main_font, anchor="w")
        self.command_label.pack(side="left", fill="x", expand=True, padx=(6, 0), pady=6)
        self.cursor_var = tk.StringVar(value="█")
        self.cursor_label = tk.Label(self.cmd_frame, textvariable=self.cursor_var, bg=c["text_bg"], fg=c["fg"], font=self.main_font)
        self.cursor_label.pack(side="right", padx=(0, 8), pady=6)
        tk.Label(bottom, text="Type help. Escape or Ctrl+Q exits.", bg=c["bg"], fg=c["accent"], font=self.small_font).pack(anchor="w", pady=(6, 0))

        self.badge = tk.Canvas(right, bg=c["text_bg"], highlightthickness=1, highlightbackground=c["dim"], width=300, height=130)
        self.badge.pack(padx=12, pady=(12, 8))
        tk.Label(right, text="SIGNAL MAP", bg=c["bg"], fg=c["fg"], font=self.title_font).pack(anchor="n", pady=(2, 4))
        self.graph = tk.Canvas(right, bg=c["text_bg"], highlightthickness=1, highlightbackground=c["dim"], width=300, height=170)
        self.graph.pack(padx=12, pady=(0, 8))
        tk.Label(right, text="DATA RAIN", bg=c["bg"], fg=c["fg"], font=self.title_font).pack(anchor="n", pady=(2, 4))
        self.matrix = tk.Canvas(right, bg=c["text_bg"], highlightthickness=1, highlightbackground=c["dim"], width=300)
        self.matrix.pack(fill="both", expand=True, padx=12, pady=(0, 8))
        self.scanbar = tk.Canvas(right, bg=c["text_bg"], highlightthickness=1, highlightbackground=c["dim"], width=300, height=96)
        self.scanbar.pack(padx=12, pady=(0, 12))
        self.flash = tk.Label(self.root, text="", bg=c["bg"], fg=c["accent"], font=self.big_font)
        self.flash.place_forget()
        self.draw_badge()
        self.setup_matrix()
        self.setup_graph()

    def random_prompt(self):
        return random.choice([f"{self.prompt_user}@ops:~# ", f"root@{self.prompt_user}:~# ", f"ghost@{self.prompt_user}:~# ", f"operator@{self.mode['tag'].lower().replace(' ', '-')}:~# "])

    def write(self, line="", tag=None):
        self.text.configure(state="normal")
        if tag:
            self.text.insert("end", line + "\n", tag)
        else:
            self.text.insert("end", line + "\n")
        self.text.see("end")
        self.text.configure(state="disabled")

    def clear(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")

    def boot_sequence(self):
        lines = [
            "[+] Booting secure operations console...",
            "[+] Loading mission modules...",
            f"[+] Mode selected: {self.cfg['mode']}",
            f"[+] Theme selected: {self.cfg['theme']}",
            "[+] Shell bridge isolated.",
            "[+] Network interface locked.",
            "[+] Visual engine online.",
            "[+] Audio profile armed.",
            "",
            f"WELCOME, AGENT {self.agent_name.upper()}",
            "TYPE help AND PRESS ENTER",
            "",
        ]
        self.run_lines(lines, final=self.finish_response)

    def draw_badge(self):
        c = self.colors()
        canvas = self.badge
        canvas.delete("all")
        canvas.create_rectangle(12, 14, 288, 116, outline=c["fg"], width=3, fill=c["panel"])
        canvas.create_text(150, 34, text=self.mode["label"], fill=c["fg"], font=("Courier New", 19, "bold"))
        canvas.create_text(150, 62, text=self.mode["tag"], fill=c["accent"], font=("Courier New", 13, "bold"))
        canvas.create_line(36, 88, 264, 88, fill=c["fg"], width=2)
        canvas.create_text(150, 105, text="LOCAL OPS CONSOLE", fill=c["accent"], font=("Courier New", 10, "bold"))

    def setup_matrix(self):
        self.columns = []
        chars = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ#$%*+<>/{}[]"
        if self.cfg["mode"] == "office":
            chars = "VPNMFAJWTCRMPRN012345"
        elif self.cfg["mode"] == "adult":
            chars = "VIPLOUNGE$XO69?"
        for x in range(18, 292, 15):
            self.columns.append([x, random.randint(-500, 0), random.randint(7, 18), random.randint(6, 19), chars])

    def setup_graph(self):
        self.nodes = []
        for _ in range(10):
            self.nodes.append([random.randint(25, 275), random.randint(25, 145), random.choice([0, 1, 2])])

    def animate_background(self):
        c = self.colors()
        if not hasattr(self, "bg_canvas"):
            return
        w = max(1, self.bg_canvas.winfo_width())
        h = max(1, self.bg_canvas.winfo_height())
        self.bg_canvas.delete("all")
        mode = self.cfg.get("mode", "cyber")
        t = self.bg_tick
        if mode == "office":
            for x in range(0, int(w), 90):
                for y in range(0, int(h), 70):
                    pulse = (x + y + t) % 140 < 70
                    self.bg_canvas.create_rectangle(x+8, y+8, x+72, y+45, outline=c["dim" if pulse else "panel"], width=1)
                    self.bg_canvas.create_text(x+40, y+26, text=random.choice(["VPN", "PDF", "MFA", "PRN", "CRM"]), fill=c["dim"], font=("Courier New", 10))
        elif mode == "adult":
            for i in range(18):
                x = (i * 85 + t * 4) % (w + 80) - 40
                y = 55 + (i * 47) % max(int(h)-80, 1)
                self.bg_canvas.create_text(x, y, text=random.choice(["VIP", "XXX", "$", "LOUNGE", "404", "BAR"]), fill=c["dim"], font=("Courier New", 18, "bold"))
            self.bg_canvas.create_rectangle(w*0.08, h*0.12, w*0.92, h*0.88, outline=c["dim"], width=2)
        else:
            for i in range(28):
                x1 = (i * 71 + t * 5) % max(w, 1)
                y1 = (i * 37) % max(h, 1)
                x2 = (x1 + 160 + i*7) % max(w, 1)
                y2 = (y1 + 90 + i*11) % max(h, 1)
                self.bg_canvas.create_line(x1, y1, x2, y2, fill=c["dim"], width=1)
                self.bg_canvas.create_rectangle(x1-3, y1-3, x1+3, y1+3, fill=c["fg"], outline="")
        self.bg_tick += 1
        self.root.after(130, self.animate_background)

    def animate_matrix(self):
        c = self.colors()
        self.matrix.delete("all")
        h = max(self.matrix.winfo_height(), 300)
        chaos = time.time() < self.glitch_until
        for col in self.columns:
            x, y, speed, length, chars = col
            for i in range(length):
                xx = x + (random.randint(-5, 5) if chaos else 0)
                color = c["danger"] if chaos and random.random() < 0.25 else (c["fg"] if i == 0 else c["dim"])
                self.matrix.create_text(xx, y - i * 15, text=random.choice(chars), fill=color, font=("Courier New", 11))
            col[1] += speed + (8 if chaos else 0)
            if col[1] - length * 15 > h:
                col[1] = random.randint(-220, 0)
                col[2] = random.randint(7, 18)
                col[3] = random.randint(6, 19)
        self.root.after(75 if chaos else 95, self.animate_matrix)

    def animate_graph(self):
        c = self.colors()
        self.graph.delete("all")
        chaos = time.time() < self.glitch_until
        for i, a in enumerate(self.nodes):
            for b in self.nodes[i+1:]:
                if random.random() < (0.18 if not chaos else 0.35):
                    self.graph.create_line(a[0], a[1], b[0], b[1], fill=c["dim"] if not chaos else c["danger"], width=1)
        for idx, n in enumerate(self.nodes):
            if random.random() < 0.08 or chaos:
                n[0] = max(20, min(280, n[0] + random.randint(-8, 8)))
                n[1] = max(20, min(150, n[1] + random.randint(-7, 7)))
            fill = c["fg"] if n[2] else c["accent"]
            if chaos and random.random() < 0.35:
                fill = c["danger"]
            self.graph.create_oval(n[0]-6, n[1]-6, n[0]+6, n[1]+6, fill=fill, outline="")
            self.graph.create_text(n[0], n[1]-13, text=str(idx), fill=c["accent"], font=("Courier New", 8))
        self.root.after(280, self.animate_graph)

    def animate_status(self):
        self.status_var.set(random.choice(self.mode["status"]))
        self.root.after(850, self.animate_status)

    def animate_scanbar(self):
        c = self.colors()
        self.scanbar.delete("all")
        h = 96
        label = "THREAT METER"
        for i in range(20):
            x1 = 10 + i * 14
            level = int((math.sin((self.scan_tick + i) / 2.0) + 1) * 22) + random.randint(2, 11)
            color = c["danger"] if time.time() < self.glitch_until and i % 3 == 0 else c["fg"]
            self.scanbar.create_rectangle(x1, h - level, x1 + 8, h - 8, fill=color, outline="")
        self.scanbar.create_text(150, 14, text=label, fill=c["accent"], font=("Courier New", 11, "bold"))
        self.scan_tick += 1
        self.root.after(110, self.animate_scanbar)

    def animate_cursor(self):
        self.cursor_var.set("█" if self.cursor_var.get() == " " else " ")
        self.root.after(500, self.animate_cursor)

    def force_focus(self):
        try:
            self.root.focus_force()
        except Exception:
            pass

    def close_app(self):
        self.music_alive = False
        self.stop_music()
        self.stop_voice()
        self.game = None
        self.tool_session = None
        try:
            self.root.destroy()
        except Exception:
            pass

    def type_line(self, line, done=None, idx=0):
        self.text.configure(state="normal")
        if idx < len(line):
            self.text.insert("end", line[idx])
            self.text.see("end")
            self.text.configure(state="disabled")
            self.root.after(5, lambda: self.type_line(line, done, idx + 1))
        else:
            self.text.insert("end", "\n")
            self.text.see("end")
            self.text.configure(state="disabled")
            if done:
                self.root.after(35, done)

    def run_lines(self, lines, final=None):
        if not lines:
            if final:
                final()
            return
        self.type_line(lines[0], done=lambda: self.run_lines(lines[1:], final))

    def flash_message(self, msg, ms=1100):
        self.flash.configure(text=msg)
        self.flash.place(relx=0.5, rely=0.43, anchor="center")
        self.glitch_until = time.time() + min(2.0, ms / 1000)
        self.root.after(ms, lambda: self.flash.place_forget())

    def set_buffer(self, text):
        self.cmd_buffer = text
        self.command_var.set(text)

    def global_keypress(self, event):
        if event.keysym == "Escape":
            self.close_app()
            return "break"
        if event.state & 0x4 and event.keysym.lower() == "q":
            self.close_app()
            return "break"
        # Do not bind normal +/-/= typing keys to volume. On Linux Mint Cinnamon
        # those keys must enter text normally; volume is controlled with typed
        # commands such as "volume up", "volume down", or "volume 0-100".
        if self.boss_active and event.char and event.char.lower() == "x":
            self.boss_hits += 1
            self.flash_message(f"TRACE HIT {self.boss_hits}/7", 500)
            if self.boss_hits >= 7:
                self.boss_active = False
                self.busy = False
                self.run_lines(["[+] Boss trace defeated", "[+] Access token awarded", ""], final=self.finish_response)
            return "break"
        if self.busy and not self.game and not self.tool_session:
            return "break"
        if event.keysym == "Return":
            self.respond()
            return "break"
        if event.keysym == "BackSpace":
            self.set_buffer(self.cmd_buffer[:-1])
            return "break"
        if event.keysym == "Up":
            if self.history:
                self.history_pos = len(self.history) - 1 if self.history_pos is None else max(0, self.history_pos - 1)
                self.set_buffer(self.history[self.history_pos])
            return "break"
        if event.keysym == "Down":
            if self.history and self.history_pos is not None:
                self.history_pos += 1
                if self.history_pos >= len(self.history):
                    self.history_pos = None
                    self.set_buffer("")
                else:
                    self.set_buffer(self.history[self.history_pos])
            return "break"
        if event.keysym in ("Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R", "Super_L", "Super_R", "Meta_L", "Meta_R", "Caps_Lock", "Tab"):
            return "break"
        if event.char and event.char.isprintable():
            self.set_buffer(self.cmd_buffer + event.char)
            return "break"
        return "break"

    def respond(self):
        cmd = self.cmd_buffer.strip()
        shown = self.cmd_buffer
        self.set_buffer("")
        self.history.append(cmd)
        self.history = self.history[-70:]
        self.history_pos = None
        lower = cmd.lower()
        self.write(self.prompt_var.get() + shown)

        if self.tool_session:
            self.handle_tool_input(lower)
            return
        if self.game:
            self.handle_game_input(lower)
            return
        self.busy = True

        if lower in ("quit", "exit"):
            self.close_app(); return
        if lower == "clear":
            self.clear(); self.busy = False; return
        if lower in ("help", "?"):
            self.run_lines(HELP, final=self.finish_response); return
        if lower == "settings":
            self.run_lines([f"name={self.agent_name}", f"theme={self.cfg['theme']}", f"mode={self.cfg['mode']}", f"music={'on' if self.music_enabled else 'off'}", f"volume={self.volume}", f"fullscreen={'on' if self.root.attributes('-fullscreen') else 'off'}", ""], final=self.finish_response); return
        if lower.startswith("theme "):
            self.change_theme(lower.split(None, 1)[1]); return
        if lower.startswith("mode "):
            self.change_mode(lower.split(None, 1)[1]); return
        if lower.startswith("profile "):
            self.change_profile(cmd.split(None, 1)[1]); return
        if lower in ("sound off", "music off"):
            self.stop_music(); self.cfg["music"] = False; save_config(self.cfg); self.run_lines(["[+] Sound disabled", ""], final=self.finish_response); return
        if lower in ("sound on", "music on"):
            self.cfg["music"] = True; save_config(self.cfg); self.music_enabled = True; self.start_music(restart=True); self.run_lines(["[+] Sound enabled", ""], final=self.finish_response); return
        if lower in ("volume up", "vol up"):
            self.adjust_volume(10); self.run_lines([f"[+] Volume {self.volume}%", ""], final=self.finish_response); return
        if lower in ("volume down", "vol down"):
            self.adjust_volume(-10); self.run_lines([f"[+] Volume {self.volume}%", ""], final=self.finish_response); return
        if lower.startswith("volume "):
            try:
                self.set_volume(int(lower.split(None, 1)[1]))
                self.run_lines([f"[+] Volume {self.volume}%", ""], final=self.finish_response); return
            except Exception:
                self.run_lines(["[!] Usage: volume 0-100", ""], final=self.finish_response); return
        if lower == "fullscreen off":
            self.root.attributes("-fullscreen", False); self.cfg["fullscreen"] = False; save_config(self.cfg); self.run_lines(["[+] Windowed mode enabled", ""], final=self.finish_response); return
        if lower == "fullscreen on":
            self.root.attributes("-fullscreen", True); self.cfg["fullscreen"] = True; save_config(self.cfg); self.run_lines(["[+] Fullscreen mode enabled", ""], final=self.finish_response); return
        if lower == "boss":
            self.start_boss(); return
        if lower in ("tools", "kali", "kalihelp"):
            self.run_lines(self.kali_tools_help(), final=self.finish_response); return
        if lower.startswith("kalihelp ") or lower.startswith("help "):
            tool = lower.split(None, 1)[1].strip()
            if tool in SIM_TOOLS:
                self.run_lines(self.kali_tool_help(tool), final=self.finish_response); return
        if lower.startswith("scenario "):
            tool = lower.split(None, 1)[1].strip()
            if tool in TOOL_SCENARIOS:
                self.run_lines(self.tool_scenario(tool), final=self.finish_response); return
        first = lower.split(None, 1)[0] if lower else ""
        if first == "burp":
            first = "burpsuite"; lower = "burpsuite " + lower.split(None, 1)[1] if " " in lower else "burpsuite"
        if first in SIM_TOOLS:
            self.start_interactive_tool(lower); return
        if lower in ("cipher", "firewall", "breach", "snake", "adventure", "modegame"):
            self.start_game(lower); return
        if lower == "matrix":
            self.flash_message("DATA SURGE", 1200)
            self.run_lines(["[*] Rain intensity boosted", "01001000 01000001 01000011 01001011", "10101010 00001111 11001100 00110011", "[+] Entropy field increased", ""], final=self.finish_response); return
        if lower == "effects":
            self.flash_message(random.choice(["TRACE SPIKE", "SIGNAL FLOOD", "ACCESS WINDOW", "KEYSPACE COLLAPSE"]), 1500)
            self.run_lines(["[*] Visual surge injected", "[*] Signal map overclocked", "[*] Data rain destabilized", ""], final=self.finish_response); return

        self.run_lines(["[!] Unknown command", "[i] Type help for available commands", "[i] Commands now require explicit tool/game/session input.", ""], final=self.finish_response)

    def finish_response(self):
        self.prompt_var.set(self.random_prompt())
        self.busy = False
        self.force_focus()

    def progress(self, width=22):
        lines = []
        for pct in (13, 27, 41, 58, 73, 86, 100):
            filled = int(width * pct / 100)
            lines.append("[" + "#" * filled + "." * (width - filled) + f"] {pct}%")
        return lines

    def sequence_for(self, cmd):
        if cmd == "scan":
            mission = random.choice(self.mode["missions"])
            return [f"[*] Scanning {mission}..."] + [f"[*] {v}" for v in random.sample(self.mode["verbs"], min(4, len(self.mode["verbs"])))] + self.progress() + ["[+] Scan complete", "[+] Interface remained isolated", ""]
        if cmd in ("decrypt", "crack"):
            return self.crack_sequence()
        if cmd == "trace":
            return ["[!] Trace vector detected", "[*] Routing through decoy tunnels", "[*] Launching counter-intrusion firewall", "[*] Reversing countdown", "[*] Burning exit node", "[+] Trace defeated", ""]
        return self.full_mission_sequence()

    def crack_sequence(self):
        target = random.choice(self.mode["missions"])
        key = random.choice(self.mode["keys"])
        lines = [f"[*] Target: {target}", f"[*] Attack profile: {self.mode['label']}"]
        for step in self.mode["crack"]:
            token = random.choice(self.mode["keys"] + CRACK_WORDS)
            score = random.randint(128, 8192)
            lines.append(f"[*] {step} :: token={token} score={score}")
            if random.random() < 0.45:
                lines.append(random.choice(["    entropy drift corrected", "    collision window narrowed", "    timing jitter stabilized", "    candidate rejected", "    candidate promoted"]))
        lines += self.progress(26)
        lines += [f"[+] Key fragment accepted: {key}-{random.randint(1000,9999)}", "[+] Session channel opened", ""]
        self.root.after(500, lambda: self.flash_message(random.choice(["ACCESS WINDOW", "KEYSPACE HIT", "HASH MATCH"]), 900))
        return lines

    def full_mission_sequence(self):
        lines = [f"[*] Mission target: {random.choice(self.mode['missions'])}"]
        lines += [f"[*] {v}" for v in random.sample(self.mode["verbs"], min(5, len(self.mode["verbs"])))]
        lines += self.crack_sequence()[:-1]
        lines += ["[+] " + random.choice(self.mode["extras"]), "[+] Mission complete", ""]
        self.root.after(650, lambda: self.flash_message(random.choice(["ACCESS GRANTED", "MISSION COMPLETE", "TRACE DEFEATED"]), 1000))
        return lines

    def change_theme(self, name):
        if name not in THEMES:
            self.run_lines(["[!] Unknown theme", "Themes: " + ", ".join(THEMES), ""], final=self.finish_response); return
        self.cfg["theme"] = name; self.theme = THEMES[name]; save_config(self.cfg); self.apply_theme(); self.run_lines([f"[+] Theme changed to {name}", ""], final=self.finish_response)

    def apply_theme(self):
        c = self.colors()
        self.root.configure(bg=c["bg"])
        for w in (self.title_label, self.sim_label, self.status_label):
            w.configure(bg=c["panel"])
        self.title_label.configure(fg=c["fg"]); self.sim_label.configure(fg=c["accent"]); self.status_label.configure(fg=c["accent"])
        self.text.configure(bg=c["text_bg"], fg=c["fg"], insertbackground=c["fg"])
        self.text.tag_configure("danger", foreground=c["danger"]); self.text.tag_configure("accent", foreground=c["accent"])
        self.cmd_frame.configure(bg=c["text_bg"], highlightbackground=c["fg"])
        for w, color in ((self.prompt_label, c["fg"]), (self.command_label, c["accent"]), (self.cursor_label, c["fg"])):
            w.configure(bg=c["text_bg"], fg=color)
        for canv in (self.badge, self.matrix, self.scanbar, self.graph, self.bg_canvas):
            canv.configure(bg=c["text_bg"], highlightbackground=c["dim"])
        self.flash.configure(bg=c["bg"], fg=c["accent"])
        self.draw_badge()

    def change_mode(self, name):
        if name not in MODES:
            self.run_lines(["[!] Unknown mode", "Modes: " + ", ".join(MODES), ""], final=self.finish_response); return
        self.cfg["mode"] = name; self.mode = MODES[name]
        self.cfg["theme"] = self.mode["theme"]; self.theme = THEMES[self.cfg["theme"]]
        save_config(self.cfg)
        self.title_label.configure(text=f"{self.mode['label']} // AGENT {self.agent_name.upper()}")
        self.setup_matrix(); self.setup_graph(); self.apply_theme(); self.start_music(restart=True)
        self.flash_message(self.mode["label"], 900)
        self.run_lines([f"[+] Mode changed to {name}", f"[+] Audio profile: {self.mode['tag']}", ""], final=self.finish_response)

    def change_profile(self, name):
        name = name.strip() or "Agent"
        self.agent_name = name; self.prompt_user = clean_name(name); self.cfg["name"] = name; save_config(self.cfg)
        self.title_label.configure(text=f"{self.mode['label']} // AGENT {self.agent_name.upper()}")
        self.run_lines([f"[+] Agent profile changed to {name}", ""], final=self.finish_response)

    def start_boss(self):
        self.boss_active = True; self.boss_hits = 0; self.busy = True
        self.flash_message("TRACE BOSS", 1000)
        self.run_lines(["[!] Boss trace incoming", "[!] Press X seven times to defeat it", ""], final=None)


    def kali_tools_help(self):
        lines = ["Available ops tools:", ""]
        for name in sorted(SIM_TOOLS):
            lines.append(f"  {name:<12} {SIM_TOOLS[name]['title']}")
        lines += ["", "Use: kalihelp TOOL", "Example: kalihelp nmap", "Example: nmap -sV -sC 192.0.2.10", ""]
        return lines

    def tool_details(self, tool):
        return TOOL_DETAILS.get(tool, {
            "purpose": SIM_TOOLS.get(tool, {}).get("title", "Runs a console operation."),
            "menu": ["help", "target", "options", "run", "output", "report"],
            "fields": ["target", "status", "result", "evidence"],
            "errors": ["invalid option", "target unavailable", "timeout"],
            "defense": "Review evidence, reduce exposure, patch, monitor, and retest.",
        })

    def kali_tool_help(self, tool):
        spec = SIM_TOOLS[tool]
        details = self.tool_details(tool)
        lines = [f"{tool} - {spec['title']}", "", "PURPOSE", f"  {details['purpose']}", "", "ACCEPTED COMMAND SHAPES"]
        lines += [f"  {x}" for x in spec["syntax"]]
        lines += ["", "HELP / MENU AREAS"] + [f"  - {x}" for x in details["menu"]]
        lines += ["", "OUTPUT FIELDS"] + [f"  - {x}" for x in details["fields"]]
        lines += ["", "COMMON ERROR STATES"] + [f"  - {x}" for x in details["errors"]]
        lines += ["", "REASONING", "  Start with scope, choose the least noisy option, validate evidence, then map the result to a fix."]
        lines += ["", "DEFENSIVE TAKEAWAY", f"  {details['defense']}", "", f"Try: scenario {tool}", ""]
        return lines

    def tool_scenario(self, tool):
        lines = [f"{tool} workflow", "=" * (len(tool) + 9)]
        for i, step in enumerate(TOOL_SCENARIOS.get(tool, []), 1):
            lines.append(f"{i:02d}. {step}")
        lines += ["", f"Run: kalihelp {tool}", f"Run: {SIM_TOOLS[tool]['syntax'][0]}", ""]
        return lines

    def sim_target(self, parts):
        joined = " ".join(parts)
        for token in parts:
            t = token.strip("'\"")
            if t.startswith("http://") or t.startswith("https://"):
                return t
            if any(ch.isdigit() for ch in t) and "." in t:
                return t
            if t.endswith(".test") or t.endswith(".local"):
                return t
        return random.choice(SIM_TARGETS)

    def start_interactive_tool(self, command):
        try:
            parts = shlex.split(command)
        except Exception:
            parts = command.split()
        tool = parts[0].lower() if parts else ""
        args = parts[1:]
        if tool == "burp":
            tool = "burpsuite"
        if tool not in SIM_TOOLS:
            self.run_lines(["[!] Tool profile not loaded", ""], final=self.finish_response); return
        self.tool_session = {"tool": tool, "command": command, "args": args, "stage": "start", "target": None, "selected": None, "batch": 0, "attempts": []}
        self.busy = False
        self.flash_message(f"{tool.upper()} READY", 800)
        self.speak(f"tool-{tool}", f"{tool} operation ready")
        self.run_lines(self.tool_intro(tool, command) + self.tool_prompt(), final=self.finish_tool_prompt)

    def finish_tool_prompt(self):
        self.busy = False
        self.force_focus()

    def tool_prompt(self):
        if not self.tool_session:
            return [""]
        tool = self.tool_session["tool"]
        if tool == "wifite":
            st = self.tool_session["stage"]
            if st == "start": return ["[INPUT] type scan to discover APs, or stop", ""]
            if st == "scanned": return ["[INPUT] type target 1-3 to select AP, or scan again, or stop", ""]
            if st == "selected": return ["[INPUT] type capture to collect handshake, options to view filters, or stop", ""]
            if st == "captured": return ["[INPUT] type crack to test next password batch, show to view status, or stop", ""]
            if st == "cracking": return ["[INPUT] type crack for next batch, show for status, finish for report, or stop", ""]
        if tool == "msfconsole":
            return ["[INPUT] type search, use 0, options, set RHOSTS TARGET, run, notes, or stop", ""]
        if tool == "burpsuite":
            return ["[INPUT] type proxy, repeater, intruder, decoder, comparer, report, or stop", ""]
        if tool in ("wireshark", "tshark"):
            return ["[INPUT] type open, filter http, conversations, stream, stats, report, or stop", ""]
        if tool in ("hydra", "john", "hashcat", "sqlmap", "aircrack-ng"):
            return ["[INPUT] type setup, run, next, show, report, or stop", ""]
        return ["[INPUT] type set target TARGET, options, run, next, report, or stop", ""]

    def handle_tool_input(self, lower):
        if not self.tool_session:
            return
        if lower in ("stop", "quit", "exit", "back"):
            tool = self.tool_session["tool"]
            self.run_lines([f"[{tool.upper()}] session closed", ""], final=self.finish_response)
            self.tool_session = None
            return
        tool = self.tool_session["tool"]
        if tool == "wifite": lines = self.tool_wifite_step(lower)
        elif tool == "msfconsole": lines = self.tool_msf_step(lower)
        elif tool == "burpsuite": lines = self.tool_burp_step(lower)
        elif tool in ("wireshark", "tshark"): lines = self.tool_packet_step(lower)
        else: lines = self.tool_generic_step(lower)
        self.run_lines(lines + self.tool_prompt(), final=self.finish_tool_prompt)

    def tool_generic_step(self, lower):
        tool = self.tool_session["tool"]
        if lower.startswith("set target "):
            self.tool_session["target"] = lower.split(None, 2)[2]
            return [f"[{tool.upper()}] target set: {self.tool_session['target']}"]
        if lower == "options":
            return self.kali_tool_help(tool)
        if lower == "setup":
            return [f"[{tool.upper()}] configuration loaded", "[SETUP] input source: console profile", "[SETUP] rate limit: enabled", "[SETUP] evidence buffer: enabled"]
        if lower in ("run", "next"):
            self.tool_session["batch"] += 1
            if tool == "hydra": return self.hydra_batch()
            if tool == "john": return self.john_batch()
            if tool == "hashcat": return self.hashcat_batch()
            if tool == "sqlmap": return self.sqlmap_batch()
            if tool == "aircrack-ng": return self.aircrack_batch()
            return self.run_sim_tool(f"{tool} " + " ".join(self.tool_session.get("args", [])))
        if lower in ("show", "status"):
            return [f"[{tool.upper()}] stage={self.tool_session.get('stage')} batch={self.tool_session.get('batch')} target={self.tool_session.get('target') or 'unset'}"]
        if lower == "report":
            return self.tool_footer(tool)
        return ["[!] expected: setup, run, next, show, report, set target TARGET, options, or stop"]

    def random_password_attempts(self, min_count=8, max_count=24):
        base = ["password", "admin", "letmein", "qwerty123", "welcome1", "summer2026", "winter2026", "consolelab", "netgear2026", "backup2026", "service1", "changeme", "dragon", "coffee_admin", "orbit-admin", "velvet-wifi"]
        count = random.randint(min_count, max_count)
        attempts = []
        for _ in range(count - 1):
            attempts.append(random.choice(base) + random.choice(["", str(random.randint(1,99)), "!", "#", "2026"]))
        success = random.choice(self.mode["keys"]).lower() + "-" + str(random.randint(1000,9999))
        attempts.append(success)
        return attempts, success

    def hydra_batch(self):
        attempts, success = self.random_password_attempts(8, 15)
        host = self.tool_session.get('target') or '192.0.2.10'
        user = random.choice(["admin", "operator", "service", "backup"])
        lines=[f"[HYDRA] credential audit started", f"[DATA] target={host} user={user} max_runtime<=30s"]
        elapsed = 0
        for i, pw in enumerate(attempts, 1):
            elapsed += random.choice([1,1,2])
            if i == len(attempts):
                lines.append(f"[{elapsed:02d}s] [22][ssh] host: {host} login: {user} password: {pw}")
                lines.append(f"[STATUS] success after {i} attempts in {elapsed}s")
            else:
                lines.append(f"[{elapsed:02d}s] [ATTEMPT {i:02d}] login={user:<9} password={pw:<18} result=401")
        self.tool_session["stage"]="complete"
        return lines

    def john_batch(self):
        attempts, success = self.random_password_attempts(7, 15)
        lines=["[JOHN] Loaded 6 password hashes", "[JOHN] format=Raw-MD5 candidate generator=wordlist+rules"]
        elapsed=0
        for i,pw in enumerate(attempts,1):
            elapsed += random.choice([1,1,2])
            if i == len(attempts):
                lines.append(f"[{elapsed:02d}s] {pw:<20} (operator)")
                lines.append(f"[JOHN] session complete: 1g {elapsed}s {random.randint(1800,4200)}p/s")
            else:
                lines.append(f"[{elapsed:02d}s] candidate={pw:<20} rejected")
        self.tool_session["stage"]="complete"
        return lines

    def hashcat_batch(self):
        attempts, success = self.random_password_attempts(8, 15)
        total = random.randint(900000, 3000000)
        lines=["[HASHCAT] Status...........: Running", "[HASHCAT] Hash.Mode........: 0 (MD5)"]
        elapsed=0
        for i,pw in enumerate(attempts,1):
            elapsed += random.choice([1,1,1,2])
            progress = min(total, i * random.randint(25000, 90000))
            if i == len(attempts):
                lines.append(f"[{elapsed:02d}s] Recovered........: 1/1 (100.00%)")
                lines.append(f"[{elapsed:02d}s] Candidate.Engine.: {pw}")
                lines.append("[HASHCAT] Status...........: Cracked")
            else:
                lines.append(f"[{elapsed:02d}s] Progress.........: {progress}/{total} Candidate={pw}")
        self.tool_session["stage"]="complete"
        return lines

    def sqlmap_batch(self):
        steps=["testing connection", "checking dynamic content", "testing boolean-based blind", "testing UNION query", "fingerprinting DBMS", "enumerating databases"]
        b=min(self.tool_session["batch"], len(steps))
        lines=[f"[SQLMAP] {steps[b-1]}"]
        if b==len(steps): lines += ["available databases [4]:", "[*] information_schema", "[*] app", "[*] users", "[*] auditlog"]
        return lines

    def aircrack_batch(self):
        attempts, success = self.random_password_attempts(8, 15)
        lines=["[AIRCRACK-NG] Opening capture.cap", "[AIRCRACK-NG] WPA handshake confirmed", "[AIRCRACK-NG] Starting offline key test"]
        elapsed=0
        for i,pw in enumerate(attempts,1):
            elapsed += random.choice([1,1,2])
            if i == len(attempts):
                lines.append(f"[{elapsed:02d}s] KEY FOUND! [ {pw} ]")
                lines.append("[AIRCRACK-NG] Master Key     : 00 11 22 33 44 55 66 77")
            else:
                lines.append(f"[{elapsed:02d}s] tested: {pw}")
        self.tool_session["stage"]="complete"
        return lines

    def tool_wifite_step(self, lower):
        aps=[("1","NETGEAR-2G-LAB","6","WPA2","72db","yes","2"),("2","HOTEL-OPS","11","WPA2","64db","no","4"),("3","CONSOLE-LAB","1","WPA2","58db","yes","1")]
        if lower == "scan":
            self.tool_session["stage"]="scanned"
            lines=["[WIFITE] scanning for wireless devices", "[WIFITE] monitor interface: wlan0mon", "NUM  ESSID              CH  ENCR  PWR   WPS  CLIENTS"]
            lines += [f"{n:<4} {e:<18} {ch:<3} {enc:<5} {pwr:<5} {wps:<4} {cli}" for n,e,ch,enc,pwr,wps,cli in aps]
            return lines
        if lower.startswith("target ") and self.tool_session["stage"] in ("scanned","selected"):
            num=lower.split()[-1]
            match=next((a for a in aps if a[0]==num), None)
            if not match: return ["[!] choose target 1, 2, or 3"]
            self.tool_session["selected"]=match; self.tool_session["stage"]="selected"
            return [f"[WIFITE] selected {match[1]} BSSID 02:00:00:00:00:0{num}", "[WIFITE] no capture started yet"]
        if lower == "options":
            return ["[WIFITE OPTIONS] --clients-only enabled", "[WIFITE OPTIONS] --skip-crack disabled", "[WIFITE OPTIONS] active methods disabled inside console", "[WIFITE OPTIONS] PMKID check enabled"]
        if lower == "capture" and self.tool_session["stage"] == "selected":
            self.tool_session["stage"]="captured"
            self.speak("wifite-capture", "objective complete")
            return ["[WIFITE] listening for EAPOL frames", "[WIFITE] handshake candidate received", "[WIFITE] PMKID artifact checked", "[WIFITE] capture saved: captures/console-lab.cap"]
        if lower == "crack" and self.tool_session["stage"] in ("captured","cracking"):
            self.tool_session["stage"]="complete"; self.tool_session["batch"]+=1
            attempts, success = self.random_password_attempts(8, 15)
            lines=["[WIFITE] offline key audit started", "[WIFITE] runtime cap: <=30s"]
            elapsed=0
            for i,w in enumerate(attempts,1):
                elapsed += random.choice([1,1,2])
                if i == len(attempts):
                    lines.append(f"[{elapsed:02d}s] [KEY FOUND] {w}")
                    lines.append(f"[WIFITE] success after {i} password tests")
                else:
                    lines.append(f"[{elapsed:02d}s] [TRY {i:02d}] {w}")
            self.speak("wifite-success", "mission complete")
            return lines
        if lower in ("show","status"):
            sel=self.tool_session.get("selected")
            return [f"[WIFITE] stage={self.tool_session['stage']}", f"[WIFITE] selected={sel[1] if sel else 'none'}", f"[WIFITE] crack_batches={self.tool_session['batch']}"]
        if lower in ("finish","report"):
            return self.tool_footer("wifite")
        return ["[!] expected: scan, target N, options, capture, crack, show, finish, or stop"]

    def tool_msf_step(self, lower):
        if lower == "search": return ["msf6 > search type:auxiliary scanner", "0 auxiliary/scanner/http/title", "1 auxiliary/scanner/smb/smb_version"]
        if lower.startswith("use"): self.tool_session["stage"]="module"; return ["msf6 > use auxiliary/scanner/http/title", "module loaded"]
        if lower == "options": return ["Module options:", "RHOSTS   yes   target hosts", "RPORT    yes   80", "THREADS  yes   1"]
        if lower.startswith("set "): return ["RHOSTS => " + lower.split()[-1]]
        if lower == "run": return self.sim_msfconsole([])
        if lower == "notes": return ["Notes", "=====" , "http-title Operations Login", "smb-version Samba 4.17.5"]
        return ["[!] expected: search, use 0, options, set RHOSTS TARGET, run, notes, stop"]

    def tool_burp_step(self, lower):
        if lower in ("proxy","history"): return self.sim_burpsuite(["proxy"])
        if lower == "repeater": return self.sim_burpsuite(["repeater"])
        if lower == "intruder": return self.sim_burpsuite(["intruder"])
        if lower == "decoder": return ["[Decoder] input: session%3Dadmin", "URL decoded: session=admin", "Base64 panel ready"]
        if lower == "comparer": return ["[Comparer] response A length=1321", "[Comparer] response B length=118", "Difference: redirect and Set-Cookie header"]
        if lower == "report": return self.tool_footer("burpsuite")
        return ["[!] expected: proxy, repeater, intruder, decoder, comparer, report, stop"]

    def tool_packet_step(self, lower):
        tool=self.tool_session["tool"]
        if lower == "open": return self.sim_wireshark([]) if tool=="wireshark" else self.sim_tshark([])
        if lower.startswith("filter"): return [f"[{tool.upper()}] display filter applied: " + (lower.split(None,1)[1] if ' ' in lower else 'http'), "5 packets displayed"]
        if lower == "conversations": return ["TCP Conversations", "192.0.2.10:51514 <-> 198.51.100.5:80  5 packets", "192.0.2.10:53210 <-> 203.0.113.53:53 2 packets"]
        if lower == "stream": return ["Follow TCP Stream", "GET /login HTTP/1.1", "Host: demo.ops.local", "HTTP/1.1 200 OK"]
        if lower == "stats": return ["Protocol hierarchy", "TCP 71.4%", "HTTP 28.6%", "DNS 14.2%"]
        if lower == "report": return self.tool_footer(tool)
        return ["[!] expected: open, filter http, conversations, stream, stats, report, stop"]

    def learning_lines(self, tool):
        details = self.tool_details(tool)
        first_field = details["fields"][0] if details.get("fields") else "result"
        first_error = details["errors"][0] if details.get("errors") else "misconfiguration"
        return [
            f"[WHY] {details['purpose']}",
            f"[REASONING] First identify scope and inputs, then compare output evidence against expected behavior.",
            f"[WATCH] Key evidence field: {first_field}",
            f"[PITFALL] Common mistake: {first_error}",
        ]

    def tool_intro(self, tool, command):
        details = self.tool_details(tool)
        return [
            f"[{tool.upper()}] {SIM_TOOLS[tool]['title']}",
            f"[PURPOSE] {details['purpose']}",
            f"[COMMAND] {command}",
            f"[SCOPE] local console range / synthetic hosts",
            "[FLOW] parse options -> wait for operator input -> run staged operation -> record evidence",
        ] + self.learning_lines(tool) + [""]

    def tool_footer(self, tool):
        details = self.tool_details(tool)
        return ["", "[EVIDENCE] output captured in console buffer", "[REASONING] Good findings include observable output, context, uncertainty, and a next action.", f"[DEFENSE] {details['defense']}", ""]

    def run_sim_tool(self, command):
        try:
            parts = shlex.split(command)
        except Exception:
            parts = command.split()
        tool = parts[0].lower() if parts else ""
        args = parts[1:]
        if tool == "burp":
            tool = "burpsuite"
        self.flash_message(f"{tool.upper()} ACTIVE", 900)
        self.speak(f"tool-{tool}", f"{tool} operation started")
        body = []
        if tool == "nmap": body = self.sim_nmap(args)
        elif tool in ("gobuster", "dirb"): body = self.sim_gobuster(tool, args)
        elif tool == "nikto": body = self.sim_nikto(args)
        elif tool == "sqlmap": body = self.sim_sqlmap(args)
        elif tool == "hydra": body = self.sim_hydra(args)
        elif tool == "john": body = self.sim_john(args)
        elif tool == "hashcat": body = self.sim_hashcat(args)
        elif tool == "msfconsole": body = self.sim_msfconsole(args)
        elif tool == "burpsuite": body = self.sim_burpsuite(args)
        elif tool == "wireshark": body = self.sim_wireshark(args)
        elif tool == "tshark": body = self.sim_tshark(args)
        elif tool == "searchsploit": body = self.sim_searchsploit(args)
        elif tool == "enum4linux": body = self.sim_enum4linux(args)
        elif tool == "smbclient": body = self.sim_smbclient(args)
        elif tool == "wpscan": body = self.sim_wpscan(args)
        elif tool == "wifite": body = self.sim_wifite(args)
        elif tool == "aircrack-ng": body = self.sim_aircrack(args)
        else: body = ["[!] Tool profile not loaded", ""]
        return self.tool_intro(tool, command) + body + self.tool_footer(tool)

    def sim_nmap(self, args):
        target = self.sim_target(args)
        ports = [(22, "ssh", "OpenSSH 8.9p1"), (80, "http", "nginx 1.22.1"), (139, "netbios-ssn", "Samba smbd"), (443, "https", "Apache httpd 2.4.57"), (445, "microsoft-ds", "Samba 4.17.5")]
        if self.cfg.get("mode") == "adult": ports = [(80,"http","VelvetDoor nginx"),(443,"https","VIP lounge portal"),(8443,"https-alt","minibar admin API")]
        lines = [f"Starting Nmap 7.94SVN ( https://nmap.org )", f"Nmap scan report for {target}", "Host is up (0.0037s latency).", "Not shown: 995 filtered tcp ports (no-response)", "PORT     STATE SERVICE       VERSION"]
        for port, svc, ver in ports:
            lines.append(f"{port:<8}/tcp open  {svc:<13} {ver}")
        if any(a in ("-sC", "-A") for a in args):
            lines += ["|_http-title: Operations Login", "| ssh-hostkey:", "|   256 SHA256:9tW... console-ed25519", "|_  2048 SHA256:Vn2... console-rsa"]
        if "--script" in args or any("vuln" in a for a in args):
            lines += ["| vuln-check:", "|   CVE-2021-41773: path traversal exposure pattern", "|_  Risk: high"]
        lines += ["OS details: Linux 5.x - 6.x, embedded appliance, or filtered host", "Network Distance: 1 hop", "Service Info: Hostname: ops-node; Device: general purpose", "TRACEROUTE (using port 80/tcp)", "HOP RTT     ADDRESS", f"1   0.37 ms {target}", "Service detection performed.", "Nmap done: 1 IP address (1 host up) scanned in 12.48 seconds", ""]
        return lines

    def sim_gobuster(self, tool, args):
        target = self.sim_target(args)
        paths = ["/admin", "/login", "/backup", "/api/v1", "/uploads", "/server-status", "/dev", "/.git"]
        if self.cfg.get("mode") == "adult": paths = ["/vip", "/lounge", "/minibar", "/blackcard", "/afterhours"]
        lines = [f"===============================================================", f"{tool.upper()} v3.6", f"Url:                     {target}", "Method:                  GET", "Threads:                 10", "Status codes:            200,204,301,302,307,401,403", "===============================================================", "Starting discovery"]
        for path in paths:
            code = random.choice([200, 200, 301, 302, 401, 403])
            size = random.randint(132, 48120)
            lines.append(f"{path:<22} (Status: {code}) [Size: {size}]")
        lines += ["Progress: 4614 / 4614 (100.00%)", "Interesting extensions: php, txt, bak, json", "Potential next steps: inspect redirects, review 401 paths, compare response sizes", "===============================================================", "Finished", ""]
        return lines

    def sim_nikto(self, args):
        target = self.sim_target(args)
        return [f"- Nikto v2.5.0", f"+ Target Host: {target}", "+ Target Port: 80", "+ Start Time: Fri May 22 16:08:00 2026", "+ Server: nginx/1.22.1", "+ Retrieved x-powered-by header: PHP/8.2", "+ The anti-clickjacking X-Frame-Options header is not present.", "+ The X-Content-Type-Options header is not set.", "+ No CGI Directories found", "+ /admin/: Admin login page found.", "+ /backup/: Directory indexing detected.", "+ /server-status: Server status interface discovered", "+ /config.bak: Backup file naming pattern", "+ 7915 requests completed", "+ 0 error(s) and 7 item(s) reported", ""]

    def sim_burpsuite(self, args):
        view = " ".join(args).lower()
        if "repeater" in view:
            return ["Burp Suite Professional", "[Repeater] Request #14", "POST /api/profile HTTP/1.1", "Host: demo.ops.local", "Cookie: session=eyJvcHMiOiJkZW1vIn0", "Content-Type: application/json", "", '{"role":"user","email":"operator@example.test"}', "", "[Send] Response received", "HTTP/1.1 200 OK", "Content-Length: 64", "", '{"status":"updated","role":"user","audit":"parameter accepted"}', ""]
        if "intruder" in view:
            return ["Burp Suite Professional", "[Intruder] Attack: sniper", "Target: http://demo.ops.local/login", "Payload positions: username=§admin§&password=§password§", "Payload count: 8", "#  Payload       Status Length Comment", "1  admin         401    1321   invalid", "2  operator      302    118    interesting redirect", "3  service       401    1321   invalid", "Attack finished: 1 interesting response", ""]
        return ["Burp Suite Professional", "Temporary project opened", "Proxy listener: 127.0.0.1:8080", "Dashboard: no live tasks", "Target site map:", "  http://demo.ops.local/", "  http://demo.ops.local/login", "  http://demo.ops.local/api/profile", "Proxy HTTP history:", "  GET  /                 200 text/html  1420", "  POST /login            302 text/html   118", "  GET  /dashboard        200 text/html  6120", "Tools: Target Proxy Repeater Intruder Decoder Comparer Logger", ""]

    def sim_wireshark(self, args):
        cap = args[0] if args else "lab-http.pcap"
        return [f"Wireshark - {cap}", "No.     Time        Source          Destination     Protocol Length Info", "1       0.000000    192.0.2.10      198.51.100.5    TCP      74     51514 -> 80 [SYN]", "2       0.000248    198.51.100.5    192.0.2.10      TCP      74     80 -> 51514 [SYN, ACK]", "3       0.000311    192.0.2.10      198.51.100.5    TCP      66     51514 -> 80 [ACK]", "4       0.014812    192.0.2.10      198.51.100.5    HTTP     450    GET /login HTTP/1.1", "5       0.018403    198.51.100.5    192.0.2.10      HTTP     1514   HTTP/1.1 200 OK", "Display filter: http || dns || tcp.analysis.flags", "Conversations: 2 TCP, 1 DNS", "Expert Info: 1 warning, 0 errors", "Follow TCP Stream: GET /login -> 200 OK", ""]

    def sim_tshark(self, args):
        return ["1 0.000000 192.0.2.10 -> 198.51.100.5 TCP 51514 > 80 [SYN]", "2 0.000248 198.51.100.5 -> 192.0.2.10 TCP 80 > 51514 [SYN, ACK]", "3 0.014812 192.0.2.10 -> 198.51.100.5 HTTP GET /login", "4 0.018403 198.51.100.5 -> 192.0.2.10 HTTP 200 OK", "5 0.101122 192.0.2.10 -> 203.0.113.53 DNS Standard query A demo.ops.local", "6 0.104901 203.0.113.53 -> 192.0.2.10 DNS Standard query response A 198.51.100.5", ""]

    def sim_sqlmap(self, args):
        target = self.sim_target(args)
        dbs = ["information_schema", "app", "users", self.mode['tag'].lower().replace(' ', '_')]
        return ["        ___", "       __H__", " ___ ___[.]_____ ___ ___  {1.8.2#stable}", "|_ -| . [(]     | .'| . |", "|___|_  [)]_|_|_|__,|  _|", "      |_|V...       |_|", "", f"[INFO] testing connection to the target URL: {target}", "[INFO] checking if the target is protected by WAF/IPS", "[INFO] testing parameter 'id'", "[INFO] GET parameter 'id' appears to be dynamic", "[INFO] heuristic test shows parameter might be injectable", "[INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'", "[INFO] testing 'UNION query NULL columns'", "[INFO] target appears to be injectable", "[INFO] back-end DBMS: PostgreSQL", "available databases [4]:"] + [f"[*] {d}" for d in dbs] + ["[INFO] fetching tables for database: app", "Database: app", "+----------+", "| users    |", "| sessions |", "| auditlog |", "+----------+", "[INFO] fetched data logged to console buffer", ""]

    def sim_hydra(self, args):
        target = self.sim_target(args)
        user = "admin"
        if "-l" in args:
            try: user = args[args.index("-l")+1]
            except Exception: pass
        lines = ["Hydra v9.5 (c) 2023 by van Hauser/THC", f"[DATA] target={target} login={user} task=16 service=ssh", "[DATA] max 16 tasks per 1 server, overall 16 tasks", "[STATUS] 64.00 tries/min, 64 tries in 00:01h, 512 to do", "[ATTEMPT] target 0 - login \"admin\" - pass \"admin\" - 1 of 512", "[ATTEMPT] target 0 - login \"admin\" - pass \"password\" - 2 of 512", "[WARNING] rate-limit detected, backing off", f"[22][ssh] host: {target}   login: {user}   password: {random.choice(self.mode['keys']).lower()}-{random.randint(100,999)}", "[STATUS] lockout window observed: 5 failures / 60 seconds", "[STATUS] valid pair stored in results buffer", "1 of 1 target successfully completed", ""]
        return lines

    def sim_john(self, args):
        return ["Using default input encoding: UTF-8", "Loaded 6 password hashes with 6 different salts", "Cost 1 (iteration count) is 5000 for all loaded hashes", "Will run 4 OpenMP threads", "Press 'q' or Ctrl-C to abort, almost any other key for status", f"{random.choice(self.mode['keys']).lower()}-{random.randint(1000,9999)}     (operator)", "3g 0:00:00:12 DONE 2/3 (2026-05-22) 0.244g/s 3120p/s", "Use --show to display cracked passwords reliably", ""]

    def sim_hashcat(self, args):
        return ["hashcat (v6.2.6) starting in autodetect mode", "OpenCL API: Portable Computing Language", "Hashes: 12 digests; 12 unique digests", "Dictionary cache built", "Status...........: Running", "Hash.Mode........: 0 (MD5)", "Speed.#1.........: 1842.7 kH/s", "Recovered........: 4/12 (33.33%)", "Progress.........: 425984/14344384 (2.97%)", "Restore.Point....: 212992/7172192", f"Candidate.Engine.: {random.choice(self.mode['keys']).lower()} -> {random.choice(CRACK_WORDS)}", "Rejected.........: 1024/425984 (0.24%)", "Hardware.Mon.#1..: Temp: 54c Util: 83%", "Started: Fri May 22 16:08:00 2026", "Stopped: Fri May 22 16:08:11 2026", "Status...........: Exhausted", ""]

    def sim_msfconsole(self, args):
        target = random.choice(SIM_TARGETS)
        return ["Metasploit Framework Console", "msf6 > search type:auxiliary scanner", "Matching Modules", "================", "  0  auxiliary/scanner/http/title", "  1  auxiliary/scanner/smb/smb_version", "msf6 > use auxiliary/scanner/http/title", f"msf6 auxiliary(scanner/http/title) > set RHOSTS {target}", "RHOSTS => " + target, "msf6 auxiliary(scanner/http/title) > run", f"[+] {target}:80 - Page title: Operations Login", "[*] Scanned 1 of 1 hosts (100% complete)", "[*] Auxiliary module execution completed", "msf6 > services", f"Services for {target}: 80/tcp http nginx", "msf6 > notes", "Notes: http-title Operations Login", "msf6 > sessions", "No active sessions.", ""]

    def sim_searchsploit(self, args):
        query = " ".join(args) or random.choice(self.mode["missions"])
        return [f"Exploit Title                                      |  Path", "--------------------------------------------------- ---------------------------------", f"{query} Auth Bypass                              | multiple/remote/50842.txt", f"{query} Information Disclosure                   | webapps/49213.txt", f"{query} Version Check Helper                      | linux/local/00002.txt", "Shellcodes: No Results", "Papers: No Results", ""]

    def sim_enum4linux(self, args):
        target = self.sim_target(args)
        return [f"Starting enum4linux v0.9.1 against {target}", "[+] Got OS info for target", "OS: Unix (Samba 4.17.5)", "[+] Enumerating shares", "Sharename       Type      Comment", "---------       ----      -------", "IPC$            IPC       IPC Service", "public          Disk      Public Files", "backups         Disk      Nightly Backups", "[+] Enumerating users", "S-1-22-1-1000 Unix User\\operator", "S-1-22-1-1001 Unix User\\service", "[+] Password policy: minimum length 10, lockout threshold 5", ""]

    def sim_smbclient(self, args):
        target = self.sim_target(args)
        return [f"Sharename       Type      Comment", "---------       ----      -------", "IPC$            IPC       IPC Service", "public          Disk      Public Files", "backups         Disk      Nightly Backups", f"Domain=[WORKGROUP] OS=[Unix] Server=[Samba 4.17.5] target=[{target}]", "smb: \\> ls", "  .                                   D        0  Fri May 22 15:00:00 2026", "  ..                                  D        0  Fri May 22 15:00:00 2026", "  notes.txt                           N      312  Fri May 22 14:52:00 2026", "  config.bak                          N     2048  Fri May 22 13:37:00 2026", ""]

    def sim_wpscan(self, args):
        target = self.sim_target(args)
        return [
            "WPScan v3.8.25",
            "_______________________________________________________________",
            "[+] URL: " + str(target),
            "[+] Started: Fri May 22 15:00:00 2026",
            "[+] Interesting Finding(s):",
            " | Headers",
            " |  - Server: nginx",
            " |  - X-Powered-By header is present",
            "[+] WordPress version 6.4 identified",
            "[+] Enumerating plugins",
            "[i] plugin: contact-form marker version 5.0",
            "[i] plugin: gallery marker version 2.1",
            "[+] Enumerating users",
            "[i] user: admin",
            "[i] user: editor",
            "[+] Finished",
            "",
        ]

    def sim_wifite(self, args):
        self.speak("wifite-capture", "wireless targets acquired")
        return [
            "   .               .    ",
            " .´  ·  .     .  ·  `.  wifite2 2.6.8",
            ":  :  :  (¯)  :  :  :  automated wireless auditor",
            " `.__·.__·.__·.__.´   ",
            "[+] scanning for wireless devices...",
            "[+] enabling monitor mode on wlan0mon",
            "[+] looking for targets...",
            "   NUM                      ESSID   CH  ENCR  PWR  WPS  CLIENT",
            "   1              NETGEAR-2G-LAB    6  WPA2   72db  yes  2",
            "   2                 HOTEL-OPS     11  WPA2   64db   no  4",
            "   3              CONSOLE-LAB       1  WPA2   58db  yes  1",
            "[+] target selected: CONSOLE-LAB (02:00:00:00:00:01)",
            "[+] starting handshake capture",
            "[+] listening for EAPOL frames",
            "[+] captured handshake: 02:00:00:00:00:01",
            "[+] launching offline key audit with wordlist.txt",
            f"[+] key found: {random.choice(self.mode['keys']).lower()}-{random.randint(1000,9999)}",
            "[+] disabling monitor mode",
            "[+] session complete",
            "",
        ]

    def sim_aircrack(self, args):
        return ["Opening capture.cap", "Read 15284 packets.", "   #  BSSID              ESSID                     Encryption", "   1  02:00:00:00:00:01  CONSOLE-LAB               WPA (1 handshake)", "Choosing first network as target.", "Opening wordlist wordlist.txt", "Aircrack-ng 1.7", "[00:00:12] 18432/14344384 keys tested (1512.00 k/s)", f"KEY FOUND! [ {random.choice(self.mode['keys']).lower()}-{random.randint(1000,9999)} ]", "Master Key     : 00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF", "Transcient Key : AA BB CC DD EE FF 00 11 22 33 44 55 66 77 88 99", "EAPOL HMAC     : 11 22 33 44 55 66 77 88 99 00 AA BB CC DD EE FF", ""]

    def start_game(self, game_type):
        self.game = {"type": game_type, "score": 0, "round": 0, "end": time.time() + 150, "answer": None, "snake": None, "adventure": None}
        self.busy = False
        self.speak(f"game-{game_type}", f"{game_type} operation started")
        if game_type == "cipher":
            self.run_lines(["[+] Cipher operation armed", "[+] Decode payloads before the window closes", "[+] Type the decoded word and press Enter", ""], final=self.next_cipher)
        elif game_type == "firewall":
            self.run_lines(["[+] Firewall operation armed", "[+] Type the displayed key exactly", ""], final=self.next_firewall)
        elif game_type == "breach":
            self.run_lines(["[+] Breach-route operation armed", "[+] Type the next node number to keep the route alive", ""], final=self.next_breach)
        elif game_type == "snake":
            self.game["snake"] = {"snake": [(5,5),(4,5),(3,5)], "food": (10,5), "dir": "d", "w": 18, "h": 10}
            self.run_lines(["[+] Snake payload armed", "[+] Use w/a/s/d then Enter to steer. Eat tokens. Avoid walls.", ""], final=self.draw_snake)
        elif game_type == "adventure":
            self.game["adventure"] = "start"
            self.run_lines(["[+] Branching operation armed", "[+] Choose numbered actions to drive the op", ""], final=self.next_adventure)
        else:
            self.start_mode_game()

    def game_time_left(self):
        if not self.game:
            return 0
        return max(0, int(self.game["end"] - time.time()))

    def end_game(self):
        score = self.game["score"] if self.game else 0
        self.game = None; self.busy = False
        self.run_lines([f"[+] Game complete. Score: {score}", ""], final=self.finish_response)

    def next_cipher(self):
        if not self.game or self.game_time_left() <= 0:
            self.end_game(); return
        word = random.choice(self.mode["keys"]).lower()
        shift = random.randint(1, 7)
        encoded = "".join(chr(((ord(ch) - 97 + shift) % 26) + 97) if ch.isalpha() else ch for ch in word)
        self.game.update({"answer": word, "round": self.game["round"] + 1})
        self.write(f"[CIPHER {self.game['round']}] shift=-{shift} payload={encoded} time={self.game_time_left()}s")

    def next_firewall(self):
        if not self.game or self.game_time_left() <= 0:
            self.end_game(); return
        key = "-".join(random.choice(self.mode["keys"]) for _ in range(2)) + f"-{random.randint(10,99)}"
        self.game.update({"answer": key.lower(), "round": self.game["round"] + 1})
        self.flash_message("FIREWALL SPIKE", 650)
        self.write(f"[FIREWALL {self.game['round']}] key={key} time={self.game_time_left()}s")

    def next_breach(self):
        if not self.game or self.game_time_left() <= 0:
            self.end_game(); return
        node = str(random.randint(0, 9))
        self.game.update({"answer": node, "round": self.game["round"] + 1})
        self.write(f"[BREACH {self.game['round']}] route node={node} time={self.game_time_left()}s")

    def draw_snake(self):
        if not self.game or not self.game.get("snake"):
            return
        st = self.game["snake"]
        snake = set(st["snake"]); food = st["food"]
        rows = []
        for y in range(st["h"]):
            row = []
            for x in range(st["w"]):
                if (x,y) == st["snake"][0]: row.append("@")
                elif (x,y) in snake: row.append("o")
                elif (x,y) == food: row.append("*")
                elif x in (0, st["w"]-1) or y in (0, st["h"]-1): row.append("#")
                else: row.append(" ")
            rows.append("".join(row))
        self.write("+" + "-"*st["w"] + "+")
        for r in rows: self.write("|" + r + "|")
        self.write("+" + "-"*st["w"] + f"+ score={self.game['score']}")

    def snake_step(self, move):
        st = self.game["snake"]
        dirs = {"w":(0,-1),"a":(-1,0),"s":(0,1),"d":(1,0)}
        if move in dirs: st["dir"] = move
        dx, dy = dirs[st["dir"]]
        hx, hy = st["snake"][0]
        head = (hx+dx, hy+dy)
        if head[0] <= 0 or head[0] >= st["w"]-1 or head[1] <= 0 or head[1] >= st["h"]-1 or head in st["snake"]:
            self.speak("snake-fail", "payload crashed")
            self.write("[-] payload crashed", "danger")
            self.end_game(); return
        st["snake"].insert(0, head)
        if head == st["food"]:
            self.game["score"] += 1
            self.speak("snake-token", "token captured")
            while True:
                f=(random.randint(1,st["w"]-2), random.randint(1,st["h"]-2))
                if f not in st["snake"]:
                    st["food"] = f; break
        else:
            st["snake"].pop()
        self.draw_snake()

    def next_adventure(self):
        state = self.game.get("adventure") if self.game else None
        scenes = {
            "start": ("You have shell on a jump box. Choose: 1 enumerate network, 2 inspect web root, 3 check creds", {"1":"net", "2":"web", "3":"creds"}),
            "net": ("Scan shows ssh/http/smb. Choose: 1 nmap scripts, 2 enum4linux, 3 pivot", {"1":"nmap", "2":"smb", "3":"pivot"}),
            "web": ("Web root has admin panel. Choose: 1 gobuster, 2 nikto, 3 sqlmap", {"1":"gob", "2":"nikto", "3":"sql"}),
            "creds": ("Cred cache found. Choose: 1 john, 2 hashcat, 3 hydra", {"1":"john", "2":"hashcat", "3":"hydra"}),
            "nmap": ("Script scan flags outdated service. Operation success.", {}),
            "smb": ("SMB backups reveal config archive. Operation success.", {}),
            "pivot": ("Pivot route established through proxy chain. Operation success.", {}),
            "gob": ("Hidden /ops-admin path discovered. Operation success.", {}),
            "nikto": ("Risky headers and backup path found. Operation success.", {}),
            "sql": ("Injectable id parameter confirmed. Operation success.", {}),
            "john": ("Hash recovered and reused against panel. Operation success.", {}),
            "hashcat": ("GPU audit recovers service token. Operation success.", {}),
            "hydra": ("Credential audit finds valid operator login. Operation success.", {}),
        }
        text, choices = scenes.get(state, scenes["start"])
        self.write("[ADVENTURE] " + text)
        if not choices:
            self.game["score"] += 3
            self.speak("adventure-success", "operation accomplished")
            self.end_game()

    def start_mode_game(self):
        mode = self.cfg.get("mode", "cyber")
        self.game["type"] = "modegame"
        self.game["answer"] = random.choice(self.mode["keys"]).lower()
        self.write(f"[+] {self.mode['label']} special operation armed")
        self.write(f"[+] Type authorization token: {self.game['answer'].upper()}")
        self.speak("modegame", f"{self.mode['label']} operation active")

    def handle_game_input(self, lower):
        if not self.game:
            return
        typ = self.game.get("type")
        if lower in ("quit", "exit", "stop"):
            self.end_game(); return
        if typ == "snake":
            self.snake_step(lower[:1] if lower else "")
            return
        if typ == "adventure":
            scenes = {
                "start": {"1":"net", "2":"web", "3":"creds"},
                "net": {"1":"nmap", "2":"smb", "3":"pivot"},
                "web": {"1":"gob", "2":"nikto", "3":"sql"},
                "creds": {"1":"john", "2":"hashcat", "3":"hydra"},
            }
            state = self.game.get("adventure")
            nxt = scenes.get(state, {}).get(lower)
            if not nxt:
                self.write("[-] invalid branch", "danger"); self.next_adventure(); return
            self.game["adventure"] = nxt
            self.next_adventure(); return
        if typ == "modegame":
            if lower == str(self.game.get("answer", "")).lower():
                self.game["score"] += 5
                self.speak("modegame-success", "mission accomplished")
                self.write("[+] authorization accepted", "accent")
                self.end_game()
            else:
                self.write("[-] token rejected", "danger")
            return
        if self.game_time_left() <= 0:
            self.end_game(); return
        if lower == str(self.game.get("answer", "")).lower():
            self.game["score"] += 1
            self.write(f"[+] hit score={self.game['score']}", "accent")
            self.speak(f"{typ}-hit", "confirmed")
            self.flash_message("HIT", 450)
        else:
            self.write(f"[-] miss expected={self.game.get('answer')}", "danger")
        if typ == "cipher": self.next_cipher()
        elif typ == "firewall": self.next_firewall()
        else: self.next_breach()

    def ensure_music(self):
        mode = self.cfg.get("mode", "cyber")
        fname = MUSIC_FILES.get(mode)
        src = SOURCE_ASSET_DIR / "music" / fname if fname else None
        if src and src.exists():
            return src
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        path = DATA_DIR / f"audio-{mode}.wav"
        if path.exists():
            return path
        profile = MODES[mode]["sound"]
        framerate = 22050
        duration = 18
        volume = 0.15
        base, lead = profile["base"], profile["lead"]
        pulse, noise, tempo = profile["pulse"], profile["noise"], profile["tempo"]
        frames = []
        rng = random.Random(mode)
        for i in range(framerate * duration):
            t = i / framerate
            beat = 1.0 if int(t * tempo) % 4 in (0, 1) else 0.55
            sweep = math.sin(2 * math.pi * (lead + math.sin(t * 1.7) * 12) * t) * 0.18
            drone = math.sin(2 * math.pi * base * t) * 0.45
            sub = math.sin(2 * math.pi * (base / 2) * t) * 0.22
            tick = math.sin(2 * math.pi * 900 * t) * 0.35 if (t * tempo) % 1.0 < 0.035 else 0.0
            hiss = (rng.random() * 2 - 1) * noise
            sample = (drone + sub + sweep + tick + hiss) * (0.65 + pulse * beat)
            val = int(max(-32767, min(32767, sample * 32767 * volume)))
            frames.append(struct.pack("<h", val))
        with wave.open(str(path), "wb") as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(framerate); wf.writeframes(b"".join(frames))
        return path


    def ensure_voice(self, key, text, base=180):
        lowered = (key + " " + text).lower()
        if "counter" in lowered or "trace" in lowered:
            name = VOICE_FILES["counter"]
        elif "mission" in lowered or "success" in lowered or "complete" in lowered or "accomplished" in lowered:
            name = VOICE_FILES["success"]
        elif "hit" in lowered or "objective" in lowered or "confirmed" in lowered:
            name = VOICE_FILES["hit"]
        elif "stealth" in lowered or "wifite" in lowered or "tool" in lowered:
            name = VOICE_FILES["stealth"]
        elif "optimal" in lowered:
            name = VOICE_FILES["optimal"]
        else:
            name = VOICE_FILES["game"]
        src = SOURCE_ASSET_DIR / "voice" / name
        if src.exists():
            return src
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        safe = "".join(ch.lower() if ch.isalnum() else "-" for ch in key).strip("-") or "voice"
        path = DATA_DIR / f"voice-{safe}.wav"
        if path.exists():
            return path
        framerate = 22050
        frames = []
        rng = random.Random(safe)
        duration = 1.4
        for i in range(int(framerate * duration)):
            t = i / framerate
            env = min(1.0, t * 8) * min(1.0, (duration - t) * 8)
            carrier = math.sin(2 * math.pi * (base + math.sin(t * 5) * 18) * t) * 0.42
            buzz = math.sin(2 * math.pi * (base * 2.01) * t) * 0.20
            noise = (rng.random() * 2 - 1) * 0.05
            sample = (carrier + buzz + noise) * env * 0.22
            frames.append(struct.pack("<h", int(max(-32767, min(32767, sample * 32767)))))
        with wave.open(str(path), "wb") as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(framerate); wf.writeframes(b"".join(frames))
        return path


    def audio_cmd(self, path):
        vol = max(0.0, min(1.0, self.volume / 100.0))
        if shutil.which("ffplay"):
            return ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", "-volume", str(int(self.volume)), str(path)]
        if shutil.which("paplay"):
            return ["paplay", "--volume", str(int(65536 * vol)), str(path)]
        if shutil.which("aplay"):
            return ["aplay", "-q", str(path)]
        return None

    def set_volume(self, value):
        self.volume = max(0, min(100, int(value)))
        self.cfg["volume"] = self.volume
        save_config(self.cfg)
        self.flash_message(f"VOLUME {self.volume}%", 550)
        if self.music_proc and self.music_proc.poll() is None:
            self.start_music(restart=True)

    def adjust_volume(self, delta):
        self.set_volume(self.volume + delta)

    def speak(self, key, text):
        if not self.cfg.get("music", True):
            return
        self.stop_voice()
        base = {"cyber":180,"office":205,"adult":165}.get(self.cfg.get("mode"), 180)
        path = self.ensure_voice(key, text, base)
        cmd = self.audio_cmd(path)
        if cmd:
            try:
                self.voice_proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                self.voice_proc = None

    def stop_voice(self):
        try:
            if self.voice_proc and self.voice_proc.poll() is None:
                self.voice_proc.terminate()
                try:
                    self.voice_proc.wait(timeout=0.35)
                except Exception:
                    self.voice_proc.kill()
        except Exception:
            pass
        self.voice_proc = None

    def music_loop(self, cmd):
        while self.music_alive:
            try:
                self.music_proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.music_proc.wait()
            except Exception:
                break
            if not self.music_alive:
                break

    def stop_music(self):
        self.music_alive = False
        try:
            if self.music_proc and self.music_proc.poll() is None:
                self.music_proc.terminate()
                try:
                    self.music_proc.wait(timeout=0.35)
                except Exception:
                    self.music_proc.kill()
        except Exception:
            pass
        self.music_proc = None; self.music_mode = None

    def start_music(self, restart=False):
        if not self.music_enabled or not self.cfg.get("music", True):
            return
        if self.music_proc and not restart and self.music_mode == self.cfg.get("mode"):
            return
        if restart:
            self.stop_music()
        self.music_alive = True
        music = self.ensure_music()
        cmd = self.audio_cmd(music)
        if cmd:
            self.music_mode = self.cfg.get("mode")
            threading.Thread(target=self.music_loop, args=(cmd,), daemon=True).start()


def main():
    parser = argparse.ArgumentParser(description="Hacker Game")
    parser.add_argument("--name")
    parser.add_argument("--theme", choices=sorted(THEMES))
    parser.add_argument("--mode", choices=sorted(MODES))
    parser.add_argument("--no-music", action="store_true")
    parser.add_argument("--windowed", action="store_true")
    args = parser.parse_args()
    cfg = load_config(args)
    save_config(cfg)
    root = tk.Tk()
    App(root, cfg)
    root.mainloop()


if __name__ == "__main__":
    main()
