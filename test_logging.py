#!/usr/bin/env python3
"""
Test script to verify Letta logging works correctly
"""
import os
import sys
from pathlib import Path

print("🧪 Testing Letta Logging Configuration...")

# Test environment setup
print(f"LETTA_DIR environment: {os.getenv('LETTA_DIR', 'Not set')}")

try:
    from letta.settings import settings
    print(f"✅ Settings loaded successfully")
    print(f"📁 Letta directory: {settings.letta_dir}")
    
    # Test directory creation
    log_dir = settings.letta_dir / "logs"
    print(f"📁 Log directory: {log_dir}")
    
    if not log_dir.exists():
        print("📝 Creating log directory...")
        log_dir.mkdir(parents=True, exist_ok=True)
        print("✅ Log directory created successfully")
    else:
        print("✅ Log directory already exists")
    
    # Test logging
    from letta.log import get_logger
    logger = get_logger("test")
    logger.info("🎉 Test log message - logging is working!")
    print("✅ Logging system initialized successfully")
    
    # Test log file creation
    log_file = log_dir / "Letta.log"
    if log_file.exists():
        print(f"✅ Log file created: {log_file}")
        # Show first few lines of log file
        with open(log_file, 'r') as f:
            lines = f.readlines()[-5:]  # Last 5 lines
            if lines:
                print("📖 Recent log entries:")
                for line in lines:
                    print(f"   {line.strip()}")
    else:
        print(f"⚠️  Log file not found: {log_file}")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error testing logging: {e}")
    sys.exit(1)

print("🎉 Logging test completed successfully!")