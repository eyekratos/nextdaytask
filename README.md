# NextDay — Personal Daily Planner

A simple free task planner built with Python + Streamlit. Plan the night before, check off tasks tomorrow, choose one main win, reflect on the day, and break long-term goals into roadmap steps.

## Run on Windows

1. Install Python 3.11+ from https://www.python.org/downloads/windows/
   - During installation, tick **Add Python to PATH**.
2. Extract this ZIP to a folder, e.g. `C:\NextDay`.
3. Open PowerShell in that folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If PowerShell blocks activation, use this alternative without activation:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

4. The app opens in your browser, usually at http://localhost:8501.

## Data and backups

- `planner_data.json` and `roadmap.json` are created beside `app.py`.
- Use the app's Export section to download backups.
- Keep these files somewhere safe if you want to preserve your tasks.

## Publish as a website for free

You can deploy on Streamlit Community Cloud:
1. Create a GitHub account and a repository.
2. Upload `app.py` and `requirements.txt` (optionally README).
3. Visit https://share.streamlit.io/ and connect GitHub.
4. Choose **Create app**, select your repository and `app.py`, then deploy.

Important: this starter app stores data in local JSON files. On a hosted service, storage may not be persistent across restarts/redeployments. For reliable cross-device cloud sync, add a database and authentication before using it as your only planner. Avoid uploading private tasks to a public repository.
