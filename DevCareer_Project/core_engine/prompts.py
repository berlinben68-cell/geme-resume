
# prompts.py

def get_resume_prompt(market="India", resume_text=""):
    """
    Returns the system prompt for rewriting a resume based on the target market.
    """
    base_prompt = f"""
    You are an expert Technical Recruiter and CTO. 
    Rewrite the following resume content to be highly effective for the {market} market.
    
    Original Resume Content:
    {resume_text}
    """
    
    if market == "India":
        specifics = """
        Focus on:
        - "Scale": Mention user base sizes, transaction volumes, etc.
        - "Microservices": Highlight distributed systems, Docker, Kubernetes.
        - "Naukri Keywords": Use high-volume search terms like Java, Spring Boot, React, AWS, System Design.
        - Tone: Professional, technical, and achievement-oriented.
        """
    elif market == "UAE":
        specifics = """
        Focus on:
        - "ROI": Highlight business impact, cost savings, and revenue generation.
        - "Visa Status": Implicitly suggest stability and readiness.
        - "English Proficiency": Ensure flawless, professional English.
        - Tone: Executive, polished, and business-centric.
        """
    else:
        specifics = "Focus on clarity, impact, and technical accuracy."

    return base_prompt + specifics

def get_github_architect_prompt(project_description, tech_stack=""):
    """
    Returns the prompt to generate a GitHub project structure.
    """
    return f"""
    Act as a Staff Software Engineer at a FAANG company.
    Create a 'Public Portfolio Showcase' for a project called: "Project_Name" based on this description: "{project_description}".
    Tech Stack context: {tech_stack}
    
    Since the original code is under NDA, we are creating a "Proof of Architecture" repo.
    
    OUTPUT FORMAT:
    Return strictly 3 sections separated by "### SECTION BREAK ###".
    
    SECTION 1: PROFESSIONAL README.md
    - Badges (Build passing, License, etc).
    - High-level problem statement.
    - 'How we scaled this' section (Metrics: TPS, Latency).
    - Setup instructions (Docker compose up).
    
    SECTION 2: MERMAID.JS DIAGRAM
    - A complex sequence diagram or system architecture showing Microservices/Load Balancers/DBs.
    - Wrap it in a mermaid code block.
    
    SECTION 3: FOLDER STRUCTURE
    - Generate a clean ASCII tree structure (using │, ├──, └── characters).
    - Do NOT use markdown code blocks (```).
    - Output ONLY the tree structure.
    - Example:
    project_root/
    ├── src/
    │   ├── main.py
    │   └── utils.py
    ├── tests/
    └── README.md
    """

def get_linkedin_optimizer_prompt(resume_text, target_role="Software Engineer", tech_stack=""):
    """
    Returns the prompt to generate a High-Ticket LinkedIn Optimization Kit.
    """
    return f"""
    You are a High-Ticket Career Strategist and LinkedIn Algorithm Expert.
    Your goal is to create a "LinkedIn Optimization Kit" that turns the candidate's profile into a Recruiter SEO Magnet.
    
    Candidate Context:
    - Target Role: {target_role}
    - Tech Stack Focus: {tech_stack}
    - Resume Content:
    {resume_text}
    
    You must generate a structured guide following these EXACT 5 steps:

    ### 1. The "Click-Bait" Headline (SEO)
    Most devs write "Software Engineer at X". This is useless.
    Craft a 220-character hook using the format: **Role | Tech Stack | Achievement/Authority**.
    - It must rank for keywords (e.g., "Java Developer Dubai", "SDE-2 React").
    - Example: "Senior Backend Engineer | Java, Spring Boot, AWS | Architected High-Scale Payments Systems (10k+ TPS) | Golden Visa Holder"
    
    ### 2. The "Story-Based" About Section
    Write a 3-paragraph bio (First Person).
    - **The Hook**: First 3 lines must grab attention (visible before "See more").
    - **The Stack**: A clear, punchy list of tools (Languages, Frameworks, Cloud).
    - **The Call to Action**: "Open to Senior Roles in [Target Market]. Contact: [Email]"
    - Tone: Professional but confident. Highlight experience in Microservices/Scale.
    
    ### 3. "Skill-Staking" (Algorithm Hacking)
    Identify the **Top 10 High-Value Skills** for the {target_role} role.
    - These must be specific (e.g., "Kubernetes" instead of "Cloud Computing", "React.js" instead of "Web Dev").
    - Instruct the user to pin these to their profile.
    
    ### 4. The "Featured Section" Strategy (Visual Proof)
    Provide a strategy for what to pin.
    - Pin 1: The Resume PDF.
    - Pin 2: A GitHub Repository (mention a specific project from their resume if possible).
    - Pin 3: A "System Architecture Diagram" (Visual eye-candy).
    
    ### 5. URL & Settings Cleanup (Hygiene)
    - **Vanity URL**: Suggest a clean URL format (e.g., linkedin.com/in/name-role-stack).
    - **"Open to Work"**: Instructions on enabling the "Green Banner" for Recruiters ONLY.
    
    **OUTPUT FORMAT**:
    Return the response as a clean Markdown document titled "**[Candidate Name] LinkedIn Optimization Kit**".
    Use clear headings and "Copy-Paste" blocks for the Headline and About section.
    """

