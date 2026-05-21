from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load dataset
df = pd.read_csv("data/gl_transactions.csv")

@app.route("/api/gl", methods=["GET"])
def get_gl():
    records = []
    for _, row in df.iterrows():
        records.append({
            "EntryNo": row["EntryNo"],
            "Date": row["Date"],
            "Territory_key": int(row["Territory_key"]),
            "Account_key": int(row["Account_key"]),
            "Details": row["Details"],
            "Debit": float(row["Debit"]),
            "Credit": float(row["Credit"])
        })
    return jsonify(records)

@app.route("/api/gl/incremental/<date>", methods=["GET"])
def get_incremental(date):
    """Simulate daily incremental transactions."""
    filtered = df[df["Date"].str.contains(date)]
    records = filtered.to_dict(orient="records")
    return jsonify(records)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
