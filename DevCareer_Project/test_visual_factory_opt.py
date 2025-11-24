from core_engine.visual_factory import VisualFactory
import os

def test_visual_factory():
    vf = VisualFactory()
    
    print("Testing Impact Card...")
    vf.generate_impact_card("Slow Monolith", "Fast Microservices", "test_impact.png")
    assert os.path.exists("test_impact.png")
    print("Impact Card generated successfully.")
    
    print("Testing Tech Badge...")
    vf.generate_tech_badge("Python, React, AWS, Docker", "test_badge.png")
    assert os.path.exists("test_badge.png")
    print("Tech Badge generated successfully.")
    
    print("Testing Carousel...")
    vf.generate_carousel_slides("My Project", ["+50% Speed", "-20% Cost"], output_pdf_path="test_carousel.pdf")
    assert os.path.exists("test_carousel.pdf")
    print("Carousel generated successfully.")
    
    print("Testing Banner...")
    vf.generate_linkedin_banner("John Doe", "Software Engineer", "https://example.com", "test_banner.png")
    assert os.path.exists("test_banner.png")
    print("Banner generated successfully.")
    
    print("All tests passed!")

if __name__ == "__main__":
    test_visual_factory()
