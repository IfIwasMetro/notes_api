# Notes API

FastAPI + SQLAlchemy (SQLite) + JWT auth.

## Run
```bash
pip install -r requirements.txt
export SECRET_KEY=$(openssl rand -hex 32)
uvicorn app.main:app --reload
```
Docs: http://127.0.0.1:8000/docs (use the Authorize button after registering).

## Notes
- Anyone can register with any role (admin/editor/user). Fine for the assignment;
  in production, remove `role` from the public register schema.
- Tags are stored in a JSON column and filtered in Python.
- Tokens expire after 30 minutes.
