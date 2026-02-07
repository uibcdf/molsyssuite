#!/usr/bin/env python
import argparse
import subprocess
import sys
from pathlib import Path

def setup_editable_repos(base_path=None):
    """
    Installs MolSysSuite repositories in editable mode.
    If base_path is provided, looks there.
    Otherwise, looks in current directory and its parent.
    """
    repos_to_link = [
        'molsysmt', 'molsysviewer', 'smonitor', 
        'argdigest', 'depdigest', 'pyunitwizard'
    ]
    
    found_repos = {}

    print("-" * 50)
    print("MolSysSuite Developer Setup")
    print("-" * 50)

    if base_path:
        search_roots = [Path(base_path).resolve()]
        print(f"Searching in provided path: {search_roots[0]}")
    else:
        # Default safe behavior: look in current dir and parent dir
        cwd = Path('.').resolve()
        search_roots = [cwd, cwd.parent]
        print(f"No path provided. Searching in:\n  {search_roots[0]}\n  {search_roots[1]}")

    for repo_name in repos_to_link:
        for root in search_roots:
            # Check direct child
            candidate = root / repo_name
            if candidate.is_dir() and ((candidate / 'setup.py').exists() or (candidate / 'pyproject.toml').exists()):
                found_repos[repo_name] = candidate
                break
            
            # If a path was explicitly provided, we might want to be slightly more lenient 
            # and check one level deep (e.g. if user gave '~/repos', look in '~/repos/molsysmt')
            # But strictly speaking, usually you point to the parent folder of the repos.
            
    # Installation
    linked = []
    for repo_name in repos_to_link:
        if repo_name in found_repos:
            repo_path = found_repos[repo_name]
            print(f"[FOUND] {repo_name} at {repo_path}")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", 
                    "--no-deps", "-e", str(repo_path)
                ])
                linked.append(repo_name)
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] Failed to install {repo_name}: {e}")
        else:
            print(f"[SKIP]  {repo_name} not found.")

    print("-" * 50)
    if linked:
        print(f"Success! Linked {len(linked)} repositories.")
    else:
        print("No repositories were found.")
        print("Usage: molsys-dev-setup [path_to_repos]")
    print("-" * 50)

def main():
    parser = argparse.ArgumentParser(description="Link local MolSysSuite repositories in editable mode.")
    parser.add_argument("path", nargs="?", help="Path to the directory containing the repositories (optional)")
    args = parser.parse_args()
    
    setup_editable_repos(args.path)

if __name__ == "__main__":
    main()
