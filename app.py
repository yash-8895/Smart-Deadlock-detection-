import os, json, sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
DB_FILE = os.environ.get("DEADLOCK_DB", "deadlock_demo.db")

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS processes (
          id INTEGER PRIMARY KEY AUTOINCREMENT, process_name TEXT UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS resources (
          id INTEGER PRIMARY KEY AUTOINCREMENT, resource_name TEXT UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS analysis_logs (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          created_at TEXT NOT NULL, algorithm TEXT NOT NULL,
          safe_state INTEGER NOT NULL, safe_sequence TEXT NOT NULL,
          max_matrix TEXT NOT NULL, allocation_matrix TEXT NOT NULL,
          available_vector TEXT NOT NULL, message TEXT NOT NULL
        );
        """)
        for i in range(1, 6):
            conn.execute("INSERT OR IGNORE INTO processes(process_name) VALUES (?)", (f"P{i}",))
        for i in range(1, 4):
            conn.execute("INSERT OR IGNORE INTO resources(resource_name) VALUES (?)", (f"R{i}",))

def run_banker(maximum, allocation, available):
    if len(maximum) == 0 or len(maximum) != len(allocation):
        raise ValueError("Maximum and Allocation must have the same non-zero number of processes.")
    resources = len(available)
    if resources == 0 or any(len(r) != resources for r in maximum + allocation):
        raise ValueError("Every matrix row must match the number of available-resource values.")
    if any(not isinstance(x, int) or x < 0 for row in maximum + allocation for x in row) or any(not isinstance(x, int) or x < 0 for x in available):
        raise ValueError("Resource values must be non-negative integers.")
    if any(allocation[i][j] > maximum[i][j] for i in range(len(maximum)) for j in range(resources)):
        raise ValueError("Allocation cannot exceed maximum demand.")
    need = [[maximum[i][j] - allocation[i][j] for j in range(resources)] for i in range(len(maximum))]
    work = available[:]
    finish = [False] * len(maximum)
    sequence = []
    while len(sequence) < len(maximum):
        progressed = False
        for i in range(len(maximum)):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(resources)):
                work = [work[j] + allocation[i][j] for j in range(resources)]
                finish[i] = True
                sequence.append(i)
                progressed = True
        if not progressed:
            return {"safe": False, "sequence": [], "need": need, "message": "Unsafe state — no safe sequence found."}
    return {"safe": True, "sequence": sequence, "need": need, "message": "Safe state — all processes can finish."}

def save_log(data, result, algorithm):
    with get_db() as conn:
        conn.execute("""INSERT INTO analysis_logs
          (created_at, algorithm, safe_state, safe_sequence, max_matrix, allocation_matrix, available_vector, message)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
          (datetime.now().isoformat(timespec="seconds"), algorithm, int(result["safe"]),
           json.dumps([f"P{i+1}" for i in result["sequence"]]),
           json.dumps(data["max"]), json.dumps(data["allocation"]),
           json.dumps(data["available"]), result["message"]))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json(force=True)
        for key in ("max", "allocation", "available"):
            if key not in data: raise ValueError(f"Missing required field: {key}")
        result = run_banker(data["max"], data["allocation"], data["available"])
        save_log(data, result, "Banker's Algorithm")
        result["sequence_labels"] = [f"P{i+1}" for i in result["sequence"]]
        return jsonify(result)
    except (ValueError, TypeError, KeyError) as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        app.logger.exception("Analysis failed")
        return jsonify({"error": "Unexpected server error. Check the terminal for details."}), 500

@app.route("/api/logs")
def logs():
    with get_db() as conn:
        rows = conn.execute("SELECT id, created_at, algorithm, safe_state, safe_sequence, message FROM analysis_logs ORDER BY id DESC LIMIT 10").fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "database": "SQLite demo database", "message": "Backend is responding."})

init_db()
if __name__ == "__main__":
    app.run(debug=True, port=8080)
