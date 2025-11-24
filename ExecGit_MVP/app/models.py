# In a real app, use SQLAlchemy or SQLModel
# This is a representation of the schema as requested

"""
SQL CREATE TABLE Commands for ExecGit Database Schema
"""

SQL_SCHEMA = """
-- 1. Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    github_id VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    timezone VARCHAR(50) DEFAULT 'UTC',
    subscription_tier VARCHAR(20) DEFAULT 'free', -- free, pro, enterprise
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Repositories Table (Managed Repos)
CREATE TABLE repositories (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    repo_name VARCHAR(255) NOT NULL,
    repo_url VARCHAR(512) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_synced_at TIMESTAMP
);

-- 3. Schedule Settings
CREATE TABLE schedule_settings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    active_days VARCHAR(50), -- e.g., "Mon,Wed,Fri"
    start_time TIME,
    end_time TIME,
    persona VARCHAR(50) -- 'weekend_warrior', 'night_owl'
);

-- 4. Activity Log (Ghostwritten Commits)
CREATE TABLE activity_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    repo_id INTEGER REFERENCES repositories(id),
    commit_hash VARCHAR(40),
    commit_message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) -- 'pending', 'pushed', 'rejected'
);

-- 5. Payment History
CREATE TABLE payment_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    amount DECIMAL(10, 2),
    currency VARCHAR(3),
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    transaction_id VARCHAR(255)
);
"""
