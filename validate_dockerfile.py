#!/usr/bin/env python3
"""
Validate Dockerfile.render for common syntax issues
"""

import re
from pathlib import Path

def validate_dockerfile():
    """Check Dockerfile for common issues"""
    dockerfile_path = Path("/app/Dockerfile.render")
    
    if not dockerfile_path.exists():
        print("❌ Dockerfile.render not found")
        return False
    
    content = dockerfile_path.read_text()
    issues = []
    
    # Check for deprecated Poetry flags
    if "--no-dev" in content:
        issues.append("❌ Found deprecated --no-dev flag (should be --without dev)")
    
    # Check for correct Poetry syntax
    if "--without dev" in content:
        print("✅ Using correct --without dev syntax")
    else:
        issues.append("⚠️  --without dev flag not found")
    
    # Check for required components
    required_patterns = [
        (r"poetry install", "Poetry install command"),
        (r"--extras.*postgres.*server", "PostgreSQL and server extras"),
        (r"--secure", "Secure mode for ADE"),
        (r"/v1/health", "Health check endpoint"),
        (r"LETTA_PG_URI", "PostgreSQL URI environment")
    ]
    
    for pattern, description in required_patterns:
        if re.search(pattern, content):
            print(f"✅ {description}: Found")
        else:
            issues.append(f"⚠️  {description}: Not found")
    
    # Summary
    print("\n" + "="*50)
    if issues:
        print(f"❌ Found {len(issues)} issue(s):")
        for issue in issues:
            print(f"   {issue}")
        return False
    else:
        print("🎉 Dockerfile.render validation passed!")
        print("✅ Ready for Render deployment")
        return True

if __name__ == "__main__":
    success = validate_dockerfile()
    exit(0 if success else 1)