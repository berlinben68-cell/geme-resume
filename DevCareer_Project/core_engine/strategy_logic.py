import google.generativeai as genai
import os
import json
import ast

# Configure Gemini API (Assuming API key is set in environment or handled elsewhere, 
# but for now we'll use a placeholder or expect it to be configured in main)
# In a real app, ensure genai.configure(api_key=...) is called.

class StrategyLogic:
    def __init__(self, api_key=None):
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def _clean_json_response(self, response_text):
        """
        Cleans and parses JSON response from Gemini.
        """
        try:
            # Remove markdown code blocks if present
            cleaned_text = response_text.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            try:
                # Fallback to ast.literal_eval if json fails (sometimes single quotes are used)
                return ast.literal_eval(cleaned_text)
            except:
                return None

    def golden_visa_gap_analysis(self, github_profile_summary):
        """
        Analyzes GitHub profile for UAE Golden Visa eligibility (AI, Blockchain, Data Science).
        """
        prompt = f"""
        Act as a UAE Immigration Consultant and Tech Architect.
        Analyze the following GitHub profile summary:
        {github_profile_summary}

        Compare it against the requirements for the 'UAE Golden Visa for Coders' (focusing on AI, Blockchain, and Data Science).
        
        Output a JSON object with the following structure:
        {{
            "status": "Eligible" or "Needs Improvement",
            "gap_analysis": "Brief analysis of why...",
            "suggested_projects": [
                {{
                    "title": "Project Title",
                    "description": "Description of the project...",
                    "tech_stack": "Tech stack to use..."
                }},
                ... (3 projects)
            ]
        }}
        """
        response = self.model.generate_content(prompt)
        return self._clean_json_response(response.text)

    def generate_arabic_readme(self, english_readme_content):
        """
        Generates a Professional Arabic translation of a README.
        """
        prompt = f"""
        Act as a Localization Expert.
        Translate the following English README content to 'Professional Arabic' (Fusha) suitable for Dubai Government entities.
        Do not use casual dialect.
        
        English Content:
        {english_readme_content}
        
        Output ONLY the Arabic translation.
        """
        response = self.model.generate_content(prompt)
        return response.text

    def western_compatibility_score(self, github_repo_summary):
        """
        Scores a GitHub repo for Western/Silicon Valley compatibility.
        """
        prompt = f"""
        Act as an International Recruiter.
        Scan the following GitHub repo summary for 'Red Flags' that Western recruiters dislike (e.g., lack of unit tests, poor variable naming, lack of license files).
        
        Repo Summary:
        {github_repo_summary}
        
        Output a JSON object:
        {{
            "score": 0-100,
            "red_flags": ["Flag 1", "Flag 2", ...],
            "improvements": ["Improvement 1", "Improvement 2", ...]
        }}
        """
        response = self.model.generate_content(prompt)
        return self._clean_json_response(response.text)

    def generate_interview_cheat_sheet(self, project_details):
        """
        Generates an Interview Cheat Sheet for a project.
        """
        prompt = f"""
        Act as a FAANG Technical Interviewer.
        Generate a 'Cheat Sheet' for the following project to help the user explain it in an interview.
        
        Project Details:
        {project_details}
        
        Output a JSON object:
        {{
            "architecture_defense": "Why did we use this stack? ...",
            "time_complexity": "Analysis of main algorithms...",
            "potential_improvements": "What could be better? ..."
        }}
        """
        response = self.model.generate_content(prompt)
        return self._clean_json_response(response.text)
