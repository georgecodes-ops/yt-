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
                return True
            except Exception:
                return False
        
        return creds.valid
    except Exception:
        return False

def get_youtube_service():
    """Get authenticated YouTube service object"""
    try:
        creds = None
        token_file = 'youtube_tokens.json'
        credentials_file = 'client_secret_919510636273-6irenq7b2tncl8r5pqajh9t8fp1n73.apps.googleusercontent.com.json'
        
        # Check if token file exists
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logging.warning(f"Token refresh failed: {e}")
                    creds = None
            
            if not creds:
                if os.path.exists(credentials_file):
                    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                    creds = flow.run_local_server(port=0)
                else:
                    logging.error(f"Credentials file not found: {credentials_file}")
                    return None
            
            # Save the credentials for the next run
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        
        # Build and return the YouTube service
        youtube = build('youtube', 'v3', credentials=creds)
        logging.info("✅ YouTube service initialized successfully")
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