def get_ats_score_prompt(resume_text, jd_text, market):
    """
    Returns the prompt to calculate ATS score.
    """
    return f"""
    You are an ATS (Applicant Tracking System) Expert and Technical Recruiter for the {market} market.
    Evaluate the following Resume against the Job Description.

    Resume Content:
    {resume_text}

    Job Description:
    {jd_text}

    Output MUST be in the following format:
    **ATS Score:** [Score]/100
    
    **Match Analysis:**
    - ✅ **Matching Keywords:** [List of matched skills/keywords]
    - ❌ **Missing Keywords:** [List of important keywords missing from resume]
    
    **Market Fit ({market}):**
    - [Specific advice for {market} market, e.g., for India focus on scale/tools, for UAE focus on ROI/English]
    
    **Improvement Plan:**
    - [3 bullet points on how to increase the score]
    """

def get_visual_content_prompt(resume_text, target_role):
    """
    Returns the prompt to extract structured data for visual assets.
    """
    return f"""
    You are a Creative Director for a Tech Personal Branding Agency.
    Extract specific data points from the following resume to generate visual assets for a LinkedIn "Featured" section.
    
    Target Role: {target_role}
    Resume Content:
    {resume_text}
    
    Identify the SINGLE most impressive project or achievement and extract the following:
    
    1. **Project Title**: A punchy, 5-7 word title (e.g., "Scaling Payment Gateway to 10k TPS").
    2. **Problem**: The technical challenge faced (max 10 words).
    3. **Solution**: The architecture/tech used to solve it (max 10 words).
    4. **Key Results**: 3 short, metric-driven bullet points (e.g., "Reduced latency by 40%").
    5. **Top 5 Tech Skills**: The most relevant skills for this project (comma separated).
    
    OUTPUT FORMAT (Strict JSON-like structure, no markdown code blocks):
    Title: [Title]
    Problem: [Problem]
    Solution: [Solution]
    Results: [Result 1] | [Result 2] | [Result 3]
    Skills: [Skill 1], [Skill 2], [Skill 3], [Skill 4], [Skill 5]
    """

def get_keyword_injection_prompt(target_role, target_keywords):
    """
    Returns the prompt for generating high-density keyword projects.
    """
    return f"""
    Act as a LinkedIn SEO Specialist.
    Target Role: {target_role}
    Target Keywords: {target_keywords}

    Task: Write 3 'Project' entries for the LinkedIn Projects section.
    Constraint: The text must be natural but heavily loaded with the target keywords.
    
    Format:
    1. Project Title: (e.g., "High-Scale Payment Gateway Migration")
    2. Description: (A 50-word description using the keywords naturally).
    3. Skills to Tag: (List of 5 skills).
    
    Output each project clearly separated.
    """

def get_recruiter_simulator_prompt(target_role):
    return f"""
    Act as a Senior Tech Recruiter at Google. 
    Look at this LinkedIn profile screenshot. You have 6 seconds to decide if you want to interview this person for a {target_role} position.
    
    Provide a "Recruiter Eye-Tracking Report":
    1. **Heatmap Analysis**: Where do your eyes go first? (e.g., "Distracted by the busy banner", "Focused on the headline").
    2. **Red Flags**: What makes you click away? (e.g., "Generic headline", "No featured section").
    3. **Trust Score**: Rate from 0-10 based on professional appearance and consistency.
    4. **Fixes**: 3 specific, actionable changes to improve conversion.
    """

def get_recommendation_prompt(role, key_achievement):
    return f"""
    Write 3 distinct LinkedIn Recommendations for a {role} who achieved: {key_achievement}.
    
    1. **FROM MANAGER**: Focus on reliability, ROI, and business impact.
    2. **FROM PEER**: Focus on coding speed, teamwork, and problem-solving.
    3. **FROM JUNIOR**: Focus on mentorship, code reviews, and guidance.
    
    Constraint: Keep them under 100 words each. Professional but warm tone.
    """

def get_content_calendar_prompt(project_name, tech_stack):
    return f"""
    Create 3 LinkedIn Text Posts (Short, punchy) for a developer to show off this project: {project_name} built with {tech_stack}.
    
    **Post 1: The Problem & Solution (Technical Case Study)**
    - Hook: The technical nightmare faced.
    - Body: How {tech_stack} solved it.
    - Ending: Question to engage others.

    **Post 2: Opinionated Tech Stack Choice**
    - Why I chose X over Y (e.g., Redis over Memcached).
    - Controversial but backed by logic.

    **Post 3: The 'Lesson Learned' (Debugging Story)**
    - A specific bug or failure and what it taught me.
    - Vulnerability = Trust.
    
    Include 3-5 relevant hashtags for the Dubai/India tech scene.
    """

def get_competitor_gap_prompt(my_resume, competitor_text, target_role):
    return f"""
    Act as a Data Scientist. Perform a "Competitor Gap Analysis" between My Profile and a Gold Standard Competitor.
    
    Target Role: {target_role}
    
    **My Profile:**
    {my_resume}
    
    **Competitor / Gold Standard Profile:**
    {competitor_text}
    
    **Analysis Output:**
    1. **Keyword Gap**: Which high-value keywords does the competitor use that I am missing? (List top 5).
    2. **Metric Gap**: How do they quantify success vs how I do? (e.g., "They use TPS/Latency, you use generic terms").
    3. **Structure Gap**: What sections or visual elements do they have that I lack?
    4. **Action Plan**: 3 steps to close the gap and beat them.
    """

