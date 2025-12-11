import streamlit as st
import os
import random
from datetime import datetime, timedelta
import subprocess

def generate_dummy_commits(repo_path, start_year, end_year):
    """
    Generates dummy commits to fill the contribution graph.
    """
    if not os.path.exists(repo_path):
        return "Repo path does not exist."
    
    start_date = datetime(start_year, 1, 1)
    end_date = datetime.now()
    
    current_date = start_date
    commits_made = 0
    
    dummy_file = os.path.join(repo_path, "activity_log.txt")
    
    while current_date <= end_date:
        # Weight towards weekdays (0=Monday, 6=Sunday)
        if current_date.weekday() < 5:
            # 80% chance of commit on weekday
            if random.random() < 0.8:
                num_commits = random.randint(1, 5)
                for _ in range(num_commits):
                    with open(dummy_file, "a") as f:
                        f.write(f"Activity on {current_date}\n")
                    
                    date_str = current_date.strftime("%Y-%m-%dT%H:%M:%S")
                    
                    # Git commit with specific date
                    # Note: This requires git to be installed and configured in the environment
                    env = os.environ.copy()
                    env["GIT_AUTHOR_DATE"] = date_str
                    env["GIT_COMMITTER_DATE"] = date_str
                    
                    subprocess.run(["git", "add", "activity_log.txt"], cwd=repo_path, env=env)
                    subprocess.run(["git", "commit", "-m", f"Update activity log {date_str}"], cwd=repo_path, env=env)
                    commits_made += 1
        else:
            # 20% chance on weekend
            if random.random() < 0.2:
                 with open(dummy_file, "a") as f:
                        f.write(f"Activity on {current_date}\n")
                 date_str = current_date.strftime("%Y-%m-%dT%H:%M:%S")
                 env = os.environ.copy()
                 env["GIT_AUTHOR_DATE"] = date_str
                 env["GIT_COMMITTER_DATE"] = date_str
                 subprocess.run(["git", "add", "activity_log.txt"], cwd=repo_path, env=env)
                 subprocess.run(["git", "commit", "-m", f"Update activity log {date_str}"], cwd=repo_path, env=env)
                 commits_made += 1

        current_date += timedelta(days=1)
        
    return f"Successfully generated {commits_made} commits from {start_year} to now."

def render_github_tools_tab():
    st.header("Legacy Migrator (History Filler)")
    st.markdown("Fill your contribution graph to match your years of experience.")
    
    repo_path = st.text_input("Absolute Path to Local Repository")
    start_year = st.number_input("Start Year", min_value=2000, max_value=2025, value=2020)
    
    if st.button("Generate History"):
        if repo_path:
            with st.spinner("Generating dummy history..."):
                result = generate_dummy_commits(repo_path, start_year, 2025)
                st.success(result)
                st.warning("Remember to 'git push --force' to update your GitHub profile.")
        else:
            st.error("Please enter a repository path.")
