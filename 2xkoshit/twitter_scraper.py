"""
2XKO Twitter/X Scraper
Logs into X with your credentials and searches for posts about
Ekko/Ahri and Ekko/Illaoi, then appends results to the markdown file.

Usage:
    python twitter_scraper.py               # Search both pairings
    python twitter_scraper.py --no-update   # Print results only, don't edit the .md file
    python twitter_scraper.py --headed      # Show the browser window (default: headless)

Requirements:
    pip install playwright python-dotenv
    playwright install chromium
"""

import argparse
import os
import re
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# ── Config ────────────────────────────────────────────────────────────────────

BASE_DIR     = Path(__file__).parent
ENV_PATH     = BASE_DIR / ".env"
MD_FILE      = BASE_DIR / "2XKO_YouTube_Videos_2026.md"
MAX_POSTS    = 15  # Maximum posts to collect per search query

SEARCHES = [
    {
        "label":   "AHRI & EKKO",
        "query":   "2xko ekko ahri",
        "url":     "https://x.com/search?q=2xko+ekko+ahri&f=live&src=typed_query",
        "section": "## TWITTER/X — AHRI & EKKO (Live Results)",
    },
    {
        "label":   "EKKO & ILLAOI",
        "query":   "2xko ekko illaoi",
        "url":     "https://x.com/search?q=2xko+ekko+illaoi&f=live&src=typed_query",
        "section": "## TWITTER/X — EKKO & ILLAOI (Live Results)",
    },
]

# ── Login ─────────────────────────────────────────────────────────────────────

def login(page, username: str, password: str) -> None:
    """Log into X. Raises RuntimeError if login fails."""
    print("[*] Navigating to x.com login …")
    page.goto("https://x.com/i/flow/login", wait_until="domcontentloaded")

    # Username / email step
    page.wait_for_selector('input[autocomplete="username"]', timeout=15_000)
    page.fill('input[autocomplete="username"]', username)
    page.keyboard.press("Enter")

    # X sometimes shows a verification step (unusual activity) — handle it
    try:
        verify_input = page.wait_for_selector(
            'input[data-testid="ocfEnterTextTextInput"]', timeout=5_000
        )
        print("[!] X is asking for a verification (phone/email). "
              "Enter the value in the browser window, then press Enter here to continue.")
        input("Press Enter after you have completed the X verification …")
    except PlaywrightTimeout:
        pass  # No extra verification needed

    # Password step
    page.wait_for_selector('input[name="password"]', timeout=15_000)
    page.fill('input[name="password"]', password)
    page.keyboard.press("Enter")

    # Confirm we reached the home feed
    try:
        page.wait_for_url("https://x.com/home", timeout=20_000)
    except PlaywrightTimeout:
        # Sometimes redirects to a slightly different URL — just check for the nav
        page.wait_for_selector('[data-testid="primaryColumn"]', timeout=10_000)

    print("[+] Logged in successfully.")


# ── Scraping ──────────────────────────────────────────────────────────────────

def scrape_posts(page, search_url: str, label: str, max_posts: int) -> list[dict]:
    """Navigate to a search URL and collect posts."""
    print(f"[*] Searching: {label} …")
    page.goto(search_url, wait_until="domcontentloaded")

    # Wait for the first tweet to appear
    try:
        page.wait_for_selector('[data-testid="tweet"]', timeout=20_000)
    except PlaywrightTimeout:
        print(f"[!] No posts loaded for '{label}'. Skipping.")
        return []

    posts = []
    seen_urls: set[str] = set()

    scroll_attempts = 0
    max_scroll_attempts = 10

    while len(posts) < max_posts and scroll_attempts < max_scroll_attempts:
        tweet_elements = page.query_selector_all('[data-testid="tweet"]')

        for tweet_el in tweet_elements:
            if len(posts) >= max_posts:
                break

            try:
                # ── Text ──────────────────────────────────────────────────────
                text_el = tweet_el.query_selector('[data-testid="tweetText"]')
                text = text_el.inner_text().strip().replace("\n", " ") if text_el else "(no text)"
                # Truncate long posts
                if len(text) > 120:
                    text = text[:117] + "…"

                # ── Author ────────────────────────────────────────────────────
                user_el = tweet_el.query_selector('[data-testid="User-Name"]')
                author = user_el.inner_text().split("\n")[0].strip() if user_el else "Unknown"

                # ── URL ───────────────────────────────────────────────────────
                link_els = tweet_el.query_selector_all('a[href*="/status/"]')
                tweet_url = ""
                for link_el in link_els:
                    href = link_el.get_attribute("href") or ""
                    if "/status/" in href:
                        # Normalise to full URL
                        if href.startswith("/"):
                            href = "https://x.com" + href
                        # Remove query params
                        tweet_url = href.split("?")[0]
                        break

                if not tweet_url or tweet_url in seen_urls:
                    continue
                seen_urls.add(tweet_url)

                # ── Likes / Reposts ───────────────────────────────────────────
                likes = _get_metric(tweet_el, "like")
                reposts = _get_metric(tweet_el, "retweet")

                # ── Date ─────────────────────────────────────────────────────
                time_el = tweet_el.query_selector("time")
                date_str = time_el.get_attribute("datetime")[:10] if time_el else "—"

                posts.append({
                    "date":    date_str,
                    "author":  author,
                    "text":    text,
                    "likes":   likes,
                    "reposts": reposts,
                    "url":     tweet_url,
                })

            except Exception:
                # Skip malformed tweet elements silently
                continue

        # Scroll down to load more
        page.evaluate("window.scrollBy(0, 1500)")
        time.sleep(2)
        scroll_attempts += 1

    print(f"[+] Collected {len(posts)} posts for '{label}'.")
    return posts