def get_role_and_stack_extraction_prompt(resume_text):
    """
    Returns the prompt to extract the most likely Target Role and Tech Stack from a resume.
    """
    return f"""
    Analyze the following resume and identify the candidate's most likely **Target Job Role**, **Core Tech Stack**, and **LinkedIn Profile URL**.
    
    Resume Content:
    {resume_text}
    
    Output strictly in JSON format:
    {{
        "role": "Suggested Job Title (e.g. Senior Java Developer)",
        "stack": "Top 5-7 Tech Skills (comma separated)",
        "linkedin_url": "Extract LinkedIn URL if present (e.g. linkedin.com/in/...), else empty string",
        "location": "City, Country (e.g. Dubai, UAE or Bangalore, India)",
        "industry": "Most likely industry (e.g. Technology, Finance, Consulting, Healthcare, Retail)"
    }}
    """
    
def get_naukri_optimizer_prompt(resume_text, target_role):
    """
    Returns the prompt to generate a Naukri.com Optimization Kit.
    """
    return f"""
    You are a Top-Rated Recruiter on Naukri.com (India's #1 Job Portal).
    Your goal is to optimize a candidate's profile to rank #1 in recruiter searches for the role: {target_role}.
    
    Resume Content:
    {resume_text}
    
    Naukri Algorithm Constraints:
    1. **Resume Headline**: This is the MOST critical field. Max 250 characters. Must be keyword-stuffed but readable.
    2. **Key Skills**: The search engine prioritizes these. Need the top 15-20 hard skills.
    3. **Profile Summary**: Needs to be a "30-second elevator pitch" focusing on years of experience, key tech stack, and scale.
    
    OUTPUT FORMAT (Strict Markdown):
    
    ### 1. 🏆 High-Ranking Resume Headline (Max 250 chars)
    [Generate 2 options: 
    Option A: Keyword Heavy
    Option B: Achievement Heavy]
    
    ### 2. 🔑 Key Skills (Comma Separated)
    [List top 20 skills relevant to {target_role} found in or inferred from the resume. Prioritize specific tools like 'Spring Boot' over generic 'Java'.]
    
    ### 3. 📝 Profile Summary (Naukri Optimized)
    [A professional summary in 3rd person. Start with "Senior {target_role} with X years of experience...". Highlight domain expertise and key achievements.]
    
    ### 4. 💼 Project Description Enhancer
    [Choose one project from the resume and rewrite its description to be "Naukri-friendly" - i.e., using action verbs and metrics.]
    """

def get_ats_simulation_prompt(resume_text):
    """
    Returns the prompt to simulate ATS data extraction.
    """
    return f"""
    Act as a legacy Application Tracking System (ATS). 
    Attempt to parse the following resume text into structured data.
    
    Resume Text:
    {resume_text}
    
    If fields are missing or unclear, mark them as "NOT FOUND".
    
    OUTPUT STRICT JSON:
    {{
        "candidate_name": "Name found",
        "email": "Email found",
        "phone": "Phone found",
        "skills": ["Skill 1", "Skill 2"],
        "education": ["Degree 1", "Degree 2"],
        "experience": [
            {{"role": "Role 1", "company": "Company 1", "duration": "Dates"}},
            {{"role": "Role 2", "company": "Company 2", "duration": "Dates"}}
        ]
    }}
    """


def get_formatting_audit_prompt(resume_text):
    """
    Returns the prompt to audit resume formatting and content structure.
    """
    return f"""
    Act as a Resume Formatting Expert. Analyze the extracted text from a resume to identify potential ATS readability issues.
    
    Extracted Text:
    {resume_text}
    
    Check for:
    1. **Garbled Text**: Are there weird characters or broken words? (Indicates bad font/encoding).
    2. **Section Headers**: Are standard headers (Experience, Education) clearly identifiable?
    3. **Contact Info**: Is it easily found at the top?
    
    OUTPUT STRICT MARKDOWN:
    
    ### 📊 Formatting Health Check
    **Readability Score**: [0-100]/100
    
    **✅ Passed Checks**:
    - [List good things]
    
    **⚠️ Potential Issues (Red Flags)**:
    - [List specific issues found in the text structure]
    
    **💡 Fix Recommendations**:
    - [Actionable advice]
    """

