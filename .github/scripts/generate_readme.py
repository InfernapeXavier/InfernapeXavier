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

    return f"""<div align="center">

<table>
<tr>
<td width="50%" valign="top">

**🎯 Currently Building**
```
🔧 Infrastructure that just works
⚙️ Backend services that scale
💡 Solutions to hard problems
```

**📺 Binge-watching right now**
```
{watching_items.rstrip()}
```

</td>
<td width="50%" valign="top">

**📚 Getting lost in these stories**
```
{reading_items.rstrip()}
```

[![spotify-github-profile](https://spotify-github-profile.kittinanx.com/api/view?uid=infernapexavier&cover_image=true&theme=novatorem&show_offline=true&background_color=121212&interchange=false&bar_color=53b14f&bar_color_cover=true)](https://spotify-github-profile.kittinanx.com/api/view?uid=infernapexavier&redirect=true)

</td>
</tr>
</table>

</div>"""


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
            genre_encoded = genre.replace(' ', '%20')
            genre_url = f"https://img.shields.io/badge/{genre_encoded}-purple?style=flat-square"
            genres_badges += f"![{genre}]({genre_url}) "

    # Music section with album art
    music_tracks = ""
    if top_tracks:
        for track in top_tracks[:5]:
            album_img = track.get("album_image", "")
            img_html = (
                f'<img src="{album_img}" width="40" height="40" style="border-radius: 4px;">'
                if album_img
                else "🎵"
            )
            track_url = track.get('external_url', '#')
            track_name = track['name']
            artist_name = track['artist']
            music_tracks += f"{img_html} | **[{track_name}]({track_url})** | *{artist_name}*\n"

    return f"""<div align="center">

<table>
<tr>
<td align="center" width="33%">

📺 **{anime_count}** anime conquered  
⏱️ *{anime_time} of pure entertainment*

</td>
<td align="center" width="33%">

📖 **{manga_count}** manga adventures  
📄 *{manga_chapters_formatted} chapters devoured*

</td>
<td align="center" width="33%">

🏷️ **My guilty pleasures**  
{genres_badges}

</td>
</tr>
</table>

</div>

*🎵 Sounds that fuel my code sessions*

| Cover | Track | Artist |
|-------|-------|--------|
{music_tracks.rstrip()}"""


def generate_readme() -> None:
    """Generate the complete README.md file."""
    # Load data
    anilist_data = load_json_data("anilist.json")
    spotify_data = load_json_data("spotify.json")

    # Generate sections
    currently_section = generate_currently_section(anilist_data)
    stats_section = generate_stats_section(anilist_data, spotify_data)

    readme_content = f"""<div align="center">

![intro](https://carbonara.solopov.dev/api/cook?code=console.log%28%22Hi%20there%20%F0%9F%91%8B%22%29%3B%0A%0A%2F%2F%20I%27m%20Rohit%21%0Aconst%20developer%20%3D%20%7B%0A%20%20name%3A%20%22Rohit%22%2C%0A%20%20role%3A%20%22Infrastructure%20Engineer%22%2C%0A%20%20company%3A%20%22Academia.edu%22%2C%0A%20%20pronouns%3A%20%22He%2FHim%22%2C%0A%20%20currentlyLearning%3A%20%5B%22Ruby%22%2C%20%22React%22%5D%2C%0A%20%20funFact%3A%20%22Red%20Pandas%20are%20not%20Pandas%21%22%0A%7D%3B%0A%0Aconsole.log%28%22Welcome%20to%20my%20profile%21%22%29%3B&config=%7B%22paddingVertical%22%3A%2216px%22%2C%22paddingHorizontal%22%3A%2215px%22%2C%22backgroundImage%22%3Anull%2C%22backgroundImageSelection%22%3Anull%2C%22backgroundMode%22%3A%22color%22%2C%22backgroundColor%22%3A%22rgba%28222%2C171%2C99%2C1%29%22%2C%22dropShadow%22%3Atrue%2C%22dropShadowOffsetY%22%3A%2220px%22%2C%22dropShadowBlurRadius%22%3A%22100px%22%2C%22theme%22%3A%22duotone-dark%22%2C%22windowTheme%22%3A%22none%22%2C%22language%22%3A%22auto%22%2C%22fontFamily%22%3A%22Fira%20Code%22%2C%22fontSize%22%3A%2214px%22%2C%22lineHeight%22%3A%22133%25%22%2C%22windowControls%22%3Atrue%2C%22widthAdjustment%22%3Atrue%2C%22lineNumbers%22%3Atrue%2C%22firstLineNumber%22%3A1%2C%22exportSize%22%3A%222x%22%2C%22watermark%22%3Afalse%2C%22squaredImage%22%3Afalse%2C%22hiddenCharacters%22%3Afalse%2C%22name%22%3A%22%22%2C%22width%22%3A680%2C%22highlights%22%3Anull%7D)

</div>

{currently_section}

{stats_section}"""

    # Write README.md
    readme_path = Path("../../README.md")
    with open(readme_path, "w") as f:
        f.write(readme_content)

    print("✅ README.md generated successfully")


if __name__ == "__main__":
    generate_readme()
