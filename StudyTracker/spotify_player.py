import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
import http.server
import socketserver
import threading
import urllib.parse
import json
from tkinter import messagebox

# Load environment variables
load_dotenv()

class SpotifyAuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        if 'code' in query_components:
            self.server.auth_code = query_components['code'][0]

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b"""
            <html>
                <body>
                    <h1>Authentication Successful!</h1>
                    <p>You can now close this window and return to the Study Tracker app.</p>
                </body>
            </html>
            """)
        else:
            self.send_error(400, "Authorization code not found")


class SpotifyPlayer:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:8888/callback')
        self.preset_playlist_uri = os.getenv('SPOTIFY_PRESET_PLAYLIST_URI')

        if not self.client_id or not self.client_secret:
            raise ValueError("Spotify credentials not found in environment variables")

        self.scope = 'user-library-read user-modify-playback-state user-read-playback-state playlist-read-private'
        self.sp_oauth = None
        self.sp = None
        self.token_cache_path = os.path.expanduser('~/.spotify_token_cache')
        self.current_device_id = None

    def get_active_device(self):
        """Get the ID of an active Spotify device."""
        try:
            devices = self.sp.devices()
            active_devices = [d for d in devices['devices'] if d['is_active']]

            if active_devices:
                # Use the currently active device
                return active_devices[0]['id']
            elif devices['devices']:
                # If no active device but devices exist, use the first available one
                return devices['devices'][0]['id']
            else:
                messagebox.showwarning(
                    "No Spotify Devices",
                    "Please open Spotify on your computer or phone first."
                )
                return None
        except Exception as e:
            print(f"Error getting devices: {e}")
            return None

    def ensure_device_active(self):
        """Ensure there's an active device and update the current_device_id."""
        if not self.current_device_id:
            self.current_device_id = self.get_active_device()
        return self.current_device_id is not None

    def start_local_server(self):
        # Find an available port
        for port in range(8888, 8900):
            try:
                self.server = socketserver.TCPServer(('localhost', port), SpotifyAuthHandler)
                self.server.auth_code = None
                break
            except OSError:
                continue

        # Start server in a separate thread
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        return port

    def authenticate(self):
        # Initialize OAuth object
        self.sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            cache_path=self.token_cache_path
        )

        # Check for existing cached token
        token_info = self.sp_oauth.get_cached_token()

        if token_info:
            # Use cached token if available
            self.sp = spotipy.Spotify(auth=token_info['access_token'])
            return True

        # Start local server to handle callback
        port = self.start_local_server()
        redirect_uri = f'http://localhost:{port}'

        # Generate authorization URL - removed show_dialog parameter
        auth_url = self.sp_oauth.get_authorize_url()

        # Open browser for user to authenticate
        webbrowser.open(auth_url)

        # Wait for authorization code (with timeout)
        timeout = 300  # 5 minutes
        for _ in range(timeout):
            if self.server.auth_code:
                # Exchange code for access token
                token_info = self.sp_oauth.get_access_token(self.server.auth_code)

                # Create Spotify client
                self.sp = spotipy.Spotify(auth=token_info['access_token'])

                # Close the server
                self.server.shutdown()
                self.server.server_close()

                return True

            # Wait a bit before checking again
            import time
            time.sleep(1)

        raise Exception("Authentication timed out")

    def play_preset_playlist(self):
        if not self.sp:
            raise Exception("Not authenticated with Spotify")

        if not self.preset_playlist_uri:
            raise Exception("No preset playlist configured")

        try:
            # Play the preset playlist
            self.sp.start_playback(context_uri=self.preset_playlist_uri)
            return True
        except Exception as e:
            print(f"Error playing playlist: {e}")
            return False

    def play(self):
        """Start or resume playback."""
        if not self.ensure_device_active():
            return

        try:
            self.sp.start_playback(device_id=self.current_device_id)
        except Exception as e:
            if "NO_ACTIVE_DEVICE" in str(e):
                messagebox.showwarning(
                    "Playback Error",
                    "Please open Spotify on your computer or phone first."
                )
            else:
                print(f"Error starting playback: {e}")

    def pause(self):
        """Pause playback."""
        if not self.ensure_device_active():
            return

        try:
            self.sp.pause_playback(device_id=self.current_device_id)
        except Exception as e:
            print(f"Error pausing playback: {e}")

    def next(self):
        """Skip to next track."""
        if not self.ensure_device_active():
            return

        try:
            self.sp.next_track(device_id=self.current_device_id)
        except Exception as e:
            print(f"Error skipping track: {e}")

    def previous(self):
        """Go to previous track."""
        if not self.ensure_device_active():
            return

        try:
            self.sp.previous_track(device_id=self.current_device_id)
        except Exception as e:
            print(f"Error going to previous track: {e}")

    def is_playing(self):
        """Check if music is currently playing."""
        try:
            current_playback = self.sp.current_playback()
            return current_playback['is_playing'] if current_playback else False
        except Exception as e:
            print(f"Error checking playback status: {e}")
            return False
