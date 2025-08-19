#!/usr/bin/env python3
"""
Test script to verify Letta server can start and connect to Supabase
"""

import os
import sys
from letta.settings import settings
from letta.server.db import DatabaseRegistry
from sqlalchemy import text

def test_database_connection():
    """Test the database connection with Letta settings"""
    try:
        print("🔍 Testing Letta database connection...")
        print(f"   Database engine: {settings.database_engine}")
        print(f"   Database URI: {settings.letta_pg_uri}")
        
        # Create database registry and get engine
        db_registry = DatabaseRegistry()
        engine = db_registry.get_engine()
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test")).fetchone()
            assert result[0] == 1
            
        print("✅ Database connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

def test_server_imports():
    """Test that server components can be imported"""
    try:
        print("🔍 Testing server imports...")
        from letta.server.rest_api.app import start_server
        print("✅ Server imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Server import failed: {str(e)}")
        return False

def main():
    print("=" * 50)
    print("🧪 Letta AI Server Test")
    print("=" * 50)
    
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run tests
    db_ok = test_database_connection()
    server_ok = test_server_imports()
    
    print("=" * 50)
    if db_ok and server_ok:
        print("🎉 All tests passed! Server is ready to deploy.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())