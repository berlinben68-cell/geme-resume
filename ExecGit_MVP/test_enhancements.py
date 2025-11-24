import sys
import os
import textwrap

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from app.services.social_bridge import SocialBridge
    from app.services.trend_surfer import TrendSurfer
    
    print("New modules imported successfully.")
    
    # Test Social Bridge
    bridge = SocialBridge()
    diff = "diff --git a/main.py b/main.py\n+ print('Optimized')"
    posts = bridge.generate_linkedin_post(diff, "Innovative CTO")
    if "viral" in posts and "professional" in posts:
        print("Social Bridge test passed.")
    else:
        print("Social Bridge test failed.")
        
    # Test Trend Surfer
    surfer = TrendSurfer()
    trends = surfer.get_trending_topics("python")
    print(f"Trends fetched: {len(trends)}")
    
    suggestion = surfer.recommend_project("FinTech CTO", ["Zero-Knowledge Proofs"])
    if "ZK-Rollup" in suggestion:
        print("Trend Surfer recommendation test passed.")
    else:
        print("Trend Surfer recommendation test failed.")
        
except Exception as e:
    print(f"Verification failed: {e}")
