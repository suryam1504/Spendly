# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the development server (port 5001)
python app.py

# Run tests
pytest

# Run a single test file
pytest tests/test_foo.py

# Install dependencies
pip install -r requirements.txt
```

## Architecture

This is a **Flask + SQLite** web app called **Spendly** — a personal expense tracker. It uses Jinja2 templates and vanilla JS (no frontend frameworks).

### Key files

- `app.py` — all Flask routes live here; no blueprints currently
- `database/db.py` — stub for SQLite helpers: `get_db()`, `init_db()`, `seed_db()`
- `templates/base.html` — shared nav + footer; all other templates extend this
- `static/css/` and `static/js/` — plain CSS and vanilla JS only

### Route inventory

| Method | Path | Status |
|--------|------|--------|
| GET | `/` | landing page |
| GET | `/register` | registration form |
| GET | `/login` | login form |
| GET | `/terms` | terms & conditions |
| GET | `/privacy` | privacy policy |
| GET | `/logout` | placeholder (Step 3) |
| GET | `/profile` | placeholder (Step 4) |
| GET | `/expenses/add` | placeholder (Step 7) |
| GET | `/expenses/<id>/edit` | placeholder (Step 8) |
| GET | `/expenses/<id>/delete` | placeholder (Step 9) |

### Implementation status

This is an **educational step-by-step project**. The database module (`database/db.py`) and most auth/expense routes are stubs waiting to be implemented. `file.txt` contains the sequenced prompts used to build the project incrementally.

### Frontend conventions

- No JS libraries — vanilla JS only
- CSS custom properties for the design system (colors, spacing)
- Typography: DM Sans (body) + DM Serif Display (headings) via Google Fonts
- Modal pattern: `data-src` on iframes for lazy-loading; clear `src` on close to stop media
