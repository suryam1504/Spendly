# Spec: Registration

## Overview
This step wires up the registration form so that new users can create an account. The `POST /register` route reads the submitted name, email, and password, validates the input, hashes the password with werkzeug, and inserts the new row into the `users` table. On success the user is redirected to the login page with a success flash message. Duplicate emails and missing fields are handled gracefully with inline error messages. A Flask `SECRET_KEY` is also introduced so that `session` and `flash` can be used in subsequent steps.

## Depends on
- Step 1 — Database setup (`users` table created by `init_db()` in `database/db.py`)

## Routes
- `POST /register` — process registration form submission — public

## Database changes
No database changes. The `users` table (`id`, `name`, `email`, `password_hash`, `created_at`) already exists in `database/db.py`.

## Templates
- **Modify:** `templates/register.html` — already renders `{{ error }}`; add a `{% with %}` block to also render `get_flashed_messages()` for the success case, preserve the submitted `name` and `email` values on validation failure so the form is not wiped, and add a "Confirm password" field below the password field.

## Files to change
- `app.py` — add `SECRET_KEY`, import `request`, `redirect`, `url_for`, `flash` from Flask; convert the `register` view to handle both GET and POST; add form validation and DB insertion logic.

## Files to create
No new files.

## New dependencies
No new dependencies. `werkzeug.security.generate_password_hash` is already imported in `database/db.py` and available via the existing `werkzeug` install.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never interpolate user input into SQL strings
- Passwords hashed with `werkzeug.security.generate_password_hash` using `method="pbkdf2:sha256"`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `SECRET_KEY` must be set on the Flask `app` object before any `session` or `flash` usage; load it from an environment variable with a safe fallback for development only
- Validate: name non-empty, email non-empty, password at least 8 characters, password matches confirm password; catch `sqlite3.IntegrityError` for duplicate email
- After successful registration redirect to `url_for('login')` and flash a success message
- On validation failure re-render the form with the error message and the previously submitted `name` and `email` so the user does not lose their input
- Never repopulate password or confirm password fields on re-render — security anti-pattern

## Definition of done
- [ ] Visiting `GET /register` still renders the form (no regression)
- [ ] Submitting the form with valid data inserts a new row in `users` and redirects to `/login`
- [ ] The login page shows a flash message confirming the account was created
- [ ] Submitting with a duplicate email re-renders the form with an error message and the typed name/email still present in the fields
- [ ] Submitting with a password shorter than 8 characters re-renders the form with a validation error
- [ ] Submitting with mismatched password and confirm password re-renders the form with "Passwords do not match."
- [ ] Submitting with an empty name or empty email re-renders the form with a validation error
- [ ] The stored password is a hash (not plaintext) — verifiable by inspecting `spendly.db` with `sqlite3 spendly.db "SELECT password_hash FROM users LIMIT 1;"`
