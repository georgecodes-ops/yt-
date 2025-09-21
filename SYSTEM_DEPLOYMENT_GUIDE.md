# 🚀 MonAY System Deployment Guide

## Overview

This guide covers system-level deployment of MonAY with proper virtual environment isolation and verified GitHub repositories for production use.

## 📋 GitHub Repositories

### 🌐 WAN (Video Generation)
- **Repository**: `https://github.com/Wan-Video/Wan2.2.git`
- **Purpose**: AI video generation capabilities (WAN 2.2 with I2V-A14B model)
- **Environment**: Separate virtual environment (`wan_venv/`)
- **Dependencies**: PyTorch, Transformers, Datasets, Git LFS for large model files

### 🎨 Stable Diffusion
- **Repository**: `https://github.com/huggingface/diffusers.git`
- **Purpose**: AI image generation and processing
- **Environment**: Main virtual environment (`venv/`)
- **Dependencies**: PyTorch 2.0+, Diffusers, XFormers

### 🤖 Transformers
- **Repository**: `https://github.com/huggingface/transformers.git`
- **Purpose**: Natural language processing and model handling
- **Environment**: Both main and WAN environments
- **Dependencies**: PyTorch, Tokenizers, SafeTensors

## 🏗️ System Architecture

### Virtual Environment Strategy

```
/opt/monay/                    # System deployment location
├── venv/                      # Main environment (Stable Diffusion)
│   ├── bin/python            # Main Python interpreter
│   └── lib/site-packages/    # Main dependencies
├── wan_venv/                 # WAN-specific environment
│   ├── bin/python           # WAN Python interpreter
│   └── lib/site-packages/   # WAN dependencies
├── src/                     # Application source code
└── config files             # .env, config.yaml, etc.
```

### Dependency Isolation

**Main Environment (`venv/`):**
- PyTorch 2.0+ with CUDA support
- Diffusers for Stable Diffusion
- Transformers for model handling
- XFormers for memory optimization
- Streamlit for web interface
- Core application dependencies

**WAN Environment (`wan_venv/`):**
- PyTorch 1.6+ (compatible version)
- Transformers for video processing
- Datasets for training data
- Accelerate for distributed computing
- Isolated from main environment

## 🔧 System Deployment Process

### 1. Automated Setup

```bash
# Run the system deployment setup
python setup_system_deployment.py
```

This script will:
- ✅ Setup system directory (owned by current user)
- ✅ Setup system-level virtual environments
- ✅ Verify GitHub repository accessibility
- ✅ Install dependencies with proper isolation
- ✅ Copy project files to `/opt/monay`
- ✅ Create systemd service configuration
- ✅ Set proper permissions (current user ownership)

### 2. Manual Verification

```bash
# Check virtual environments
sudo -u monay /opt/monay/venv/bin/python --version
sudo -u monay /opt/monay/wan_venv/bin/python --version

# Test Stable Diffusion
sudo -u monay /opt/monay/venv/bin/python -c "import torch; import diffusers; print('SD Ready')"

# Test WAN environment
sudo -u monay /opt/monay/wan_venv/bin/python -c "import torch; import transformers; print('WAN Ready')"
```

### 3. Service Management

```bash
# Enable and start the service
sudo systemctl enable monay
sudo systemctl start monay

# Check service status
sudo systemctl status monay

# View logs
sudo journalctl -u monay -f
```

## 🔒 Security Configuration

### System User
- **User**: `monay` (system user, no shell access)
- **Home**: `/opt/monay`
- **Permissions**: Read/write only to `/opt/monay`

### Service Security
- `NoNewPrivileges=true`
- `ProtectSystem=strict`
- `ProtectHome=true`
- `PrivateTmp=true`
- Resource limits (Memory: 8GB, CPU: 90%)

## 🌐 Environment Detection

The system automatically detects the appropriate environment:

1. **System Deployment**: `/opt/monay/wan_venv/bin/python`
2. **Local Windows**: `wan_venv/Scripts/python.exe`
3. **Local Unix**: `wan_venv/bin/python`
4. **Fallback**: Main environment if WAN not available

## 📊 Resource Management

### Memory Allocation
- **Main Environment**: 6GB (Stable Diffusion models)
- **WAN Environment**: 2GB (Video processing)
- **System Overhead**: 1GB
- **Total Recommended**: 16GB RAM

### CPU Usage
- **Service Limit**: 90% CPU quota
- **Concurrent Processing**: Managed by environment isolation
- **Background Tasks**: Automatic resource balancing

### Storage Requirements
- **Base Installation**: 5GB
- **Model Cache**: 10GB (HuggingFace models)
- **Video Processing**: 20GB (temporary files)
- **Logs and Data**: 5GB
- **Total Recommended**: 50GB free space

## 🔍 Monitoring and Maintenance

### Health Checks

