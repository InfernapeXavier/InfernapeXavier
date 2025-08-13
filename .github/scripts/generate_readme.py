#!/usr/bin/env python3
"""Generate developer-focused README.md with dynamic data."""

import json
from datetime import datetime
from pathlib import Path


def load_json_data(filename: str) -> dict:
    """Load JSON data from file, return empty dict if not found."""
    data_dir = Path("../../data")
    file_path = data_dir / filename

    if not file_path.exists():
        return {}

    try:
        with open(file_path) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"⚠️ Error loading {filename}: {e}")
        return {}


def format_minutes_to_readable(minutes: int) -> str:
    """Convert minutes to a readable format."""
    if minutes < 60:
        return f"{minutes}m"
    elif minutes < 1440:  # Less than a day
        hours = minutes // 60
        remaining_minutes = minutes % 60
        return f"{hours}h {remaining_minutes}m" if remaining_minutes else f"{hours}h"
    else:
        days = minutes // 1440
        remaining_hours = (minutes % 1440) // 60
        return f"{days}d {remaining_hours}h" if remaining_hours else f"{days}d"


def format_large_number(num: int) -> str:
    """Format large numbers with k suffix."""
    if num >= 1000:
        return f"{num/1000:.1f}k"
    return str(num)


def generate_currently_section(anilist_data: dict) -> str:
    """Generate the 'Currently' section with HTML cards."""
    watching = anilist_data.get("currentlyWatching", [])
    reading = anilist_data.get("currentlyReading", [])

    watching_items = ""
    if watching:
        for item in watching[:5]:
            watching_items += f'<li>📺 {item["title"]}</li>'
    else:
        watching_items = '<li>Nothing currently</li>'

    reading_items = ""
    if reading:
        for item in reading[:5]:
            reading_items += f'<li>📖 {item["title"]}</li>'
    else:
        reading_items = '<li>Nothing currently</li>'

    return f'''<div align="center">
<table>
<tr>
<td width="50%">

<div style="border: 2px solid #30363d; border-radius: 10px; padding: 15px; background: linear-gradient(135deg, #0d1117 0%, #161b22 100%); margin: 10px;">
<h3 align="center">🎯 Working On</h3>
<ul>
<li>🔧 Infrastructure automation</li>
<li>⚙️ Backend services</li>
</ul>
</div>

<div style="border: 2px solid #238636; border-radius: 10px; padding: 15px; background: linear-gradient(135deg, #0d1117 0%, #0f1419 100%); margin: 10px;">
<h3 align="center">📺 Currently Watching</h3>
<ul>
{watching_items}
</ul>
</div>

</td>
<td width="50%">

<div style="border: 2px solid #1f6feb; border-radius: 10px; padding: 15px; background: linear-gradient(135deg, #0d1117 0%, #0f1419 100%); margin: 10px;">
<h3 align="center">📚 Currently Reading</h3>
<ul>
{reading_items}
</ul>
</div>

<div style="border: 2px solid #f85149; border-radius: 10px; padding: 15px; background: linear-gradient(135deg, #0d1117 0%, #161b22 100%); margin: 10px;">
<h3 align="center">⚡ Status</h3>
<p align="center">
<img src="https://img.shields.io/badge/status-online-brightgreen?style=for-the-badge&logo=statuspage" alt="Status">
</p>
</div>

</td>
</tr>
</table>
</div>'''


