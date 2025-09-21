#!/usr/bin/env python3
"""
Test script to verify distribution module imports work correctly
"""
import os
import sys

# Add src directory to Python path
src_dir = os.path.join(os.path.dirname(__file__), 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

print("Testing distribution module imports...")

try:
    from distribution import EnhancedUploadManager, BlogManager, PODManager
    print("✅ All distribution modules imported successfully")
    
    # Test creating instances
    print("\nTesting class instantiation...")
    
    try:
        upload_manager = EnhancedUploadManager()
        print("✅ EnhancedUploadManager instantiated")
    except Exception as e:
        print(f"⚠️ EnhancedUploadManager failed: {e}")
    
    try:
        blog_manager = BlogManager()
        print("✅ BlogManager instantiated")
    except Exception as e:
        print(f"⚠️ BlogManager failed: {e}")
    
    try:
        pod_manager = PODManager()
        print("✅ PODManager instantiated")
    except Exception as e:
        print(f"⚠️ PODManager failed: {e}")
    
    print("\n✅ Distribution module test completed successfully")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nPython path:")
    for path in sys.path:
        print(f"  {path}")
    
    print("\nCurrent directory contents:")
    for item in os.listdir('.'):
        print(f"  {item}")
        
    print("\nDistribution directory contents:")
    try:
        for item in os.listdir('src/distribution'):
            print(f"  {item}")
    except Exception as e:
        print(f"  Error listing distribution: {e}")

except Exception as e:
    print(f"❌ Unexpected error: {e}")