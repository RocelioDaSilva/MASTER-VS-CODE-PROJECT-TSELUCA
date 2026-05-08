"""
2XKO Video Downloader — Ekko/Ahri & Ekko/Illaoi
================================================
Uses yt-dlp to download all tracked videos from the .md reference file
plus newly discovered content from YouTube search results.

Usage:
    python download_videos.py                   # Download everything (best quality)
    python download_videos.py --list            # Print URLs only (no download)
    python download_videos.py --folder ahri     # Download Ahri/Ekko folder only
    python download_videos.py --folder illaoi   # Download Ekko/Illaoi folder only
    python download_videos.py --folder shorts   # Download Shorts only
    python download_videos.py --folder tournament  # Download tournament VODs only
    python download_videos.py --quality 720     # Cap at 720p (default: best)
    python download_videos.py --audio-only      # Download audio only (mp3)
    python download_videos.py --update          # Re-fetch titles and update this file
"""

import argparse
import os
import sys

# ──────────────────────────────────────────────────────────────────────────────
# VIDEO LIBRARY
# Each entry: (url, title, folder)
#   folder: "ahri" | "illaoi" | "shorts" | "tournament"
# ──────────────────────────────────────────────────────────────────────────────

VIDEOS = {
    # ──────────────── FOLDER 1: AHRI & EKKO ────────────────────────────────
    "ahri": [
        # From .md — verified existing
        ("https://www.youtube.com/watch?v=mR92xVB7sT0",  "INZEM (Ahri-Ekko) vs SONICFOX (Ahri-Ekko) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=_AKzl5wkh7M",  "EKKO/AHRI Freestyle 1001 Damage Combo"),
        ("https://www.youtube.com/watch?v=viPd6RAbErE",  "SonicFox+INZEM (Ahri/Caitlyn) vs Semiij (Ekko/Ahri) ▰ High Level"),
        ("https://www.youtube.com/watch?v=ULOCNbs9lac",  "SONICFOX-INZEM (Ahri-Caitlyn) vs SEMIIJ (Ahri-Ekko) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=V6cmPTOJZMA",  "Ekko/Ahri 1125 Damage Freestyle Combo"),
        ("https://www.youtube.com/watch?v=Dq01cpMF90E",  "Sonicfox (Ahri/Ekko) vs Inzem (Ahri/Ekko) ▰ High Level"),
        ("https://www.youtube.com/watch?v=wzBHrZxq91Y",  "Hikari (Vi/Ahri) vs SoulDemonXL (Ekko/Ahri) ▰ High Level"),
        ("https://www.youtube.com/watch?v=SvNRx3-sLB8",  "SONICFOX (Ekko-Ahri) vs HIKARI (Yasuo-Illaoi) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=U1XUUo-L5w4",  "CAT GIRL ILLAOI (Akali-Ahri) vs SOULDEMONXL (Ekko-Ahri) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=rEtzvwJIaus",  "Ahri + Ekko Freestyle Combo Bible (31 min)"),
        # Newly discovered from YouTube search
        ("https://www.youtube.com/watch?v=kwxTRnX278s",  "Supernoon (Teemo/Ekko) vs Squrrei (Ekko/Ahri)"),
        ("https://www.youtube.com/watch?v=dPSjfMGJtEI",  "SoulDemonXL (Ahri/Ekko) vs Ronnichu (Ahri/Yasuo) ▰ High Level"),
        ("https://www.youtube.com/watch?v=ql4QCGAljok",  "SonicFox+INZEM (Ahri/Teemo) vs SoulDemonXL (Ekko/Ahri) ▰ High Level"),
        ("https://www.youtube.com/watch?v=F-7ltfKXpOE",  "JANEMBA (Ekko-Illaoi) vs WAWA (Ekko-Ahri) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=CKY4fDAotwU",  "MAZA (Yasuo-Ekko) vs INZEM (Ahri-Ekko) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=Zd7z7y2WXDo",  "Sonicfox+Inzem (Ahri/Caitlyn) vs Semiij (Ekko/Ahri) ▰ High Level"),
        ("https://www.youtube.com/watch?v=sUtgCfv9fCI",  "WADE (Ekko-Warwick) vs VERSO (Ahri-Ekko) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=pIZWPtY6njY",  "SEMIIJ (Ahri-Ekko) vs WINDZERO7 (Darius-Blitzcrank) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=CEUOj-k1AkU",  "DRX POKA (Ahri-Ekko) vs DOROPON (Ekko-Warwick) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=JT95uQx1wnA",  "2XKO Ahri Ekko Combo Guide"),
        ("https://www.youtube.com/watch?v=tXcxROQwjHQ",  "Verso (Ahri/Ekko) vs Shine (Blitzcrank/Ahri) ▰ High Level"),
        ("https://www.youtube.com/watch?v=r9PD237w6pM",  "HIKARI (Yasuo-Ahri) vs SOULDEMONXL (Ahri-Ekko) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=TmH5-C6oatE",  "EYECONIC (Teemo-Caitlyn) vs LUNOVUNE (Ahri-Ekko) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=8iu5bY6mQRc",  "TOMICHI (Ekko-Ahri) vs LEV TRINKI76 (Vi-Ekko) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=xyK3lFtz2H8",  "2XKO Ahri Ekko gameplay"),
    ],

    # ──────────────── FOLDER 2: EKKO & ILLAOI ───────────────────────────────
    "illaoi": [
        # From .md — verified existing
        ("https://www.youtube.com/watch?v=LcWLcPi8qZw",  "HIKARI (Yasuo-Ekko) vs BLEED (Ekko-Illaoi) ▰ Pro Replays [Jan]"),
        ("https://www.youtube.com/watch?v=wAjssNcuk0g",  "CLOUD805 (Yasuo-Ekko) vs BLEED (Ekko-Illaoi) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=h5fDR7Slx1M",  "JAKEYTHESNAKEY (Jinx-Ekko) vs BLEED (Ekko-Illaoi) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=o6HA7Dt9biU",  "FILIPINO CHAMP (Jinx-Illaoi) vs BLEED (Ekko-Illaoi) ▰ Pro Replays"),
        # Newly discovered from YouTube search
        ("https://www.youtube.com/watch?v=-ix_hLPjilo",  "LIGHTWHISP (Braum-Darius) vs PINKPINK (Ekko-Illaoi) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=fQ70gdiUK48",  "2XKO Ekko/Illaoi combo (2X Assist)"),
        ("https://www.youtube.com/watch?v=6MPEAYZdgmE",  "BLEED (Ekko-Illaoi) vs BLAIZZY (Vi-Ahri) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=sBI28VTXoh4",  "LEFFEN (Ekko-Warwick) vs HEAPSKI (Illaoi-Ekko) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=QOpIEa46iIc",  "HIKARI (Yasuo-Vi) vs SONICFOX (Ekko-Illaoi) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=3I_61M0m_bI",  "HIKARI (Yasuo-Ekko) vs BLEED (Ekko-Illaoi) ▰ Pro Replays [Feb]"),
        ("https://www.youtube.com/watch?v=pZ06O0uwHn0",  "BLEED (Ekko-Illaoi) vs LOOKEWARM (Vi-Ahri) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=uLjG-8KWDvQ",  "BLEED (Ekko-Illaoi) vs JORDANA (Yasuo-Teemo) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=Y4_ROL8VEsY",  "Wade (Ekko-Illaoi) vs NOKA (Ekko-Vi) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=QFHA97y2UFo",  "BLEED (Ekko-Illaoi) vs MAZE (Ekko-Illaoi) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=Qcv9P49Zhg0",  "TAPION (Ekko-Illaoi) vs BENIMARU (Darius-Ahri) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=gRoSGFbEOa0",  "DINGUSPUNCH (Vi-Blitzcrank) vs BLEED (Ekko-Illaoi) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=qhfo-TWEMjg",  "Inzem (Teemo/Ekko) vs Pinkpinkpinkpink (Illaoi/Ekko) ▰ High Level"),
        ("https://www.youtube.com/watch?v=RKq9Dhslg84",  "JAMES06 (Yasuo-Ekko) vs BLEED (Ekko-Illaoi) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=oRqBpT22VlU",  "NOKA (Vi-Ekko) vs WADE (Ekko-Illaoi) ▰ Pro Replays"),
        ("https://www.youtube.com/watch?v=DQinu2erA5k",  "Bleed (Illaoi/Ekko) vs Quainty (Yasuo/Blitzcrank) ▰ High Level"),
    ],

    # ──────────────── SHORTS ────────────────────────────────────────────────
    "shorts": [
        # Ahri/Ekko Shorts
        ("https://www.youtube.com/shorts/iAXPaB8nK7w",  "Learn These Ahri/Ekko Mixups in 2XKO!"),
        ("https://www.youtube.com/shorts/Ssc5-eS1H0Q",  "Ahri + Ekko BIG DAMAGE COMBO | 2XKO"),
        ("https://www.youtube.com/shorts/BHQDQG0MlMs",  "737% Ekko & Ahri Combo | #2xko"),
        # Ekko/Illaoi Shorts
        ("https://www.youtube.com/shorts/qH23kinR9MI",  "Ekko & Illaoi Tag Combo #2xko #fgc"),
        ("https://www.youtube.com/shorts/Lrrnf-GNkw4",  "Ekko corner combo meterless tag launch end #2xko #ekko #illaoi"),
        # New Shorts from search
        ("https://www.youtube.com/shorts/ttj2YSbEa4g",  "Most Difficult Character in 2XKO?"),
        ("https://www.youtube.com/shorts/GkWsUaR9s18",  "Rating Ahri Level 3 Super in 2XKO"),
        ("https://www.youtube.com/shorts/UafiV9Dy4DU",  "#2XKO Ahri Evens it Up Setting Up a Final Showdown w/ Vi!"),
    ],

    # ──────────────── TOURNAMENT VODS ───────────────────────────────────────
    "tournament": [
        # Frosty Faustings 2026 — First Major
        ("https://www.youtube.com/watch?v=uUjWahkss4k",  "Frosty Faustings 2026 — Top 8 Full VOD (7h)"),
        ("https://www.youtube.com/watch?v=OZTPUx8ZDBQ",  "Frosty Faustings 2026 — Official Recap"),
        # Evo Japan 2026 — Second Major
        ("https://youtu.be/FJgQ3txydkc",                 "Evo Japan 2026 — Top 8 Full VOD"),
        ("https://youtu.be/pbZqYFmpiP0",                 "Evo Japan 2026 — Official Event Recap"),
        # Deep-dive analysis
        ("https://youtu.be/YPUPO5SpnAU",                 "Frosty Faustings Grand Finals Analysis — DingusPunch"),
        ("https://youtu.be/zLZf6Z6EH2Q",                 "Frosty Faustings to Firing Lines — Deep Dive"),
        # Community events
        ("https://www.youtube.com/watch?v=YHOI3BZnmag",  "TNS Four Kingdoms Community Event"),
    ],
}

# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT DIRECTORIES
# ──────────────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")

FOLDER_MAP = {
    "ahri":       os.path.join(BASE_DIR, "01_Ahri_Ekko"),
    "illaoi":     os.path.join(BASE_DIR, "02_Ekko_Illaoi"),
    "shorts":     os.path.join(BASE_DIR, "03_Shorts"),
    "tournament": os.path.join(BASE_DIR, "04_Tournament_VODs"),
}

# ──────────────────────────────────────────────────────────────────────────────
# DOWNLOADER
# ──────────────────────────────────────────────────────────────────────────────
def get_ydl_opts(output_dir: str, quality: str, audio_only: bool) -> dict:
    """Build yt-dlp options dict."""
    os.makedirs(output_dir, exist_ok=True)

    outtmpl = os.path.join(output_dir, "%(upload_date>%Y-%m-%d)s — %(title)s [%(id)s].%(ext)s")

    # ffmpeg installed via winget — hardcoded path so it works regardless of PATH env
    FFMPEG_DIR = r"C:\Users\PCGAME\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin"

    if audio_only:
        return {
            "format": "bestaudio/best",
            "outtmpl": outtmpl,
            "ffmpeg_location": FFMPEG_DIR,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "ignoreerrors": True,
            "quiet": False,
            "no_warnings": False,
        }

    # ffmpeg installed via winget — hardcoded path so it works regardless of PATH env
    FFMPEG_DIR = r"C:\Users\PCGAME\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin"

    if quality == "best":
        fmt = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
    else:
        fmt = f"bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={quality}]+bestaudio/best[height<={quality}]"

    return {
        "format": fmt,
        "outtmpl": outtmpl,
        "merge_output_format": "mp4",
        "ffmpeg_location": FFMPEG_DIR,
        "writesubtitles": False,
        "writethumbnail": False,
        "ignoreerrors": True,
        "quiet": False,
        "no_warnings": False,
        "retries": 3,
        "fragment_retries": 3,
    }


