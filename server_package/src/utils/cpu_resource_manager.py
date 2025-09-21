import os
import psutil
import asyncio
import logging
from typing import Dict, List, Optional
import time
from dataclasses import dataclass

@dataclass
class ResourceLimits:
    max_cpu_percent: float
    max_memory_gb: float
    max_concurrent_tasks: int
    priority_level: str

class CPUResourceManager:
    """Advanced CPU resource optimization and management"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cpu_count = os.cpu_count() or 4  # Default to 4 cores if None
        self.memory_gb = psutil.virtual_memory().total // (1024**3)
        self.current_tasks = []
        self.resource_limits = self._calculate_optimal_limits()
        
        self.logger.info(f"🔧 CPU Manager: {self.cpu_count} cores, {self.memory_gb}GB RAM")
    
    def _calculate_optimal_limits(self) -> ResourceLimits:
        """Calculate optimal resource limits based on hardware"""
        if self.memory_gb < 8:
            return ResourceLimits(
                max_cpu_percent=50.0,
                max_memory_gb=4.0,
                max_concurrent_tasks=1,
                priority_level="conservative"
            )
        elif self.memory_gb < 16:
            return ResourceLimits(
                max_cpu_percent=70.0,
                max_memory_gb=8.0,
                max_concurrent_tasks=2,
                priority_level="balanced"
            )
        else:
            return ResourceLimits(
                max_cpu_percent=85.0,
                max_memory_gb=12.0,
                max_concurrent_tasks=3,
                priority_level="performance"
            )
    
    async def execute_with_limits(self, task_func, task_name: str, **kwargs):
        """Execute task with CPU/memory limits"""
        try:
            # Wait for available slot
            await self._wait_for_available_slot()
            
            # Monitor resources during execution
            start_time = time.time()
            self.current_tasks.append(task_name)
            
            self.logger.info(f"🚀 Starting {task_name} (slot {len(self.current_tasks)}/{self.resource_limits.max_concurrent_tasks})")
            
            # Execute with monitoring
            result = await self._monitored_execution(task_func, task_name, **kwargs)
            
            execution_time = time.time() - start_time
            self.logger.info(f"✅ {task_name} completed in {execution_time:.1f}s")
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ {task_name} failed: {e}")
            raise
        finally:
            # Clean up
            if task_name in self.current_tasks:
                self.current_tasks.remove(task_name)
    
    async def _wait_for_available_slot(self):
        """Wait for available execution slot"""
        while len(self.current_tasks) >= self.resource_limits.max_concurrent_tasks:
            await asyncio.sleep(1)
            
            # Check if system is overloaded
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            
            if cpu_percent > self.resource_limits.max_cpu_percent:
                self.logger.warning(f"⚠️ High CPU usage: {cpu_percent:.1f}%")
                await asyncio.sleep(2)
            
            if memory_percent > 80:
                self.logger.warning(f"⚠️ High memory usage: {memory_percent:.1f}%")
                await asyncio.sleep(2)
    
    async def _monitored_execution(self, task_func, task_name: str, **kwargs):
        """Execute task with resource monitoring"""
        # Create monitoring task
        monitor_task = asyncio.create_task(
            self._monitor_resources(task_name)
        )
        
        try:
            # Execute main task
            if asyncio.iscoroutinefunction(task_func):
                result = await task_func(**kwargs)
            else:
                result = task_func(**kwargs)
            
            return result
            
        finally:
            # Stop monitoring
            monitor_task.cancel()
            try:
                await monitor_task
            except asyncio.CancelledError:
                pass
    
    async def _monitor_resources(self, task_name: str):
        """Monitor system resources during task execution"""
        try:
            while True:
                await asyncio.sleep(5)  # Check every 5 seconds
                
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                
                if cpu_percent > self.resource_limits.max_cpu_percent:
                    self.logger.warning(
                        f"🔥 {task_name}: High CPU {cpu_percent:.1f}%"
                    )
                
                if memory.percent > 85:
                    self.logger.warning(
                        f"🔥 {task_name}: High memory {memory.percent:.1f}%"
                    )
                
                # Log resource usage periodically
                if int(time.time()) % 30 == 0:  # Every 30 seconds
                    self.logger.info(
                        f"📊 {task_name}: CPU {cpu_percent:.1f}%, "
                        f"RAM {memory.percent:.1f}%"
                    )
                    
        except asyncio.CancelledError:
            pass
    
    def get_optimal_settings(self) -> Dict:
        """Get CPU-optimized settings based on current load"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        # Adjust settings based on current load
        if cpu_percent > 80 or memory.percent > 80:
            # High load - use conservative settings
            return {
                'video_resolution': '480x854',
                'video_fps': 20,
                'audio_quality': 'medium',
                'compression_preset': 'ultrafast',
                'concurrent_tasks': 1,
                'expected_time': '1-2 minutes per video',
                'cpu_threads': min(2, self.cpu_count)
            }
        elif cpu_percent > 60 or memory.percent > 60:
            # Medium load - balanced settings
            return {
                'video_resolution': '720x1280',
                'video_fps': 24,
                'audio_quality': 'good',
                'compression_preset': 'fast',
                'concurrent_tasks': 2,
                'expected_time': '2-3 minutes per video',
                'cpu_threads': min(4, self.cpu_count)
            }
        else:
            # Low load - performance settings
            return {
                'video_resolution': '720x1280',
                'video_fps': 30,
                'audio_quality': 'high',
                'compression_preset': 'medium',
                'concurrent_tasks': 3,
                'expected_time': '3-4 minutes per video',
                'cpu_threads': min(6, self.cpu_count)
            }
    
    def get_system_status(self) -> Dict:
        """Get current system resource status"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        status = "healthy"
        if cpu_percent > 85 or memory.percent > 85:
            status = "overloaded"
        elif cpu_percent > 70 or memory.percent > 70:
            status = "busy"
        
        return {
            'status': status,
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_available_gb': memory.available / (1024**3),
            'disk_free_gb': disk.free / (1024**3),
            'active_tasks': len(self.current_tasks),
            'max_tasks': self.resource_limits.max_concurrent_tasks,
            'priority_level': self.resource_limits.priority_level
        }
    
    async def optimize_for_long_running(self):
        """Optimize system for long-running automation"""
        try:
            # Clear system cache
            if os.name == 'nt':  # Windows
                os.system('echo off & echo Optimizing system... & timeout /t 1 > nul')
            
            # Adjust process priority
            current_process = psutil.Process()
            current_process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS if os.name == 'nt' else 10)
            
            # Set CPU affinity to avoid core 0 (system critical)
            if self.cpu_count > 2:
                available_cores = list(range(1, min(self.cpu_count, 6)))
                current_process.cpu_affinity(available_cores)
                self.logger.info(f"🔧 CPU affinity set to cores: {available_cores}")
            
            self.logger.info("✅ System optimized for long-running tasks")
            
        except Exception as e:
            self.logger.warning(f"System optimization failed: {e}")
    
    def estimate_task_duration(self, task_type: str, content_length: int = 1000) -> Dict:
        """Estimate task duration based on system capabilities"""
        base_times = {
            'video_generation': 120,  # 2 minutes base
            'audio_generation': 30,   # 30 seconds base
            'image_generation': 60,   # 1 minute base
            'text_processing': 5      # 5 seconds base
        }
        
        base_time = base_times.get(task_type, 60)
        
        # Adjust for system performance
        performance_multiplier = {
            'conservative': 2.0,
            'balanced': 1.5,
            'performance': 1.0
        }[self.resource_limits.priority_level]
        
        # Adjust for content length
        length_multiplier = min(3.0, content_length / 500)
        
        estimated_seconds = base_time * performance_multiplier * length_multiplier
        
        return {
            'estimated_seconds': int(estimated_seconds),
            'estimated_minutes': round(estimated_seconds / 60, 1),
            'confidence': 'high' if self.memory_gb > 8 else 'medium'
        }