def generate_stats_section(anilist_data: dict, spotify_data: dict) -> str:
    """Generate the stats section with HTML cards and visual elements."""
    stats = anilist_data.get("user", {}).get("stats", {})
    anime_stats = stats.get("anime", {})
    manga_stats = stats.get("manga", {})
    top_tracks = spotify_data.get("topTracks", [])

    # Anime/Manga stats
    anime_count = anime_stats.get("count", 0)
    anime_minutes = anime_stats.get("minutesWatched", 0)
    manga_count = manga_stats.get("count", 0)
    manga_chapters = manga_stats.get("chaptersRead", 0)

    # Convert minutes to readable format
    anime_time = format_minutes_to_readable(anime_minutes)
    manga_chapters_formatted = format_large_number(manga_chapters)

    # Top genres
    anime_genres = anime_stats.get("topGenres", [])[:3]
    manga_genres = manga_stats.get("topGenres", [])[:3]
    all_genres = list(set(anime_genres + manga_genres))[:5]
    genres_badges = ""
    if all_genres:
        for genre in all_genres:
            genres_badges += f'<img src="https://img.shields.io/badge/{genre}-purple?style=flat-square" alt="{genre}"> '

    # Music section
    music_tracks = ""
    if top_tracks:
        for i, track in enumerate(top_tracks[:5], 1):
            music_tracks += f'''<tr>
<td>{i}</td>
<td><strong>{track['name']}</strong></td>
<td>{track['artist']}</td>
</tr>'''

    return f'''<div align="center">

<h2>📊 Analytics & Statistics</h2>

<table>
<tr>
<td width="33%">

<div style="border: 2px solid #fd7e14; border-radius: 15px; padding: 20px; background: linear-gradient(135deg, #0d1117 0%, #1a0f0a 100%); text-align: center;">
<h3>📺 Anime</h3>
<h2 style="color: #fd7e14; margin: 10px 0;">{anime_count}</h2>
<p><strong>completed</strong></p>
<p style="color: #8b949e;">⏱️ {anime_time} watched</p>
</div>

</td>
<td width="33%">

<div style="border: 2px solid #20c997; border-radius: 15px; padding: 20px; background: linear-gradient(135deg, #0d1117 0%, #0a1a16 100%); text-align: center;">
<h3>📖 Manga</h3>
<h2 style="color: #20c997; margin: 10px 0;">{manga_count}</h2>
<p><strong>completed</strong></p>
<p style="color: #8b949e;">📄 {manga_chapters_formatted} chapters</p>
</div>

</td>
<td width="33%">

<div style="border: 2px solid #6f42c1; border-radius: 15px; padding: 20px; background: linear-gradient(135deg, #0d1117 0%, #1a0f1a 100%); text-align: center;">
<h3>🏷️ Top Genres</h3>
<div style="margin: 15px 0;">
{genres_badges}
</div>
</div>

</td>
</tr>
</table>

</div>

<div align="center" style="margin-top: 20px;">

<div style="border: 2px solid #1db954; border-radius: 15px; padding: 20px; background: linear-gradient(135deg, #0d1117 0%, #0a1a0f 100%); max-width: 600px;">
<h3>🎵 This Month's Top Tracks</h3>
<table width="100%" style="margin-top: 15px;">
<thead>
<tr>
<th width="10%">#</th>
<th width="50%">Track</th>
<th width="40%">Artist</th>
</tr>
</thead>
<tbody>
{music_tracks}
</tbody>
</table>
</div>

</div>'''


def generate_readme() -> None:
    """Generate the complete README.md file."""
    # Load data
    anilist_data = load_json_data("anilist.json")
    spotify_data = load_json_data("spotify.json")

    # Generate sections
    currently_section = generate_currently_section(anilist_data)
    stats_section = generate_stats_section(anilist_data, spotify_data)

    readme_content = f'''<div align="center">

<img width="100%" height="2" src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif">

<h1 style="background: linear-gradient(90deg, #00d4ff, #9f4cff, #ff6b6b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3em;">
InfernapeXavier
</h1>

<h3 style="color: #8b949e; margin-bottom: 20px;">🔧 Infrastructure Engineer @ Academia.edu</h3>

<div style="background: linear-gradient(135deg, #0d1117 0%, #161b22 100%); border-radius: 20px; padding: 20px; margin: 20px; border: 1px solid #30363d;">

[![spotify-github-profile](https://spotify-github-profile.kittinanx.com/api/view?uid=infernapexavier&cover_image=true&theme=novatorem&show_offline=true&background_color=121212&interchange=false&bar_color=53b14f&bar_color_cover=true)](https://spotify-github-profile.kittinanx.com/api/view?uid=infernapexavier&redirect=true)

<br>

<img src="https://img.shields.io/badge/🎧_Now_Playing-Spotify-1DB954?style=for-the-badge&logo=spotify&logoColor=white" alt="Now Playing">

</div>

<img width="100%" height="2" src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif">

</div>

{currently_section}

<br>

{stats_section}

<div align="center" style="margin-top: 30px;">
<img width="100%" height="2" src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif">
<br>
<sub style="color: #8b949e;">✨ Profile auto-updates every 6 hours via GitHub Actions ✨</sub>
</div>'''

    # Write README.md
    readme_path = Path("../../README.md")
    with open(readme_path, "w") as f:
        f.write(readme_content)

    print("✅ README.md generated successfully")


if __name__ == "__main__":
    generate_readme()
