# CLAUDE.md

## Repository purpose

This is the GitHub profile repository for InfernapeXavier/InfernapeXavier.
`README.md` is generated: it contains a professional introduction and a collapsed
**Outside of work** section with AniList watching and reading lists.

## Architecture

- `.github/workflows/update-profile.yml` runs every six hours, on pushes to
  main/master, or by manual dispatch. It uses uv and Python 3.13 to lint, test,
  fetch AniList data, generate the README, and commit updates.
- `.github/scripts/fetch_anilist.py` queries AniList's public GraphQL API and
  saves `data/anilist.json`. It excludes unreleased anime, prioritizes releasing
  anime, and excludes manga tagged Ecchi. The cache keeps up to five titles per list.
- `.github/scripts/generate_readme.py` owns the profile copy and layout. It shows
  up to three titles per list, with fallbacks when cached data is unavailable.
- `.github/scripts/test_generate_readme.py` covers README generation.

Spotify and Carbonara integrations have been retired. The only required GitHub
secret is `ANILIST_USERNAME`. See `.github/SETUP.md` for setup and behavior.

## Development

Run from `.github/scripts`:

```bash
uv sync
uv run ruff check .
uv run ruff format .
uv run python -m unittest discover -v
uv run python generate_readme.py
```

To fetch current data, set `ANILIST_USERNAME` and run
`uv run python fetch_anilist.py`. Fetch failures are logged and preserve the cache;
they do not currently fail the workflow.

Edit the generator rather than only the README so automated runs preserve the
layout. The workflow stages only `README.md` and `data/anilist.json` and uses
`[Skip GitHub Action]` in update commit messages.
