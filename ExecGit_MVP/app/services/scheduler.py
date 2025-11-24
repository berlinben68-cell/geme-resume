import os
import random
import datetime
from git import Repo, Actor
from typing import Optional

class GreenSquareScheduler:
    """
    Handles the 'Green Square' Heatmap Scheduler logic.
    Manipulates Git timestamps to match specific personas.
    """

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        # Ensure repo exists or handle error in real app
        try:
            self.repo = Repo(self.repo_path)
        except Exception as e:
            print(f"Warning: Could not initialize repo at {repo_path}: {e}")
            self.repo = None

    def _get_persona_timestamp(self, persona: str) -> datetime.datetime:
        """
        Generates a timestamp based on the requested persona.
        """
        now = datetime.datetime.now()
        
        if persona == "weekend_warrior":
            # Find the next Saturday or Sunday
            days_ahead = 5 - now.weekday() # 5 is Saturday
            if days_ahead <= 0: # Today is Sat or Sun
                days_ahead += 7
            
            # Randomize time between 10 AM and 6 PM
            target_date = now + datetime.timedelta(days=days_ahead)
            target_hour = random.randint(10, 18)
            target_minute = random.randint(0, 59)
            return target_date.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)

        elif persona == "night_owl":
            # Set time to late night (e.g., 11 PM - 3 AM)
            # If it's currently day, schedule for tonight. If it's already late, do it now or soon.
            target_hour = random.choice([23, 0, 1, 2, 3])
            target_minute = random.randint(0, 59)
            
            target_date = now
            if now.hour < 12 and target_hour >= 23:
                 # It's morning, schedule for tonight (same date if > midnight, but logic here is simple)
                 # Actually if it's 10 AM and we want 11 PM, it's same day.
                 pass
            elif now.hour > 4 and target_hour <= 3:
                # It's daytime, schedule for next early morning (tomorrow)
                target_date = now + datetime.timedelta(days=1)
            
            return target_date.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
        
        else:
            # Default: standard "during work" or immediate
            return now

    def commit_with_timestamp(self, message: str, files: list, persona: str = "standard", author_name: str = "GhostWriter", author_email: str = "ghost@execgit.com"):
        """
        Commits files with a manipulated timestamp.
        """
        if not self.repo:
            return {"status": "error", "message": "Repository not initialized"}

        # Stage files
        self.repo.index.add(files)

        # Calculate timestamp
        commit_date = self._get_persona_timestamp(persona)
        
        # Format for Git (ISO 8601-like or seconds since epoch)
        # GitPython allows passing author_date and commit_date
        # We need to convert datetime to string format expected by Git or use Actor
        
        # Create Actor with the specific time
        # Note: GitPython Actor takes name, email. Date is handled in commit args usually or by setting env vars.
        # But a cleaner way in GitPython is to pass 'author_date' and 'commit_date' to the commit function.
        
        # Convert to ISO format string
        date_str = commit_date.strftime("%Y-%m-%d %H:%M:%S")
        
        author = Actor(author_name, author_email)
        committer = Actor(author_name, author_email)
        
        # Commit with custom dates
        new_commit = self.repo.index.commit(
            message, 
            author=author, 
            committer=committer, 
            author_date=date_str, 
            commit_date=date_str
        )
        
        return {
            "status": "success", 
            "commit_hash": new_commit.hexsha, 
            "timestamp_used": date_str,
            "persona": persona
        }
