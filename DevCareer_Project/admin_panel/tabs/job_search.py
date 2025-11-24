import streamlit as st
from datetime import datetime

def render_job_search():
    st.header("💼 Intelligent Job Search")
    
    # Custom CSS for the Job Search UI to match the dark aesthetic
    st.markdown("""
    <style>
        .job-card {
            background-color: #1E1E1E;
            border: 1px solid #333;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            transition: transform 0.2s;
        }
        .job-card:hover {
            transform: translateY(-2px);
            border-color: #555;
        }
        .job-title {
            font-size: 18px;
            font-weight: bold;
            color: #FFFFFF;
            margin-bottom: 5px;
        }
        .company-name {
            font-size: 14px;
            color: #AAAAAA;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .job-desc {
            font-size: 14px;
            color: #DDDDDD;
            margin-bottom: 15px;
            line-height: 1.5;
        }
        .job-meta {
            font-size: 12px;
            color: #888888;
            display: flex;
            justify_content: space-between;
            align-items: center;
        }
        .status-badge {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }
        .status-active { background-color: #2E74B5; color: white; }
        .status-saved { background-color: #333; color: #AAA; border: 1px solid #555; }
    </style>
    """, unsafe_allow_html=True)

    # --- Top Navigation Tabs ---
    tabs = ["ALL JOBS", "SAVED (0)", "APPLIED (0)", "INTERVIEWING (0)", "REJECTED (0)"]
    selected_tab = st.radio("Navigation", tabs, horizontal=True, label_visibility="collapsed")
    
    st.markdown("---")

    # --- Search & Filter Bar ---
    c1, c2, c3 = st.columns([3, 2, 1])
    with c1:
        st.text_input("Role", placeholder="Senior Software Engineer", label_visibility="collapsed")
    with c2:
        locations = ["United Arab Emirates", "India", "Remote"]
        selected_loc = st.selectbox("Location", locations, label_visibility="collapsed")
    with c3:
        # Job Source Filter
        sources = ["All Sources", "Naukri.com", "Monster.com", "Naukri Gulf"]
        selected_source = st.selectbox("Source", sources, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Extended Mock Job Data ---
    all_jobs = [
        # UAE Jobs
        {"title": "Senior Software Engineer", "company": "Delivery Hero", "location": "United Arab Emirates", "source": "Naukri Gulf", "logo": "🎒", "desc": "Senior Backend Engineer sought to join Growth team in Dubai. Microservices, Go, AWS.", "date": "Nov 21, 2025"},
        {"title": "Senior Software Engineer", "company": "Property Finder", "location": "United Arab Emirates", "source": "Naukri Gulf", "logo": "🏠", "desc": "Seeking a talented Software Engineer to develop scalable full-stack applications.", "date": "Oct 17, 2025"},
        {"title": "Senior Software Developer", "company": "Core42", "location": "United Arab Emirates", "source": "Monster.com", "logo": "💻", "desc": "Develop end-to-end web apps using ReactJS and .NET Core.", "date": "Nov 14, 2025"},
        {"title": "Senior Fullstack Engineer", "company": "Parser Limited", "location": "United Arab Emirates", "source": "Naukri.com", "logo": "KP", "desc": "Design, build, and maintain scalable full-stack applications in Dubai.", "date": "Nov 19, 2025"},
        {"title": "DevOps Engineer", "company": "Emirates Group", "location": "United Arab Emirates", "source": "Naukri Gulf", "logo": "✈️", "desc": "Manage CI/CD pipelines and cloud infrastructure for airline systems.", "date": "Nov 23, 2025"},
        {"title": "Product Manager", "company": "Careem", "location": "United Arab Emirates", "source": "Naukri.com", "logo": "🚗", "desc": "Lead the super-app product vision and strategy.", "date": "Nov 20, 2025"},
        
        # India Jobs
        {"title": "Lead Java Developer", "company": "Flipkart", "location": "India", "source": "Naukri.com", "logo": "🛒", "desc": "Leading e-commerce giant seeking Java experts for order processing systems.", "date": "Nov 22, 2025"},
        {"title": "SDE-II (Backend)", "company": "Swiggy", "location": "India", "source": "Naukri.com", "logo": "🍱", "desc": "Optimize logistics algorithms using Go and Python.", "date": "Nov 20, 2025"},
        {"title": "Data Scientist", "company": "Ola Electric", "location": "India", "source": "Monster.com", "logo": "🔋", "desc": "Analyze battery telemetry data to improve EV performance.", "date": "Nov 18, 2025"},
        {"title": "Frontend Engineer", "company": "Razorpay", "location": "India", "source": "Naukri.com", "logo": "💳", "desc": "Build seamless payment checkout experiences using React.", "date": "Nov 15, 2025"},
        {"title": "Cloud Architect", "company": "TCS", "location": "India", "source": "Monster.com", "logo": "☁️", "desc": "Architect enterprise cloud solutions on Azure and AWS.", "date": "Nov 24, 2025"},
        {"title": "AI Researcher", "company": "Google India", "location": "India", "source": "Naukri.com", "logo": "🧠", "desc": "Research and develop next-gen LLM applications.", "date": "Nov 21, 2025"},
        {"title": "Mobile Developer", "company": "Zomato", "location": "India", "source": "Naukri.com", "logo": "🍅", "desc": "Build the next generation of food delivery mobile apps.", "date": "Nov 19, 2025"},
        
        # Remote Jobs
        {"title": "Senior Python Dev", "company": "Automattic", "location": "Remote", "source": "Monster.com", "logo": "W", "desc": "Work on WordPress.com backend systems from anywhere.", "date": "Nov 23, 2025"},
        {"title": "Go Engineer", "company": "Doist", "location": "Remote", "source": "Naukri.com", "logo": "✅", "desc": "Build productivity tools for millions of users.", "date": "Nov 21, 2025"}
    ]
    
    # Filter Jobs
    filtered_jobs = [j for j in all_jobs if j['location'] == selected_loc]
    if selected_source != "All Sources":
        filtered_jobs = [j for j in filtered_jobs if j['source'] == selected_source]

    # --- Pagination Logic ---
    items_per_page = 5
    total_jobs = len(filtered_jobs)
    total_pages = max(1, (total_jobs + items_per_page - 1) // items_per_page)
    
    if 'job_page' not in st.session_state:
        st.session_state.job_page = 1
        
    # Reset page if filters change (simple check: if current page > total pages)
    if st.session_state.job_page > total_pages:
        st.session_state.job_page = 1

    # Pagination Controls
    col_p1, col_p2, col_p3 = st.columns([2, 6, 2])
    with col_p1:
        if st.button("⬅️ Previous", disabled=st.session_state.job_page == 1):
            st.session_state.job_page -= 1
            st.rerun()
    with col_p2:
        st.markdown(f"<div style='text-align: center; padding-top: 5px;'>Page <b>{st.session_state.job_page}</b> of <b>{total_pages}</b> ({total_jobs} Jobs)</div>", unsafe_allow_html=True)
    with col_p3:
        if st.button("Next ➡️", disabled=st.session_state.job_page == total_pages):
            st.session_state.job_page += 1
            st.rerun()

    # Slice Data
    start_idx = (st.session_state.job_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    jobs_to_show = filtered_jobs[start_idx:end_idx]

    # --- Job List Render ---
    for i, job in enumerate(jobs_to_show):
        with st.container():
            # Enhanced HTML Card
            st.markdown(f"""<div class="job-card" style="border-left: 4px solid #2E74B5;">
    <div style="display: flex; justify-content: space-between; align-items: start;">
        <div style="flex: 1;">
            <div class="job-title">{job['title']}</div>
            <div class="company-name">
                <span style="font-size: 18px; margin-right: 8px;">{job['logo']}</span> 
                <span style="color: #FFF;">{job['company']}</span> 
                <span style="margin: 0 8px; color: #555;">|</span> 
                {job['location']}
            </div>
        </div>
        <div style="text-align: right;">
            <div style="background-color: #333; color: #AAA; padding: 2px 8px; border-radius: 4px; font-size: 11px; display: inline-block; margin-bottom: 5px;">
                {job['source']}
            </div>
            <div style="color: #666; font-size: 12px;">{job['date']}</div>
        </div>
    </div>
    
    <div style="margin-top: 12px; padding: 10px; background-color: #252526; border-radius: 6px; border: 1px dashed #444;">
        <div style="color: #DDD; font-size: 13px; line-height: 1.4;">
            <span style="color: #2E74B5; font-weight: bold;">Role Overview:</span> {job['desc']}
        </div>
    </div>
</div>""", unsafe_allow_html=True)
            
            # Action Buttons
            c_act1, c_act2, c_act3, c_act4 = st.columns([6, 2, 0.5, 0.5])
            with c_act2:
                st.button("TARGET RESUME", key=f"target_{start_idx + i}", use_container_width=True)
            with c_act3:
                st.button("❤️", key=f"save_{start_idx + i}")
            with c_act4:
                st.button("...", key=f"more_{start_idx + i}")
            
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