def download_folder(folder_key: str, quality: str, audio_only: bool, dry_run: bool):
    """Download all videos in a named folder."""
    import yt_dlp

    entries = VIDEOS[folder_key]
    output_dir = FOLDER_MAP[folder_key]
    opts = get_ydl_opts(output_dir, quality, audio_only)

    print(f"\n{'='*60}")
    print(f"  Folder : {folder_key.upper()}  ({len(entries)} videos)")
    print(f"  Output : {output_dir}")
    print(f"  Quality: {'audio-only' if audio_only else quality}p")
    print(f"{'='*60}")

    urls = [url for url, _ in entries]

    if dry_run:
        for url, title in entries:
            print(f"  [LIST] {url}  —  {title}")
        return

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download(urls)


def list_all():
    """Print all tracked videos without downloading."""
    total = 0
    for folder_key, entries in VIDEOS.items():
        print(f"\n── {folder_key.upper()} ({len(entries)}) ──────────────────────────")
        for url, title in entries:
            print(f"  {url}")
            print(f"    {title}")
        total += len(entries)
    print(f"\nTotal: {total} videos")


def update_titles():
    """Use yt-dlp to fetch current titles for all videos and print a diff."""
    try:
        import yt_dlp
    except ImportError:
        print("yt-dlp not installed. Run: pip install yt-dlp")
        sys.exit(1)

    print("Fetching current video titles from YouTube…")
    all_urls = [url for entries in VIDEOS.values() for url, _ in entries]

    opts = {
        "quiet": True,
        "skip_download": True,
        "ignoreerrors": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        for url in all_urls:
            try:
                info = ydl.extract_info(url, download=False)
                if info:
                    print(f"  OK  {url}\n      {info.get('title','(no title)')}")
                else:
                    print(f"  ERR {url}  (unavailable)")
            except Exception as e:
                print(f"  ERR {url}  {e}")


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Download 2XKO Ekko/Ahri & Ekko/Illaoi videos via yt-dlp",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--folder", choices=["ahri", "illaoi", "shorts", "tournament", "all"],
        default="all", help="Which folder to download (default: all)"
    )
    parser.add_argument(
        "--quality", default="best",
        help="Max video height in px, e.g. 720, 1080, or 'best' (default: best)"
    )
    parser.add_argument(
        "--audio-only", action="store_true",
        help="Download audio only as mp3"
    )
    parser.add_argument(
        "--list", action="store_true",
        help="Print all URLs without downloading"
    )
    parser.add_argument(
        "--update", action="store_true",
        help="Fetch current titles from YouTube and print"
    )
    args = parser.parse_args()

    # Validate yt-dlp is available unless just listing
    if not args.list and not args.update:
        try:
            import yt_dlp  # noqa: F401
        except ImportError:
            print("yt-dlp is not installed.")
            print("Install with:  pip install yt-dlp")
            sys.exit(1)

    if args.list:
        list_all()
        return

    if args.update:
        update_titles()
        return

    folders = list(VIDEOS.keys()) if args.folder == "all" else [args.folder]
    total_videos = sum(len(VIDEOS[f]) for f in folders)

    print(f"\n2XKO Video Downloader")
    print(f"Folders  : {', '.join(folders)}")
    print(f"Videos   : {total_videos}")
    print(f"Quality  : {'audio-only mp3' if args.audio_only else args.quality}")
    print(f"Base dir : {BASE_DIR}\n")

    for folder_key in folders:
        download_folder(folder_key, args.quality, args.audio_only, dry_run=False)

    print(f"\nAll done. Files saved to: {BASE_DIR}")


if __name__ == "__main__":
    main()
