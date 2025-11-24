# ExecGit Frontend Structure

This document outlines the recommended structure for the React frontend of ExecGit.

## Directory Layout

```
ExecGit_MVP/
└── frontend/
    ├── public/
    │   ├── index.html       # Main HTML file
    │   └── favicon.ico
    ├── src/
    │   ├── components/
    │   │   ├── Dashboard.js # Main Dashboard Component (Implemented)
    │   │   ├── Navbar.js    # Navigation Bar
    │   │   └── Sidebar.js   # Sidebar Menu
    │   ├── assets/
    │   │   └── styles.css   # Global Styles (Tailwind directives)
    │   ├── App.js           # Main App Component
    │   └── index.js         # Entry Point
    ├── package.json         # Dependencies (React, Tailwind, etc.)
    └── tailwind.config.js   # Tailwind Configuration
```

## Key Components

1.  **Dashboard.js**: The central hub for the user. Contains:
    *   Stealth Mode Toggle
    *   DNA Match Visualizer
    *   Growth Graph
    *   Pending Approvals List

2.  **Tailwind Configuration**:
    *   Theme should be customized for "Cyberpunk/Hacker" aesthetic.
    *   Colors: Primary Green (`#00ff00`), Dark Gray (`#1a1a1a`).
    *   Fonts: Monospace (e.g., 'Fira Code', 'Roboto Mono').

## Integration
The frontend should communicate with the FastAPI backend via REST endpoints:
- `GET /status`: For Stealth Mode status.
- `GET /stats`: For Growth Graph and DNA Match score.
- `GET /pending-commits`: For the approvals list.
- `POST /approve-commit`: To trigger the git push.