def get_resume_parsing_prompt(resume_text):
    """
    Returns the prompt to extract structured data for the Resume Builder.
    """
    return f"""
    Act as an Elite Executive Resume Writer and Data Extraction Specialist.
    Your task is to transform the provided resume text (from PDF/DOCX/LinkedIn) into a perfectly structured, Board-Ready JSON format.
    
    Resume Text:
    {resume_text}
    
    OBJECTIVES:
    1. **Extraction**: Capture all key details accurately.
    2. **Professional Polish**: 
       - Fix all capitalization errors (e.g., convert "python" to "Python", "aws" to "AWS").
       - Ensure the "Summary" is written in a professional, third-person executive voice.
       - Standardize date formats (e.g., "Jan 2023" or "2023").
    3. **Structure**: Output strict JSON.

    OUTPUT STRICT JSON (No markdown code blocks, just the raw JSON):
    {{
        "contact": {{
            "name": "Full Name (Title Case)",
            "email": "Email",
            "phone": "Phone",
            "location": "City, Country",
            "linkedin": "LinkedIn URL",
            "portfolio": "Portfolio URL"
        }},
        "summary": "Professional Summary (Polished & Impactful)",
        "experience": [
            {{
                "title": "Job Title (Standardized)",
                "company": "Company Name",
                "dates": "Start - End Date",
                "location": "Location",
                "description": "<ul><li>Action-oriented bullet point 1.</li><li>Achievement-focused bullet point 2.</li></ul>" 
            }}
        ],
        "projects": [
            {{
                "title": "Project Name",
                "tech_stack": "Tech Stack (Comma separated, Capitalized)",
                "description": "<ul><li>Project detail 1.</li><li>Project detail 2.</li></ul>"
            }}
        ],
        "education": [
            {{
                "school": "University Name",
                "degree": "Degree Name",
                "dates": "Graduation Year"
            }}
        ],
        "skills": "Skill 1, Skill 2, Skill 3 (Comma separated, Capitalized)",
        "certifications": "Cert 1\\nCert 2 (Newline separated)",
        "languages": "Lang 1, Lang 2 (Comma separated)"
    }}
    
    Rules:
    1. If a field is missing, use an empty string "" or empty list [].
    2. For 'description' fields, YOU MUST format bullet points as HTML <ul><li>...</li></ul>. Do not use plain text paragraphs.
    3. Ensure valid JSON.
    """

def get_cover_letter_prompt(resume_text, job_description, tone="Professional"):
    """
    Returns the prompt to generate a tailored cover letter.
    """
    return f"""
    Act as a Professional Career Coach and Resume Writer.
    Write a compelling Cover Letter for a candidate applying to a specific job.
    
    Tone: {tone}
    
    Resume Content:
    {resume_text}
    
    Job Description:
    {job_description}
    
    Instructions:
    1. **Header**: Include placeholders for [Date], [Hiring Manager Name], and [Company Address].
    2. **Opening**: Hook the reader immediately by mentioning the specific role and why the candidate is a perfect fit.
    3. **Body Paragraphs**: 
       - Connect specific achievements from the resume to the requirements in the Job Description.
       - Use the STAR method (Situation, Task, Action, Result) briefly where appropriate.
       - Show enthusiasm for the company (infer from JD).
    4. **Closing**: Strong call to action (requesting an interview).
    5. **Sign-off**: Professional sign-off.
    
    Output Format:
    Return ONLY the body of the cover letter (including header/footer). Do not include any conversational filler.
    """

def get_linkedin_profile_kit_prompt(role, region, resume_text):
    """
    Returns the prompt to generate a JSON-based LinkedIn Profile Kit.
    """
    return f"""
    You are a LinkedIn Personal Branding Expert and Technical Recruiter specialized in Software Engineering. 
    Your goal is to rewrite a profile to rank high in search results (SEO) and convert profile views into recruiter DMs.

    INPUT DATA:
    Target Role: {role}
    Target Location: {region}
    Candidate Resume/Notes: "{resume_text}"

    INSTRUCTIONS:
    Analyze the Candidate Resume data provided above. Do NOT invent facts. If specific metrics are missing, use placeholders like [Insert Metric].

    GENERATE A PROFILE KIT (JSON Format):

    {{
      "headlines": [
        "Provide 3 distinct options:",
        "1. The Authority (Focus on seniority/leadership)",
        "2. The Specialist (Focus on specific stack/niche)",
        "3. The Results-Driven (Focus on the biggest achievement)"
      ],
      "about_section": {{
        "hook": "Draft a 2-sentence hook based on the candidate's most impressive achievement found in the resume.",
        "body": "Summarize their technical journey. Focus on problem-solving methodology. Use the 'STAR' method (Situation, Task, Action, Result).",
        "tech_stack_list": "A clean, bulleted list of their primary languages, frameworks, and tools.",
        "call_to_action": "A professional closing inviting recruiters in {region} to connect."
      }},
      "experience_optimization_tips": [
        "Analyze the resume and provide 3 specific bullet points that need rewriting to be more 'impact-driven'.",
        "Example format: 'Instead of [Original], say [Action Verb + Tech + Result + Metric]'"
      ],
      "skills_seo": [
        "List the top 15 hard skills strictly relevant to {role} and {region} market demands.",
        "Order them by search volume relevance."
      ],
      "featured_section_strategy": "Based on the resume, suggest exactly what to pin. (e.g., 'Pin the case study regarding the API migration')."
    }}
    """

