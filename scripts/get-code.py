#!/usr/bin/env python3
"""
Sync STM32MP code directly to OpenGrok directory using repo tool.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(cmd, cwd=None, shell=True):
    """Execute shell command and return result"""
    print(f"Executing command: {cmd}")
    try:
        result = subprocess.run(
            cmd, shell=shell, cwd=cwd, capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"Command failed: {result.stderr}")
            return False
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except Exception as e:
        print(f"Error executing command: {e}")
        return False


def setup_environment():
    """Set up environment variables"""
    target_dir = os.path.join(os.environ["HOME"], "opengrok", "src")

    # Set repo mirror source
    os.environ["REPO_URL"] = "https://mirrors.tuna.tsinghua.edu.cn/git/git-repo"

    print(f"Target directory (for direct sync): {target_dir}")
    print(f"REPO mirror source: {os.environ['REPO_URL']}")

    return target_dir


def cleanup_target_directory(target_dir):
    """Clean up target directory if needed"""
    if os.path.exists(target_dir):
        print(f"Target directory already exists: {target_dir}")

        # Check if target directory is empty
        if os.listdir(target_dir):
            print("Target directory is not empty.")
            print("Options:")
            print("  1. Clean up and continue")
            print("  2. Skip cleanup (may cause issues)")
            print("  3. Exit")

            while True:
                choice = input("Enter your choice (1/2/3): ").strip()
                if choice == "1":
                    print(f"Cleaning up {target_dir}...")
                    # Remove all contents but keep the directory
                    for item in os.listdir(target_dir):
                        item_path = os.path.join(target_dir, item)
                        try:
                            if os.path.isdir(item_path):
                                shutil.rmtree(item_path)
                            else:
                                os.remove(item_path)
                        except Exception as e:
                            print(f"Warning: Could not remove {item_path}: {e}")
                    print("Cleanup completed.")
                    return True
                elif choice == "2":
                    print("Continuing without cleanup...")
                    return True
                elif choice == "3":
                    print("Exiting...")
                    return False
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
        else:
            print("Target directory is empty, proceeding...")
            return True
    else:
        print(f"Creating target directory: {target_dir}")
        os.makedirs(target_dir, exist_ok=True)
        return True


def main():
    """Main function"""
    print("=" * 60)
    print("STM32MP Code Synchronization Script")
    print("Direct sync to OpenGrok directory")
    print("=" * 60)

    # Step 1: Set up environment and get target directory
    target_dir = setup_environment()

    # # Step 2: Clean up target directory if needed
    # if not cleanup_target_directory(target_dir):
    #     return 1

    # Step 3: Change to target directory
    os.chdir(target_dir)
    print(f"Current working directory: {os.getcwd()}")

    # Step 4: Initialize repo directly in target directory
    print("\n1. Initializing repo repository in target directory...")
    repo_init_cmd = (
        "repo init -u git@gitee.com:zhyantao/manifest.git "
        "-b cross-referencer -m STM32MP157_V11.xml"
    )
    if not run_command(repo_init_cmd):
        print("Repo initialization failed")
        return 1

    # Step 5: Sync code directly to target directory
    print(f"\n2. Syncing code repositories directly to {target_dir}...")
    repo_sync_cmd = f"cd {target_dir}/.repo/manifests; git pull --rebase; cd {target_dir}; repo sync --force-sync -j8"
    if not run_command(repo_sync_cmd):
        print("Repo sync failed")
        return 1

    print("\n" + "=" * 60)
    print("Code synchronization completed!")
    print(f"Code synced directly to: {target_dir}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
