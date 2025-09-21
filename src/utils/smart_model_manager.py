import os
import logging
import time
import requests
import subprocess
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SmartModelManager:
    def __init__(self):
        self.models = {
            "ollama_mistral": {
                "name": "Ollama Mistral",
                "health_check": self._check_ollama_mistral_health,
                "available": False,
                "priority": 1,
                "endpoint": "http://localhost:11434"
            },
            "wan_2_1": {
                "name": "WAN 2.1",
                "health_check": self._check_wan_health,
                "available": False,
                "priority": 2
            }
        }
        self.last_health_check = {}
        self.health_check_interval = 60  # seconds
        self._update_model_availability()

    def _check_ollama_mistral_health(self):
        """Check if Ollama Mistral is available and healthy."""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                mistral_available = any('mistral' in model.get('name', '').lower() for model in models)
                if mistral_available:
                    logging.info("Ollama Mistral health check: OK")
                    return True
                else:
                    logging.warning("Ollama service running but Mistral model not found")
                    return False
            else:
                logging.warning(f"Ollama health check failed: HTTP {response.status_code}")
                return False
        except Exception as e:
            logging.error(f"Ollama Mistral health check failed: {e}")
            return False

    def _check_wan_health(self):
        """Check if WAN 2.1 is available locally (CPU-compatible)"""
        try:
            # Set CPU-only mode at process level before any imports
            
            # Create a separate Python process with CPU-only environment
            env = os.environ.copy()
            env['CUDA_VISIBLE_DEVICES'] = ''
            env['CUDA_LAUNCH_BLOCKING'] = '1'
            env['TORCH_USE_CUDA_DSA'] = '0'
            
            # Test WAN import in isolated process
            test_script = "import wan; print('SUCCESS'); print(getattr(wan, '__version__', 'Unknown'))"
            result = subprocess.run(
                [sys.executable, '-c', test_script],
                env=env,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and 'SUCCESS' in result.stdout:
                version = result.stdout.strip().split('\n')[-1] if '\n' in result.stdout else 'Unknown'
                logging.info(f"WAN 2.1 health check: OK (Version: {version}, CPU mode)")
                return True
            else:
                logging.warning(f"WAN 2.1 subprocess test failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logging.error("WAN 2.1 health check timed out")
            return False
        except Exception as e:
            logging.error(f"WAN 2.1 health check failed: {e}")
            return False

    def _update_model_availability(self):
        current_time = time.time()
        for model_id, model_info in self.models.items():
            if (model_id not in self.last_health_check or
                current_time - self.last_health_check[model_id] > self.health_check_interval):
                model_info["available"] = model_info["health_check"]()
                self.last_health_check[model_id] = current_time
                logging.info(f"Model '{model_info['name']}' availability updated to: {model_info['available']}")

    def get_optimal_model(self):
        self._update_model_availability()
        available_models = [
            model_info for model_id, model_info in self.models.items()
            if model_info["available"]
        ]
        if not available_models:
            logging.warning("No models are currently available.")
            return None

        available_models.sort(key=lambda x: x["priority"])
        optimal_model = available_models[0]
        logging.info(f"Optimal model selected: {optimal_model['name']}")
        return optimal_model

    def get_model_health_summary(self):
        summary = {"timestamp": time.time(), "models": {}}
        for model_id, model_info in self.models.items():
            summary["models"][model_id] = {
                "name": model_info["name"],
                "available": model_info["available"],
                "last_checked": self.last_health_check.get(model_id, "N/A")
            }
        return summary

# Example Usage:
if __name__ == "__main__":
    manager = SmartModelManager()
    print("Health Summary:", manager.get_model_health_summary())
    print("Optimal Model:", manager.get_optimal_model())