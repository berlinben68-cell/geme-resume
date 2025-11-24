from typing import List, Dict

class OnboardingQuestionnaire:
    """
    'Onboarding Questionnaire' Logic.
    Determines user persona and adjusts AI settings.
    """

    def __init__(self):
        self.questions = [
            {
                "id": 1,
                "text": "Do you want to appear as a Specialist (Deep Python) or a Generalist (Full Stack)?",
                "options": ["Specialist", "Generalist"],
                "impact": "Adjusts language variety in generated repos."
            },
            {
                "id": 2,
                "text": "Are you targeting a job in FinTech, HealthTech, or E-commerce?",
                "options": ["FinTech", "HealthTech", "E-commerce", "General Tech"],
                "impact": "Selects domain-specific keywords and project types."
            },
            {
                "id": 3,
                "text": "What is your preferred coding style?",
                "options": ["Clean & Minimal", "Verbose & Documented", "Performance-Optimized"],
                "impact": "Tunes the Style Matcher parameters."
            },
            {
                "id": 4,
                "text": "How active do you want to appear on GitHub?",
                "options": ["Weekend Warrior (Sat/Sun)", "Daily Grinder (Mon-Fri)", "Night Owl (Late Night)"],
                "impact": "Sets the Green Square Scheduler persona."
            },
            {
                "id": 5,
                "text": "What is your primary goal?",
                "options": ["Get Hired", "Attract Investors", "Build Authority"],
                "impact": "Adjusts the tone of LinkedIn posts (Viral vs Professional)."
            }
        ]

    def get_questions(self) -> List[Dict]:
        return self.questions

    def process_answers(self, answers: Dict[int, str]) -> Dict:
        """
        Translates user answers into system configuration.
        """
        config = {
            "persona": "standard",
            "domain_focus": "general",
            "commit_frequency": "medium",
            "style_preset": "pep8"
        }
        
        # Logic to map answers to config
        # Mock implementation
        if "Weekend Warrior" in answers.get(4, ""):
            config["persona"] = "weekend_warrior"
        elif "Night Owl" in answers.get(4, ""):
            config["persona"] = "night_owl"
            
        if "FinTech" in answers.get(2, ""):
            config["domain_focus"] = "fintech"
            
        return config