def _get_metric(tweet_el, metric_name: str) -> str:
    """Return like or retweet count from a tweet element, e.g. '1.2K'."""
    el = tweet_el.query_selector(f'[data-testid="{metric_name}"]')
    if not el:
        return "—"
    text = el.inner_text().strip()
    return text if text else "—"


# ── Markdown formatting ───────────────────────────────────────────────────────

def posts_to_markdown(posts: list[dict], section_header: str, query: str) -> str:
    """Format a list of posts as a markdown section."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "",
        "---",
        "",
        section_header,
        "",
        f"> Search query: `{query}` | Scraped: {now}",
        "",
        "| Date | Author | Post | Likes | Reposts | URL |",
        "|------|--------|------|-------|---------|-----|",
    ]
    for p in posts:
        # Escape pipes inside cells
        text    = p["text"].replace("|", "\\|")
        author  = p["author"].replace("|", "\\|")
        lines.append(
            f"| {p['date']} | {author} | {text} | {p['likes']} | {p['reposts']} | {p['url']} |"
        )
    lines.append("")
    return "\n".join(lines)


# ── Markdown file update ──────────────────────────────────────────────────────

# Markers that bracket the auto-generated Twitter sections in the .md file
_BLOCK_START = "<!-- TWITTER_SCRAPER_START -->"
_BLOCK_END   = "<!-- TWITTER_SCRAPER_END -->"


def update_markdown_file(md_path: Path, all_sections: list[str]) -> None:
    """Insert or replace the scraped Twitter sections in the markdown file."""
    content = md_path.read_text(encoding="utf-8")
    new_block = (
        f"{_BLOCK_START}\n"
        + "\n".join(all_sections)
        + f"\n{_BLOCK_END}"
    )

    if _BLOCK_START in content and _BLOCK_END in content:
        # Replace existing block
        pattern = re.compile(
            re.escape(_BLOCK_START) + r".*?" + re.escape(_BLOCK_END),
            re.DOTALL,
        )
        content = pattern.sub(new_block, content)
        print("[+] Replaced existing Twitter block in the markdown file.")
    else:
        # Append before the Notes section, or at the end if not found
        notes_marker = "\n## Notes\n"
        if notes_marker in content:
            content = content.replace(notes_marker, f"\n{new_block}\n{notes_marker}")
            print("[+] Inserted Twitter block before the Notes section.")
        else:
            content += f"\n{new_block}\n"
            print("[+] Appended Twitter block at the end of the markdown file.")

    md_path.write_text(content, encoding="utf-8")


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape X/Twitter for 2XKO posts.")
    parser.add_argument("--no-update", action="store_true",
                        help="Print results only, do not modify the markdown file.")
    parser.add_argument("--headed", action="store_true",
                        help="Show the browser window (useful for debugging or 2FA).")
    args = parser.parse_args()

    # Load credentials from .env
    load_dotenv(ENV_PATH)
    username = os.getenv("TWITTER_USERNAME", "").strip()
    password = os.getenv("TWITTER_PASSWORD", "").strip()

    if not username or not password:
        raise SystemExit(
            "[ERROR] TWITTER_USERNAME and TWITTER_PASSWORD must be set in the .env file."
        )

    all_sections: list[str] = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not args.headed)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 900},
        )
        page = context.new_page()

        login(page, username, password)

        for search in SEARCHES:
            posts = scrape_posts(page, search["url"], search["label"], MAX_POSTS)
            md_section = posts_to_markdown(posts, search["section"], search["query"])
            all_sections.append(md_section)

            # Print to console regardless
            print(md_section)

        browser.close()

    if not args.no_update:
        update_markdown_file(MD_FILE, all_sections)
        print(f"\n[+] '{MD_FILE.name}' updated.")
    else:
        print("\n[--no-update] Markdown file was NOT modified.")


if __name__ == "__main__":
    main()
