from typing import List, Dict

class SocialBridge:
    """
    'Commit-to-LinkedIn' Ghostwriter.
    Generates viral-style LinkedIn posts from code updates.
    """

    def __init__(self):
        # Initialize LLM client here (mocked for MVP)
        pass

    def generate_linkedin_post(self, commit_diff: str, user_persona: str) -> Dict[str, str]:
        """
        Generates 3 variations of a LinkedIn post based on the commit diff and persona.
        """
        
        # System Prompt Construction (for the LLM)
        system_prompt = f"""
        Act as a Developer Advocate and Social Media Expert.
        I will provide a 'git diff' and a 'User Persona'.
        
        User Persona: {user_persona}
        
        Tone Check:
        - If Persona is "CTO": Focus on "Scalability, ROI, and Business Impact."
        - If Persona is "Architect": Focus on "Performance, Latency, and Clean Code."
        
        Task:
        Write 3 variations of a LinkedIn post:
        1. Viral Style: Short sentences, hooks, "Learn More" CTA.
        2. Professional Style: Formal, discussing the engineering challenge.
        3. Educational Style: "Here is how I solved X."
        
        Do NOT just summarize the code. Tell a story about a problem and a solution.
        """
        
        # Mock LLM Call
        # response = llm.chat(system_prompt, commit_diff)
        
        # Mock Response based on persona
        if "CTO" in user_persona:
            viral = "Just slashed our cloud bill by 30% with one simple optimization. 🚀\n\nScalability isn't just about handling more users; it's about efficiency. \n\n#TechLeadership #ROI #CloudComputing"
            professional = "Optimizing for cost-efficiency is a key responsibility of technical leadership. We recently refactored our core service to reduce overhead, resulting in significant operational savings."
            educational = "Here is how we optimized our cloud infrastructure:\n1. Analyzed resource utilization.\n2. Identified bottlenecks.\n3. Refactored for concurrency.\n\nResult: 30% cost reduction."
        else: # Architect or others
            viral = "Latency is the new downtime. ⚡\n\nJust shaved 200ms off our API response time. Clean code pays dividends.\n\n#Engineering #Performance #Python"
            professional = "Performance optimization is an ongoing journey. By refactoring our data access layer, we achieved a 200ms reduction in P99 latency."
            educational = "Here is how I solved the latency issue:\n1. Profiled the application.\n2. Optimized database queries.\n3. Implemented caching.\n\nResult: Faster API responses."

        return {
            "viral": viral,
            "professional": professional,
            "educational": educational,
            "system_prompt_used": system_prompt
        }
