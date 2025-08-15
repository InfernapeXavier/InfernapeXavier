#!/usr/bin/env python3
"""Generate developer-focused README.md with dynamic data."""

import json
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
        return f"{num / 1000:.1f}k"
    return str(num)


def generate_currently_section(anilist_data: dict) -> str:
    """Generate the 'Currently' section with GitHub-compatible formatting."""
    watching = anilist_data.get("currentlyWatching", [])
    reading = anilist_data.get("currentlyReading", [])

    watching_items = ""
    if watching:
        for item in watching[:5]:
            watching_items += f"• 📺 {item['title']}\n"
    else:
        watching_items = "• Nothing currently\n"

    reading_items = ""
    if reading:
        for item in reading[:5]:
            reading_items += f"• 📖 {item['title']}\n"
    else:
        reading_items = "• Nothing currently\n"

    # Format watching/reading for terminal display
    watching_terminal = "\n".join([f"  {item['title']}" for item in anilist_data.get("currentlyWatching", [])[:5]]) or "  Nothing currently"
    reading_terminal = "\n".join([f"  {item['title']}" for item in anilist_data.get("currentlyReading", [])[:5]]) or "  Nothing currently"

    return f"""<table>
<tr>
<td width="50%" valign="top">

```bash
$ ps aux | grep "anime"
Currently watching:
{watching_terminal}

$ echo "Anime processes active"
```

</td>
<td width="50%" valign="top">

```bash
$ ps aux | grep "manga"
Currently reading:  
{reading_terminal}

$ echo "Manga processes active"
```

</td>
</tr>
</table>"""


def generate_terminal_stats(anilist_data: dict) -> str:
    """Generate terminal-style stats section in 2-column layout."""
    stats = anilist_data.get("user", {}).get("stats", {})
    anime_stats = stats.get("anime", {})
    manga_stats = stats.get("manga", {})

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

    return f"""<table>
<tr>
<td width="50%" valign="top">

```bash
$ whoami
rohit@dev:~$ 

$ cat ~/.media_stats
anime_completed={anime_count}
time_watched="{anime_time}"
manga_completed={manga_count}  
chapters_read="{manga_chapters_formatted}"

$ echo $FAVORITE_GENRES
{" ".join([genre.lower().replace(" ", "_") for genre in all_genres[:3]])}

$ uptime
Life uptime: Making things work since forever

$ echo "System stats loaded successfully"
All entertainment metrics up to date
```

</td>
<td width="50%" valign="top">

<div align="center">

[![spotify-github-profile](https://spotify-github-profile.kittinanx.com/api/view?uid=infernapexavier&cover_image=true&theme=default&show_offline=true&background_color=121212&interchange=true&bar_color=53b14f&bar_color_cover=true)](https://spotify-github-profile.kittinanx.com/api/view?uid=infernapexavier&redirect=true)

</div>

</td>
</tr>
</table>"""


def generate_stats_section(anilist_data: dict, spotify_data: dict) -> str:
    """Generate the stats section with GitHub-compatible formatting."""
    top_tracks = spotify_data.get("topTracks", [])

    # Music section with album art
    music_tracks = ""
    if top_tracks:
        for track in top_tracks[:5]:
            album_img = track.get("album_image", "")
            img_html = (
                f'<img src="{album_img}" width="40" height="40" '
                f'style="border-radius: 4px;" alt="{track["name"]} album cover">'
                if album_img
                else "🎵"
            )
            track_url = track.get('external_url', '#')
            track_name = track['name']
            artist_name = track['artist']
            music_tracks += f"{img_html} | **[{track_name}]({track_url})** | *{artist_name}*\n"

    return f"""<table>
<tr>
<td width="100%" valign="top">

*My current top songs*

| Cover | Track | Artist |
|-------|-------|--------|
{music_tracks.rstrip()}

</td>
</tr>
</table>"""


def generate_readme() -> None:
    """Generate the complete README.md file."""
    # Load data
    anilist_data = load_json_data("anilist.json")
    spotify_data = load_json_data("spotify.json")

    # Generate sections
    currently_section = generate_currently_section(anilist_data)
    terminal_stats = generate_terminal_stats(anilist_data)
    stats_section = generate_stats_section(anilist_data, spotify_data)

    readme_content = f"""<div align="center">

![Rohit's GitHub profile intro banner](images/intro.png)

</div>

{currently_section}

{terminal_stats}

{stats_section}"""

    # Write README.md
    readme_path = Path("../../README.md")
    with open(readme_path, "w") as f:
        f.write(readme_content)

    print("✅ README.md generated successfully")


if __name__ == "__main__":
    generate_readme()
