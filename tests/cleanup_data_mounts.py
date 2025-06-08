#!/usr/bin/env python3
"""
Data Mount Cleanup Utility

This script helps clean up old/duplicate data mount directories that can
accumulate during development and testing.

Usage:
    python tests/cleanup_data_mounts.py [--dry-run]
"""

import os
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, check=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr, e.returncode

def check_container_running():
    """Check if MCPO container is running"""
    stdout, stderr, code = run_command("docker compose ps mcpo", check=False)
    return "Up" in stdout and "healthy" in stdout

def list_data_directories():
    """List all directories in the data mount"""
    data_path = Path("data")
    if not data_path.exists():
        return []
    
    directories = []
    for item in data_path.iterdir():
        if item.is_dir():
            directories.append(item.name)
    return directories

def get_expected_structure():
    """Get the expected data mount structure"""
    return {
        "mcp-servers": "New structure working directories",
        ".uv-cache": "UV package cache"
    }

def cleanup_old_directories(dry_run=False):
    """Clean up old/duplicate directories"""
    print("🧹 Data Mount Cleanup Utility")
    print("=" * 50)
    
    # Check if container is running
    if not check_container_running():
        print("❌ MCPO container is not running or not healthy")
        print("   Please start the container first: docker compose up -d")
        return False
    
    # List current directories
    current_dirs = list_data_directories()
    expected = get_expected_structure()
    
    print(f"\n📁 Current data directories:")
    for dir_name in current_dirs:
        if dir_name in expected:
            print(f"   ✅ {dir_name} - {expected[dir_name]}")
        else:
            print(f"   ⚠️  {dir_name} - Unknown/Legacy directory")
    
    # Identify cleanup candidates
    cleanup_candidates = [d for d in current_dirs if d not in expected]
    
    if not cleanup_candidates:
        print(f"\n🎉 Data mount is clean! No cleanup needed.")
        return True
    
    print(f"\n🗑️  Cleanup candidates:")
    for candidate in cleanup_candidates:
        print(f"   - {candidate}")
    
    if dry_run:
        print(f"\n🔍 DRY RUN: Would clean up {len(cleanup_candidates)} directories")
        return True
    
    # Confirm cleanup
    response = input(f"\n❓ Clean up {len(cleanup_candidates)} directories? (y/N): ")
    if response.lower() != 'y':
        print("   Cleanup cancelled.")
        return True
    
    # Perform cleanup
    success_count = 0
    for candidate in cleanup_candidates:
        print(f"\n🗑️  Cleaning up: {candidate}")
        
        # Use docker exec to remove directories (handles permissions)
        cmd = f"docker exec mcpo rm -rf /memory/{candidate}"
        stdout, stderr, code = run_command(cmd, check=False)
        
        if code == 0:
            print(f"   ✅ Successfully removed {candidate}")
            success_count += 1
        else:
            print(f"   ❌ Failed to remove {candidate}: {stderr}")
    
    print(f"\n📊 Cleanup Summary:")
    print(f"   Successfully cleaned: {success_count}/{len(cleanup_candidates)}")
    
    if success_count == len(cleanup_candidates):
        print(f"   🎉 All cleanup completed successfully!")
        return True
    else:
        print(f"   ⚠️  Some cleanup operations failed")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Clean up data mount directories")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be cleaned up without actually doing it")
    
    args = parser.parse_args()
    
    try:
        success = cleanup_old_directories(dry_run=args.dry_run)
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Cleanup interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Cleanup error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
