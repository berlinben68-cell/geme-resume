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
        # Template-specific colors
        'yellow_bright': (255, 221, 89),
        'yellow_dark': (242, 193, 39),
        'gold': (255, 215, 0),
        'purple': (138, 43, 226),
        'orange': (255, 140, 0),
        'cyan_bright': (0, 255, 255),
        'gray_dark': (45, 45, 45),
    }
    
    # Banner Template Definitions
    BANNER_TEMPLATES = {
        'lead_generation': {
            'name': 'Lead Generation',
            'bg_primary': (255, 221, 89),  # Yellow
            'bg_secondary': (255, 255, 255),  # White
            'accent': (0, 0, 0),  # Black
            'text_primary': (0, 0, 0),
            'text_secondary': (80, 80, 80),
            'hook': 'Convert Your LinkedIn Profile As Lead Machine',
            'tagline': 'Rise to the Top and Attract High-Quality Leads on Autopilot'
        },
        'professional_authority': {
            'name': 'Professional Authority',
            'bg_primary': (10, 25, 47),  # Navy
            'bg_secondary': (255, 215, 0),  # Gold
            'accent': (255, 215, 0),
            'text_primary': (255, 255, 255),
            'text_secondary': (255, 215, 0),
            'hook': 'Trusted by Fortune 500 Leaders',
            'tagline': 'Driving Innovation and Excellence in [Industry]'
        },
        'tech_innovator': {
            'name': 'Tech Innovator',
            'bg_primary': (45, 45, 45),  # Dark Gray
            'bg_secondary': (0, 255, 255),  # Cyan
            'accent': (0, 255, 255),
            'text_primary': (255, 255, 255),
            'text_secondary': (0, 255, 255),
            'hook': 'Building the Future with [Tech Stack]',
            'tagline': 'Transforming Complex Problems into Scalable Solutions'
        },
        'executive_premium': {
            'name': 'Executive Premium',
            'bg_primary': (0, 0, 0),  # Black
            'bg_secondary': (255, 255, 255),  # White
            'accent': (255, 215, 0),  # Gold
            'text_primary': (255, 255, 255),
            'text_secondary': (255, 215, 0),
            'hook': 'Driving [X]% Growth in [Industry]',
            'tagline': 'Strategic Leadership | Proven Results | Global Impact'
        },
        'creative_bold': {
            'name': 'Creative Bold',
            'bg_primary': (138, 43, 226),  # Purple
            'bg_secondary': (255, 140, 0),  # Orange
            'accent': (255, 255, 255),
            'text_primary': (255, 255, 255),
            'text_secondary': (255, 255, 255),
            'hook': 'Transforming Ideas into Impact',
            'tagline': 'Where Creativity Meets Strategy and Innovation'
        },
        'modern_gradient': {
            'name': 'Modern Gradient',
            'bg_primary': (30, 60, 114),  # Deep Blue
            'bg_secondary': (42, 82, 152),  # Medium Blue
            'accent': (0, 180, 216),  # Bright Cyan
            'text_primary': (255, 255, 255),
            'text_secondary': (0, 180, 216),
            'hook': 'Innovating at the Intersection of Tech & Business',
            'tagline': 'Delivering Results Through Data-Driven Solutions'
        },
        'success_green': {
            'name': 'Success Green',
            'bg_primary': (16, 124, 16),  # Forest Green
            'bg_secondary': (255, 255, 255),  # White
            'accent': (255, 215, 0),  # Gold
            'text_primary': (255, 255, 255),
            'text_secondary': (255, 215, 0),
            'hook': 'Proven Track Record of Success',
            'tagline': 'Scaling Businesses Through Strategic Technology Leadership'
        },
        'elegant_rose': {
            'name': 'Elegant Rose',
            'bg_primary': (255, 255, 255),  # White
            'bg_secondary': (220, 53, 69),  # Rose Red
            'accent': (220, 53, 69),
            'text_primary': (33, 37, 41),  # Dark Gray
            'text_secondary': (220, 53, 69),
            'hook': 'Elevating Brands Through Digital Excellence',
            'tagline': 'Award-Winning Designer | 500+ Projects Delivered'
        }
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

    def generate_linkedin_banner(self, name: str, tagline: str, portfolio_url: str, profile_photo_path: Optional[str] = None, output_path: str = "linkedin_banner.png") -> str:
        """
        Generates a custom LinkedIn Banner with QR Code and optional profile photo.
        """
        width, height = 1584, 396 # LinkedIn Banner Size
        img = Image.new('RGB', (width, height), color=self.COLORS['bg_navy'])
        draw = ImageDraw.Draw(img)
        
        # Fonts
        f_name = self._get_font(60, bold=True)
        f_tag = self._get_font(40)
        
        # Add profile photo if provided
        photo_size = 300
        if profile_photo_path and os.path.exists(profile_photo_path):
            try:
                profile_photo = Image.open(profile_photo_path)
                # Create circular mask
                mask = Image.new('L', (photo_size, photo_size), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse((0, 0, photo_size, photo_size), fill=255)
                
                # Resize and crop to square
                profile_photo = profile_photo.resize((photo_size, photo_size))
                
                # Apply circular mask
                output_photo = Image.new('RGBA', (photo_size, photo_size))
                output_photo.paste(profile_photo, (0, 0))
                output_photo.putalpha(mask)
                
                # Paste onto banner
                img.paste(output_photo, (900, 50), output_photo)
            except Exception as e:
                print(f"Error adding profile photo: {e}")
        
        # Text (adjusted position if photo is present)
        text_x = 50
        draw.text((text_x, 100), name, fill=self.COLORS['text_white'], font=f_name)
        draw.text((text_x, 180), tagline, fill=self.COLORS['text_cyan'], font=f_tag)
        
        # QR Code
        qr = qrcode.make(portfolio_url)
        qr = qr.resize((250, 250))
        img.paste(qr, (1250, 70))
        
        # CTA
        draw.text((1260, 330), "Scan for Portfolio", fill=self.COLORS['text_white'], font=self._get_font(20))
        
        img.save(output_path)
        return output_path

    def generate_banner_with_template(self, template_key: str, custom_hook: Optional[str] = None, 
                                      custom_tagline: Optional[str] = None, profile_photo_path: Optional[str] = None,
                                      portfolio_url: str = "https://linkedin.com", company_name: Optional[str] = None,
                                      output_path: str = "linkedin_banner_template.png") -> str:
        """
        Generates a LinkedIn banner using a predefined template with geometric patterns.
        
        Args:
            template_key: One of 'lead_generation', 'professional_authority', 'tech_innovator', 'executive_premium', 'creative_bold'
            custom_hook: Override the default hook text
            custom_tagline: Override the default tagline
            profile_photo_path: Path to profile photo (optional)
            portfolio_url: URL for QR code
            company_name: Company/brand name to display
            output_path: Output file path
        """
        if template_key not in self.BANNER_TEMPLATES:
            template_key = 'lead_generation'  # Default fallback
        
        template = self.BANNER_TEMPLATES[template_key]
        width, height = 1584, 396
        
        # Create base image with primary background
        img = Image.new('RGB', (width, height), color=template['bg_primary'])
        draw = ImageDraw.Draw(img)
        
        # Add geometric patterns based on template
        self._add_geometric_patterns(draw, template_key, width, height, template)
        
        # Add profile photo if provided
        photo_size = 280
        photo_x = 950
        if profile_photo_path and os.path.exists(profile_photo_path):
            try:
                profile_photo = Image.open(profile_photo_path)
                # Create circular mask
                mask = Image.new('L', (photo_size, photo_size), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse((0, 0, photo_size, photo_size), fill=255)
                
                # Resize to square
                profile_photo = profile_photo.resize((photo_size, photo_size))
                
                # Apply circular mask
                output_photo = Image.new('RGBA', (photo_size, photo_size))
                output_photo.paste(profile_photo, (0, 0))
                output_photo.putalpha(mask)
                
                # Paste onto banner
                img.paste(output_photo, (photo_x, 60), output_photo)
            except Exception as e:
                print(f"Error adding profile photo: {e}")
        
        # Text content
        hook_text = custom_hook if custom_hook else template['hook']
        tagline_text = custom_tagline if custom_tagline else template['tagline']
        
        # Fonts
        f_hook = self._get_font(48, bold=True)
        f_tagline = self._get_font(28)
        f_company = self._get_font(20)
        
        # Draw hook (main headline)
        text_x = 50
        text_y = 80
        
        # Wrap hook text if too long
        wrapped_hook = textwrap.wrap(hook_text, width=30)
        for line in wrapped_hook[:2]:  # Max 2 lines
            draw.text((text_x, text_y), line, fill=template['text_primary'], font=f_hook)
            text_y += 60
        
        # Draw tagline
        text_y += 20
        wrapped_tagline = textwrap.wrap(tagline_text, width=45)
        for line in wrapped_tagline[:2]:  # Max 2 lines
            draw.text((text_x, text_y), line, fill=template['text_secondary'], font=f_tagline)
            text_y += 35
        
        # Company name if provided
        if company_name:
            draw.text((text_x, height - 50), company_name, fill=template['accent'], font=f_company)
        
        # QR Code (smaller, positioned at bottom right)
        qr = qrcode.make(portfolio_url)
        qr = qr.resize((180, 180))
        img.paste(qr, (width - 220, height - 200))
        
        # CTA text near QR
        draw.text((width - 210, height - 25), "Scan to Connect", fill=template['text_primary'], font=self._get_font(16))
        
        img.save(output_path)
        return output_path
    
    def _add_geometric_patterns(self, draw: ImageDraw.ImageDraw, template_key: str, 
                                width: int, height: int, template: dict):
        """
        Adds sophisticated geometric patterns specific to each template theme.
        Enhanced for professional appeal and visual impact.
        """
        if template_key == 'lead_generation':
            # Enhanced Yellow/Black design with modern geometric elements
            
            # Large gradient-like circle on left (simulated with multiple circles)
            for i in range(5):
                alpha = 255 - (i * 40)
                radius = 200 - (i * 20)
                draw.ellipse([250 - radius, 100 - radius, 250 + radius, 100 + radius], 
                           fill=template['bg_secondary'], outline=None)
            
            # Dot pattern grid (top right) - more refined
            dot_size = 5
            spacing = 18
            for i in range(10):
                for j in range(5):
                    x = 480 + i * spacing
                    y = 15 + j * spacing
                    draw.ellipse([x, y, x + dot_size, y + dot_size], fill=template['text_secondary'])
            
            # Modern accent circles with varying sizes
            draw.ellipse([650, 50, 720, 120], fill=template['accent'])
            draw.ellipse([680, 250, 730, 300], fill=(50, 50, 50))  # Dark gray
            draw.ellipse([width - 180, 260, width - 120, 320], fill=template['accent'])
            
            # Geometric shapes - rectangles with rotation effect
            draw.rectangle([440, 100, 560, 220], fill=template['accent'])
            draw.polygon([(width - 220, 15), (width - 120, 15), (width - 100, 95), (width - 240, 95)], 
                        fill=template['text_secondary'])
            
            # Chevron arrows on left (modern touch)
            for i in range(4):
                y_start = 50 + (i * 25)
                draw.line([(20, y_start), (35, y_start + 10)], fill=template['text_secondary'], width=3)
                draw.line([(35, y_start + 10), (20, y_start + 20)], fill=template['text_secondary'], width=3)
            
        elif template_key == 'professional_authority':
            # Sophisticated Navy/Gold design with elegant patterns
            
            # Diagonal gold accent lines (refined)
            for i in range(6):
                y_start = i * 80
                draw.line([(0, y_start), (250, y_start + 150)], fill=template['accent'], width=3)
            
            # Gold corner triangle (larger, more prominent)
            draw.polygon([(width - 400, 0), (width, 0), (width, 250)], fill=template['accent'])
            
            # Elegant circles on the gold triangle
            draw.ellipse([width - 200, 50, width - 150, 100], fill=template['bg_primary'])
            draw.ellipse([width - 150, 120, width - 100, 170], fill=template['bg_primary'])
            
            # Horizontal accent lines (bottom)
            draw.line([(0, height - 5), (width, height - 5)], fill=template['accent'], width=5)
            
            # Subtle grid pattern in background
            for i in range(0, width, 150):
                draw.line([(i, 0), (i, height)], fill=(20, 40, 70), width=1)
            
        elif template_key == 'tech_innovator':
            # Modern tech circuit board design with enhanced patterns
            
            # Circuit board grid (more refined)
            grid_color = (0, 200, 200)  # Brighter cyan
            for i in range(0, width, 120):
                draw.line([(i, 0), (i, height)], fill=grid_color, width=1)
            for i in range(0, height, 120):
                draw.line([(0, i), (width, i)], fill=grid_color, width=1)
            
            # Connection nodes with glow effect
            node_positions = [
                (150, 120), (400, 80), (650, 150), (900, 100), (1150, 130),
                (200, 280), (500, 250), (800, 290), (1100, 260)
            ]
            
            for x, y in node_positions:
                # Glow effect (multiple circles)
                for r in range(15, 5, -3):
                    alpha_color = (0, 255 - (r * 10), 255 - (r * 10))
                    draw.ellipse([x-r, y-r, x+r, y+r], fill=alpha_color)
                # Center node
                draw.ellipse([x-4, y-4, x+4, y+4], fill=(255, 255, 255))
            
            # Connection lines between nodes
            connections = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (2, 6), (3, 7), (4, 8)]
            for start_idx, end_idx in connections:
                x1, y1 = node_positions[start_idx]
                x2, y2 = node_positions[end_idx]
                draw.line([(x1, y1), (x2, y2)], fill=template['accent'], width=2)
            
            # Tech hexagons
            for i in range(3):
                x_hex = width - 300 + (i * 80)
                y_hex = 200
                hex_points = [
                    (x_hex, y_hex - 20), (x_hex + 15, y_hex - 10),
                    (x_hex + 15, y_hex + 10), (x_hex, y_hex + 20),
                    (x_hex - 15, y_hex + 10), (x_hex - 15, y_hex - 10)
                ]
                draw.polygon(hex_points, outline=template['accent'], width=2)
            
        elif template_key == 'executive_premium':
            # Ultra-premium minimalist design with gold accents
            
            # Top horizontal gold bar
            draw.rectangle([0, 0, width, 8], fill=template['accent'])
            
            # Elegant horizontal accent lines (left side)
            line_positions = [60, 120, 180]
            for y in line_positions:
                draw.line([(40, y), (450, y)], fill=template['accent'], width=4)
            
            # Bottom horizontal gold bar
            draw.rectangle([0, height - 8, width, height], fill=template['accent'])
            
            # Vertical accent line (right side)
            draw.line([(width - 280, 40), (width - 280, height - 40)], fill=template['accent'], width=3)
            
            # Minimalist geometric shapes
            draw.rectangle([width - 250, 150, width - 200, 200], outline=template['accent'], width=3)
            draw.ellipse([width - 180, 150, width - 130, 200], outline=template['accent'], width=3)
            
            # Subtle corner accents
            draw.polygon([(0, 0), (80, 0), (0, 80)], fill=(40, 40, 40))
            draw.polygon([(width, height), (width - 80, height), (width, height - 80)], fill=(40, 40, 40))
            
        elif template_key == 'creative_bold':
            # Vibrant creative design with gradient-like effects
            
            # Large overlapping circles with gradient simulation
            # Purple circles
            for i in range(4):
                radius = 120 - (i * 15)
                color_val = 226 - (i * 30)
                draw.ellipse([80 - radius, 150 - radius, 80 + radius, 150 + radius], 
                           fill=(138, 43, color_val))
            
            # Orange circles
            for i in range(4):
                radius = 110 - (i * 15)
                color_val = 140 - (i * 20)
                draw.ellipse([220 - radius, 200 - radius, 220 + radius, 200 + radius], 
                           fill=(255, color_val, 0))
            
            # Abstract flowing shapes
            draw.polygon([
                (width - 350, 0), (width - 250, 80), (width - 200, 150),
                (width - 280, 200), (width - 400, 120)
            ], fill=template['accent'])
            
            # Curved lines (simulated with multiple short lines)
            for i in range(20):
                x1 = 400 + (i * 30)
                y1 = 100 + (i * 5)
                x2 = x1 + 25
                y2 = y1 + 8
                draw.line([(x1, y1), (x2, y2)], fill=template['accent'], width=3)
            
            # Decorative dots
            dot_positions = [(500, 80), (550, 120), (600, 90), (650, 140), (700, 100)]
            for x, y in dot_positions:
                draw.ellipse([x-8, y-8, x+8, y+8], fill=template['accent'])
            
            # Wave pattern at bottom
            for i in range(0, width, 40):
                draw.arc([i - 20, height - 60, i + 20, height - 20], 0, 180, fill=template['bg_primary'], width=3)
        
        elif template_key == 'modern_gradient':
            # Modern gradient-inspired design with flowing shapes
            
            # Gradient simulation with horizontal bands
            band_height = height // 5
            for i in range(5):
                y_start = i * band_height
                # Gradually lighten the blue
                color_r = 30 + (i * 3)
                color_g = 60 + (i * 5)
                color_b = 114 + (i * 8)
                draw.rectangle([0, y_start, width, y_start + band_height], 
                             fill=(color_r, color_g, color_b))
            
            # Flowing wave shapes
            for i in range(3):
                y_wave = 80 + (i * 100)
                for x in range(0, width, 60):
                    draw.arc([x - 30, y_wave - 20, x + 30, y_wave + 20], 
                           0, 180, fill=template['accent'], width=3)
            
            # Modern geometric circles
            circle_positions = [(width - 200, 100), (width - 120, 200), (width - 250, 280)]
            for x, y in circle_positions:
                draw.ellipse([x-40, y-40, x+40, y+40], outline=template['accent'], width=3)
            
            # Diagonal accent lines
            for i in range(5):
                x_start = i * 150
                draw.line([(x_start, 0), (x_start + 100, height)], 
                        fill=(0, 180, 216, 50), width=2)
        
        elif template_key == 'success_green':
            # Success-themed design with achievement elements
            
            # Trophy/achievement icons (simplified geometric shapes)
            # Star shapes (simplified as polygons)
            star_positions = [(100, 100), (200, 280), (width - 150, 150)]
            for cx, cy in star_positions:
                # 5-pointed star approximation
                points = []
                for i in range(10):
                    angle = (i * 36) * 3.14159 / 180
                    radius = 25 if i % 2 == 0 else 12
                    x = cx + radius * (0.5 if i % 2 == 0 else 0.3)
                    y = cy + radius * (0.5 if i % 2 == 0 else 0.3)
                    points.append((x, y))
                draw.polygon(points, fill=template['accent'])
            
            # Growth arrow
            arrow_points = [
                (width - 300, height - 100), (width - 250, height - 150),
                (width - 200, height - 120), (width - 150, height - 180),
                (width - 100, height - 140)
            ]
            for i in range(len(arrow_points) - 1):
                draw.line([arrow_points[i], arrow_points[i+1]], 
                        fill=template['accent'], width=5)
            
            # Success checkmarks
            check_positions = [(400, 80), (550, 200), (700, 120)]
            for cx, cy in check_positions:
                draw.line([(cx, cy), (cx + 15, cy + 20)], fill=template['bg_secondary'], width=4)
                draw.line([(cx + 15, cy + 20), (cx + 35, cy - 10)], fill=template['bg_secondary'], width=4)
            
            # Horizontal accent bars
            draw.rectangle([0, height - 10, width, height], fill=template['accent'])
        
        elif template_key == 'elegant_rose':
            # Elegant design with rose/red accents
            
            # Flowing rose-colored ribbons
            for i in range(3):
                y_ribbon = 100 + (i * 100)
                ribbon_points = [
                    (width - 400, y_ribbon), (width - 300, y_ribbon - 30),
                    (width - 200, y_ribbon + 20), (width - 100, y_ribbon - 10),
                    (width, y_ribbon + 15)
                ]
                for j in range(len(ribbon_points) - 1):
                    draw.line([ribbon_points[j], ribbon_points[j+1]], 
                            fill=template['accent'], width=4)
            
            # Elegant circles with rose accent
            circle_positions = [(150, 120), (280, 250), (420, 180)]
            for x, y in circle_positions:
                # Outer circle
                draw.ellipse([x-35, y-35, x+35, y+35], outline=template['accent'], width=3)
                # Inner filled circle
                draw.ellipse([x-15, y-15, x+15, y+15], fill=template['accent'])
            
            # Decorative corner elements
            # Top left corner
            draw.line([(0, 50), (100, 50)], fill=template['accent'], width=3)
            draw.line([(50, 0), (50, 100)], fill=template['accent'], width=3)
            
            # Bottom right corner
            draw.line([(width - 100, height - 50), (width, height - 50)], fill=template['accent'], width=3)
            draw.line([(width - 50, height - 100), (width - 50, height)], fill=template['accent'], width=3)
            
            # Elegant dots pattern
            for i in range(8):
                for j in range(3):
                    x = 500 + (i * 25)
                    y = 50 + (j * 25)
                    draw.ellipse([x-3, y-3, x+3, y+3], fill=template['text_secondary'])

