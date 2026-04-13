# Spec: Login and Logout

## Overview
This step wires up the login form and logout route so that registered users can authenticate and maintain a session. The `POST /login` route reads the submitted email and password, looks up the user by email, verifies the password hash with werkzeug, and stores the user's `id` and `name` in Flask's `session` on success. The `GET /logout` route clears the session and redirects to the landing page. The shared `base.html` nav is updated to show context-aware links: unauthenticated users see "Sign in" and "Get started"; authenticated users see "Logout" instead.

## Depends on
- Step 1 — Database setup (`users` table created by `init_db()`)
- Step 2 — Registration (`POST /register` creates user rows; `SECRET_KEY` and `flash` already wired)

## Routes
- `POST /login` — process login form, set session on success — public
- `GET /logout` — clear session, redirect to landing — logged-in (but gracefully handles unauthenticated calls too)

## Database changes
No database changes. The `users` table already has all required columns: `id`, `email`, `password_hash`.

## Templates
- **Modify:** `templates/login.html` — add a `{% with %}` block to render `get_flashed_messages()` (for flash messages from registration); preserve the submitted `email` value on authentication failure so the field is not wiped.
- **Modify:** `templates/base.html` — update the `.nav-links` block to show "Logout" link (`/logout`) when `session.user_id` is set, and "Sign in" + "Get started" when not.

## Files to change
- `app.py` — convert `login` view to handle both GET and POST; add `check_password_hash` import from `werkzeug.security`; add `session` import from Flask; implement `POST /login` validation, lookup, and session write; implement `GET /logout` to clear session and redirect.
- `templates/login.html` — add flash message rendering; preserve submitted `email` on error.
- `templates/base.html` — conditional nav links based on `session.get('user_id')`.

## Files to create
No new files.

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` is available via the existing werkzeug install.

## Rules for implementation
- Redirect already-authenticated users away from `/login` and `/register` — check `session.get('user_id')` at the top of both views and redirect to `url_for('landing')` if set
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never interpolate user input into SQL strings
- Passwords verified with `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Store only `user_id` (int) and `user_name` (str) in `session` — never store the password hash or full user row
- Use a deliberately vague error message on login failure ("Invalid email or password.") — do not reveal whether the email exists
- On successful login, redirect to `url_for('landing')` (dashboard route does not exist yet)
- On logout, call `session.clear()` then redirect to `url_for('landing')` with a flash info message
- `GET /logout` should work even if the user is not logged in (session.clear() is safe on an empty session)

## Definition of done
- [ ] Visiting `GET /login` while already logged in redirects to `/` instead of showing the form
- [ ] Visiting `GET /register` while already logged in redirects to `/` instead of showing the form
- [ ] Visiting `GET /login` renders the form (no regression)
- [ ] Submitting valid credentials sets the session and redirects to `/`
- [ ] After login, the navbar shows a "Logout" link and hides "Sign in" / "Get started"
- [ ] Submitting an unknown email re-renders the form with "Invalid email or password." and the typed email still in the field
- [ ] Submitting a correct email but wrong password re-renders the form with the same vague error message
- [ ] Visiting `GET /logout` clears the session and redirects to `/`
- [ ] After logout, the navbar shows "Sign in" and "Get started" again
- [ ] Flash messages from registration (e.g. "Account created! Please sign in.") are visible on the login page
- [ ] Submitting an empty email or empty password re-renders the form with a validation error (client-side `required` is acceptable)
