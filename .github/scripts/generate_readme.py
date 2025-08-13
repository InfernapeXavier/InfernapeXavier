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
    """Generate the 'Currently' section with GitHub-compatible formatting."""
    watching = anilist_data.get("currentlyWatching", [])
    reading = anilist_data.get("currentlyReading", [])

    watching_items = ""
    if watching:
        for item in watching[:5]:
            watching_items += f'• 📺 {item["title"]}\n'
    else:
        watching_items = '• Nothing currently\n'

    reading_items = ""
    if reading:
        for item in reading[:5]:
            reading_items += f'• 📖 {item["title"]}\n'
    else:
        reading_items = '• Nothing currently\n'

    return f'''<div align="center">

<table>
<tr>
<td width="50%" valign="top">

**🎯 Working On**
```
🔧 Infrastructure automation
⚙️ Backend services
```

**📺 Currently Watching**
```
{watching_items.rstrip()}
```

</td>
<td width="50%" valign="top">

**📚 Currently Reading**
```
{reading_items.rstrip()}
```

**⚡ Status**

![Status](https://img.shields.io/badge/status-online-brightgreen?style=for-the-badge&logo=statuspage)

</td>
</tr>
</table>

</div>'''


def generate_stats_section(anilist_data: dict, spotify_data: dict) -> str:
    """Generate the stats section with GitHub-compatible formatting."""
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
            genres_badges += f'![{genre}](https://img.shields.io/badge/{genre.replace(" ", "%20")}-purple?style=flat-square) '

    # Music section
    music_tracks = ""
    if top_tracks:
        for i, track in enumerate(top_tracks[:5], 1):
            music_tracks += f'| {i} | **{track["name"]}** | {track["artist"]} |\n'

    return f'''## 📊 Analytics & Statistics

<div align="center">

<table>
<tr>
<td align="center" width="33%">

**📺 Anime**

### {anime_count}
**completed**

⏱️ *{anime_time} watched*

</td>
<td align="center" width="33%">

**📖 Manga**

### {manga_count}
**completed**

📄 *{manga_chapters_formatted} chapters*

</td>
<td align="center" width="33%">

**🏷️ Top Genres**

{genres_badges}

</td>
</tr>
</table>

</div>

## 🎵 This Month's Top Tracks

| # | Track | Artist |
|---|-------|--------|
{music_tracks.rstrip()}'''


def generate_readme() -> None:
    """Generate the complete README.md file."""
    # Load data
    anilist_data = load_json_data("anilist.json")
    spotify_data = load_json_data("spotify.json")

    # Generate sections
    currently_section = generate_currently_section(anilist_data)
    stats_section = generate_stats_section(anilist_data, spotify_data)

    readme_content = f'''<div align="center">

![Header](https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif)

# 🔥 InfernapeXavier

### 🔧 Infrastructure Engineer @ Academia.edu

---

[![spotify-github-profile](https://spotify-github-profile.kittinanx.com/api/view?uid=infernapexavier&cover_image=true&theme=novatorem&show_offline=true&background_color=121212&interchange=false&bar_color=53b14f&bar_color_cover=true)](https://spotify-github-profile.kittinanx.com/api/view?uid=infernapexavier&redirect=true)

![Now Playing](https://img.shields.io/badge/🎧_Now_Playing-Spotify-1DB954?style=for-the-badge&logo=spotify&logoColor=white)

---

</div>

{currently_section}

{stats_section}'''

    # Write README.md
    readme_path = Path("../../README.md")
    with open(readme_path, "w") as f:
        f.write(readme_content)

    print("✅ README.md generated successfully")


if __name__ == "__main__":
    generate_readme()
