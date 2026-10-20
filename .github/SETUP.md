# GitHub Profile Automation

The profile is a text-first professional introduction with a collapsed
**Outside of work** section. AniList supplies up to three currently watching
and reading titles; Spotify widgets, music fetching, and generated image banners
are no longer used.

## How it works

The `update-profile.yml` workflow runs every six hours, on pushes to `main` or
`master`, or by manual dispatch. It installs Python 3.13 and dependencies with uv,
runs Ruff and generator tests, fetches AniList data, generates `README.md`, and
commits changes to the README and AniList cache.

- `.github/scripts/fetch_anilist.py` queries AniList's public GraphQL API and
  writes `data/anilist.json`.
- `.github/scripts/generate_readme.py` owns the introduction and interests layout.
  Edit this template, not just the generated README, to preserve changes across
  automated updates.
- `.github/scripts/test_generate_readme.py` tests generation from cached and
  missing data.

## Configuration

Set the repository secret `ANILIST_USERNAME` to your AniList username. No API key
is required. Existing Spotify secrets are unused and can be removed from the
repository settings.

## Local development

Run these commands from `.github/scripts`:

```bash
uv sync
uv run ruff check .
uv run python -m unittest discover -v
uv run python generate_readme.py
```

To refresh the AniList cache, set `ANILIST_USERNAME` and run:

```bash
uv run python fetch_anilist.py
```

The fetcher excludes unreleased anime, prioritizes releasing anime, and excludes
manga tagged Ecchi. The cache keeps up to five titles per list; the profile shows
the first three. Missing credentials or fetch failures preserve the existing
cache. Missing or invalid cache files render “Nothing currently.” for both lists.

Use the Actions logs to inspect fetch failures; the AniList fetcher currently logs
errors without failing the workflow.
