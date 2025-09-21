import json
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class ChannelVerifier:
    def __init__(self, tokens_path="youtube_tokens.json"):
        self.tokens_path = tokens_path
        self.youtube = None
        
    def load_credentials(self):
        """Load YouTube API credentials from tokens file"""
        try:
            if not os.path.exists(self.tokens_path):
                print(f"❌ Tokens file not found: {self.tokens_path}")
                return False
                
            # Use the SAME scopes as your OAuth setup
            creds = Credentials.from_authorized_user_file(
                self.tokens_path,
                scopes=[
                    'https://www.googleapis.com/auth/youtube.upload',
                    'https://www.googleapis.com/auth/youtube.readonly'
                ]
            )
            
            self.youtube = build("youtube", "v3", credentials=creds)
            print("✅ Successfully loaded YouTube API credentials")
            return True
            
        except Exception as e:
            print(f"❌ Error loading credentials: {str(e)}")
            return False
    
    def verify_connected_channel(self):
        """Verify which YouTube channel the tokens are connected to"""
        if not self.load_credentials():
            return None
            
        try:
            # Get channel information for authenticated user
            response = self.youtube.channels().list(
                part="snippet,contentDetails,statistics,brandingSettings",
                mine=True
            ).execute()
            
            channels = response.get("items", [])
            
            if not channels:
                print("❌ No channels found for this account")
                return None
                
            print("\n" + "="*60)
            print("🎯 CONNECTED YOUTUBE CHANNEL VERIFICATION")
            print("="*60)
            
            for i, channel in enumerate(channels, 1):
                snippet = channel.get('snippet', {})
                statistics = channel.get('statistics', {})
                branding = channel.get('brandingSettings', {}).get('channel', {})
                
                print(f"\n📺 Channel #{i}:")
                print(f"   Title: {snippet.get('title', 'N/A')}")
                print(f"   Channel ID: {channel.get('id', 'N/A')}")
                print(f"   Handle: @{branding.get('unsubscribedTrailer', 'N/A')}")
                print(f"   Description: {snippet.get('description', 'N/A')[:100]}...")
                print(f"   Country: {snippet.get('country', 'N/A')}")
                print(f"   Created: {snippet.get('publishedAt', 'N/A')}")
                print(f"   Subscribers: {statistics.get('subscriberCount', 'Hidden')}")
                print(f"   Total Views: {statistics.get('viewCount', '0')}")
                print(f"   Video Count: {statistics.get('videoCount', '0')}")
                
            print("\n" + "="*60)
            
            return channels[0] if channels else None
            
        except HttpError as e:
            print(f"❌ YouTube API Error: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return None
    
    def check_upload_permissions(self):
        """Check if the tokens have upload permissions"""
        try:
            # Try to get upload playlist (requires upload scope)
            response = self.youtube.channels().list(
                part="contentDetails",
                mine=True
            ).execute()
            
            if response.get("items"):
                upload_playlist = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
                print(f"✅ Upload permissions verified - Upload Playlist ID: {upload_playlist}")
                return True
            else:
                print("❌ No upload permissions or channel access")
                return False
                
        except HttpError as e:
            if "insufficient permissions" in str(e).lower():
                print("⚠️  Limited permissions - may need to re-authorize with upload scope")
            else:
                print(f"❌ Permission check failed: {e}")
            return False

def main():
    """Main verification function"""
    print("🔍 MonAY System - YouTube Channel Verification")
    print("=" * 50)
    
    verifier = ChannelVerifier()
    
    # Verify connected channel
    channel_info = verifier.verify_connected_channel()
    
    if channel_info:
        print("\n✅ Channel verification completed successfully!")
        
        # Check upload permissions
        print("\n🔐 Checking upload permissions...")
        verifier.check_upload_permissions()
        
        # Save channel info for MonAY system
        channel_data = {
            "channel_id": channel_info.get('id'),
            "channel_title": channel_info.get('snippet', {}).get('title'),
            "verified_at": str(datetime.now())
        }
        
        with open("verified_channel.json", "w") as f:
            json.dump(channel_data, f, indent=2)
            
        print(f"\n💾 Channel info saved to verified_channel.json")
        
    else:
        print("\n❌ Channel verification failed!")
        print("\n🔧 Troubleshooting steps:")
        print("1. Check if youtube_tokens.json exists")
        print("2. Re-run OAuth authorization with correct Google account")
        print("3. Ensure you have YouTube channel access")

if __name__ == "__main__":
    from datetime import datetime
    main()