---
description: How to deploy the LinkedIn Optimizer on Windows Server
---

# Deploying DevCareer Project on Windows Server

This guide outlines the steps to deploy the Streamlit application on a Windows Server.

## Prerequisites

1.  **Python 3.10+**: Download and install from [python.org](https://www.python.org/downloads/windows/).
    *   **Important**: Check "Add Python to PATH" during installation.
2.  **Git**: Download and install from [git-scm.com](https://git-scm.com/download/win).

## Step 1: Clone the Repository

Open PowerShell or Command Prompt and run:

```powershell
cd C:\
git clone <YOUR_REPO_URL> geme-resume
cd geme-resume
```
*(Or copy your project folder `d:\geme-resume` to the server manually)*

## Step 2: Set up Virtual Environment

It's best practice to run Python apps in a virtual environment.

```powershell
python -m venv venv
.\venv\Scripts\activate
```

## Step 3: Install Dependencies

Install the required Python packages:

```powershell
pip install -r requirements.txt
```

*If you don't have a `requirements.txt`, create one with:*
```powershell
pip freeze > requirements.txt
```
*(Make sure `streamlit`, `google-generativeai`, `pypdf`, `python-docx`, `pillow`, `qrcode` are installed)*

## Step 4: Configure API Key

You need to set your Gemini API Key.

**Option A: Environment Variable (Recommended)**
```powershell
$env:GEMINI_API_KEY="your_actual_api_key_here"
```
*(To make this permanent, search "Edit the system environment variables" in Windows Start menu)*

**Option B: Secrets File**
Create a file at `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_actual_api_key_here"
```

## Step 5: Run the Application

```powershell
streamlit run DevCareer_Project/admin_panel/dashboard.py --server.port 80
```

*   Access the app at `http://localhost` or `http://<YOUR_SERVER_IP>`.

## Step 6: Run as a Background Service (Optional)

To keep the app running after you log out, use **NSSM (Non-Sucking Service Manager)**.

1.  Download NSSM from [nssm.cc](https://nssm.cc/download).
2.  Extract `nssm.exe` to `C:\Windows\System32`.
3.  Run:
    ```powershell
    nssm install DevCareerApp
    ```
4.  **Path**: `C:\path\to\geme-resume\venv\Scripts\streamlit.exe`
5.  **Startup Directory**: `C:\path\to\geme-resume`
6.  **Arguments**: `run DevCareer_Project/admin_panel/dashboard.py --server.port 80`
7.  Click **Install Service**.
8.  Start the service: `nssm start DevCareerApp`

Your app is now live! 🚀
