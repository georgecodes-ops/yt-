import logging
import os
import subprocess
import psutil
import requests
import time
from typing import Dict, List
import json
from datetime import datetime

class SystemHealthChecker:
    """Proactive system health monitoring to prevent failures"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.health_report = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'unknown',
            'checks': {},
            'warnings': [],
            'critical_issues': []
        }
    
    async def run_comprehensive_health_check(self) -> Dict:
        """Run all health checks and return comprehensive report"""
        self.logger.info("🔍 Starting comprehensive system health check...")
        
        # Core system checks
        await self.check_memory_usage()
        await self.check_disk_space()
        await self.check_cpu_usage()
        
        # Service dependency checks
        await self.check_ollama_service()
        await self.check_ffmpeg_installation()
        await self.check_python_environment()
        
        # API and network checks
        await self.check_youtube_api_quota()
        await self.check_network_connectivity()
        await self.check_external_apis()
        
        # File system checks
        await self.check_output_directories()
        await self.check_temp_file_cleanup()
        
        # Process health checks
        await self.check_running_processes()
        await self.check_log_file_sizes()
        
        # Determine overall status
        self._calculate_overall_status()
        
        self.logger.info(f"✅ Health check completed: {self.health_report['overall_status']}")
        return self.health_report
    
    async def check_memory_usage(self):
        """Check system memory usage and detect potential issues"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            memory_percent = memory.percent
            swap_percent = swap.percent if swap.total > 0 else 0
            
            self.health_report['checks']['memory'] = {
                'status': 'healthy',
                'memory_percent': memory_percent,
                'swap_percent': swap_percent,
                'available_gb': round(memory.available / (1024**3), 2),
                'total_gb': round(memory.total / (1024**3), 2)
            }
            
            # Warning thresholds
            if memory_percent > 85:
                self.health_report['warnings'].append(f"High memory usage: {memory_percent}%")
                self.health_report['checks']['memory']['status'] = 'warning'
            
            if memory_percent > 95:
                self.health_report['critical_issues'].append(f"Critical memory usage: {memory_percent}%")
                self.health_report['checks']['memory']['status'] = 'critical'
            
            if swap_percent > 50:
                self.health_report['warnings'].append(f"High swap usage: {swap_percent}%")
                
        except Exception as e:
            self.health_report['checks']['memory'] = {'status': 'error', 'error': str(e)}
    
    async def check_disk_space(self):
        """Check disk space usage and predict potential issues"""
        try:
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            free_gb = disk.free / (1024**3)
            
            self.health_report['checks']['disk_space'] = {
                'status': 'healthy',
                'disk_percent': round(disk_percent, 2),
                'free_gb': round(free_gb, 2),
                'total_gb': round(disk.total / (1024**3), 2)
            }
            
            # Critical for video generation
            if free_gb < 5:
                self.health_report['critical_issues'].append(f"Low disk space: {free_gb:.1f}GB free")
                self.health_report['checks']['disk_space']['status'] = 'critical'
            elif free_gb < 10:
                self.health_report['warnings'].append(f"Low disk space warning: {free_gb:.1f}GB free")
                self.health_report['checks']['disk_space']['status'] = 'warning'
                
        except Exception as e:
            self.health_report['checks']['disk_space'] = {'status': 'error', 'error': str(e)}
    
    async def check_cpu_usage(self):
        """Check CPU usage patterns"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            load_avg = os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
            
            self.health_report['checks']['cpu'] = {
                'status': 'healthy',
                'cpu_percent': cpu_percent,
                'cpu_count': cpu_count,
                'load_average': load_avg[0] if load_avg else 0
            }
            
            if cpu_percent > 90:
                self.health_report['warnings'].append(f"High CPU usage: {cpu_percent}%")
                self.health_report['checks']['cpu']['status'] = 'warning'
                
        except Exception as e:
            self.health_report['checks']['cpu'] = {'status': 'error', 'error': str(e)}
    
    async def check_ollama_service(self):
        """Check Ollama service health and connectivity"""
        try:
            # Test basic connectivity
            response = requests.get('http://localhost:11434', timeout=10)
            if response.status_code == 200 and "Ollama is running" in response.text:
                # Test API endpoint
                api_response = requests.get('http://localhost:11434/api/version', timeout=10)
                if api_response.status_code == 200:
                    version_data = api_response.json()
                    self.health_report['checks']['ollama'] = {
                        'status': 'healthy',
                        'version': version_data.get('version', 'unknown'),
                        'api_accessible': True
                    }
                else:
                    self.health_report['checks']['ollama'] = {
                        'status': 'warning',
                        'service_running': True,
                        'api_accessible': False
                    }
                    self.health_report['warnings'].append("Ollama service running but API not accessible")
            else:
                self.health_report['checks']['ollama'] = {'status': 'critical', 'service_running': False}
                self.health_report['critical_issues'].append("Ollama service not running")
                
        except requests.exceptions.ConnectionError:
            self.health_report['checks']['ollama'] = {'status': 'critical', 'error': 'Connection refused'}
            self.health_report['critical_issues'].append("Cannot connect to Ollama service")
        except Exception as e:
            self.health_report['checks']['ollama'] = {'status': 'error', 'error': str(e)}
    
    async def check_ffmpeg_installation(self):
        """Check FFmpeg installation and version"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                self.health_report['checks']['ffmpeg'] = {
                    'status': 'healthy',
                    'installed': True,
                    'version': version_line
                }
            else:
                self.health_report['checks']['ffmpeg'] = {'status': 'critical', 'installed': False}
                self.health_report['critical_issues'].append("FFmpeg not working properly")
                
        except FileNotFoundError:
            self.health_report['checks']['ffmpeg'] = {'status': 'critical', 'installed': False}
            self.health_report['critical_issues'].append("FFmpeg not installed")
        except Exception as e:
            self.health_report['checks']['ffmpeg'] = {'status': 'error', 'error': str(e)}
    
    async def check_python_environment(self):
        """Check Python environment and key packages"""
        try:
            import sys
            python_version = sys.version
            
            # Check key packages
            packages_to_check = ['moviepy', 'gtts', 'requests', 'psutil']
            package_status = {}
            
            for package in packages_to_check:
                try:
                    __import__(package)
                    package_status[package] = 'installed'
                except ImportError:
                    package_status[package] = 'missing'
            
            missing_packages = [pkg for pkg, status in package_status.items() if status == 'missing']
            
            self.health_report['checks']['python_environment'] = {
                'status': 'healthy' if not missing_packages else 'warning',
                'python_version': python_version,
                'packages': package_status
            }
            
            if missing_packages:
                self.health_report['warnings'].append(f"Missing packages: {', '.join(missing_packages)}")
                
        except Exception as e:
            self.health_report['checks']['python_environment'] = {'status': 'error', 'error': str(e)}
    
    async def check_youtube_api_quota(self):
        """Check YouTube API quota usage (if possible)"""
        try:
            # This would require actual API key and quota checking
            # For now, we'll just check if the API key exists
            api_key_exists = os.getenv('YOUTUBE_API_KEY') is not None
            
            self.health_report['checks']['youtube_api'] = {
                'status': 'healthy' if api_key_exists else 'warning',
                'api_key_configured': api_key_exists,
                'note': 'Quota usage requires actual API calls to check'
            }
            
            if not api_key_exists:
                self.health_report['warnings'].append("YouTube API key not configured")
                
        except Exception as e:
            self.health_report['checks']['youtube_api'] = {'status': 'error', 'error': str(e)}
    
    async def check_network_connectivity(self):
        """Check network connectivity to key services"""
        try:
            test_urls = [
                'https://www.google.com',
                'https://api.github.com',
                'https://www.youtube.com'
            ]
            
            connectivity_results = {}
            for url in test_urls:
                try:
                    response = requests.get(url, timeout=5)
                    connectivity_results[url] = response.status_code == 200
                except:
                    connectivity_results[url] = False
            
            failed_connections = [url for url, success in connectivity_results.items() if not success]
            
            self.health_report['checks']['network'] = {
                'status': 'healthy' if not failed_connections else 'warning',
                'connectivity_results': connectivity_results
            }
            
            if failed_connections:
                self.health_report['warnings'].append(f"Network connectivity issues: {failed_connections}")
                
        except Exception as e:
            self.health_report['checks']['network'] = {'status': 'error', 'error': str(e)}
    
    async def check_external_apis(self):
        """Check external API availability"""
        try:
            # Test news APIs and other external services
            api_tests = {
                'google_tts': 'https://translate.google.com',
                'reddit': 'https://www.reddit.com'
            }
            
            api_status = {}
            for api_name, url in api_tests.items():
                try:
                    response = requests.get(url, timeout=5)
                    api_status[api_name] = response.status_code == 200
                except:
                    api_status[api_name] = False
            
            failed_apis = [api for api, status in api_status.items() if not status]
            
            self.health_report['checks']['external_apis'] = {
                'status': 'healthy' if not failed_apis else 'warning',
                'api_status': api_status
            }
            
            if failed_apis:
                self.health_report['warnings'].append(f"External API issues: {failed_apis}")
                
        except Exception as e:
            self.health_report['checks']['external_apis'] = {'status': 'error', 'error': str(e)}
    
    async def check_output_directories(self):
        """Check output directories exist and are writable"""
        try:
            directories_to_check = ['outputs', 'data/videos', 'data/temp']
            directory_status = {}
            
            for directory in directories_to_check:
                try:
                    os.makedirs(directory, exist_ok=True)
                    # Test write permission
                    test_file = os.path.join(directory, 'health_check_test.tmp')
                    with open(test_file, 'w') as f:
                        f.write('test')
                    os.remove(test_file)
                    directory_status[directory] = 'writable'
                except:
                    directory_status[directory] = 'not_writable'
            
            failed_dirs = [d for d, status in directory_status.items() if status != 'writable']
            
            self.health_report['checks']['output_directories'] = {
                'status': 'healthy' if not failed_dirs else 'critical',
                'directory_status': directory_status
            }
            
            if failed_dirs:
                self.health_report['critical_issues'].append(f"Cannot write to directories: {failed_dirs}")
                
        except Exception as e:
            self.health_report['checks']['output_directories'] = {'status': 'error', 'error': str(e)}
    
    async def check_temp_file_cleanup(self):
        """Check for excessive temp files that could cause issues"""
        try:
            temp_dirs = ['outputs', 'data/temp', '/tmp']
            temp_file_info = {}
            
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    file_count = len([f for f in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, f))])
                    temp_file_info[temp_dir] = file_count
                else:
                    temp_file_info[temp_dir] = 0
            
            total_temp_files = sum(temp_file_info.values())
            
            self.health_report['checks']['temp_files'] = {
                'status': 'healthy' if total_temp_files < 100 else 'warning',
                'temp_file_counts': temp_file_info,
                'total_temp_files': total_temp_files
            }
            
            if total_temp_files > 100:
                self.health_report['warnings'].append(f"High temp file count: {total_temp_files}")
                
        except Exception as e:
            self.health_report['checks']['temp_files'] = {'status': 'error', 'error': str(e)}
    
    async def check_running_processes(self):
        """Check for relevant running processes"""
        try:
            relevant_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
                try:
                    if any(keyword in proc.info['name'].lower() for keyword in ['python', 'ffmpeg', 'ollama']):
                        relevant_processes.append(proc.info)
                except:
                    continue
            
            self.health_report['checks']['processes'] = {
                'status': 'healthy',
                'relevant_processes': relevant_processes,
                'process_count': len(relevant_processes)
            }
            
        except Exception as e:
            self.health_report['checks']['processes'] = {'status': 'error', 'error': str(e)}
    
    async def check_log_file_sizes(self):
        """Check log file sizes to prevent disk space issues"""
        try:
            log_files = ['debug.log', 'enhanced_system.log']
            log_info = {}
            
            for log_file in log_files:
                if os.path.exists(log_file):
                    size_mb = os.path.getsize(log_file) / (1024 * 1024)
                    log_info[log_file] = round(size_mb, 2)
                else:
                    log_info[log_file] = 0
            
            large_logs = {f: size for f, size in log_info.items() if size > 100}
            
            self.health_report['checks']['log_files'] = {
                'status': 'healthy' if not large_logs else 'warning',
                'log_sizes_mb': log_info,
                'large_logs': large_logs
            }
            
            if large_logs:
                self.health_report['warnings'].append(f"Large log files detected: {large_logs}")
                
        except Exception as e:
            self.health_report['checks']['log_files'] = {'status': 'error', 'error': str(e)}
    
    def _calculate_overall_status(self):
        """Calculate overall system health status"""
        if self.health_report['critical_issues']:
            self.health_report['overall_status'] = 'critical'
        elif self.health_report['warnings']:
            self.health_report['overall_status'] = 'warning'
        else:
            self.health_report['overall_status'] = 'healthy'
    
    def save_health_report(self, filename: str = None):
        """Save health report to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"health_report_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.health_report, f, indent=2)
        
        self.logger.info(f"Health report saved to {filename}")
        return filename

# Usage example
async def main():
    checker = SystemHealthChecker()
    report = await checker.run_comprehensive_health_check()
    
    print(f"Overall Status: {report['overall_status']}")
    if report['critical_issues']:
        print("Critical Issues:")
        for issue in report['critical_issues']:
            print(f"  ❌ {issue}")
    
    if report['warnings']:
        print("Warnings:")
        for warning in report['warnings']:
            print(f"  ⚠️ {warning}")
    
    checker.save_health_report()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())