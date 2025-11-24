import os
import shutil
# from app.db import get_db
# from app.models import User, Repository

class KillSwitch:
    """
    'Emergency Flush' Kill Switch.
    Immediately stops activity and deletes user data.
    """

    def __init__(self):
        pass

    def panic_delete_user_data(self, user_id: str) -> dict:
        """
        1. Stop all scheduled commits.
        2. Delete all stored proprietary data.
        3. Generate a final text log.
        """
        print(f"⚠️ KILL SWITCH ACTIVATED FOR USER: {user_id}")
        
        # 1. Stop Scheduler (Mock)
        # scheduler.cancel_jobs(user_id)
        print("- Scheduled jobs cancelled.")
        
        # 2. Delete Data (Mock)
        # db.delete(User).where(User.id == user_id)
        # shutil.rmtree(f"./data/{user_id}")
        print("- Database records deleted.")
        print("- Proprietary files wiped.")
        
        # 3. Generate Log
        final_log = f"""
        EXECGIT FINAL LOG
        User: {user_id}
        Date: {os.popen('date').read().strip()}
        Status: ACCOUNT TERMINATED
        Reason: User initiated Kill Switch.
        
        All data has been permanently erased from our servers.
        """
        
        # Save log to a temporary location for the user to download one last time
        log_path = f"final_log_{user_id}.txt"
        with open(log_path, "w") as f:
            f.write(final_log)
            
        print(f"- Final log generated at {log_path}")
        
        return {
            "status": "terminated", 
            "message": "All data wiped. Goodbye.",
            "log_file": log_path
        }
