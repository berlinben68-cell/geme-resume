
def get_all_templates():
    """
    Returns a list of 50+ curated resume design templates.
    Each template has a name, category, and config (color, font, layout).
    """
    
    # Base Palettes
    colors = {
        "Tech Blue": "#2E74B5",
        "Deep Navy": "#000080",
        "Spotify Green": "#1DB954",
        "Forest Green": "#228B22",
        "Netflix Red": "#E50914",
        "Crimson": "#DC143C",
        "Amazon Orange": "#FF9900",
        "Burnt Sienna": "#E97451",
        "Google Blue": "#4285F4",
        "Sky Blue": "#87CEEB",
        "Cyber Punk": "#FA582D",
        "Purple Haze": "#800080",
        "Royal Violet": "#8A2BE2",
        "Uber Black": "#000000",
        "Charcoal": "#36454F",
        "Slate Grey": "#708090",
        "Teal": "#008080",
        "Turquoise": "#40E0D0",
        "Gold Standard": "#DAA520",
        "Coral": "#FF7F50",
        "Magenta": "#FF00FF",
        "Lime": "#32CD32",
        "Indigo": "#4B0082",
        "Brown": "#A52A2A",
        "Pink": "#FFC0CB"
    }

    fonts = ["Arial", "Calibri", "Roboto", "Open Sans", "Lato", "Montserrat", "Times New Roman"]
    layouts = ["Classic (Single Column)", "Modern (Left Column)"]

    templates = []
    
    # 1. Generate Curated Combinations
    
    # Professional / Corporate (Serif + Classic + Dark Colors)
    corp_colors = ["Deep Navy", "Charcoal", "Uber Black", "Slate Grey", "Tech Blue"]
    for i, color_name in enumerate(corp_colors):
        templates.append({
            "name": f"Executive {color_name.split()[0]}",
            "category": "Professional",
            "config": {"color": colors[color_name], "font": "Times New Roman", "layout": "Classic (Single Column)"}
        })
        templates.append({
            "name": f"Modern Corp {color_name.split()[0]}",
            "category": "Professional",
            "config": {"color": colors[color_name], "font": "Arial", "layout": "Modern (Left Column)"}
        })

    # Tech / Startup (Sans-Serif + Modern + Vibrant Colors)
    tech_colors = ["Spotify Green", "Google Blue", "Amazon Orange", "Cyber Punk", "Teal", "Turquoise"]
    for i, color_name in enumerate(tech_colors):
        templates.append({
            "name": f"Startup {color_name.split()[0]}",
            "category": "Tech",
            "config": {"color": colors[color_name], "font": "Roboto", "layout": "Modern (Left Column)"}
        })
        templates.append({
            "name": f"Minimalist {color_name.split()[0]}",
            "category": "Tech",
            "config": {"color": colors[color_name], "font": "Open Sans", "layout": "Classic (Single Column)"}
        })

    # Creative / Design (Unique Fonts + Bold Colors)
    creative_colors = ["Netflix Red", "Purple Haze", "Gold Standard", "Coral", "Magenta", "Lime", "Indigo"]
    for i, color_name in enumerate(creative_colors):
        templates.append({
            "name": f"Creative {color_name.split()[0]}",
            "category": "Creative",
            "config": {"color": colors[color_name], "font": "Montserrat", "layout": "Modern (Left Column)"}
        })
        templates.append({
            "name": f"Bold {color_name.split()[0]}",
            "category": "Creative",
            "config": {"color": colors[color_name], "font": "Lato", "layout": "Classic (Single Column)"}
        })

    # Academic / Simple (Calibri + Neutral)
    academic_colors = ["Deep Navy", "Brown", "Forest Green", "Slate Grey"]
    for i, color_name in enumerate(academic_colors):
        templates.append({
            "name": f"Academic {color_name.split()[0]}",
            "category": "Academic",
            "config": {"color": colors[color_name], "font": "Calibri", "layout": "Classic (Single Column)"}
        })

    # Ensure we have at least 50
    # We have: 
    # Corp: 5 * 2 = 10
    # Tech: 6 * 2 = 12
    # Creative: 7 * 2 = 14
    # Academic: 4 * 1 = 4
    # Total so far: 40. Need 10 more.

    # 2. Mix and Match for Variety
    extras = [
        ("Obsidian", "Uber Black", "Montserrat", "Modern (Left Column)"),
        ("Glacier", "Sky Blue", "Open Sans", "Modern (Left Column)"),
        ("Crimson Tide", "Crimson", "Lato", "Classic (Single Column)"),
        ("Royal", "Royal Violet", "Times New Roman", "Classic (Single Column)"),
        ("Mint", "Spotify Green", "Calibri", "Modern (Left Column)"),
        ("Sunset", "Burnt Sienna", "Roboto", "Modern (Left Column)"),
        ("Steel", "Slate Grey", "Arial", "Classic (Single Column)"),
        ("Ocean", "Teal", "Montserrat", "Modern (Left Column)"),
        ("Berry", "Purple Haze", "Lato", "Classic (Single Column)"),
        ("Matrix", "Lime", "Roboto", "Modern (Left Column)"),
        ("Fire", "Cyber Punk", "Open Sans", "Classic (Single Column)"),
        ("Earth", "Brown", "Calibri", "Modern (Left Column)")
    ]

    for name, c_name, font, layout in extras:
        templates.append({
            "name": name,
            "category": "Curated",
            "config": {"color": colors.get(c_name, "#000000"), "font": font, "layout": layout}
        })

    return templates
