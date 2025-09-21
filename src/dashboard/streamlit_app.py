"""
Streamlit Dashboard - Real-time monitoring and analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import asyncio
import logging
# Remove this line (line 13):
# from main import MonAYOrchestrator

class DashboardManager:
    """Manages the Streamlit dashboard"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    async def start_dashboard(self):
        """Start the Streamlit dashboard"""
        self.logger.info("Starting dashboard server...")
        # In production, this would start the Streamlit server
        # For now, we'll create the dashboard structure
        
    async def update_metrics(self, metrics_data=None):
        """Update dashboard metrics"""
        try:
            # Keep only this local import (line 31):
            from enhanced_main import EnhancedMonAYOrchestrator
            orchestrator = EnhancedMonAYOrchestrator()
            
            # Update metrics in session state
            if 'metrics' not in st.session_state:
                st.session_state.metrics = {}
            
            update_data = {
                'last_updated': datetime.now(),
                'status': 'running',
                'active_agents': 0,
                'content_generated': 0
            }
            
            # Merge with provided metrics if any
            if metrics_data:
                update_data.update(metrics_data)
                
            st.session_state.metrics.update(update_data)
            
            return True
        except Exception as e:
            st.error(f"Failed to update metrics: {e}")
            return False

    def update_enhanced_metrics(self, metrics_data):
        """
        Update enhanced metrics for the dashboard
        """
        try:
            import datetime
            
            if not metrics_data:
                metrics_data = self._get_default_metrics()
            
            # Update cache with new metrics
            if not hasattr(self, 'metrics_cache'):
                self.metrics_cache = {}
            
            self.metrics_cache.update({
                'content_performance': metrics_data.get('content_performance', {}),
                'engagement_metrics': metrics_data.get('engagement_metrics', {}),
                'revenue_metrics': metrics_data.get('revenue_metrics', {}),
                'growth_metrics': metrics_data.get('growth_metrics', {}),
                'algorithm_insights': metrics_data.get('algorithm_insights', {}),
                'last_updated': datetime.datetime.now().isoformat()
            })
            
            return {
                'status': 'success',
                'metrics_updated': len(self.metrics_cache)
            }
            
        except Exception as e:
            print(f"Error updating enhanced metrics: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _get_default_metrics(self):
        """Get default metrics when no data is available"""
        return {
            'content_performance': {'total_videos': 0, 'avg_views': 0, 'avg_engagement': 0.0},
            'engagement_metrics': {'likes': 0, 'comments': 0, 'shares': 0, 'retention_rate': 0.0},
            'revenue_metrics': {'total_revenue': 0.0, 'ad_revenue': 0.0, 'affiliate_revenue': 0.0},
            'growth_metrics': {'subscriber_growth': 0, 'view_growth': 0.0, 'engagement_growth': 0.0},
            'algorithm_insights': {'trending_score': 0.5, 'algorithm_fit': 0.5, 'optimization_suggestions': []}
        }

def create_dashboard():
    """Create the main dashboard interface"""
    st.set_page_config(
        page_title="MonAY - YouTube Automation Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("🚀 MonAY - YouTube Automation Dashboard")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Overview", "Agents", "Content", "Revenue", "Analytics", "Settings"]
    )
    
    if page == "Overview":
        show_overview()
    elif page == "Agents":
        show_agents()
    elif page == "Content":
        show_content()
    elif page == "Revenue":
        show_revenue()
    elif page == "Analytics":
        show_analytics()
    elif page == "Settings":
        show_settings()

def show_overview():
    """Show overview dashboard"""
    st.header("📈 System Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Active Agents",
            value="12",
            delta="+2"
        )
    
    with col2:
        st.metric(
            label="Total Revenue (24h)",
            value="$1,247",
            delta="+15.3%"
        )
    
    with col3:
        st.metric(
            label="Videos Uploaded",
            value="48",
            delta="+8"
        )
    
    with col4:
        st.metric(
            label="Total Views",
            value="2.1M",
            delta="+12.7%"
        )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue Trend")
        # Sample data
        dates = pd.date_range(start='2024-01-01', end='2024-01-30', freq='D')
        revenue_data = pd.DataFrame({
            'Date': dates,
            'Revenue': [100 + i*5 + (i%7)*20 for i in range(len(dates))]
        })
        
        fig = px.line(revenue_data, x='Date', y='Revenue', title='Daily Revenue')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Agent Performance")
        agent_data = pd.DataFrame({
            'Agent': [f'Agent {i}' for i in range(1, 11)],
            'Performance': [0.8, 0.9, 0.7, 0.85, 0.92, 0.78, 0.88, 0.83, 0.91, 0.76]
        })
        
        fig = px.bar(agent_data, x='Agent', y='Performance', title='Agent Performance Scores')
        st.plotly_chart(fig, use_container_width=True)

