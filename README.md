# AgentDev

Project overview and quick start. See `PROJECT_STRUCTURE.md` for detailed layout.

Quick start

```bash
# Backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Frontend (inside frontend/)
cd frontend
npm install
npm run dev
```
