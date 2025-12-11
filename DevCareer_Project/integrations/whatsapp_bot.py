from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os

# Note: This requires 'flask' and 'twilio' to be installed.
# pip install flask twilio

app = Flask(__name__)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body').lower()
    resp = MessagingResponse()
    
    print(f"Received message: {msg}")

    if 'idea:' in msg:
        # Trigger Repo Generation Logic (Mock)
        idea = msg.replace('idea:', '').strip()
        reply_text = f"On it. Generating repo structure for: '{idea}'..."
        # In real app: call_repo_generator(idea)
        resp.message(reply_text)
        
    elif 'status' in msg:
        # Trigger Status Check (Mock)
        reply_text = "You have 4 commits pending approval."
        resp.message(reply_text)
        
    else:
        resp.message("I didn't catch that. Send 'Idea: <your idea>' or 'Status'.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
