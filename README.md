# Phase 2 demo — Smart Deadlock Detection and Resource Management

## What this version demonstrates
- **OS:** Banker's Algorithm, Need = Maximum − Allocation, safe/unsafe state, safe sequence.
- **DBMS:** a local SQLite database stores Processes, Resources, and Analysis Logs so the history survives refreshes.
- **Frontend:** responsive web dashboard with editable matrices, input validation, live results, and recent logs.
- **Project groundwork:** original Random Forest model and dataset/training files are included, but ML is not wired into this Phase 2 UI yet.

## Run the demo
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Run `python -m pip install -r requirements.txt`
4. Run `python app.py`
5. Open `http://127.0.0.1:8080`

The app creates `deadlock_demo.db` automatically. Use **Run Banker's Algorithm** and then point out the recent logs.

## MySQL / DBMS presentation
`schema_mysql.sql` is the MySQL 8 schema for your database demonstration. Open MySQL Workbench, run the script, and show the tables `Processes`, `Resources`, `Resource_Allocation`, and `Analysis_Logs`. The current web app uses SQLite for a no-configuration local demo; do not claim that the running app is writing to MySQL unless you integrate and configure a MySQL connector.

## Files to show the teacher
1. `templates/index.html` — frontend layout.
2. `static/style.css` — responsive design.
3. `static/app.js` — frontend actions and API calls.
4. `app.py` — Flask routes, Banker's Algorithm, validation, and persistence.
5. `schema_mysql.sql` — DBMS schema and relationships.
6. `bankers.py` — original standalone algorithm module (the demo app has its own validated implementation in `app.py`).
7. `dataset_generator.py`, `preprocessing.py`, `model_train.py`, and the `.pkl` files — show only as future/next-phase ML groundwork if asked.

## Suggested live demo
1. Run the app and show the dashboard responding.
2. Click **Run Banker's Algorithm** with the default sample; show SAFE STATE and the sequence.
3. Change Available resources to `0, 0, 0` and rerun; show UNSAFE STATE.
4. Refresh DBMS logs; show both analyses were recorded.
5. Open `schema_mysql.sql` in Workbench and explain the tables and foreign-key relationship.
6. Explain that ML comparison and recovery/advanced logging are planned next; don't claim unfinished features are complete.

## Important
This is a Phase 2 presentation starter, not a claim that the full project is complete. It demonstrates the core OS flow and a working database-backed prototype. The included app currently persists to SQLite; the MySQL schema is supplied for the DBMS demonstration and needs connector integration before the app can write directly to MySQL.
