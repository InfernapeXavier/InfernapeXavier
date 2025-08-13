#!/usr/bin/env python3
"""Fetch Spotify data for GitHub profile."""

import base64
import json
import os
from pathlib import Path

import httpx

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE = "https://api.spotify.com/v1"


async def get_access_token(client_id: str, client_secret: str, refresh_token: str) -> str | None:
    """Get access token using refresh token."""
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                SPOTIFY_TOKEN_URL,
                headers={
                    "Authorization": f"Basic {auth_header}",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token
                }
            )
            response.raise_for_status()

            token_data = response.json()
            return token_data["access_token"]

        except httpx.HTTPError as e:
            print(f"❌ Error getting Spotify access token: {e}")
            return None


async def fetch_spotify_data() -> None:
    """Fetch Spotify top tracks and save to JSON file."""
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        print("Spotify credentials not set, skipping Spotify data fetch")
        return

    # Get access token
    access_token = await get_access_token(client_id, client_secret, refresh_token)
    if not access_token:
        return

    async with httpx.AsyncClient() as client:
        try:
            # Fetch top tracks from last month (short term)
            response = await client.get(
                f"{SPOTIFY_API_BASE}/me/top/tracks",
                headers={"Authorization": f"Bearer {access_token}"},
                params={"time_range": "short_term", "limit": 5}
            )
            response.raise_for_status()

            tracks_data = response.json()

            # Process the tracks data
            spotify_data = {
                "topTracks": [
                    {
                        "name": track["name"],
                        "artist": ", ".join(artist["name"] for artist in track["artists"]),
                        "album": track["album"]["name"],
                        "external_url": track["external_urls"]["spotify"],
                        "popularity": track["popularity"]
                    }
                    for track in tracks_data["items"]
                ],
                "lastUpdated": "2025-01-01T00:00:00.000Z"  # Will be updated by datetime
            }

            # Create data directory
            data_dir = Path("../../data")
            data_dir.mkdir(exist_ok=True)

            # Write data to file
            with open(data_dir / "spotify.json", "w") as f:
                json.dump(spotify_data, f, indent=2)

            print("✅ Spotify data fetched successfully")
            print(f"🎵 Top tracks: {len(spotify_data['topTracks'])}")

        except httpx.HTTPError as e:
            print(f"❌ HTTP error fetching Spotify data: {e}")
        except Exception as e:
            print(f"❌ Error fetching Spotify data: {e}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(fetch_spotify_data())
