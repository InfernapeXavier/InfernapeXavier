# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a GitHub profile repository (InfernapeXavier/InfernapeXavier) that automatically generates a dynamic README profile using data from AniList and Spotify APIs. The main README.md displays currently watching anime/manga and top Spotify tracks in a developer-focused JSON format.

## Architecture

The automation system consists of three main components:

1. **GitHub Action Workflow** (`.github/workflows/update-profile.yml`)
   - Runs every 6 hours, on push to main/master, or manual trigger
   - Uses uv package manager with Python 3.13.x
   - Executes linting, data fetching, and README generation

2. **Data Fetching Scripts** (`.github/scripts/`)
   - `fetch_anilist.py`: GraphQL queries to AniList API with smart content filtering
   - `fetch_spotify.py`: OAuth2 refresh token authentication to Spotify API
   - `generate_readme.py`: Template engine that creates README from cached data

3. **Data Storage** (`data/`)
   - `anilist.json`: Cached anime/manga statistics and current lists
   - `spotify.json`: Cached top tracks data

## Content Filtering Logic

The system applies intelligent filtering to ensure professional, relevant content:

- **Anime filtering**: Excludes `NOT_YET_RELEASED` status, prioritizes `RELEASING` over `FINISHED`
- **Manga filtering**: Excludes titles with "Ecchi" genre tag
- **Limits**: Shows top 5 items for watching/reading lists, top 5 Spotify tracks

## Common Development Commands

### Environment Setup
```bash
cd .github/scripts
uv sync                    # Install Python dependencies
uv run ruff check .        # Run linting
uv run ruff format .       # Format code
```

### Testing Data Fetching
```bash
# Test AniList integration
export ANILIST_USERNAME=your_username
uv run python fetch_anilist.py

# Test Spotify integration  
export SPOTIFY_CLIENT_ID=your_client_id
export SPOTIFY_CLIENT_SECRET=your_client_secret
export SPOTIFY_REFRESH_TOKEN=your_refresh_token
uv run python fetch_spotify.py

# Generate README from cached data
uv run python generate_readme.py
```

### Spotify OAuth Setup
```bash
# Automated Spotify token generation
uv run python spotify_auth.py
```

## Required GitHub Secrets

- `ANILIST_USERNAME`: AniList username for profile data
- `SPOTIFY_CLIENT_ID`: Spotify app client ID
- `SPOTIFY_CLIENT_SECRET`: Spotify app client secret  
- `SPOTIFY_REFRESH_TOKEN`: OAuth2 refresh token for API access

## Key Implementation Details

- **Profile Priority**: Root `README.md` displays as GitHub profile (`.github/README.md` would override it)
- **Error Handling**: Scripts gracefully handle missing credentials and network errors
- **Commit Strategy**: Uses "[Skip GitHub Action]" in commit messages to prevent workflow loops
- **Template Structure**: JSON-style "Currently" section with multiline arrays for clean display
- **API Limits**: AniList uses public GraphQL (no auth required), Spotify requires OAuth2 flow

## Customization Points

- **README template**: Modify template strings in `generate_readme.py`
- **Data sources**: Adjust GraphQL queries in `fetch_anilist.py` or API parameters in `fetch_spotify.py`  
- **Update frequency**: Change cron schedule in `update-profile.yml`
- **Content filtering**: Modify filtering logic for different content preferences