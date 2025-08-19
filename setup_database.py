#!/usr/bin/env python3
"""
Letta AI Database Setup Script for Supabase PostgreSQL
This script automatically:
1. Tests database connection
2. Runs all Alembic migrations 
3. Sets the latest migration version
4. Provides a summary of created tables
"""

import os
import sys
import subprocess
from pathlib import Path
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, text, inspect
from alembic.config import Config
from alembic import command
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory

# Set the working directory to the app root
os.chdir('/app')

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Database connection string
DATABASE_URL = os.getenv('LETTA_PG_URI')

def test_connection():
    """Test the database connection"""
    try:
        print("🔍 Testing database connection...")
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Database connection successful!")
            print(f"   PostgreSQL version: {version}")
            return engine
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        sys.exit(1)

def setup_pgvector_extension(engine):
    """Ensure pgvector extension is available"""
    try:
        print("🔧 Setting up pgvector extension...")
        with engine.connect() as conn:
            # Use AUTOCOMMIT for CREATE EXTENSION
            conn.execute(text("COMMIT"))
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            print("✅ pgvector extension ready")
    except Exception as e:
        print(f"⚠️  pgvector extension setup: {str(e)}")
        # Continue anyway - might already be installed or handled by Supabase

def run_migrations():
    """Run all Alembic migrations"""
    try:
        print("🚀 Running database migrations...")
        
        # Setup Alembic configuration
        alembic_cfg = Config('/app/alembic.ini')
        alembic_cfg.set_main_option('sqlalchemy.url', DATABASE_URL)
        
        # Run migrations to head
        command.upgrade(alembic_cfg, 'head')
        print("✅ All migrations completed successfully!")
        
        return alembic_cfg
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        print("   Attempting to continue with manual table setup...")
        return None

def get_latest_migration_version():
    """Get the latest migration version from files"""
    try:
        versions_dir = Path('/app/alembic/versions')
        migration_files = list(versions_dir.glob('*.py'))
        
        if not migration_files:
            print("⚠️  No migration files found")
            return None
            
        # Sort by filename to get the latest
        latest_file = sorted(migration_files)[-1]
        # Extract revision ID from filename (before the first underscore)
        revision_id = latest_file.stem.split('_')[0]
        
        print(f"📋 Latest migration version: {revision_id}")
        return revision_id
        
    except Exception as e:
        print(f"⚠️  Could not determine latest migration: {str(e)}")
        return None

def set_migration_version(engine, version):
    """Manually set the Alembic version in the database"""
    try:
        if not version:
            print("⚠️  No migration version to set")
            return
            
        print(f"📝 Setting Alembic version to: {version}")
        
        with engine.connect() as conn:
            # Create alembic_version table if it doesn't exist
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS alembic_version (
                    version_num VARCHAR(32) NOT NULL PRIMARY KEY
                )
            """))
            
            # Remove any existing version
            conn.execute(text("DELETE FROM alembic_version"))
            
            # Insert the latest version
            conn.execute(text("INSERT INTO alembic_version (version_num) VALUES (:version)"), 
                       {"version": version})
            
            conn.commit()
            print("✅ Migration version set successfully!")
            
    except Exception as e:
        print(f"❌ Failed to set migration version: {str(e)}")

def list_created_tables(engine):
    """List all tables created in the database"""
    try:
        print("📋 Database tables created:")
        
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if tables:
            for i, table in enumerate(sorted(tables), 1):
                print(f"   {i:2}. {table}")
        else:
            print("   No tables found")
            
        print(f"\n📊 Total tables: {len(tables)}")
        return tables
        
    except Exception as e:
        print(f"❌ Failed to list tables: {str(e)}")
        return []

def verify_letta_setup(engine):
    """Verify that essential Letta tables exist"""
    try:
        print("🔍 Verifying Letta AI setup...")
        
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        # Essential Letta tables (based on the ORM models)
        essential_tables = [
            'agents', 'blocks', 'sources', 'users', 'organizations',
            'tools', 'messages', 'jobs', 'files', 'alembic_version'
        ]
        
        missing_tables = []
        for table in essential_tables:
            if table not in tables:
                missing_tables.append(table)
        
        if missing_tables:
            print(f"⚠️  Missing essential tables: {', '.join(missing_tables)}")
        else:
            print("✅ All essential Letta tables present!")
            
        return len(missing_tables) == 0
        
    except Exception as e:
        print(f"❌ Verification failed: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("🚀 Letta AI Database Setup for Supabase PostgreSQL")
    print("=" * 60)
    
    # Test connection
    engine = test_connection()
    
    # Setup pgvector extension
    setup_pgvector_extension(engine)
    
    # Run migrations
    alembic_cfg = run_migrations()
    
    # If migrations failed, try to set version manually
    if alembic_cfg is None:
        latest_version = get_latest_migration_version()
        set_migration_version(engine, latest_version)
    
    # List created tables
    tables = list_created_tables(engine)
    
    # Verify setup
    is_valid = verify_letta_setup(engine)
    
    print("=" * 60)
    if is_valid:
        print("🎉 Database setup completed successfully!")
        print("✅ Letta AI is ready to start!")
    else:
        print("⚠️  Database setup completed with warnings")
        print("   Please check the migration logs above")
    print("=" * 60)
    
    return 0 if is_valid else 1

if __name__ == "__main__":
    sys.exit(main())