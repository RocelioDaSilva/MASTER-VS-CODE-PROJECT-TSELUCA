# News Monitoring Setup - Real-Time Intelligence Hub

> Track Angola oil & gas developments, operator announcements, and career opportunities using Google Alerts, RSS feeds, and automated daily digests.

---

## Quick Start

### 1. Set Up Google Alerts (5 minutes)

Go to [Google Alerts](https://www.google.com/alerts) and create alerts for these search terms. Set delivery to **RSS feed** (not email).

| Alert Query | Why |
|------------|-----|
| `"Angola" "oil and gas"` | General Angola O&G news |
| `"TotalEnergies" "Angola"` | Largest operator - Block 17, 32 |
| `"Chevron" "Angola" OR "CABGOC"` | Block 0, 14 operator |
| `"Eni" "Angola"` | Block 15/06 operator |
| `"Azule Energy"` | bp/[Eni](../data/company-directory/eni.md) JV - major Angola presence |
| `"Sonangol"` | National oil company |
| `"ANPG" "Angola"` | Regulator - licensing, local content |
| `"SLB" OR "[Schlumberger](../data/company-directory/slb.md)" Angola` | Largest service company |
| `"FPSO" "Angola"` | [FPSO](../docs/glossary.md) deployments, contracts |
| `"subsea" "Angola" OR "West Africa"` | Subsea projects, SURF contracts |
| `"petroleum engineer" hiring Angola` | Job opportunities |
| `"offshore jobs" Angola` | Broader job search |
| `"oil price" "Angola"` | Market impact on Angola operations |
| `"deepwater" "Namibia" OR "Angola"` | Frontier exploration (Namibia is booming) |

### 2. Save RSS Feed URLs

After creating each alert, copy the RSS feed URL. Google Alerts RSS URLs look like:
```
https://www.google.com/alerts/feeds/XXXXXXXX/YYYYYYYY
```

Paste all URLs into `alert_feeds.txt` (one per line) in the `automation/` folder.

### 3. Run the Daily Digest Script

```bash
# Install dependencies
pip install -r requirements.txt

# Run manually
python automation/fetch_alerts.py

# Or use the Windows batch file
automation\run_daily.bat
```

This creates a daily markdown digest in `news/YYYY/MM/YYYY-MM-DD.md`.

### 4. (Optional) Set Up GitHub Actions for Automated Daily Runs

If hosting on GitHub, the workflow at `.github/workflows/fetch_news.yml` runs the script daily at 07:00 UTC and commits new digests automatically.

---

## Directory Structure

```
â”œâ”€â”€ automation/
â”‚   â”œâ”€â”€ alert_feeds.txt                # Your Google Alerts RSS URLs (one per line)
â”‚   â”œâ”€â”€ fetch_alerts.py                # Main script - fetches RSS, generates digest
â”‚   â”œâ”€â”€ requirements.txt               # Dependencies for automation scripts
â”‚   â”œâ”€â”€ run_daily.bat                  # Windows scheduled task launcher
â”‚   â””â”€â”€ NEWS_MONITORING_SETUP.md       # This file
â”œâ”€â”€ news/                              # Auto-generated daily digests
â”‚   â””â”€â”€ 2026/
â”‚       â””â”€â”€ 04/
â”‚           â”œâ”€â”€ 2026-04-14.md
â”‚           â””â”€â”€ 2026-04-15.md
â””â”€â”€ .github/
    â””â”€â”€ workflows/
        â””â”€â”€ fetch_news.yml             # GitHub Actions daily workflow
```

---

## How It Works

1. **Google Alerts** monitors the web for your specified search queries.
2. **RSS feeds** deliver new results in a machine-readable format.
3. **`fetch_alerts.py`** reads all RSS URLs from `alert_feeds.txt`, fetches new entries, deduplicates, and writes a daily markdown summary.
4. **Caching**: The script keeps a `news/.seen_entries.json` file to avoid duplicating entries across runs.
5. **Output**: Each day gets a single `.md` file with all new items organized by source alert.

---

## Customization

### Adding More Feeds

Add any RSS feed URL to `alert_feeds.txt` - not just Google Alerts. For example:

```
# Google Alerts
https://www.google.com/alerts/feeds/...

# Rigzone Angola news
https://www.rigzone.com/news/rss/country_angola.aspx

# Upstream Online
https://www.upstreamonline.com/rss

# OilPrice.com
https://oilprice.com/rss/main
```

### Changing the Schedule

**Windows Task Scheduler:**
1. Open Task Scheduler â†’ Create Basic Task
2. Trigger: Daily at 07:00
3. Action: Start a Program â†’ `automation\run_daily.bat`
4. Working directory: this repository root

**GitHub Actions:** Edit `.github/workflows/fetch_news.yml` and change the cron schedule.

---

## Recommended Alert Categories

### Must-Have (Angola Job Seeker)
- Angola operator news ([TotalEnergies](../data/company-directory/totalenergies.md), Chevron, Eni, Azule, Sonangol)
- ANPG licensing rounds and local content updates
- Angola [FPSO](../docs/glossary.md) contracts and deployments
- Offshore jobs Angola

### Nice-to-Have (Industry Awareness)
- Oil price movements
- Deepwater exploration (Namibia, Guyana, Brazil)
- Service company earnings ([SLB](../data/company-directory/slb.md), [Halliburton](../data/company-directory/halliburton.md), [Baker Hughes](../data/company-directory/bakerhughes.md))
- Energy transition news (CCS, geothermal, hydrogen)

### Career Intelligence
- "Graduate program" oil gas 2026
- SPE conference announcements
- Petroleum engineering scholarships

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No entries in digest | Check that `alert_feeds.txt` has valid RSS URLs. Test URLs in a browser. |
| Google Alerts not generating RSS | Make sure you selected "RSS feed" (not email) when creating the alert. |
| Script fails with SSL error | Try: `pip install --upgrade certifi` |
| Duplicate entries appearing | Delete `news/.seen_entries.json` to reset cache, then re-run. |
| UTF-8 encoding issues | The script uses UTF-8 by default. Check your terminal encoding. |

---

*Last updated: April 2026*


