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
    """Generate the 'Currently' section with JSON-like formatting."""
    watching = anilist_data.get("currentlyWatching", [])
    reading = anilist_data.get("currentlyReading", [])

    # Format watching as individual lines
    watching_str = "[\n"
    if watching:
        for item in watching[:5]:
            watching_str += f'    "{item["title"]}",\n'
        watching_str = watching_str.rstrip(",\n") + "\n  ]"
    else:
        watching_str = "null"

    # Format reading as individual lines  
    reading_str = "[\n"
    if reading:
        for item in reading[:5]:
            reading_str += f'    "{item["title"]}",\n'
        reading_str = reading_str.rstrip(",\n") + "\n  ]"
    else:
        reading_str = "null"

    return f'''## Currently
```bash
$ cat ~/.config/status.json
{{
  "working_on": ["Infrastructure automation", "Backend services"],
  "watching": {watching_str},
  "reading": {reading_str},
  "status": "online"
}}
```'''


def generate_stats_section(anilist_data: dict, spotify_data: dict) -> str:
    """Generate the stats section with anime/manga and music data."""
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
    genres_str = ", ".join(all_genres) if all_genres else "Various"

    # Music section
    music_section = ""
    if top_tracks:
        music_section = "\n 🎵 This month's top tracks:\n"
        for _i, track in enumerate(top_tracks[:5], 1):
            music_section += f"    ├─ {track['name']} - {track['artist']}\n"

    return f'''## Stats
```
 📺 Anime: {anime_count} completed ({anime_time})
 📖 Manga: {manga_count} completed ({manga_chapters_formatted} chapters)
 🏷️ Genres: {genres_str}{music_section}```'''


def generate_readme() -> None:
    """Generate the complete README.md file."""
    # Load data
    anilist_data = load_json_data("anilist.json")
    spotify_data = load_json_data("spotify.json")

    # Generate sections
    currently_section = generate_currently_section(anilist_data)
    stats_section = generate_stats_section(anilist_data, spotify_data)

    readme_content = f'''# InfernapeXavier

> Infrastructure Engineer @ Academia.edu

{currently_section}

{stats_section}

<p align="center">
  <a
    href="https://spotify-github-profile.kittinanx.com/api/view?uid=infernapexavier&redirect=true"
  >
    <img
      src="https://spotify-github-profile.kittinanx.com/api/view?uid=infernapexavier&cover_image=true&theme=default&show_offline=true&background_color=0d1117&bar_color_cover=true"
      alt="Rohit's currently playing song"
    />
  </a>
</p>
'''

    # Write README.md
    readme_path = Path("../../README.md")
    with open(readme_path, "w") as f:
        f.write(readme_content)

    print("✅ README.md generated successfully")


if __name__ == "__main__":
    generate_readme()
