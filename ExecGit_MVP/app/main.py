from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional, List

# Import Services
from app.services.scheduler import GreenSquareScheduler
from app.services.style_matcher import StyleMatcher
from app.services.audio_engine import AudioEngine
from app.services.sanitizer import CorporateSanitizer
from app.services.scorer import RecruiterVisionScorer

app = FastAPI(title="ExecGit API", description="GitHub Ghostwriting for Technical Managers", version="0.1.0")

# Initialize Services
# Note: Repo path would be dynamic in a real multi-tenant app. 
# Here we default to a local temp repo for demonstration.
scheduler = GreenSquareScheduler(repo_path="./temp_repo") 
style_matcher = StyleMatcher()
audio_engine = AudioEngine()
sanitizer = CorporateSanitizer()
scorer = RecruiterVisionScorer()

# --- Data Models ---
class CommitRequest(BaseModel):
    message: str
    files: List[str] # List of file paths to commit
    persona: str = "standard" # weekend_warrior, night_owl

class StyleRequest(BaseModel):
    code_snippet: str

class SanitizeRequest(BaseModel):
    code: str

class ScoreRequest(BaseModel):
    github_username: str

# --- Endpoints ---

@app.get("/")
async def root():
    return {"message": "Welcome to ExecGit API - The GitHub Ghostwriter"}

# 1. Audio-to-Repo
@app.post("/generate-repo")
async def generate_repo_from_audio(file: UploadFile = File(...)):
    """
    Upload an audio note to generate a full repo structure.
    """
    # Save temp file
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        buffer.write(await file.read())
    
    result = audio_engine.process_audio(temp_filename)
    return result

# 2. Code DNA Style Matcher
@app.post("/analyze-style")
async def analyze_code_style(request: StyleRequest):
    """
    Analyze code snippet to extract 'Code DNA' style.
    """
    return style_matcher.analyze_style(request.code_snippet)

# 3. Green Square Scheduler
@app.post("/schedule-commit")
async def schedule_commit(request: CommitRequest):
    """
    Schedule a commit with a manipulated timestamp based on persona.
    """
    result = scheduler.commit_with_timestamp(
        message=request.message,
        files=request.files,
        persona=request.persona
    )
    
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result["message"])
        
    return result

# 4. Corporate Sanitizer
@app.post("/sanitize-code")
async def sanitize_code(request: SanitizeRequest):
    """
    Strip sensitive data and rewrite code for open source.
    """
    cleaned_code = sanitizer.sanitize(request.code)
    return {"original_length": len(request.code), "sanitized_code": cleaned_code}

# 5. Recruiter Vision Scorer
@app.post("/score-profile")
async def score_profile(request: ScoreRequest):
    """
    Get a hireability score based on UAE/India CTO trends.
    """
    return scorer.score_profile(request.github_username)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
