
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
    Analyze the following resume and identify the candidate's most likely **Target Job Role** and **Core Tech Stack**.
    
    Resume Content:
    {resume_text}
    
    Output strictly in JSON format:
    {{
        "role": "Suggested Job Title (e.g. Senior Java Developer)",
        "stack": "Top 5-7 Tech Skills (comma separated)"
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
    Act as a Data Extraction Specialist.
    Extract data from the following resume text into a strict JSON format compatible with a resume builder.
    
    Resume Text:
    {resume_text}
    
    OUTPUT STRICT JSON (No markdown code blocks, just the raw JSON):
    {{
        "contact": {{
            "name": "Full Name",
            "email": "Email",
            "phone": "Phone",
            "location": "City, Country",
            "linkedin": "LinkedIn URL",
            "portfolio": "Portfolio URL"
        }},
        "summary": "Professional Summary / Bio",
        "experience": [
            {{
                "title": "Job Title",
                "company": "Company Name",
                "dates": "Start - End Date",
                "location": "Location",
                "description": "<ul><li>Bullet point 1</li><li>Bullet point 2</li></ul>" 
            }}
        ],
        "projects": [
            {{
                "title": "Project Name",
                "tech_stack": "Tech Stack Used",
                "description": "<ul><li>Project detail 1</li><li>Project detail 2</li></ul>"
            }}
        ],
        "education": [
            {{
                "school": "University Name",
                "degree": "Degree Name",
                "dates": "Graduation Year"
            }}
        ],
        "skills": "Skill 1, Skill 2, Skill 3 (Comma separated string)",
        "certifications": "Cert 1\\nCert 2 (Newline separated string)",
        "languages": "Lang 1, Lang 2 (Comma separated string)"
    }}
    
    Rules:
    1. If a field is missing, use an empty string "" or empty list [].
    2. For 'description' fields, try to format bullet points as HTML <ul><li>...</li></ul> if possible, otherwise just plain text.
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
