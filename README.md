# Bing Wallpaper for macOS

A tiny daily Bing wallpaper updater for macOS (Apple Silicon & Intel).

- **Zero pip dependencies** — runs on the system `/usr/bin/python3`
  (standard library only: `urllib`, `json`, `hashlib`, `subprocess`).
- **Native scheduling** with `launchd` (a `LaunchAgent`).
- **Catch-up on wake**: if the Mac is asleep at the scheduled time,
  launchd fires the job the moment the system wakes — you never miss a day.
- **Native wallpaper API** via `osascript` / AppleScript
  (`tell application "System Events" to tell every desktop to set picture to ...`).
- **Native notifications** via `osascript` `display notification`.
- Negligible footprint: no resident process, just a one-shot script
  the kernel wakes at most once per day.

## Files

| File | Purpose |
| --- | --- |
| `main.py` | Fetch image from Bing and set it as the desktop wallpaper. |
| `RUNME.sh` | Wrapper that reads `config.yml` and runs `main.py` with system Python. |
| `config.yml` | `path`, `mode`, daily `hour`/`minute`. |
| `com.user.bingwallpaper.plist` | LaunchAgent template. |
| `install.sh` | Render the template and load it into `launchd`. |
| `uninstall.sh` | Unload and delete the LaunchAgent. |

## Setup

1. Edit `config.yml` and set `path` to this folder’s absolute path,
   plus your preferred daily run time:

   ```yaml
   path: /Users/yourname/Projects/BingWallpaper-Ubuntu
   mode: 0       # 0 = today, 1 = yesterday, ...
   hour: 9
   minute: 0
   ```

2. Make the scripts executable and install the LaunchAgent:

   ```bash
   chmod +x RUNME.sh install.sh uninstall.sh
   ./install.sh
   ```

   This writes `~/Library/LaunchAgents/com.user.bingwallpaper.plist`
   and registers it with `launchctl`.

3. (Optional) Trigger an update right now:

   ```bash
   launchctl start com.user.bingwallpaper
   # or, without launchd:
   ./RUNME.sh
   ```

The first run will ask macOS for permission to send notifications — accept
it once and future runs are silent except for the toast.

## How the “catch up after wake” behavior works

`launchd`’s `StartCalendarInterval` is documented to run a job at the
**next opportunity** if the system is asleep, shut down or otherwise
unavailable at the scheduled time. We also set `RunAtLoad`, so the job
runs once shortly after login as a second safety net. The script itself
calls a small `wait_for_network()` loop before hitting Bing, which avoids
spurious failures when launchd fires the job immediately on wake while
Wi-Fi is still associating.

## Uninstall

```bash
./uninstall.sh
```

## Inspect / debug

```bash
launchctl list | grep bingwallpaper
tail -f picture/launchd.out.log picture/launchd.err.log
```