def get_linkedin_seo_prompt(role, region, resume_text):
    """
    Returns the prompt to generate a JSON-based LinkedIn SEO Audit.
    """
    return f"""
    You are a Senior Technical Recruiter and LinkedIn Algorithm Specialist. You know exactly how the 'LinkedIn Recruiter' search engine works.
    Your goal is to optimize the candidate's profile to rank #1 for the target role in the target location.

    INPUT DATA:
    Target Role: {role}
    Target Location: {region}
    Candidate Resume: "{resume_text}"

    ### STEP 1: KEYWORD EXTRACTION & STRATEGY
    1. Analyze the "Target Role" and generate a list of the top 20 "High-Volume Search Keywords" recruiters use for this role in {region}.
    2. Compare these keywords against the candidate's resume. Identify missing keywords that the candidate likely possesses but forgot to list (Semantic Analysis).

    ### STEP 2: GENERATE OPTIMIZED PROFILE (JSON Format)

    {{
      "seo_audit": {{
        "missing_keywords": "List critical keywords missing from their current resume that MUST be added to rank.",
        "primary_keyword_cluster": "The top 3 terms that should be repeated (naturally) throughout the profile."
      }},

      "headline_optimization": {{
        "strategy": "Formula: [Target Role] | [Top 3 Hard Skills] | [Unique Value/Achievement]",
        "options": [
          "Option 1 (Safe/Corporate): Standard title + Core Tech",
          "Option 2 (Aggressive/Startup): Niche Tech + Metric-driven claim",
          "Option 3 (Keyword Heavy): Maximum keyword density for search visibility"
        ]
      }},

      "about_section_seo": "Write a bio that naturally weaves in the 'High-Volume Search Keywords' identified in Step 1. Do not stuff keywords; make it readable but algorithm-friendly. Bold the top skills.",

      "experience_rewrites": [
        {{
          "instruction": "Rewrite the most recent job description to include specific tech keywords.",
          "original_role": "[Extract from resume]",
          "optimized_bullet_points": [
            "Write 3 bullet points that combine Action Verbs + Hard Skill Keywords + Numerical Impact.",
            "Ensure the 'Primary Keyword Cluster' is present here."
          ]
        }}
      ],

      "skills_section_ordering": {{
        "top_3_pinned": "Which 3 skills should be pinned to the top? (These weigh heaviest in the algorithm).",
        "industry_knowledge": "List 10 auxiliary skills (e.g., Agile, System Design).",
        "tools_technologies": "List 20 specific tools (e.g., Docker, Kubernetes, Jenkins) to ensure they hit specific search filters."
      }},

      "hidden_ranking_factors": [
        "Provide 3 actionable tips for this specific candidate to boost ranking (e.g., 'Get an endorsement for [Skill X]', 'Change URL to...', 'Follow [Company Y]')."
      ]
    }}
    """

def get_linkedin_visual_prompt(role, industry_vibe, visual_input):
    """
    Returns the prompt to generate a JSON-based LinkedIn Visual Audit.
    """
    return f"""
    You are a LinkedIn Visual Branding Consultant and Image Psychologist. 
    Your goal is to audit the visual elements of a profile to ensure they build trust, authority, and approachability.

    INPUT DATA:
    Target Role: {role} (e.g. Senior Java Developer)
    Industry Vibe: {industry_vibe} (e.g. Corporate Banking vs. Modern Tech Startup)
    Visual Input: "{visual_input}" 
    (Note: If analyzing images, strictly evaluate what you see. If analyzing a text description, visualize it based on the text.)

    GENERATE A VISUAL AUDIT REPORT (JSON Format):

    {{
      "profile_photo_audit": {{
        "score": "1-10",
        "impression_analysis": "What does this face say? (e.g., 'Approachable but lacks authority', 'Too serious', 'Great energy').",
        "technical_check": {{
          "lighting": "Is the face evenly lit or shadowed?",
          "composition": "Is the face occupying 60% of the frame? (Crucial for mobile visibility)",
          "background": "Is it distracting? Suggest a solid color or blurred office background if needed."
        }},
        "improvement_tip": "One specific change to increase click-through rate (e.g., 'Crop tighter around the shoulders', 'Smile with teeth to increase likability')."
      }},

      "banner_image_audit": {{
        "score": "1-10",
        "relevance_check": "Does the banner scream '{{role}}' immediately? (e.g., Code snippets for Devs, Skyline for Sales).",
        "text_readability": "If there is text, is it blocked by the Profile Photo circle on mobile? (The 'Safe Zone' check).",
        "branding_consistency": "Do the colors match the industry vibe?",
        "suggestion": "Provide a concrete idea for a better banner. (e.g., 'Use a dark mode IDE screenshot with the text: Building Scalable Systems in Dubai')."
      }},

      "psychological_consistency": "Does the Photo (Personality) match the Banner (Context)? Do they look like they belong to the same brand?"
    }}
    """