```bash
# Service health
sudo systemctl is-active monay

# Environment health
sudo -u monay /opt/monay/venv/bin/python -c "import torch; print('CUDA:', torch.cuda.is_available())"

# WAN environment health
sudo -u monay /opt/monay/wan_venv/bin/python -c "import transformers; print('WAN OK')"

# Web interface
curl -f http://localhost:8501/health || echo "Web interface down"
```

### Log Monitoring

```bash
# System logs
sudo journalctl -u monay --since "1 hour ago"

# Application logs
sudo tail -f /opt/monay/logs/enhanced_system.log

# Error monitoring
sudo journalctl -u monay -p err
```

### Updates and Maintenance

```bash
# Update dependencies (main environment)
sudo -u monay /opt/monay/venv/bin/pip install --upgrade torch diffusers transformers

# Update WAN dependencies
sudo -u monay /opt/monay/wan_venv/bin/pip install --upgrade torch transformers

# Restart service after updates
sudo systemctl restart monay
```

## 🚨 Troubleshooting

### Common Issues

#### "WAN environment not found"
```bash
# Check WAN environment
ls -la /opt/monay/wan_venv/bin/python

# Recreate if missing
sudo -u monay python3 -m venv /opt/monay/wan_venv
sudo -u monay /opt/monay/wan_venv/bin/pip install torch transformers
```

#### "CUDA not available"
```bash
# Check NVIDIA drivers
nvidia-smi

# Reinstall PyTorch with CUDA
sudo -u monay /opt/monay/venv/bin/pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### "Service fails to start"
```bash
# Check service logs
sudo journalctl -u monay -n 50

# Check permissions
sudo ls -la /opt/monay/
sudo chown -R monay:monay /opt/monay/
```

#### "Memory issues"
```bash
# Check memory usage
free -h

# Adjust service limits
sudo systemctl edit monay
# Add: [Service]
#      MemoryMax=12G
```

### Performance Optimization

#### GPU Optimization
```bash
# Enable XFormers for memory efficiency
sudo -u monay /opt/monay/venv/bin/pip install xformers

# Set CUDA memory fraction
echo 'export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512' | sudo tee -a /opt/monay/.bashrc
```

#### CPU Optimization
```bash
# Set CPU affinity for better performance
sudo systemctl edit monay
# Add: [Service]
#      CPUAffinity=0-7
```

## 📈 Production Deployment Checklist

- [ ] ✅ System user created (`monay`)
- [ ] ✅ Virtual environments isolated (`venv/`, `wan_venv/`)
- [ ] ✅ GitHub repositories verified and accessible
- [ ] ✅ Dependencies installed without conflicts
- [ ] ✅ Service configuration created
- [ ] ✅ Security settings applied
- [ ] ✅ Resource limits configured
- [ ] ✅ Monitoring setup
- [ ] ✅ Backup strategy implemented
- [ ] ✅ Update procedures documented

## 📋 Post-Deployment Verification

After running the deployment script, verify the installation using the provided validation tools:

### Quick Validation
```bash
# Run the validation script for quick checks
chmod +x validate_deployment.sh
./validate_deployment.sh
```

### Comprehensive Testing
```bash
# Run the full test suite
python3 test_deployment.py
```

### Manual Verification
```bash
# Check service status
sudo systemctl status monay.service

# Check service logs
journalctl -u monay.service -f

# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8001/health  # AI service
curl http://localhost:8002/health  # Video service

# Check virtual environments
/opt/monay/venv/bin/python --version
/opt/monay/ai_service/venv/bin/python --version
/opt/monay/video_service/venv/bin/python --version
/opt/monay/wan/venv/bin/python --version
```

### Troubleshooting

If validation fails:

1. **Check service logs**: `journalctl -u monay.service --no-pager`
2. **Verify dependencies**: Run `test_deployment.py` for detailed dependency checks
3. **Check permissions**: Ensure `/opt/monay` is owned by the deployment user
4. **Restart service**: `sudo systemctl restart monay.service`
5. **Check configuration**: Verify `.env` file has required API keys

## 🔄 Backup and Recovery

### Backup Strategy
```bash
# Backup configuration
sudo tar -czf monay-config-$(date +%Y%m%d).tar.gz /opt/monay/*.yaml /opt/monay/.env

# Backup models (if needed)
sudo tar -czf monay-models-$(date +%Y%m%d).tar.gz /opt/monay/.cache/huggingface/

# Backup application code
sudo tar -czf monay-src-$(date +%Y%m%d).tar.gz /opt/monay/src/
```

### Recovery Process
```bash
# Stop service
sudo systemctl stop monay

# Restore from backup
sudo tar -xzf monay-config-YYYYMMDD.tar.gz -C /
sudo tar -xzf monay-src-YYYYMMDD.tar.gz -C /

# Fix permissions (replace with your username)
sudo chown -R $USER:$USER /opt/monay/

# Start service
sudo systemctl start monay
```

This system deployment ensures proper isolation, security, and maintainability for production use of MonAY with verified GitHub repositories and optimized virtual environment management.