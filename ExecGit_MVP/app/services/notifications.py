class NotificationSystem:
    """
    'Notification System'.
    Sends weekly digests to clients via Email or WhatsApp (Mocked).
    """

    def __init__(self):
        pass

    def send_weekly_digest(self, user_id: str, stats: dict):
        """
        Sends a 'Boss Mode' digest.
        """
        message = f"""
        Boss Mode Activated 🚀
        
        User: {user_id}
        
        This week's achievements:
        - Pushed {stats.get('commits', 0)} commits
        - Fixed {stats.get('docs_fixed', 0)} docs
        - Profile views up {stats.get('view_increase', '0%')}
        
        Click here to approve next week's schedule: [Link]
        """
        
        # Mock Sending (e.g., via Twilio or SMTP)
        print(f"Sending Digest to {user_id}:")
        print(message)
        
        return {"status": "sent", "recipient": user_id}
