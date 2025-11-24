import os
import textwrap
from typing import List, Tuple, Optional, Dict, Any, Union
from PIL import Image, ImageDraw, ImageFont
import qrcode

class VisualFactory:
    # Theme Constants
    COLORS = {
        'bg_dark': (20, 20, 20),
        'bg_navy': (10, 25, 47),
        'bg_white': (255, 255, 255),
        'bg_light_gray': (240, 240, 240),
        'text_white': (255, 255, 255),
        'text_black': (0, 0, 0),
        'text_gray': (200, 200, 200),
        'text_cyan': (100, 255, 218),
        'text_red': (255, 80, 80),
        'text_green': (80, 255, 80),
        'text_dark_green': (0, 153, 76),
        'text_blue': (0, 102, 204),
        'line_gray': (100, 100, 100),
    }
    
    FONTS = {
        'arial': "C:\\Windows\\Fonts\\arial.ttf",
        'arial_bold': "C:\\Windows\\Fonts\\arialbd.ttf"
    }

    def __init__(self):
        self._font_cache: Dict[Tuple[str, int], Union[ImageFont.FreeTypeFont, ImageFont.ImageFont]] = {}
        # Validate fonts exist, otherwise fallback logic will handle it in _get_font
        self.has_custom_fonts = os.path.exists(self.FONTS['arial']) and os.path.exists(self.FONTS['arial_bold'])

    def _get_font(self, size: int, bold: bool = False) -> Union[ImageFont.FreeTypeFont, ImageFont.ImageFont]:
        key = ('bold' if bold else 'regular', size)
        if key in self._font_cache:
            return self._font_cache[key]

        font = None
        try:
            if self.has_custom_fonts:
                path = self.FONTS['arial_bold'] if bold else self.FONTS['arial']
                font = ImageFont.truetype(path, size)
            else:
                # Fallback to default if custom fonts are missing
                font = ImageFont.load_default()
        except Exception:
             font = ImageFont.load_default()
        
        self._font_cache[key] = font
        return font

    def _draw_multiline_text(self, draw: ImageDraw.ImageDraw, text: str, x: float, y: float, 
                             font: Any, fill: Union[Tuple[int, int, int], str], width_chars: int, line_spacing: int = 50) -> int:
        """
        Draws wrapped text and returns the new Y position.
        """
        lines = textwrap.wrap(text, width=width_chars)
        current_y = y
        for line in lines:
            draw.text((x, current_y), line, fill=fill, font=font)
            current_y += line_spacing
        return current_y

    def generate_impact_card(self, problem: str, solution: str, output_path: str = "impact_card.png") -> str:
        """
        Generates a split-screen Before/After Impact Card.
        """
        width, height = 1200, 630 # LinkedIn Post Size
        img = Image.new('RGB', (width, height), color=self.COLORS['bg_dark'])
        draw = ImageDraw.Draw(img)
        
        # Split Line
        draw.line([(width/2, 50), (width/2, height-50)], fill=self.COLORS['line_gray'], width=3)
        
        # Fonts
        title_font = self._get_font(60, bold=True)
        text_font = self._get_font(40)
        
        # Left Side (Problem)
        draw.text((50, 50), "BEFORE", fill=self.COLORS['text_red'], font=title_font)
        self._draw_multiline_text(draw, problem, 50, 150, text_font, self.COLORS['text_gray'], 20)
            
        # Right Side (Solution)
        draw.text((width/2 + 50, 50), "AFTER", fill=self.COLORS['text_green'], font=title_font)
        self._draw_multiline_text(draw, solution, width/2 + 50, 150, text_font, self.COLORS['text_gray'], 20)
            
        img.save(output_path)
        return output_path

    def generate_tech_badge(self, tech_stack: str, output_path: str = "tech_badge.png") -> str:
        """
        Generates a sleek dark-mode tech stack badge.
        """
        width, height = 1200, 400
        img = Image.new('RGB', (width, height), color=self.COLORS['bg_navy'])
        draw = ImageDraw.Draw(img)
        
        # Title
        title_font = self._get_font(50, bold=True)
        draw.text((50, 30), "CORE TECH STACK", fill=self.COLORS['text_cyan'], font=title_font)
        
        # Tech Items
        item_font = self._get_font(40)
        tech_items = [t.strip() for t in tech_stack.split(',')]
        
        x = 50
        y = 120
        for item in tech_items:
            # Draw a "pill" or box
            text_bbox = draw.textbbox((x, y), f"  {item}  ", font=item_font)
            text_width = text_bbox[2] - text_bbox[0]
            
            draw.rectangle([x, y, x + text_width, y + 60], outline=self.COLORS['text_cyan'], width=2)
            draw.text((x, y + 5), f"  {item}  ", fill=self.COLORS['text_white'], font=item_font)
            
            x += text_width + 30
            if x > width - 100: # Wrap to next line if needed
                x = 50
                y += 80

        img.save(output_path)
        return output_path

    def generate_carousel_slides(self, title: str, metrics: List[str], problem: str = "Legacy System", 
                                 solution: str = "Microservices", tech_stack: str = "Java, AWS", 
                                 output_pdf_path: str = "carousel.pdf") -> str:
        """
        Generates 5 slides and saves as a PDF.
        """
        width, height = 1080, 1080 # Square for Carousel
        slides = []
        
        # Helper to create a blank slide
        def create_slide(bg_color: Tuple[int, int, int]) -> Image.Image:
            return Image.new('RGB', (width, height), color=bg_color)

        f_title = self._get_font(80, bold=True)
        f_header = self._get_font(60, bold=True)
        f_text = self._get_font(40)
        
        # Slide 1: Hook Title
        s1 = create_slide(self.COLORS['bg_navy'])
        d1 = ImageDraw.Draw(s1)
        d1.text((100, 400), "CASE STUDY:", fill=self.COLORS['text_cyan'], font=f_text)
        self._draw_multiline_text(d1, title, 100, 500, f_title, self.COLORS['text_white'], 15, 100)
        slides.append(s1)
        
        # Slide 2: The Challenge
        s2 = create_slide(self.COLORS['bg_light_gray'])
        d2 = ImageDraw.Draw(s2)
        d2.text((100, 100), "THE CHALLENGE", fill=self.COLORS['text_black'], font=f_header)
        self._draw_multiline_text(d2, problem, 100, 300, f_title, self.COLORS['text_red'], 25, 90)
        slides.append(s2)
        
        # Slide 3: The Solution (Architecture)
        s3 = create_slide(self.COLORS['bg_white'])
        d3 = ImageDraw.Draw(s3)
        d3.text((100, 100), "THE SOLUTION", fill=self.COLORS['text_black'], font=f_header)
        
        # Placeholder Diagram
        d3.rectangle([200, 300, 400, 500], outline="black", width=5)
        d3.text((220, 380), "Client", fill="black", font=f_text)
        d3.line([(400, 400), (600, 400)], fill="black", width=5)
        d3.rectangle([600, 300, 800, 500], outline="black", width=5)
        d3.text((620, 380), "Server", fill="black", font=f_text)
        d3.text((200, 800), solution, fill=self.COLORS['text_blue'], font=f_text)
        slides.append(s3)

        # Slide 4: Tech Stack
        s4 = create_slide(self.COLORS['bg_navy'])
        d4 = ImageDraw.Draw(s4)
        d4.text((100, 100), "TECH STACK", fill=self.COLORS['text_cyan'], font=f_header)
        
        stack_items = tech_stack.split(',')
        y = 300
        for item in stack_items:
            d4.text((150, y), f"> {item.strip()}", fill=self.COLORS['text_white'], font=f_title)
            y += 120
        slides.append(s4)
        
        # Slide 5: The Result
        s5 = create_slide(self.COLORS['bg_white'])
        d5 = ImageDraw.Draw(s5)
        d5.text((100, 100), "KEY RESULTS", fill=self.COLORS['text_black'], font=f_header)
        
        y = 300
        for metric in metrics:
            d5.text((100, y), f"• {metric}", fill=self.COLORS['text_dark_green'], font=f_text)
            y += 150
        slides.append(s5)
        
        # Save as PDF
        slides[0].save(output_pdf_path, save_all=True, append_images=slides[1:])
        return output_pdf_path

    def generate_linkedin_banner(self, name: str, tagline: str, portfolio_url: str, output_path: str = "linkedin_banner.png") -> str:
        """
        Generates a custom LinkedIn Banner with QR Code.
        """
        width, height = 1584, 396 # LinkedIn Banner Size
        img = Image.new('RGB', (width, height), color=self.COLORS['bg_navy'])
        draw = ImageDraw.Draw(img)
        
        # Fonts
        f_name = self._get_font(60, bold=True)
        f_tag = self._get_font(40)
        
        # Text
        draw.text((50, 100), name, fill=self.COLORS['text_white'], font=f_name)
        draw.text((50, 180), tagline, fill=self.COLORS['text_cyan'], font=f_tag)
        
        # QR Code
        qr = qrcode.make(portfolio_url)
        qr = qr.resize((250, 250))
        img.paste(qr, (1250, 70))
        
        # CTA
        draw.text((1260, 330), "Scan for Portfolio", fill=self.COLORS['text_white'], font=self._get_font(20))
        
        img.save(output_path)
        return output_path
