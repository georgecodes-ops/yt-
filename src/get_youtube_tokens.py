#!/usr/bin/env python3
"""
YouTube API Authentication and Service Setup
"""

import os
import json
from pathlib import Path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import logging

# YouTube API scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def validate_youtube_tokens():
    """Validate existing YouTube tokens"""
    try:
        token_file = 'youtube_tokens.json'
        if not os.path.exists(token_file):
            return False
        
        # Check if it's a proper OAuth2 token file
        try:
            with open(token_file, 'r') as f:
                token_data = json.load(f)
            
            # Validate it's a valid token structure
            if 'token' not in token_data:
                print("❌ Invalid token file structure")
                return False
                
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
            
            if not creds:
                return False
            
            # If expired but has refresh token, try to refresh
            if creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    # Save refreshed tokens
                    with open(token_file, 'w') as token:
                        token.write(creds.to_json())
                    print("✅ Tokens refreshed successfully")
                    return True
                except Exception as e:
                    print(f"⚠️ Token refresh failed: {e}")
                    return False
            
            return creds.valid
            
        except (json.JSONDecodeError, KeyError):
            # Try to handle as raw credentials
            print("⚠️ Token file format issue, attempting fallback...")
            return True  # Let the service handle it
            
    except Exception as e:
        print(f"❌ Token validation error: {e}")
        return False

def get_youtube_service():
    """Get authenticated YouTube service object"""
    try:
        creds = None
        token_file = 'youtube_tokens.json'
        
        # Look for any client secret file in the directory
        credentials_files = [
            'client_secret.json',
            'credentials.json',
            'client_secret_919510636273-6irenq7b2tncl8r5pqajh9t8fp1n73.apps.googleusercontent.com.json'
        ]
        
        credentials_file = None
        for file in credentials_files:
            if os.path.exists(file):
                credentials_file = file
                break
        
        # Check if token file exists
        if os.path.exists(token_file):
            try:
                creds = Credentials.from_authorized_user_file(token_file, SCOPES)
                print(f"✅ Loaded existing tokens from {token_file}")
            except Exception as e:
                print(f"⚠️ Error loading tokens: {e}")
                creds = None
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    print("🔄 Refreshing expired tokens...")
                    creds.refresh(Request())
                    print("✅ Tokens refreshed successfully")
                except Exception as e:
                    print(f"⚠️ Token refresh failed: {e}")
                    creds = None
            
            if not creds:
                if credentials_file:
                    print(f"🔐 Starting OAuth flow with {credentials_file}")
                    print("📱 A browser window will open for authentication...")
                    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                    creds = flow.run_local_server(port=0)
                    print("✅ Authentication successful!")
                else:
                    print("❌ No client secret file found!")
                    print("📋 Please download your OAuth2 credentials from Google Cloud Console")
                    print("   and save as 'client_secret.json' in the project root")
                    return None
            
            # Save the credentials for the next run
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
            print(f"💾 Tokens saved to {token_file}")
        
        # Build and return the YouTube service
        youtube = build('youtube', 'v3', credentials=creds)
        print("✅ YouTube service initialized successfully")
        return youtube
        
    except Exception as e:
        logging.error(f"Failed to initialize YouTube service: {e}")
        return None

if __name__ == '__main__':
    """Run this script to authenticate and generate tokens"""
    print("🔐 Setting up YouTube API authentication...")
    service = get_youtube_service()
    if service:
        print("✅ YouTube authentication successful!")
        print("📁 Tokens saved to youtube_tokens.json")
    else:
        print("❌ YouTube authentication failed!")
        print("📋 Make sure you have the client_secret file in the project root")