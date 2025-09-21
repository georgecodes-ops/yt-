import os
import json
import webbrowser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# Fixed for Linux/any OS
CLIENT_SECRETS_FILE = "client_secret_919510636273.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
          'https://www.googleapis.com/auth/youtube.readonly']
TOKEN_FILE = "youtube_tokens.json"

def validate_youtube_tokens():
    """Validate existing YouTube tokens"""
    try:
        if not os.path.exists(TOKEN_FILE):
            return False
        
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        
        if not creds:
            return False
        
        # If expired but has refresh token, try to refresh
        if creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                # Save refreshed tokens
                with open(TOKEN_FILE, 'w') as token:
                    token.write(creds.to_json())
                return True
            except Exception:
                return False
        
        return creds.valid
    except Exception:
        return False

def get_youtube_service():
    """Get authenticated YouTube service"""
    creds = None
    
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRETS_FILE):
                print(f"❌ {CLIENT_SECRETS_FILE} not found!")
                return None
                
            flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            flow.redirect_uri = 'http://localhost:8080/oauth2callback'  # Match your redirect URI
            
            auth_url, _ = flow.authorization_url(prompt='consent')
            print(f"🌐 Open this URL: {auth_url}")
            webbrowser.open(auth_url)
            
            code = input('🔑 Enter authorization code: ')
            flow.fetch_token(code=code)
            creds = flow.credentials
            
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
    
    return build('youtube', 'v3', credentials=creds)

if __name__ == "__main__":
    print("🚀 Setting up YouTube authentication...")
    service = get_youtube_service()
    if service:
        print("✅ YouTube authentication complete!")
    else:
        print("❌ Authentication failed")