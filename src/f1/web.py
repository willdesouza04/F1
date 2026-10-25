"""Web interface for F1 lap times."""

import webbrowser
from threading import Timer

from flask import Flask, render_template, request, jsonify

from .client import OpenF1Client
from .exceptions import OpenF1Error

app = Flask(__name__)
client = OpenF1Client()


@app.route("/")
def index():
    """Home page."""
    return render_template("index.html")


@app.route("/api/meetings", methods=["GET"])
def get_meetings():
    """Get all F1 meetings (races)."""
    year = request.args.get("year", type=int, default=2024)

    try:
        meetings = client.get_meetings(year=year)
        return jsonify(meetings)
    except OpenF1Error as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/sessions/<int:meeting_key>", methods=["GET"])
def get_meeting_sessions(meeting_key):
    """Get sessions for a specific meeting."""
    try:
        sessions = client.get_sessions(meeting_key=meeting_key)
        return jsonify(sessions)
    except OpenF1Error as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/laps/<int:session_key>", methods=["GET"])
def get_laps(session_key):
    """Get lap times for a session with driver names."""
    try:
        # Get laps
        laps = client.get_laps(session_key=session_key)

        # Filter: only completed laps (not pit outs, with lap_duration)
        laps = [
            lap for lap in laps
            if lap.get("lap_duration") and not lap.get("is_pit_out_lap")
        ]

        if not laps:
            return jsonify([])

        # Get drivers to enrich lap data with names
        drivers = client.get_drivers(session_key=session_key)
        driver_map = {d["driver_number"]: d for d in drivers}

        # Enrich laps with driver info
        for lap in laps:
            driver_num = lap.get("driver_number")
            if driver_num in driver_map:
                driver = driver_map[driver_num]
                lap["driver_name"] = (
                    f"{driver.get('first_name', '')} {driver.get('last_name', '')}"
                )
                lap["team_name"] = driver.get("team_name", "Unknown")
            # Normalize field name for frontend
            lap["duration_seconds"] = lap.get("lap_duration")

        # Sort by driver and lap number
        laps.sort(key=lambda x: (x.get("driver_number"), x.get("lap_number")))

        return jsonify(laps)
    except OpenF1Error as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/drivers/<int:session_key>", methods=["GET"])
def get_drivers_list(session_key):
    """Get drivers for a session."""
    try:
        drivers = client.get_drivers(session_key=session_key)
        return jsonify(drivers)
    except OpenF1Error as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/test/<int:session_key>", methods=["GET"])
def test_api(session_key):
    """Test API connection and return raw data."""
    try:
        laps = client.get_laps(session_key=session_key)
        drivers = client.get_drivers(session_key=session_key)

        completed_laps = [
            l for l in laps if l.get("lap_duration") and not l.get("is_pit_out_lap")
        ]

        return jsonify({
            "total_laps": len(laps),
            "completed_laps": len(completed_laps),
            "total_drivers": len(drivers),
            "sample_lap": laps[0] if laps else None,
            "sample_driver": drivers[0] if drivers else None,
            "laps_with_lap_duration": len([l for l in laps if l.get("lap_duration")]),
            "pit_out_laps": len([l for l in laps if l.get("is_pit_out_lap")]),
            "error": None
        })
    except OpenF1Error as e:
        return jsonify({"error": str(e), "type": "OpenF1Error"}), 500
    except Exception as e:
        return jsonify({"error": str(e), "type": "GeneralError"}), 500


def open_browser():
    """Open browser after a short delay to let the server start."""
    webbrowser.open("http://localhost:5000")


if __name__ == "__main__":
    # Print banner
    print("\n" + "=" * 70)
    print("🏁 F1 ANALYTICS - TEMPOS DE VOLTA".center(70))
    print("=" * 70)
    print("\n📍 Servidor iniciado em: http://localhost:5000".ljust(70))
    print("\n📖 Instruções:".ljust(70))
    print("  1. Selecione o ANO (2023 ou 2024)".ljust(70))
    print("  2. Escolha uma REUNIÃO (Grande Prêmio)".ljust(70))
    print("  3. Selecione a SESSÃO (Treino, Classificação ou Corrida)".ljust(70))
    print("  4. Veja os tempos de volta com ranking de pilotos".ljust(70))
    print("\n⌨️  Para parar: Pressione CTRL+C".ljust(70))
    print("\n" + "=" * 70 + "\n")

    # Open browser after 1 second
    Timer(1.0, open_browser).start()

    # Run Flask app
    app.run(debug=False, port=5000)
