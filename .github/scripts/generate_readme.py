#!/usr/bin/env python3
"""Generate a professional profile with a collapsible interests section."""

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


def generate_currently_section(anilist_data: dict) -> str:
    """Keep the current watching and reading lists compact."""
    watching = (
        "\n".join(f"- {item['title']}" for item in anilist_data.get("currentlyWatching", [])[:3])
        or "Nothing currently."
    )
    reading = (
        "\n".join(f"- {item['title']}" for item in anilist_data.get("currentlyReading", [])[:3])
        or "Nothing currently."
    )

    return f"""### Watching

{watching}

### Reading

{reading}"""


def generate_readme() -> None:
    """Generate the complete README.md file from cached AniList data."""
    anilist_data = load_json_data("anilist.json")
    currently_section = generate_currently_section(anilist_data)

    readme_content = f"""# Hi, I'm Rohit

**Infrastructure Engineer** at [Academia.edu](https://www.academia.edu).

I work on **AI tooling infrastructure**—the systems and workflows behind
AI-powered developer tools.

I'm interested in making those tools more reliable, useful, and easy to work with.

[rohitc.tech ↗](http://rohitc.tech)

---

<details>
<summary><strong>Outside of work</strong></summary>

I enjoy reading, anime, and gaming.

{currently_section}

</details>
"""

    readme_path = Path("../../README.md")
    with open(readme_path, "w") as f:
        f.write(readme_content)

    print("✅ README.md generated successfully")


if __name__ == "__main__":
    generate_readme()
