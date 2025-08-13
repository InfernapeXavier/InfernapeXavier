#!/usr/bin/env python3
"""Fetch AniList data for GitHub profile."""

import json
import os
from pathlib import Path

import httpx

ANILIST_API = "https://graphql.anilist.co"

QUERY = """
query ($userName: String) {
  User(name: $userName) {
    id
    name
    statistics {
      anime {
        count
        minutesWatched
        genrePreview: genres(limit: 5, sort: COUNT_DESC) {
          genre
          count
        }
      }
      manga {
        count
        chaptersRead
        genrePreview: genres(limit: 5, sort: COUNT_DESC) {
          genre
          count
        }
      }
    }
  }

  watchingList: MediaListCollection(userName: $userName, type: ANIME, status: CURRENT) {
    lists {
      entries {
        media {
          title {
            romaji
            english
          }
          episodes
          status
        }
        progress
      }
    }
  }

  readingList: MediaListCollection(userName: $userName, type: MANGA, status: CURRENT) {
    lists {
      entries {
        media {
          title {
            romaji
            english
          }
          chapters
          status
        }
        progress
      }
    }
  }
}
"""


async def fetch_anilist_data() -> None:
    """Fetch AniList data and save to JSON file."""
    username = os.getenv("ANILIST_USERNAME")

    if not username:
        print("ANILIST_USERNAME not set, skipping AniList data fetch")
        return

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                ANILIST_API,
                json={"query": QUERY, "variables": {"userName": username}},
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()

            if "errors" in data:
                print(f"AniList API errors: {data['errors']}")
                return

            user = data["data"]["User"]
            watching_entries = data["data"]["watchingList"]["lists"]
            watching_list = watching_entries[0]["entries"] if watching_entries else []
            reading_entries = data["data"]["readingList"]["lists"]
            reading_list = reading_entries[0]["entries"] if reading_entries else []

            # Process the data
            anilist_data = {
                "user": {
                    "name": user["name"],
                    "stats": {
                        "anime": {
                            "count": user["statistics"]["anime"]["count"],
                            "minutesWatched": user["statistics"]["anime"]["minutesWatched"],
                            "topGenres": [
                                g["genre"] for g in user["statistics"]["anime"]["genrePreview"]
                            ]
                        },
                        "manga": {
                            "count": user["statistics"]["manga"]["count"],
                            "chaptersRead": user["statistics"]["manga"]["chaptersRead"],
                            "topGenres": [
                                g["genre"] for g in user["statistics"]["manga"]["genrePreview"]
                            ]
                        }
                    }
                },
                "currentlyWatching": [
                    {
                        "title": (
                            entry["media"]["title"]["english"] or entry["media"]["title"]["romaji"]
                        ),
                        "progress": entry["progress"],
                        "totalEpisodes": entry["media"]["episodes"],
                        "status": entry["media"]["status"]
                    }
                    for entry in watching_list[:3]  # Top 3
                ],
                "currentlyReading": [
                    {
                        "title": (
                            entry["media"]["title"]["english"] or entry["media"]["title"]["romaji"]
                        ),
                        "progress": entry["progress"],
                        "totalChapters": entry["media"]["chapters"],
                        "status": entry["media"]["status"]
                    }
                    for entry in reading_list[:3]  # Top 3
                ],
                "lastUpdated": "2025-01-01T00:00:00.000Z"  # Will be updated by datetime
            }

            # Create data directory
            data_dir = Path("../../data")
            data_dir.mkdir(exist_ok=True)

            # Write data to file
            with open(data_dir / "anilist.json", "w") as f:
                json.dump(anilist_data, f, indent=2)

            print("✅ AniList data fetched successfully")
            print(f"📺 Watching: {len(anilist_data['currentlyWatching'])} anime")
            print(f"📖 Reading: {len(anilist_data['currentlyReading'])} manga")

        except httpx.HTTPError as e:
            print(f"❌ HTTP error fetching AniList data: {e}")
        except Exception as e:
            print(f"❌ Error fetching AniList data: {e}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(fetch_anilist_data())
