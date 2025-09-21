"""
Browser Manager - Handles headless browser setup for server environments
"""

import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class BrowserManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.driver = None
        
    def setup_headless_browser(self):
        """Setup headless Chrome browser for server environment"""
        try:
            chrome_options = Options()
            
            # Essential headless options for servers
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-images')
            chrome_options.add_argument('--disable-javascript')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
            
            # Try different Chrome paths
            chrome_paths = [
                '/usr/bin/chromium-browser',
                '/usr/bin/google-chrome',
                '/usr/bin/chrome',
                '/snap/bin/chromium'
            ]
            
            chrome_binary = None
            for path in chrome_paths:
                if os.path.exists(path):
                    chrome_binary = path
                    break
                    
            if chrome_binary:
                chrome_options.binary_location = chrome_binary
                self.logger.info(f"Using Chrome binary: {chrome_binary}")
            
            # Setup ChromeDriver
            try:
                service = Service(ChromeDriverManager().install())
            except Exception:
                # Fallback to system chromedriver
                service = Service('/usr/bin/chromedriver')
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.logger.info("✅ Headless browser setup successful")
            return self.driver
            
        except Exception as e:
            self.logger.error(f"❌ Browser setup failed: {e}")
            return None
            
    def close_browser(self):
        """Close browser safely"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("Browser closed successfully")
            except Exception as e:
                self.logger.error(f"Error closing browser: {e}")