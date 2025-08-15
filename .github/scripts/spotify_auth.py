#!/usr/bin/env python3
"""Automated Spotify OAuth flow to get refresh token."""

import base64
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from urllib.parse import parse_qs, urlparse

import httpx


class AuthHandler(BaseHTTPRequestHandler):
    """HTTP handler for OAuth callback."""

    def do_GET(self):
        """Handle GET request with authorization code."""
        if self.path.startswith("/callback"):
            # Parse the authorization code from URL
            parsed_url = urlparse(self.path)
            params = parse_qs(parsed_url.query)

            if "code" in params:
                self.server.auth_code = params["code"][0]
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"""
                <html><body>
                <h1>Success!</h1>
                <p>Authorization code received. You can close this window.</p>
                <script>window.close();</script>
                </body></html>
                """)
            else:
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"<html><body><h1>Error: No authorization code</h1></body></html>")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, fmt, *args):
        """Override to suppress HTTP server log messages."""
        pass


async def get_refresh_token(client_id: str, client_secret: str) -> str:
    """Get Spotify refresh token through automated OAuth flow."""
    redirect_uri = "http://127.0.0.1:3000/callback"

    # Start local server
    server = HTTPServer(("127.0.0.1", 3000), AuthHandler)
    server.auth_code = None
    server_thread = Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    print("🌐 Starting local server at http://127.0.0.1:3000")

    # Build authorization URL
    auth_params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "user-top-read",
    }
    auth_url = f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(auth_params)}"

    print("🔐 Opening browser for Spotify authorization...")
    print(f"    If browser doesn't open, visit: {auth_url}")

    # Open browser
    webbrowser.open(auth_url)

    # Wait for authorization code
    print("⏳ Waiting for authorization code...")
    while server.auth_code is None:
        import time

        time.sleep(0.1)

    print("✅ Authorization code received!")
    auth_code = server.auth_code
    server.shutdown()

    # Exchange code for tokens
    print("🔄 Exchanging code for refresh token...")

    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://accounts.spotify.com/api/token",
            headers={
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "grant_type": "authorization_code",
                "code": auth_code,
                "redirect_uri": redirect_uri,
            },
        )

        if response.status_code != 200:
            print(f"❌ Error: {response.text}")
            return None

        token_data = response.json()
        return token_data.get("refresh_token")


async def main():
    """Main function."""
    print("🎵 Spotify OAuth Automation Tool")
    print("=" * 50)

    # Get credentials from user
    client_id = input("Enter your Spotify Client ID: ").strip()
    client_secret = input("Enter your Spotify Client Secret: ").strip()

    if not client_id or not client_secret:
        print("❌ Both Client ID and Client Secret are required!")
        return

    print("\n📋 Setup Instructions:")
    print("1. Go to https://developer.spotify.com/dashboard")
    print("2. Open your Spotify app settings")
    print("3. Add this redirect URI: http://127.0.0.1:3000/callback")
    print("4. Save the settings")

    input("\nPress Enter when you've completed the setup...")

    # Get refresh token
    refresh_token = await get_refresh_token(client_id, client_secret)

    if refresh_token:
        print("\n🎉 Success! Your Spotify refresh token:")
        print("=" * 50)
        print(refresh_token)
        print("=" * 50)
        print("\n📝 Add this to your GitHub repository secrets as:")
        print("   SPOTIFY_REFRESH_TOKEN")
        print("\n🔒 Keep this token secure - it provides access to your Spotify data!")
    else:
        print("\n❌ Failed to get refresh token. Please try again.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
