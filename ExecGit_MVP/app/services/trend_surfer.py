import requests
from bs4 import BeautifulSoup
from typing import List, Dict

class TrendSurfer:
    """
    'Trend Surfer' Relevance Engine.
    Ensures clients have repositories featuring the latest technology.
    """

    def __init__(self):
        self.trending_url = "https://github.com/trending"
        self.hot_keywords = ["RAG", "Agents", "Blockchain", "Zero-Knowledge Proofs", "Rust", "LLM", "Generative AI"]

    def get_trending_topics(self, language: str = "") -> List[str]:
        """
        Scrapes GitHub Trending page for repository names and descriptions.
        """
        url = self.trending_url
        if language:
            url += f"/{language}"
            
        try:
            # Note: GitHub often blocks simple scrapers. 
            # In production, use GitHub API or a robust scraper with headers/proxies.
            # For MVP, we'll try a simple request, but fallback to mock data if it fails.
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                repos = soup.select('article.Box-row h2 a')
                return [repo.text.strip().replace("\n", "").replace(" ", "") for repo in repos[:10]]
            else:
                return self._get_mock_trends(language)
        except Exception:
            return self._get_mock_trends(language)

    def _get_mock_trends(self, language: str) -> List[str]:
        """
        Fallback mock data for trending topics.
        """
        if language == "python":
            return ["AutoGPT", "LangChain-Demo", "FastAPI-Boilerplate", "PyTorch-Transformers"]
        elif language == "javascript":
            return ["Next.js-14", "React-Three-Fiber", "Bun-Runtime", "Vite-Config"]
        else:
            return ["DeepSeek-LLM", "Rust-Kernel", "Zero-Knowledge-Rollup", "Agent-Swarm"]

    def recommend_project(self, client_profile: str, current_trends: List[str]) -> str:
        """
        Recommends a project based on client profile and current trends.
        """
        # Simple keyword matching for MVP
        recommendation = "Create a new repository."
        
        if "FinTech" in client_profile:
            if any("Zero-Knowledge" in t for t in current_trends) or "Zero-Knowledge Proofs" in self.hot_keywords:
                recommendation = "Suggestion: Create a simple 'ZK-Rollup-Demo' repo. This tech is trending in FinTech right now."
            elif "Blockchain" in self.hot_keywords:
                 recommendation = "Suggestion: Build a 'DeFi-Aggregator' prototype. Blockchain is hot."
        
        elif "AI" in client_profile or "Data" in client_profile:
            if "RAG" in self.hot_keywords:
                recommendation = "Suggestion: Implement a 'RAG-Document-Chat' using LangChain. Retrieval Augmented Generation is very popular."
            elif "Agents" in self.hot_keywords:
                recommendation = "Suggestion: Build a multi-agent system simulation. Autonomous Agents are the next big thing."

        return recommendation

    def analyze_trends_for_client(self, client_profile: str) -> Dict:
        """
        Full analysis pipeline.
        """
        # 1. Fetch Trends (Global)
        global_trends = self.get_trending_topics()
        
        # 2. Filter/Match
        suggestion = self.recommend_project(client_profile, global_trends)
        
        return {
            "global_trends": global_trends,
            "hot_keywords_tracked": self.hot_keywords,
            "project_suggestion": suggestion
        }
