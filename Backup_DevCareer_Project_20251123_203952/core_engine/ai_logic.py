
# ai_logic.py
import os
try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

from .prompts import (
    get_resume_prompt, get_github_architect_prompt, get_linkedin_optimizer_prompt, 
    get_ats_score_prompt, get_visual_content_prompt, get_keyword_injection_prompt,
    get_recruiter_simulator_prompt, get_recommendation_prompt, 
    get_content_calendar_prompt, get_competitor_gap_prompt,
    get_role_and_stack_extraction_prompt, get_naukri_optimizer_prompt,
    get_ats_simulation_prompt, get_formatting_audit_prompt,
    get_resume_parsing_prompt, get_cover_letter_prompt
)

class IntelligenceEngine:
    def __init__(self, api_key):
        self.api_key = api_key
        if genai:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp') # Using a capable model
        else:
            print("Warning: google-generativeai not installed.")

    def parse_pdf(self, file_path):
        """
        Extracts text from a PDF file.
        """
        if not PdfReader:
            return "Error: pypdf library not installed."
        
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"

    def generate_content(self, prompt):
        """
        Generates content using Gemini.
        """
        if not genai:
            return "Error: google-generativeai library not installed."
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating content: {str(e)}"

    def rewrite_resume(self, resume_text, market="India"):
        prompt = get_resume_prompt(market, resume_text)
        return self.generate_content(prompt)

    def architect_project(self, description, tech_stack=""):
        prompt = get_github_architect_prompt(description, tech_stack)
        raw_text = self.generate_content(prompt)
        
        # Parse the 3 sections
        try:
            parts = raw_text.split("### SECTION BREAK ###")
            
            # Clean structure output
            structure_clean = parts[2].strip() if len(parts) > 2 else "Error generating Structure"
            structure_clean = structure_clean.replace("```", "").strip()
            
            return {
                "readme": parts[0].strip() if len(parts) > 0 else "Error generating README",
                "mermaid": parts[1].strip() if len(parts) > 1 else "graph TD; A[Error]-->B[No Diagram]",
                "structure": structure_clean
            }
        except Exception as e:
            return {
                "readme": f"Error parsing output: {e}\n\nRaw Output:\n{raw_text}",
                "mermaid": "graph TD; A[Error]-->B[Parse Failed]",
                "structure": ""
            }

    def optimize_linkedin(self, resume_text, target_role="Software Engineer", tech_stack=""):
        prompt = get_linkedin_optimizer_prompt(resume_text, target_role, tech_stack)
        return self.generate_content(prompt)

    def generate_bullets(self, role, company, description):
        """
        Generates high-impact bullet points for a specific job role.
        """
        prompt = f"""
        Act as an Expert Resume Writer.
        Write 3-4 high-impact, metric-driven bullet points for the following role:
        
        Role: {role}
        Company: {company}
        Context/Draft: {description}
        
        Rules:
        - Start with strong action verbs (Engineered, Spearheaded, Optimized).
        - Include numbers/metrics where possible (e.g., "Reduced latency by 20%").
        - Output ONLY the bullet points as an HTML unordered list (<ul><li>...</li></ul>).
        """
        return self.generate_content(prompt)

    def check_ats_score(self, resume_text, jd_text, market):
        prompt = get_ats_score_prompt(resume_text, jd_text, market)
        return self.generate_content(prompt)

    def extract_visual_content(self, resume_text, target_role):
        """
        Extracts structured data for visual assets.
        """
        prompt = get_visual_content_prompt(resume_text, target_role)
        raw_text = self.generate_content(prompt)
        
        # Clean up markdown code blocks if present
        clean_text = raw_text.replace("```json", "").replace("```", "").strip()
        
        data = {}
        try:
            lines = clean_text.split('\n')
            for line in lines:
                line = line.strip()
                if not line: continue
                
                # Remove potential bold markers and bullet points
                clean_line = line.replace("**", "").replace("*", "").strip()
                if clean_line.startswith("- "): clean_line = clean_line[2:]
                
                # Flexible parsing
                if clean_line.lower().startswith("title:"): 
                    data['title'] = clean_line.split(":", 1)[1].strip()
                elif clean_line.lower().startswith("problem:"): 
                    data['problem'] = clean_line.split(":", 1)[1].strip()
                elif clean_line.lower().startswith("solution:"): 
                    data['solution'] = clean_line.split(":", 1)[1].strip()
                elif clean_line.lower().startswith("results:"): 
                    results_part = clean_line.split(":", 1)[1].strip()
                    data['results'] = [r.strip() for r in results_part.split('|')]
                elif clean_line.lower().startswith("skills:"): 
                    data['skills'] = clean_line.split(":", 1)[1].strip()
            
            # Ensure we have at least some data to avoid failure
            if not data.get('title'): data['title'] = "Project Case Study"
            if not data.get('problem'): data['problem'] = "Scalability Challenge"
            if not data.get('solution'): data['solution'] = "Microservices Architecture"
            if not data.get('results'): data['results'] = ["Improved Performance", "Reduced Costs", "Higher Uptime"]
            if not data.get('skills'): data['skills'] = "Java, Python, AWS"
            
        except Exception as e:
            print(f"Error parsing visual content: {e}")
            # Return defaults on error so the user still gets something
            data = {
                'title': "Project Case Study",
                'problem': "Technical Challenge",
                'solution': "Innovative Solution",
                'results': ["Result 1", "Result 2", "Result 3"],
                'skills': "Tech 1, Tech 2, Tech 3"
            }
            
        return data

    def generate_keyword_injection(self, target_role, target_keywords):
        """
        Generates keyword-heavy project descriptions for SEO.
        """
        prompt = get_keyword_injection_prompt(target_role, target_keywords)
        return self.generate_content(prompt)

    def simulate_recruiter_review(self, image_data, target_role):
        """
        Uses Gemini Vision to critique a LinkedIn profile screenshot.
        image_data: bytes of the image
        """
        if not genai:
            return "Error: google-generativeai library not installed."
            
        prompt = get_recruiter_simulator_prompt(target_role)
        
        try:
            # Create the image part
            import PIL.Image
            import io
            image = PIL.Image.open(io.BytesIO(image_data))
            
            response = self.model.generate_content([prompt, image])
            return response.text
        except Exception as e:
            return f"Error analyzing image: {str(e)}"

    def generate_recommendations(self, role, key_achievement):
        prompt = get_recommendation_prompt(role, key_achievement)
        return self.generate_content(prompt)

    def generate_content_calendar(self, project_name, tech_stack):
        prompt = get_content_calendar_prompt(project_name, tech_stack)
        return self.generate_content(prompt)

    def analyze_competitor_gap(self, my_resume, competitor_text, target_role):
        prompt = get_competitor_gap_prompt(my_resume, competitor_text, target_role)
        return self.generate_content(prompt)

    def _extract_json(self, text):
        """
        Helper to robustly extract JSON from text.
        """
        import json
        import re
        import ast
        
        try:
            # 1. Try Regex + JSON
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                json_str = match.group(0)
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    pass # Try other methods
            
            # 2. Try cleaning + JSON
            clean_text = text.replace("```json", "").replace("```", "").strip()
            try:
                return json.loads(clean_text)
            except json.JSONDecodeError:
                pass

            # 3. Try ast.literal_eval (for single quotes/trailing commas)
            try:
                if match:
                    return ast.literal_eval(match.group(0))
                return ast.literal_eval(clean_text)
            except (ValueError, SyntaxError):
                pass
                
            print(f"Failed to parse JSON from: {text}")
            return None
        except Exception as e:
            print(f"Unexpected error in _extract_json: {e}")
            return None

    def extract_role_and_stack(self, resume_text):
        """
        Extracts suggested role and stack from resume.
        """
        prompt = get_role_and_stack_extraction_prompt(resume_text)
        raw_text = self.generate_content(prompt)
        
        data = self._extract_json(raw_text)
        if data:
            return data
        else:
            print(f"Error parsing role/stack from: {raw_text}")
            return {"role": "", "stack": ""}

    def optimize_naukri_profile(self, resume_text, target_role):
        """
        Generates Naukri.com optimization content.
        """
        prompt = get_naukri_optimizer_prompt(resume_text, target_role)
        return self.generate_content(prompt)

    def simulate_ats_parsing(self, resume_text):
        """
        Simulates how an ATS parses the resume.
        """
        prompt = get_ats_simulation_prompt(resume_text)
        print("DEBUG: Sending prompt to Gemini...")
        raw_text = self.generate_content(prompt)
        print(f"DEBUG: Raw Gemini response: {raw_text}")
        
        data = self._extract_json(raw_text)
        if data:
            return data
        else:
            print(f"Error parsing ATS simulation from: {raw_text}")
            return {
                "error": "Failed to parse ATS output", 
                "raw_output": raw_text
            }

    def audit_resume_formatting(self, resume_text):
        """
        Audits the resume for formatting issues based on extracted text.
        """
        prompt = get_formatting_audit_prompt(resume_text)
        return self.generate_content(prompt)

    def parse_resume_json(self, resume_text):
        """
        Parses resume text into structured JSON for the builder.
        """
        prompt = get_resume_parsing_prompt(resume_text)
        raw_text = self.generate_content(prompt)
        
        data = self._extract_json(raw_text)
        if data:
            return data
        else:
            print(f"Error parsing resume JSON from: {raw_text}")
            return None

    def generate_cover_letter(self, resume_text, job_description, tone="Professional"):
        """
        Generates a tailored cover letter.
        """
        prompt = get_cover_letter_prompt(resume_text, job_description, tone)
        return self.generate_content(prompt)