def get_linkedin_master_prompt(role, region, industry, resume_text, visual_context, linkedin_url):
    """
    Returns the prompt to generate a JSON-based Master LinkedIn Optimization Kit.
    """
    
    # 1. Define Market Nuances
    if "UAE" in region.upper() or "DUBAI" in region.upper():
        market_instruction = """
        **MARKET: UAE (Dubai/Abu Dhabi/GCC)**
        - **Culture:** Hierarchical, formal, and prestige-driven.
        - **Key Values:** Loyalty, International Experience, Stability.
        - **Formatting:** Clean, professional, minimal formatting.
        - **Tone:** "Executive Presence." Use British English spelling.
        - **Critical:** Mention visa status or "Available to join immediately" if implied.
        """
    else:  # India or Global
        market_instruction = """
        **MARKET: INDIA / GLOBAL**
        - **Culture:** Competitive, volume-driven, and skill-centric.
        - **Key Values:** Scalability, Hustle, Tech Stack depth, Educational pedigree.
        - **Tone:** Action-oriented. Use American or British English (consistent).
        - **Critical:** Highlight rank/percentiles (e.g., "Top 5% performer").
        """

    return f"""
    You are an elite LinkedIn Personal Branding Expert, Technical Recruiter, and SEO Algorithm Specialist. 
    Your goal is to generate a complete "Profile Optimization Kit" that helps the candidate rank #1 for their target role and converts views into recruiter messages.

    ### INPUT DATA
    - **Target Role:** {role}
    - **Target Location:** {region}
    - **Target Industry:** {industry}
    - **Visual Context:** "{visual_context}"
    - **LinkedIn URL:** "{linkedin_url}"
    - **Resume/Profile Content:**
    {resume_text}

    {market_instruction}

    ### SPECIAL INSTRUCTION FOR LINKEDIN PDF EXPORTS
    If the Resume Content looks like a LinkedIn PDF export (contains "Page x of y", "Top Skills", "Certifications"):
    1. **Extract Hidden Gems:** Look for the "Top Skills" section at the end. These are high-value keywords.
    2. **Ignore Noise:** Ignore page numbers, "Contact", and footer links.
    3. **Smart Rewrite:** Use the existing "Summary" as a baseline but rewrite it completely to match the Market Tone.

    ### OUTPUT FORMAT (Strict JSON)
    Return a single JSON object with this structure:
    {{
      "url_settings_audit": {{
        "public_visibility": "Check if URL is clean (e.g. /in/name) or messy (/in/name-123a). Suggest fix.",
        "url_optimization": {{
          "status": "Good/Bad",
          "fix": "Exact clean URL to claim."
        }}
      }},

      "seo_strategy_audit": {{
        "primary_keyword_cluster": ["List 5 high-traffic keywords for {role} in {region}"],
        "keyword_gap_analysis": ["List 5 keywords missing from the resume but critical for this role"],
        "search_appearance_score": "Estimated score 0-100 based on keyword density"
      }},

      "text_optimization": {{
        "headline_options": [
          "Option 1: The 'Authority' Formula (Role | Niche | Result)",
          "Option 2: The 'Keyword' Formula (Role | Skill 1 | Skill 2 | Skill 3)",
          "Option 3: The 'Value' Formula (Helping X do Y | Role)"
        ],
        "about_section": {{
          "hook": "First 2 lines to grab attention (visible before 'See More').",
          "body": "The rest of the bio. Use bullet points for achievements. Tone: {region} style.",
          "call_to_action": "Clear next step (e.g., 'DM for collaboration')."
        }},
        "experience_rewrites": {{
            "role": "Most recent/relevant role title",
            "impact_statements": [
                "Rewrite bullet 1 using Google XYZ formula (Accomplished X as measured by Y, by doing Z)",
                "Rewrite bullet 2 focusing on ROI/Scale",
                "Rewrite bullet 3 focusing on Leadership/Tech"
            ]
        }}
      }},

      "visual_audit": {{
        "profile_photo_check": {{
          "technical_score": "1-10",
          "sixty_percent_rule": "Does the face occupy 60% of the circle?",
          "fix": "One specific actionable tip to improve it."
        }},
        "banner_image_check": {{
          "relevance": "Does the banner immediately signal '{role}'?",
          "safe_zone": "Is the text or key visual blocked by the profile picture on mobile screens?",
          "recommendation": "If the current banner is weak, describe exactly what image they should design/find to replace it."
        }}
      }}
    }}
    """

def get_resume_agent_prompt(query, resume_context):
    """
    Returns the prompt for the AI Resume Agent chat.
    """
    return f"""
    You are an AI Resume Agent, a highly skilled career coach and resume expert.
    Your goal is to assist the user with their resume, job search, and career advice.

    RESUME CONTEXT:
    {resume_context}

    USER QUERY:
    "{query}"

    CAPABILITIES:
    1. Improve Score: Analyze the resume and suggest improvements for ATS and readability.
    2. Target Resume: Help tailor the resume for a specific job description (if provided).
    3. Find Jobs: Suggest job titles and search strategies based on the resume skills.
    4. General Advice: Answer questions about resume formatting, cover letters, etc.

    INSTRUCTIONS:
    - Be helpful, encouraging, and professional.
    - If the user asks to "Improve Score", provide a brief audit and 3 actionable tips.
    - If the user asks to "Target Resume", ask for the Job Description if not provided.
    - If the user asks to "Find Jobs", suggest 3 relevant job titles and a search query string.
    """

