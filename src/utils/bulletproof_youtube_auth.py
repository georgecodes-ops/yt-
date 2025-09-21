"""
Bulletproof YouTube Authentication System
Handles token refresh, validation, and fallback scenarios
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class BulletproofYouTubeAuth:
    """Bulletproof YouTube authentication with auto-refresh"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.credentials = None
        self.youtube_service = None
        self.scopes = ['https://www.googleapis.com/auth/youtube.upload']
        
    def get_token_file_path(self) -> Optional[str]:
        """Find YouTube token file with multiple fallback locations"""
        token_files = [
            'youtube_tokens.json',
            '/opt/monay/youtube_tokens.json',
            '/opt/monay/credentials/youtube_tokens.json',
            'credentials.json',
            '/opt/monay/credentials.json'
        ]
        
        for token_file in token_files:
            if os.path.exists(token_file):
                self.logger.info(f"✅ Found token file: {token_file}")
                return token_file
        
        self.logger.warning("⚠️ No token file found")
        return None
    
    def load_credentials(self) -> bool:
        """Load and validate YouTube credentials"""
        try:
            token_file = self.get_token_file_path()
            if not token_file:
                self.logger.warning("No credentials file found")
                return False
            
            with open(token_file, 'r') as f:
                token_data = json.load(f)
            
            # Handle different token formats
            if 'token' in token_data:
                # OAuth token format
                self.credentials = Credentials(
                    token=token_data['token'],
                    refresh_token=token_data.get('refresh_token'),
                    token_uri=token_data.get('token_uri', 'https://oauth2.googleapis.com/token'),
                    client_id=token_data.get('client_id'),
                    client_secret=token_data.get('client_secret'),
                    scopes=self.scopes
                )
            else:
                self.logger.warning("Unknown token format - using fallback")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load credentials: {e}")
            return False
    
    def refresh_credentials(self) -> bool:
        """Refresh expired credentials"""
        try:
            if not self.credentials:
                return False
            
            if self.credentials.expired and self.credentials.refresh_token:
                self.logger.info("🔄 Refreshing expired YouTube credentials...")
                self.credentials.refresh(Request())
                
                # Save refreshed credentials
                token_file = self.get_token_file_path()
                if token_file:
                    token_data = {
                        'token': self.credentials.token,
                        'refresh_token': self.credentials.refresh_token,
                        'token_uri': self.credentials.token_uri,
                        'client_id': self.credentials.client_id,
                        'client_secret': self.credentials.client_secret,
                        'scopes': self.credentials.scopes,
                        'expiry': self.credentials.expiry.isoformat() if self.credentials.expiry else None
                    }
                    
                    with open(token_file, 'w') as f:
                        json.dump(token_data, f, indent=2)
                    
                    self.logger.info("✅ Credentials refreshed and saved")
                
                return True
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to refresh credentials: {e}")
            return False
    
    def get_youtube_service(self):
        """Get authenticated YouTube service with auto-refresh"""
        try:
            if not self.credentials:
                if not self.load_credentials():
                    self.logger.warning("No valid credentials available")
                    return None
            
            # Refresh if needed
            if not self.refresh_credentials():
                self.logger.warning("Failed to refresh credentials")
                return None
            
            # Build YouTube service
            self.youtube_service = build('youtube', 'v3', credentials=self.credentials)
            self.logger.info("✅ YouTube service authenticated successfully")
            return self.youtube_service
            
        except Exception as e:
            self.logger.error(f"Failed to get YouTube service: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Test YouTube API connection"""
        try:
            service = self.get_youtube_service()
            if not service:
                return False
            
            # Test with a simple API call
            channels_response = service.channels().list(part='snippet', mine=True).execute()
            
            if 'items' in channels_response and len(channels_response['items']) > 0:
                channel = channels_response['items'][0]
                self.logger.info(f"✅ Connected to channel: {channel['snippet']['title']}")
                return True
            else:
                self.logger.warning("No channels found for authenticated user")
                return False
                
        except Exception as e:
            self.logger.error(f"YouTube connection test failed: {e}")
            return False

# Global instance for easy access
youtube_auth = BulletproofYouTubeAuth()

def get_youtube_service():
    """Get authenticated YouTube service (global function)"""
    return youtube_auth.get_youtube_service()

def test_youtube_connection():
    """Test YouTube connection (global function)"""
    return youtube_auth.test_connection()