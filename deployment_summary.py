#!/usr/bin/env python3
"""
Letta AI Deployment Summary Script
Provides a complete overview of the deployment setup and database status.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_section(title):
    print(f"\n📋 {title}")
    print("-" * 40)

def check_database_status():
    """Check database connection and migration status"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        from letta.settings import settings
        from letta.server.db import DatabaseRegistry
        from sqlalchemy import text
        
        print("🔍 Testing database connection...")
        
        # Test connection
        db_registry = DatabaseRegistry()
        engine = db_registry.get_engine()
        
        with engine.connect() as conn:
            # Test basic connection
            result = conn.execute(text("SELECT 1")).fetchone()
            
            # Get migration version
            try:
                version_result = conn.execute(text("SELECT version_num FROM alembic_version")).fetchone()
                migration_version = version_result[0] if version_result else "Not set"
            except:
                migration_version = "Table not found"
            
            # Count tables
            tables_result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)).fetchone()
            table_count = tables_result[0] if tables_result else 0
        
        print(f"   ✅ Connection: Successful")
        print(f"   📊 Tables: {table_count}")
        print(f"   🔢 Migration Version: {migration_version}")
        
        return True, {
            'table_count': table_count,
            'migration_version': migration_version,
            'database_type': 'PostgreSQL (Supabase)',
            'uri': settings.letta_pg_uri.split('@')[1].split('/')[0] if '@' in settings.letta_pg_uri else 'localhost'
        }
        
    except Exception as e:
        print(f"   ❌ Database check failed: {str(e)}")
        return False, {}

def main():
    print_header("🚀 LETTA AI DEPLOYMENT SUMMARY")
    
    # Deployment Information
    print_section("Deployment Information")
    print(f"📅 Setup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🏗️  Platform: Render (render.com)")
    print(f"🗄️  Database: Supabase PostgreSQL")
    print(f"📦 Letta Version: 0.11.3")
    
    # Database Status
    print_section("Database Status")
    db_ok, db_info = check_database_status()
    
    if db_ok:
        print(f"   🎯 Host: {db_info.get('uri', 'Unknown')}")
        print(f"   🏷️  Type: {db_info.get('database_type', 'Unknown')}")
        print(f"   📊 Tables: {db_info.get('table_count', 0)}")
        print(f"   🔢 Migration: {db_info.get('migration_version', 'Unknown')}")
    
    # Files Created
    print_section("Deployment Files Created")
    files = [
        ("Dockerfile.render", "Production-optimized Docker configuration"),
        ("render.yaml", "Render Blueprint for automatic deployment"),
        ("start_render.sh", "Startup script with health checks"),
        (".env", "Environment variables for local development"),
        ("setup_database.py", "Database setup and migration script"),
        ("RENDER_DEPLOYMENT.md", "Complete deployment documentation"),
        ("deployment_summary.py", "This summary script")
    ]
    
    for filename, description in files:
        if Path(f"/app/{filename}").exists():
            print(f"   ✅ {filename:<20} - {description}")
        else:
            print(f"   ❌ {filename:<20} - Missing!")
    
    # Environment Variables
    print_section("Environment Configuration")
    env_vars = [
        "LETTA_PG_URI",
        "LETTA_PG_HOST", 
        "LETTA_PG_DB",
        "LETTA_ENVIRONMENT"
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive data
            if "PASSWORD" in var or "URI" in var:
                masked_value = value[:10] + "..." + value[-10:] if len(value) > 20 else "***"
                print(f"   ✅ {var:<20} = {masked_value}")
            else:
                print(f"   ✅ {var:<20} = {value}")
        else:
            print(f"   ⚠️  {var:<20} = Not set")
    
    # API Endpoints
    print_section("API Endpoints (After Deployment)")
    endpoints = [
        ("/v1/health", "Health check endpoint"),
        ("/v1/agents", "Agent management"),
        ("/v1/sources", "Data source management"),
        ("/v1/tools", "Tool management"),
        ("/openai/chat/completions", "OpenAI-compatible chat API"),
        ("/docs", "Interactive API documentation")
    ]
    
    print("   Base URL: https://your-app.onrender.com")
    for endpoint, description in endpoints:
        print(f"   📡 {endpoint:<25} - {description}")
    
    # Deployment Steps
    print_section("Next Steps for Deployment")
    steps = [
        "1. Push this code to your GitHub repository",
        "2. Go to Render Dashboard (dashboard.render.com)",
        "3. Click 'New' → 'Blueprint'",
        "4. Connect your GitHub repository",
        "5. Render will detect render.yaml and deploy automatically",
        "6. Monitor deployment logs in Render dashboard",
        "7. Access your API at https://your-app.onrender.com"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    # Summary
    print_section("Deployment Readiness")
    
    readiness_checks = [
        ("Database Connection", db_ok),
        ("Migration Status", db_ok and db_info.get('migration_version') != 'Not set'),
        ("Docker Configuration", Path("/app/Dockerfile.render").exists()),
        ("Render Configuration", Path("/app/render.yaml").exists()),
        ("Environment Setup", bool(os.getenv("LETTA_PG_URI")))
    ]
    
    all_ready = all(check[1] for check in readiness_checks)
    
    for check_name, status in readiness_checks:
        status_emoji = "✅" if status else "❌"
        print(f"   {status_emoji} {check_name}")
    
    print_header("DEPLOYMENT STATUS")
    if all_ready:
        print("🎉 ALL SYSTEMS GO! Ready for deployment to Render")
        print("📚 See RENDER_DEPLOYMENT.md for detailed instructions")
    else:
        print("⚠️  Some issues detected. Please resolve before deployment.")
    
    print("\n🔗 Useful Links:")
    print("   - Render Dashboard: https://dashboard.render.com")
    print("   - Supabase Dashboard: https://app.supabase.com")
    print("   - Letta Documentation: https://docs.letta.com")
    
    return 0 if all_ready else 1

if __name__ == "__main__":
    sys.exit(main())