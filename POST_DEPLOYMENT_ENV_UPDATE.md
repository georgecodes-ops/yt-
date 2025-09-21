# 🔧 Post-Deployment Environment Configuration

After running `setup_system_deployment.py`, you need to update the environment configuration for optimal production performance. This guide explains how to use the provided scripts to configure your `.env` file with production-optimized settings.

## 📋 Overview

The deployment script copies your current `.env` file to the deployment directory, but it needs to be updated with:
- Production file paths (deployment directory instead of relative paths)
- CPU-only optimizations for WAN and Stable Diffusion
- Server-appropriate resource limits and timeouts
- Production service configuration

**Platform-specific deployment paths:**
- **Linux/Ubuntu:** `/opt/monay/`
- **Windows:** `C:/opt/monay/`

## 🚀 Quick Start (Ubuntu Server)

### Step 1: Run the deployment script
```bash
python3 setup_system_deployment.py
```

### Step 2: Update environment configuration
```bash
# Make the script executable
chmod +x update_env_after_deployment.sh

# Run the environment update
./update_env_after_deployment.sh
```

That's it! The script will:
- ✅ Backup your current `.env` file
- ✅ Update with production-optimized settings
- ✅ Restart the MonAY service
- ✅ Show service status

## 📁 Files Included

### For Ubuntu Server (Production)
- **`update_env_after_deployment.sh`** - Main post-deployment script
- **`update_production_env.py`** - Python environment updater

### For Windows (Local Testing)
- **`update_env_after_deployment.cmd`** - Windows batch script for local testing

## 🔧 What Gets Updated

### Production Paths
```bash
# Before (relative paths)
DATABASE_URL=sqlite:///monay.db
LOG_DIRECTORY=./logs

# After (production paths)
# Linux:
DATABASE_URL=sqlite:////opt/monay/data/monay.db
LOG_DIRECTORY=/opt/monay/logs

# Windows:
DATABASE_URL=sqlite:///C:/opt/monay/data/monay.db
LOG_DIRECTORY=C:/opt/monay/logs
```

### CPU Optimizations
```bash
# WAN Configuration
WAN_CPU_MODE=true
WAN_RESOLUTION=512x512
WAN_INFERENCE_STEPS=15
WAN_BATCH_SIZE=1

# Stable Diffusion Configuration
SD_CPU_MODE=true
SD_RESOLUTION=512x512
SD_INFERENCE_STEPS=20
```

### Resource Limits
```bash
# Server-appropriate limits
CPU_LIMIT=50%
MEMORY_LIMIT=4GB
MAX_WORKERS=2
AUTOMATION_CYCLE_HOURS=8
GENERATION_TIMEOUT_SECONDS=3600
```

### Service Configuration
```bash
# Production service paths
# Linux:
PYTHON_PATH=/opt/monay/main_venv/bin/python
WAN_PYTHON_PATH=/opt/monay/wan_venv/bin/python
AI_PYTHON_PATH=/opt/monay/ai_service_venv/bin/python
SERVICE_HOME=/opt/monay

# Windows:
PYTHON_PATH=C:/opt/monay/main_venv/Scripts/python.exe
WAN_PYTHON_PATH=C:/opt/monay/wan_venv/Scripts/python.exe
AI_PYTHON_PATH=C:/opt/monay/ai_service_venv/Scripts/python.exe
SERVICE_HOME=C:/opt/monay
```

## 🔍 Manual Usage

### If you prefer to run the Python script directly:
```bash
# Navigate to project directory
cd /path/to/monay_restored

# Run the Python updater
python3 update_production_env.py  # Linux
python update_production_env.py   # Windows

# Restart service manually (Linux only)
# Windows users: run start_monay.bat
```sudo systemctl restart monay
```

### Check the results:
```bash
# View updated .env file
cat /opt/monay/.env

# Check service status
sudo systemctl status monay

# Monitor logs
journalctl -u monay -f

# Test health endpoint
curl http://localhost:8000/health
```

## 🔒 Security Features

- **Backup Creation**: Original `.env` saved as `.env.backup`
- **Permission Setting**: `.env` file set to `600` (owner read/write only)
- **User Validation**: Scripts check for proper user context
- **Path Validation**: Verifies deployment directory exists

## 🐛 Troubleshooting

### Script fails with "deployment directory not found"
```bash
# Check if deployment completed
ls -la /opt/monay/

# Re-run deployment if needed
python3 setup_system_deployment.py
```

### Service fails to start after update
```bash
# Check service logs
journalctl -u monay --no-pager

# Verify .env file syntax
cat /opt/monay/.env | grep -E "^[A-Z_]+=.*$"

# Restore backup if needed
cp /opt/monay/.env.backup /opt/monay/.env
sudo systemctl restart monay
```

### Permission errors
```bash
# Check file ownership
ls -la /opt/monay/.env

# Fix permissions if needed
chmod 600 /opt/monay/.env
```

## 📊 Verification

After running the update script, verify everything works:

```bash
# 1. Check service is running
sudo systemctl status monay

# 2. Test API endpoints
curl http://localhost:8000/health

# 3. Check CPU-only mode is active
grep "CPU_MODE=true" /opt/monay/.env

# 4. Verify production paths
grep "/opt/monay" /opt/monay/.env

# 5. Monitor resource usage
top -p $(pgrep -f monay)
```

## 🔄 Rollback

If you need to rollback the changes:

```bash
# Restore original .env
cp /opt/monay/.env.backup /opt/monay/.env

# Restart service
sudo systemctl restart monay

# Verify rollback
sudo systemctl status monay
```

## 📋 Next Steps

After successful environment update:

1. **Monitor Performance**: Watch CPU and memory usage
2. **Test Video Generation**: Verify WAN and SD work in CPU mode
3. **Check YouTube Integration**: Test upload functionality
4. **Set Up Monitoring**: Configure log rotation and alerts
5. **Schedule Backups**: Set up regular data backups

## 🆘 Support

If you encounter issues:

1. Check the service logs: `journalctl -u monay -f`
2. Verify all virtual environments: `ls -la /opt/monay/*/bin/python`
3. Test individual components: `python3 test_deployment.py`
4. Review the deployment guide: `SYSTEM_DEPLOYMENT_GUIDE.md`

---

**Note**: These scripts are designed specifically for Ubuntu server deployment. For local development on Windows, use the `.cmd` version for testing purposes only.