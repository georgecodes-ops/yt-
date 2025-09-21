#!/usr/bin/env python3
"""
YouTube Token Refresh Script
Refreshes expired YouTube OAuth tokens
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

def refresh_tokens():
    """Refresh YouTube tokens"""
    print("🔄 Refreshing YouTube tokens...")
    
    try:
        from get_youtube_tokens import get_youtube_service
        
        # This will automatically refresh tokens if possible
        service = get_youtube_service()
        
        if service:
            # Test the connection
            try:
                response = service.channels().list(
                    part='snippet',
                    mine=True
                ).execute()
                
                if response.get('items'):
                    channel_title = response['items'][0]['snippet']['title']
                    print(f"✅ Successfully refreshed tokens for channel: {channel_title}")
                    return True
                else:
                    print("❌ No channel found after refresh")
                    return False
            except Exception as e:
                print(f"❌ API test failed after refresh: {e}")
                return False
        else:
            print("❌ Failed to get YouTube service")
            return False
            
    except Exception as e:
        print(f"❌ Token refresh failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 YouTube Token Refresh")
    print("=" * 30)
    
    if not os.path.exists('youtube_tokens.json'):
        print("❌ No YouTube tokens found")
        print("💡 Run: python get_youtube_tokens.py")
        return False
    
    success = refresh_tokens()
    
    if success:
        print("\n🎉 Token refresh successful!")
        print("✅ You can now run: python quick_youtube_test.py")
    else:
        print("\n❌ Token refresh failed")
        print("💡 You may need to re-authenticate:")
        print("   python get_youtube_tokens.py")
    
    return success

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)