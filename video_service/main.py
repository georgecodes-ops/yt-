import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.dashboard.streamlit_app import StreamlitApp
from src.content.video_processor import VideoProcessor
from src.analytics.daily_metrics_dashboard import DailyMetricsDashboard
from shared.api_client import APIClient
from shared.config import Config

def main():
    st.set_page_config(
        page_title="Monay Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("🚀 Monay Content Dashboard")
    
    # Initialize components
    app = StreamlitApp()
    video_processor = VideoProcessor()
    metrics = DailyMetricsDashboard()
    api_client = APIClient()
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Dashboard", "Content Creation", "Analytics", "Settings"]
    )
    
    if page == "Dashboard":
        app.show_dashboard()
    elif page == "Content Creation":
        app.show_content_creation()
    elif page == "Analytics":
        app.show_analytics()
    elif page == "Settings":
        app.show_settings()

if __name__ == "__main__":
    main()