def show_agents():
    """Show agents management page"""
    st.header("🤖 Agent Management")
    
    # Agent list
    st.subheader("Active Agents")
    
    agent_data = pd.DataFrame({
        'Agent ID': [f'agent_{i}' for i in range(1, 13)],
        'Channel Name': [f'AutoChannel {i}' for i in range(1, 13)],
        'Status': ['Active'] * 10 + ['Suspended'] * 2,
        'Revenue (24h)': [f'${i*50 + 100}' for i in range(1, 13)],
        'Videos': [i*2 + 5 for i in range(1, 13)],
        'Subscribers': [f'{i*1000 + 5000}' for i in range(1, 13)]
    })
    
    st.dataframe(agent_data, use_container_width=True)
    
    # Agent actions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Create New Agent"):
            st.success("New agent creation initiated!")
    
    with col2:
        if st.button("Auto-Scale Agents"):
            st.info("Auto-scaling analysis started...")
    
    with col3:
        if st.button("Refresh Data"):
            st.rerun()

def show_content():
    """Show content management page"""
    st.header("📹 Content Management")
    
    # Content pipeline status
    st.subheader("Content Pipeline Status")
    
    pipeline_data = pd.DataFrame({
        'Stage': ['Trend Analysis', 'Content Generation', 'Video Production', 'Upload Queue', 'Published'],
        'Count': [25, 18, 12, 8, 45],
        'Status': ['Active', 'Active', 'Active', 'Active', 'Completed']
    })
    
    st.dataframe(pipeline_data, use_container_width=True)
    
    # Recent uploads
    st.subheader("Recent Uploads")
    
    upload_data = pd.DataFrame({
        'Video Title': [
            'Amazing AI Technology Explained',
            'Top 10 Programming Tips',
            'Climate Change Solutions',
            'Cryptocurrency Guide 2024',
            'Remote Work Best Practices'
        ],
        'Agent': ['agent_1', 'agent_3', 'agent_2', 'agent_5', 'agent_1'],
        'Upload Time': [
            '2024-01-15 14:30',
            '2024-01-15 12:15',
            '2024-01-15 10:45',
            '2024-01-15 09:20',
            '2024-01-15 08:00'
        ],
        'Views': [1250, 890, 2100, 1580, 950],
        'Status': ['Published', 'Published', 'Published', 'Processing', 'Published']
    })
    
    st.dataframe(upload_data, use_container_width=True)

def show_revenue():
    """Show revenue analytics page"""
    st.header("💰 Revenue Analytics")
    
    # Revenue summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Revenue (Month)", "$38,247", "+23.5%")
    
    with col2:
        st.metric("Average RPM", "$2.45", "+0.15")
    
    with col3:
        st.metric("Top Performing Agent", "Agent 5", "$3,247")
    
    # Revenue breakdown
    st.subheader("Revenue Breakdown")
    
    revenue_sources = pd.DataFrame({
        'Source': ['Ad Revenue', 'Channel Memberships', 'Super Chat', 'Merchandise'],
        'Amount': [28500, 5200, 2800, 1747],
        'Percentage': [74.5, 13.6, 7.3, 4.6]
    })
    
    fig = px.pie(revenue_sources, values='Amount', names='Source', title='Revenue by Source')
    st.plotly_chart(fig, use_container_width=True)

def show_analytics():
    """Show detailed analytics page"""
    st.header("📊 Detailed Analytics")
    
    # Trend analysis
    st.subheader("Trending Topics")
    
    trend_data = pd.DataFrame({
        'Topic': ['AI Technology', 'Climate Change', 'Remote Work', 'Cryptocurrency', 'Health Tips'],
        'Trend Score': [95, 87, 82, 78, 75],
        'Predicted Views': [15000, 12000, 10000, 9500, 8500],
        'Competition': ['Medium', 'High', 'Low', 'High', 'Medium']
    })
    
    st.dataframe(trend_data, use_container_width=True)
    
    # Performance metrics
    st.subheader("Performance Metrics")
    
    metrics_data = pd.DataFrame({
        'Metric': ['Click-through Rate', 'Watch Time', 'Engagement Rate', 'Subscriber Growth'],
        'Current': ['3.2%', '4:25', '8.7%', '+125/day'],
        'Target': ['4.0%', '5:00', '10.0%', '+150/day'],
        'Status': ['Below', 'Below', 'Below', 'Below']
    })
    
    st.dataframe(metrics_data, use_container_width=True)

def show_settings():
    """Show settings page"""
    st.header("⚙️ System Settings")
    
    # API Configuration
    st.subheader("API Configuration")
    
    with st.expander("YouTube API"):
        st.text_input("API Key", type="password", placeholder="Enter YouTube API key")
        st.text_input("Client ID", placeholder="Enter Client ID")
        st.number_input("Daily Quota Limit", value=10000)
    
    with st.expander("Ollama Configuration"):
        st.text_input("Host", value="http://localhost:11434", placeholder="Ollama host URL")
        st.selectbox("Model", ["mistral", "llama2", "codellama"])
    
    # System Configuration
    st.subheader("System Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.number_input("Max Agents", value=50, min_value=1, max_value=100)
        st.number_input("Upload Frequency (hours)", value=6, min_value=1, max_value=24)
        st.selectbox("Content Type", ["Educational", "Entertainment", "Mixed"])
    
    with col2:
        st.number_input("Performance Threshold", value=0.8, min_value=0.1, max_value=1.0, step=0.1)
        st.number_input("Revenue Target ($/day)", value=1000, min_value=100)
        st.checkbox("Auto-scaling Enabled", value=True)
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

if __name__ == "__main__":
    create_dashboard()