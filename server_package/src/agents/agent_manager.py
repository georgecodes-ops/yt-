"""
Agent Manager - Handles multiple YouTube accounts and channels
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path  # Add this line

@dataclass
class Agent:
    """Represents a YouTube channel agent"""
    id: str
    channel_id: str
    channel_name: str
    access_token: str
    refresh_token: str
    created_at: datetime
    last_upload: Optional[datetime] = None
    total_revenue: float = 0.0
    total_views: int = 0
    subscriber_count: int = 0
    video_count: int = 0
    quota_used: int = 0
    quota_limit: int = 10000
    status: str = "active"  # active, suspended, quota_exceeded
    performance_score: float = 0.0

# Change relative import to absolute import
# Fix this import (line 31):
from utils.simple_storage import SimpleFileStorage  # Changed from "from src.utils.simple_storage import SimpleFileStorage"
import json

class AgentManager:
    def __init__(self):
        self.agents = {}
        self.logger = logging.getLogger(__name__)
        self.storage = SimpleFileStorage()
    
    async def initialize(self):
        """Initialize the agent manager and load existing agents"""
        self.logger.info("Initializing Agent Manager...")
        await self.load_existing_agents()
        self.logger.info(f"Agent Manager initialized with {len(self.agents)} agents")
        return True
    
    async def load_existing_agents(self):
        """Load existing agents from file storage"""
        try:
            agents_data = self.storage.load_agents()
            
            for agent_id, agent_data in agents_data.items():
                agent = Agent(
                    id=agent_data['id'],
                    channel_id=agent_data['channel_id'],
                    channel_name=agent_data['channel_name'],
                    access_token=agent_data.get('access_token', 'demo_token'),
                    refresh_token=agent_data.get('refresh_token', 'demo_refresh'),
                    created_at=datetime.fromisoformat(agent_data['created_at']) if 'created_at' in agent_data else datetime.now(),
                    last_upload=datetime.fromisoformat(agent_data['last_upload']) if agent_data.get('last_upload') else None,
                    total_revenue=agent_data.get('total_revenue', 0.0),
                    total_views=agent_data.get('total_views', 0),
                    subscriber_count=agent_data.get('subscriber_count', 0),
                    video_count=agent_data.get('video_count', 0),
                    quota_used=agent_data.get('quota_used', 0),
                    quota_limit=agent_data.get('quota_limit', 10000),
                    status=agent_data.get('status', 'active'),
                    performance_score=agent_data.get('performance_score', 0.0)
                )
                self.agents[agent.id] = agent
            
            if not self.agents:
                # Create demo agents for testing
                await self.create_demo_agents()
            
            self.logger.info(f"Loaded {len(self.agents)} agents from file storage")
            
        except Exception as e:
            self.logger.error(f"Error loading agents: {e}")
            await self.create_demo_agents()
    
    async def create_demo_agents(self):
        """Create demo agents for testing"""
        demo_agents = [
            {
                'id': 'agent_001',
                'channel_id': 'demo_channel_1',
                'channel_name': 'MonAY Demo Channel 1',
                'access_token': 'demo_token_1',
                'refresh_token': 'demo_refresh_1'
            },
            {
                'id': 'agent_002', 
                'channel_id': 'demo_channel_2',
                'channel_name': 'MonAY Demo Channel 2',
                'access_token': 'demo_token_2',
                'refresh_token': 'demo_refresh_2'
            }
        ]
        
        for agent_data in demo_agents:
            agent = Agent(
                id=agent_data['id'],
                channel_id=agent_data['channel_id'],
                channel_name=agent_data['channel_name'],
                access_token=agent_data['access_token'],
                refresh_token=agent_data['refresh_token'],
                created_at=datetime.now()
            )
            self.agents[agent.id] = agent
        
        await self.save_agents_data()
        self.logger.info("Created demo agents for testing")
    
    async def save_agents_data(self):
        """Save agents data to file storage"""
        try:
            agents_data = {}
            for agent_id, agent in self.agents.items():
                agents_data[agent_id] = {
                    'id': agent.id,
                    'channel_id': agent.channel_id,
                    'channel_name': agent.channel_name,
                    'access_token': agent.access_token,
                    'refresh_token': agent.refresh_token,
                    'created_at': agent.created_at.isoformat(),
                    'last_upload': agent.last_upload.isoformat() if agent.last_upload else None,
                    'total_revenue': agent.total_revenue,
                    'total_views': agent.total_views,
                    'subscriber_count': agent.subscriber_count,
                    'video_count': agent.video_count,
                    'quota_used': agent.quota_used,
                    'quota_limit': agent.quota_limit,
                    'status': agent.status,
                    'performance_score': agent.performance_score
                }
            
            self.storage.save_agents(agents_data)
            
        except Exception as e:
            self.logger.error(f"Error saving agents data: {e}")
    
    def get_active_agent_count(self) -> int:
        """Get count of active agents"""
        return len([a for a in self.agents.values() if a.status == "active"])
    
    def get_next_available_agent(self) -> Optional[Agent]:
        """Get the next available agent for content upload"""
        available_agents = [
            agent for agent in self.agents.values()
            if agent.status == "active" and agent.quota_used < agent.quota_limit * 0.9
        ]
        
        if not available_agents:
            # Auto-create demo agent if none available
            self.logger.warning("No available agents, creating demo agent")
            demo_agent = self._create_demo_agent()
            self.agents[demo_agent.id] = demo_agent
            return demo_agent
        
        # Return agent with lowest recent activity
        return min(available_agents, key=lambda a: a.quota_used)
    
    async def update_agent_performance(self, agent_id: str, metrics: Dict) -> bool:
        """Update agent performance metrics"""
        try:
            if agent_id not in self.agents:
                self.logger.error(f"Agent {agent_id} not found")
                return False
            
            agent = self.agents[agent_id]
            
            # Update metrics
            agent.total_revenue += metrics.get('revenue', 0)
            agent.total_views += metrics.get('views', 0)
            agent.subscriber_count = metrics.get('subscribers', agent.subscriber_count)
            agent.video_count += metrics.get('videos_uploaded', 0)
            agent.quota_used += metrics.get('quota_used', 0)
            
            # Update last upload time if video was uploaded
            if metrics.get('videos_uploaded', 0) > 0:
                agent.last_upload = datetime.now()
            
            # Recalculate performance score
            agent.performance_score = self.calculate_performance_score(agent)
            
            # Check if agent should be suspended due to poor performance
            if agent.performance_score < 0.3 and agent.video_count > 10:
                agent.status = "suspended"
                self.logger.warning(f"Agent {agent_id} suspended due to poor performance")
            
            # Check quota limits
            if agent.quota_used >= agent.quota_limit:
                agent.status = "quota_exceeded"
                self.logger.warning(f"Agent {agent_id} exceeded quota limit")
            
            # Save updated agent data
            await self.save_agents_data()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating agent performance: {e}")
            return False
    
    async def save_agents_data(self):
        """Save agents data to persistent storage"""
        try:
            agents_file = Path("data/agents.json")
            agents_file.parent.mkdir(exist_ok=True)
            
            agents_data = []
            for agent in self.agents.values():
                agent_dict = {
                    'id': agent.id,
                    'channel_id': agent.channel_id,
                    'channel_name': agent.channel_name,
                    'access_token': agent.access_token,
                    'refresh_token': agent.refresh_token,
                    'created_at': agent.created_at.isoformat(),
                    'last_upload': agent.last_upload.isoformat() if agent.last_upload else None,
                    'total_revenue': agent.total_revenue,
                    'total_views': agent.total_views,
                    'subscriber_count': agent.subscriber_count,
                    'video_count': agent.video_count,
                    'quota_used': agent.quota_used,
                    'quota_limit': agent.quota_limit,
                    'status': agent.status,
                    'performance_score': agent.performance_score
                }
                agents_data.append(agent_dict)
            
            with open(agents_file, 'w') as f:
                json.dump(agents_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error saving agents data: {e}")
    
    def get_active_agent_count(self) -> int:
        """Get count of active agents"""
        return len([a for a in self.agents.values() if a.status == "active"])
    
    def get_next_available_agent(self) -> Agent:
        """Get next available agent - Fixed to always return an agent"""
        available_agents = [
            agent for agent in self.agents.values() 
            if agent.status == 'active' and agent.quota_used < agent.quota_limit
        ]
        
        if not available_agents:
            # Auto-create demo agent if none available
            self.logger.warning("No available agents, creating demo agent")
            demo_agent = self._create_demo_agent()
            self.agents[demo_agent.id] = demo_agent
            return demo_agent
        
        # Return agent with best performance score
        return max(available_agents, key=lambda x: x.performance_score)
    
    def _create_demo_agent(self) -> Agent:
        """Create a demo agent for testing"""
        agent_id = f"demo_agent_{len(self.agents) + 1}"
        return Agent(
            id=agent_id,
            channel_id=f"demo_channel_{len(self.agents) + 1}",
            channel_name=f"MonAY Demo Channel {len(self.agents) + 1}",
            access_token="demo_token",
            refresh_token="demo_refresh",
            created_at=datetime.now(),
            status="active",
            performance_score=0.5
        )
    
    async def update_agent_performance(self, agent_id: str, metrics: Dict) -> bool:
        """Update agent performance metrics"""
        try:
            if agent_id not in self.agents:
                self.logger.warning(f"Agent {agent_id} not found")
                return False
            
            agent = self.agents[agent_id]
            agent.total_revenue += metrics.get('revenue', 0)
            agent.total_views += metrics.get('views', 0)
            agent.subscriber_count = metrics.get('subscribers', agent.subscriber_count)
            agent.performance_score = self.calculate_performance_score(agent)
            
            self.logger.info(f"Updated performance for agent {agent_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating agent performance: {e}")
            return False
        agent.video_count += metrics.get('new_videos', 0)
        agent.quota_used += metrics.get('quota_used', 0)
        
        # Calculate performance score
        agent.performance_score = self.calculate_performance_score(agent)
        
        self.logger.info(f"Updated performance for {agent_id}: score={agent.performance_score:.2f}")
    
    def calculate_performance_score(self, agent: Agent) -> float:
        """Calculate performance score for an agent"""
        # Simple scoring based on revenue per video and engagement
        if agent.video_count == 0:
            return 0.0
        
        revenue_per_video = agent.total_revenue / agent.video_count
        views_per_video = agent.total_views / agent.video_count
        
        # Normalize and combine metrics
        score = min(1.0, (revenue_per_video / 100) * 0.6 + (views_per_video / 10000) * 0.4)
        return score
    
    async def auto_scale_agents(self):
        """Automatically scale agents based on performance"""
        high_performers = [
            agent for agent in self.agents.values()
            if agent.performance_score > self.performance_threshold
        ]
        
        # Scale up if we have high performers and room for more agents
        if len(high_performers) > len(self.agents) * 0.7 and len(self.agents) < self.max_agents:
            await self.create_new_agent()
        
        # Scale down poor performers
        poor_performers = [
            agent for agent in self.agents.values()
            if agent.performance_score < 0.3 and 
            (datetime.now() - agent.created_at).days > 30
        ]
        
        for agent in poor_performers[:2]:  # Limit removals
            await self.deactivate_agent(agent.id)
    
    async def create_new_agent(self):
        """Create a new agent by cloning a high performer"""
        # Find best performing agent to clone
        best_agent = max(self.agents.values(), key=lambda a: a.performance_score)
        
        new_id = f"agent_{len(self.agents) + 1}"
        new_agent = Agent(
            id=new_id,
            channel_id=f"channel_{len(self.agents) + 1}",
            channel_name=f"Clone of {best_agent.channel_name}",
            access_token=f"token_{new_id}",
            refresh_token=f"refresh_{new_id}",
            created_at=datetime.now()
        )
        
        self.agents[new_id] = new_agent
        self.logger.info(f"Created new agent: {new_id} (cloned from {best_agent.id})")
    
    async def deactivate_agent(self, agent_id: str):
        """Deactivate a poor performing agent"""
        if agent_id in self.agents:
            self.agents[agent_id].status = "suspended"
            self.logger.info(f"Deactivated agent: {agent_id}")
    
    def update_channel_info(self, channel_id: str, channel_title: str):
        """Update channel information for the current agent"""
        self.logger.info(f"Updating channel info: {channel_title} (ID: {channel_id})")
        
        # Update the current agent's channel info if it exists
        for agent_id, agent in self.agents.items():
            if agent.channel_id == channel_id:
                agent.channel_name = channel_title
                self.logger.info(f"Updated agent {agent_id} with channel info")
                break
        else:
            # If no existing agent found, log the channel info for future use
            self.logger.info(f"Channel info stored: {channel_title} (ID: {channel_id})")
    
    async def cleanup(self):
        """Cleanup agent manager resources"""
        self.logger.info("Cleaning up Agent Manager...")
        # Save agent states, close connections, etc.

    # Around lines 84, 92 - fix missing returns
    async def create_agent(self, agent_config: Dict) -> Dict:
        try:
            agent_id = agent_config['id']
            agent_data = {
                'agent_id': agent_id,
                'name': agent_config['name'],
                'type': agent_config['type'],
                'status': 'active',
                'created_at': datetime.now().isoformat()
            }
            
            self.agents[agent_id] = agent_data
            return agent_data  # Fix: Return agent data
            
        except Exception as e:
            self.logger.error(f"Agent creation failed: {e}")
            return {'status': 'failed', 'error': str(e)}  # Return error dict
    
    async def update_agent_status(self, agent_id: str, status: str) -> Dict:
        try:
            if agent_id in self.agents:
                self.agents[agent_id]['status'] = status
                self.agents[agent_id]['updated_at'] = datetime.now().isoformat()
                
                return {
                    'agent_id': agent_id,
                    'status': status,
                    'updated': True
                }  # Fix: Return update result
            else:
                return {
                    'agent_id': agent_id,
                    'status': 'not_found',
                    'updated': False
                }  # Return not found result
                
        except Exception as e:
            self.logger.error(f"Agent status update failed: {e}")
            return {'status': 'failed', 'error': str(e)}  # Return error dict

    # Fix missing return in agent management
    async def manage_agents(self, task_data: Dict) -> Dict:
        try:
            # Agent management logic
            agent_results = await self._execute_agent_tasks(task_data)
            return {
                'status': 'completed',
                'agent_results': agent_results,
                'task_id': task_data.get('id'),
                'completed_at': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Agent management failed: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'task_data': task_data
            }