def get_tone_tuner_prompt(target_market, bio_text):
    """
    Returns the prompt for refining bio tone based on market.
    """
    return f"""
    You are a Cross-Cultural Career Consultant. 
    Review the "About Section" generated previously and refine the tone based on the target location.

    INPUT:
    - Target Market: {target_market} (India or UAE)
    - Current Draft Bio: "{bio_text}"

    INSTRUCTIONS:
    1. IF INDIA: 
       - Increase density of "Hard Skills" and "Certifications". 
       - Highlight "Hustle," "Scaling," and "Volume" (e.g., 'Handled 1M users', 'Certified in X').
       - Tone: Energetic, Technical, Ambitious.

    2. IF UAE (Dubai/Abu Dhabi):
       - Increase focus on "Business Value," "Reliability," and "Cross-Cultural Communication."
       - Highlight "International Standards," "Cost Saving," and "Efficiency."
       - Tone: Professional, Executive, Polished.

    OUTPUT:
    - The Revised "Culturally Tuned" About Section.
    - A list of 3 specific changes you made and why they work for this region.
    """

def get_service_page_proposal_prompt(project_details, profile_data, target_role="Target Role", client_name="Client", tone="Direct and Authority-Driven"):
    """
    Generates a high-ticket Service Page Proposal using advanced sales psychology.
    """
    return f"""
    Role: You are an elite Executive Career Consultant & Personal Branding Strategist. You specialize in converting "cold leads" from LinkedIn Service Pages into high-paying clients ($500+).
    
    Objective: Write a hyper-personalized, "Pattern-Interrupt" proposal that ignores the typical "I can help you" script and leverages acute pain-point analysis.

    Input Data:
    1. [CLIENT NAME]: {client_name}
    2. [TARGET ROLE]: {target_role}
    3. [PROJECT CONTEXT]: {project_details}
    4. [PROFILE DATA (RAW)]: {profile_data}
    5. [DESIRED TONE]: {tone}

    Your Strategy (The "Gap Analysis" Method):
    1.  **The Hook (0-3 Seconds):** Do NOT start with a greeting like "I hope you are well". Start immediately with an observation about their profile vs. their target role. 
        *   Good: "{client_name}, I reviewed your profile and saw you're targeting {target_role} roles, but your headline doesn't position you as an expert."
        *   Bad: "Hi! I am a resume writer..."
    2.  **The Gap (The Pain):** Identify ONE specific "fatal flaw" in their current profile that is costing them interviews. (e.g., "Generic summary", "Duty-based bullets", "No metrics").
    3.  **The Solution (The ROI):** Briefly mention your methodology (e.g., "ATS-compliant", "STAR Method", "Executive Branding").
    4.  **The Call to Value (Not Action):** Do not ask for a call. Ask for permission to send value. "I have a 3-minute video audit of your profile. Can I send it over?"

    Strict Rules:
    -   Word Count: Under 120 words. (Busy executives don't read essays).
    -   No Fluff: Remove words like "passionate", "dedicated", "help".
    -   Formatting: Use short paragraphs (1-2 sentences max).

    Output a JSON object with the following structure:
    {{
        "resume_audit": {{
            "failure_1": "Specific critique of their current headline or summary...",
            "failure_2": "Specific critique of their experience section or lack of metrics..."
        }},
        "before_after_analysis": {{
            "current_state": "e.g., 'Generalist Manager' (Low Value)",
            "future_state": "e.g., 'Strategic {target_role} Leader' (High Value)"
        }},
        "proposal_script": "The complete, ready-to-send proposal text..."
    }}
    """

def get_content_improver_prompt(text, target_role="Professional"):
    """
    Returns the prompt to rewrite resume content for impact.
    """
    return f"""
    Act as a Professional Resume Writer.
    Rewrite the following text to be more impactful, concise, and result-oriented.
    
    Target Role/Context: {target_role}
    Original Text:
    "{text}"
    
    Instructions:
    1. Use strong action verbs.
    2. Quantify results where possible.
    3. Remove fluff and buzzwords.
    4. Keep it professional and concise.
    """

