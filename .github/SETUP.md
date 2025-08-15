# GitHub Profile Automation

This directory contains a custom GitHub Action system that automatically updates the profile README with live data from AniList and Spotify APIs.

## Overview

The system replaces the heavy `lowlighter/metrics` action with a lightweight, custom Python-based solution that focuses on:
- Currently watching anime/reading manga from AniList
- Top Spotify tracks from the last month
- Clean, developer-focused aesthetic with JSON-style status display

## Architecture

```
.github/
├── workflows/
│   └── update-profile.yml          # Main GitHub Action workflow
└── scripts/                        # Python automation scripts
    ├── pyproject.toml              # Python dependencies & config
    ├── fetch_anilist.py            # AniList API integration
    ├── fetch_spotify.py            # Spotify API integration
    └── generate_readme.py          # README template engine

data/                               # Generated API data cache
├── anilist.json                   # AniList user data
└── spotify.json                   # Spotify track data
```

## How It Works

### 1. GitHub Action Workflow (`update-profile.yml`)
- **Triggers**: Every 6 hours, on push to main/master, or manual dispatch
- **Environment**: Ubuntu with Python 3.13.x, uv package manager, ruff linting
- **Steps**:
  1. Install uv and setup Python environment
  2. Install dependencies and run linting
  3. Fetch fresh data from AniList and Spotify APIs
  4. Generate updated README.md from template
  5. Commit changes (if any) back to repository

### 2. Data Fetching Scripts

#### `fetch_anilist.py`
- Fetches user statistics (anime count, watch time, manga chapters, top genres)
- Gets currently watching anime and reading manga (top 3 each)
- Uses GraphQL queries to AniList's public API
- Saves data to `data/anilist.json`

#### `fetch_spotify.py`
- Authenticates using OAuth2 refresh token flow
- Fetches top tracks from short-term period (last ~4 weeks)
- Saves track data to `data/spotify.json`

#### `generate_readme.py`
- Loads cached JSON data from both APIs
- Generates developer-focused README with:
  - JSON-style "Currently" section showing status
  - Stats section with anime/manga counts and Spotify tracks
  - Preserves existing Spotify widget
- Handles missing data gracefully with fallbacks

## Setup Instructions

### 1. Required GitHub Secrets

Add these secrets to your repository settings:

```bash
# AniList Integration
ANILIST_USERNAME=YourAniListUsername

# Spotify Integration  
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REFRESH_TOKEN=your_spotify_refresh_token
```

### 2. Spotify API Setup

#### Option A: Automated Setup (Recommended)

1. Create a Spotify app at [developer.spotify.com](https://developer.spotify.com/dashboard)
2. Get your Client ID and Client Secret
3. Run the automated OAuth script:
   ```bash
   cd .github/scripts
   uv run python spotify_auth.py
   ```
4. Follow the prompts - the script will:
   - Tell you what redirect URI to add (`http://127.0.0.1:3000/callback`)
   - Open your browser for Spotify authorization
   - Automatically capture the authorization code
   - Exchange it for a refresh token

#### Option B: Manual Setup

1. Create a Spotify app at [developer.spotify.com](https://developer.spotify.com/dashboard)
2. Set the redirect URI in your Spotify app settings to: `http://127.0.0.1:3000/callback`
3. Get your Client ID and Client Secret
4. Use Spotify's authorization flow to get a refresh token:
   ```bash
   # 1. Visit this URL in your browser (replace YOUR_CLIENT_ID)
   https://accounts.spotify.com/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A3000%2Fcallback&scope=user-top-read
   
   # 2. After authorizing, copy the 'code' parameter from the redirect URL (page will show connection error, that's expected)
   # 3. Exchange authorization code for refresh token (replace YOUR_CLIENT_ID, YOUR_CLIENT_SECRET, and AUTHORIZATION_CODE)
   #    NOTE: Authorization codes expire in ~10 minutes, so do this quickly!
   curl -X POST "https://accounts.spotify.com/api/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "grant_type=authorization_code&code=AUTHORIZATION_CODE&redirect_uri=http://127.0.0.1:3000/callback&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET"
   
   # If you get "invalid_grant" error:
   # - The authorization code may have expired (get a new one)
   # - Make sure the redirect_uri matches exactly what you set in Spotify app settings
   # - Ensure you're using the correct client_id and client_secret
   ```

### 3. AniList Setup

Simply provide your AniList username - no API keys required as it uses public GraphQL endpoints.

## Local Development

### Prerequisites
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager

### Setup
```bash
cd .github/scripts
uv sync                    # Install dependencies
uv run ruff check .        # Run linting
```

### Testing Scripts
```bash
# Test AniList fetching (requires ANILIST_USERNAME env var)
export ANILIST_USERNAME=your_username
uv run python fetch_anilist.py

# Test Spotify fetching (requires Spotify env vars)
export SPOTIFY_CLIENT_ID=your_client_id
export SPOTIFY_CLIENT_SECRET=your_client_secret
export SPOTIFY_REFRESH_TOKEN=your_refresh_token
uv run python fetch_spotify.py

# Generate README from cached data
uv run python generate_readme.py
```

## Customization

### Modifying the README Template
Edit the template strings in `generate_readme.py`:
- Update the tagline/subtitle
- Modify the "working_on" items in the JSON status
- Change the stats format or add new sections

### Adjusting Data Sources
- **AniList**: Modify the GraphQL query in `fetch_anilist.py` to fetch different fields
- **Spotify**: Change the `time_range` parameter in `fetch_spotify.py` ("short_term", "medium_term", "long_term")
- **Update frequency**: Edit the cron schedule in `update-profile.yml`

### Error Handling
All scripts include graceful error handling:
- Missing API credentials skip that service
- Network errors are logged but don't break the workflow  
- Missing data files result in placeholder content
- Failed API calls fallback to cached data

## Dependencies

- **httpx**: Modern async HTTP client for API requests
- **python-dotenv**: Environment variable management
- **ruff**: Fast Python linter and formatter
- **uv**: Fast Python package installer and resolver

## Monitoring

Check the GitHub Actions tab to monitor workflow runs. The scripts provide detailed logging:
- ✅ Success indicators for each API fetch
- ❌ Error messages with specific failure reasons
- 📊 Data summaries (e.g., "Watching: 3 anime", "Top tracks: 5")