def get_master_prompt(target_market, target_job, profile_text):
    
    # 1. Define Market Nuances
    if target_market == "UAE":
        market_instruction = """
        **MARKET: UAE (Dubai/Abu Dhabi/GCC)**
        - **Culture:** Hierarchical, formal, and prestige-driven.
        - **Key Values:** Loyalty, International Experience, Stability.
        - **Formatting:** Clean, professional, minimal formatting.
        - **Tone:** "Executive Presence." Use British English spelling.
        - **Critical:** Mention visa status or "Available to join immediately" if implied.
        """
    else:  # India or others, default to India style for now as per request logic, or generic if needed. 
           # The user request specifically had 'else: # India' logic.
        market_instruction = """
        **MARKET: INDIA**
        - **Culture:** Competitive, volume-driven, and skill-centric.
        - **Key Values:** Scalability, Hustle, Tech Stack depth, Educational pedigree.
        - **Tone:** Action-oriented. Use American or British English (consistent).
        - **Critical:** Highlight rank/percentiles (e.g., "Top 5% performer").
        """

    # 2. Construct the Prompt
    prompt = f"""
    **ROLE:** Expert CV Writer & LinkedIn Strategist for {target_market}.
    
    **OBJECTIVE:** Rewrite the user's LinkedIn profile to bypass ATS filters and impress human recruiters for the role of: {target_job}.
    
    {market_instruction}
    
    **STRICT NEGATIVE CONSTRAINTS (DO NOT IGNORE):**
    - NO AI buzzwords: "Delve," "Tapestry," "Unleash," "Elevate," "Synergy."
    - NO passive voice.
    - NO flowery introductions like "In the dynamic world of..."
    
    **INPUT DATA:**
    {profile_text}
    
    **SPECIAL INSTRUCTION FOR LINKEDIN PDF EXPORTS:**
    If the input data looks like a LinkedIn PDF export (contains "Page x of y", "Top Skills", "Certifications" sections):
    1. **Extract Hidden Gems:** Look for the "Top Skills" section at the end of the PDF. These are often high-value keywords.
    2. **Ignore Formatting Noise:** Ignore page numbers, "Contact", and "www.linkedin.com" footers.
    3. **Use Summary as Base:** If a "Summary" section exists, use it as the baseline for the new "About Section" but rewrite it completely.
    
    **REQUIRED OUTPUT FORMAT (Markdown):**
    
    ### 1. Headline (Strictly <220 chars)
    [Formula: Role | Key Hard Skill | Unique Value | Metric]
    *(Example: Sales Director | B2B SaaS | Scaling Revenue 0 to $10M | Market Expansion)*
    
    ### 2. About Section (First Person, <2600 chars)
    - **Hook:** 2 sentences stating exactly what you solve.
    - **Body:** 3-4 bullet points of "Signature Achievements" with bolded metrics.
    - **Closing:** Call to Action (e.g., "Open to discussions regarding...").
    
    ### 3. Experience Refinement (Top 3 Roles)
    - Rewrite the most recent roles using the "Google XYZ Formula": "Accomplished [X] as measured by [Y], by doing [Z]."
    
    ### 4. Skills Strategy
    - List 5 "Hard Skills" to pin to the top of the profile.
    - List 5 "Soft Skills" validated by the market culture.
    
    ### 5. "Cold Message" Draft (Bonus)
    - Draft a 300-character connection request message tailored to a recruiter in {target_market}.
      (UAE: Polite & Formal | India: Direct & Value-led)
    """
    return prompt



def get_keyword_matcher_prompt(resume_text, jd_text):
    """
    Returns the prompt to compare resume against JD keywords.
    """
    return f"""
    Act as an ATS (Applicant Tracking System) Algorithm.
    Compare the Resume against the Job Description to find keyword gaps.
    
    Resume Text:
    {resume_text}
    
    Job Description:
    {jd_text}
    
    Output a JSON object:
    {{
        "match_score": "0-100 (Integer)",
        "missing_keywords": ["Keyword 1", "Keyword 2", "Keyword 3"],
        "matching_keywords": ["Keyword A", "Keyword B"]
    }}
    """

def get_logistics_prompt(market, notice_period, visa_status, location):
    """
    Returns the prompt for generating a strategic availability note.
    """
    return f"""
    Act as a Career Strategist.
    Generate a concise "Logistics Strategy Note" for a candidate's resume or cover letter.
    
    Context:
    - Target Market: {market}
    - Notice Period: {notice_period}
    - Visa Status: {visa_status}
    - Current Location: {location}
    
    INSTRUCTIONS:
    1. If Notice Period is "Immediate", highlight it as a competitive advantage.
    2. If Market is "UAE" and candidate is in "India", address the relocation/visa aspect professionally (e.g., "Ready to relocate at own expense").
    3. If Market is "India", focus on "Serving Notice" or "Buyout Options".
    4. If UAE + Golden Visa: Write "Golden Visa Holder (No Sponsorship Needed)."
    
    GENERATE:
    1. A 1-sentence "Logistics Tagline" for the Headline.
    2. A professional 2-sentence explanation for the bottom of the About section.
    """


def get_linkedin_banner_content_extraction_prompt(linkedin_text, target_role):
    """
    Extracts custom hook, tagline, and LinkedIn URL from LinkedIn profile text for banner generation.
    """
    return f"""
    You are a LinkedIn Personal Branding Expert. Analyze the following LinkedIn profile content and extract/generate compelling banner content.
    
    LinkedIn Profile Content:
    {linkedin_text}
    
    Target Role: {target_role}
    
    Your task is to:
    1. Extract the LinkedIn profile URL if present
    2. Generate an attractive, attention-grabbing HOOK (main headline) for a LinkedIn banner
    3. Generate a compelling TAGLINE (subheadline) that supports the hook
    
    HOOK Guidelines:
    - Should be 3-8 words maximum
    - Must be action-oriented and value-driven
    - Should immediately communicate the professional's unique value
    - Examples: "Transforming Data Into Business Growth", "Building Scalable Cloud Solutions", "Leading Digital Transformation"
    
    TAGLINE Guidelines:
    - Should be 8-15 words maximum
    - Expands on the hook with specific skills or achievements
    - Should include measurable impact if possible
    - Examples: "Helping Fortune 500 Companies Scale with AWS & Kubernetes", "10+ Years Driving Revenue Through AI/ML Solutions"
    
    Output strictly in JSON format:
    {{
        "linkedin_url": "Extract the LinkedIn URL (e.g., linkedin.com/in/username) or empty string if not found",
        "custom_hook": "Generated attention-grabbing hook based on profile",
        "custom_tagline": "Generated compelling tagline based on profile and achievements"
    }}
    
    IMPORTANT: Base the hook and tagline on the actual profile content. Look for:
    - Current headline
    - About section
    - Key achievements
    - Core skills
    - Years of experience
    - Industry focus
    """
