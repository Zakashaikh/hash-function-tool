# app.py - Flask web app for generating and comparing cryptographic hashes.

import hashlib

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for

from database import init_db, save_hash_result, get_hash_history

ALGORITHMS = ("MD5", "SHA-1", "SHA-256", "SHA-512")

app = Flask(__name__)
app.secret_key = 'your-secret-key-for-security'

init_db()


def digest_all(data: bytes) -> dict:
    """Return {algorithm: hex digest} for every supported algorithm."""
    return {
        "MD5": hashlib.md5(data).hexdigest(),
        "SHA-1": hashlib.sha1(data).hexdigest(),
        "SHA-256": hashlib.sha256(data).hexdigest(),
        "SHA-512": hashlib.sha512(data).hexdigest(),
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/hash_text", methods=["POST"])
def hash_text():
    text_input = request.form.get("text_input")
    if not text_input:
        flash("Please enter some text to hash!", "error")
        return redirect(url_for("index"))

    hashes = digest_all(text_input.encode())

    summary = text_input[:50] + ("..." if len(text_input) > 50 else "")
    for algorithm, hash_value in hashes.items():
        save_hash_result(
            input_type="text",
            input_value=summary,
            algorithm=algorithm,
            hash_result=hash_value,
        )

    return render_template(
        "results.html", input_type="Text", input_value=text_input, hashes=hashes
    )


@app.route("/hash_file", methods=["POST"])
def hash_file():
    file = request.files.get("file")
    if file is None or file.filename == "":
        flash("No file selected!", "error")
        return redirect(url_for("index"))

    try:
        hashes = digest_all(file.read())
    except Exception as e:
        flash(f"Error processing file: {str(e)}", "error")
        return redirect(url_for("index"))

    for algorithm, hash_value in hashes.items():
        save_hash_result(
            input_type="file",
            input_value=file.filename,
            algorithm=algorithm,
            hash_result=hash_value,
        )

    return render_template(
        "results.html", input_type="File", input_value=file.filename, hashes=hashes
    )


@app.route("/history")
def history():
    return render_template("history.html", history=get_hash_history())


@app.route("/api/hash", methods=["POST"])
def api_hash():
    try:
        data = request.json
        text_input = data.get("text")
        if not text_input:
            return jsonify({"error": "No text provided"}), 400

        hashes = {alg.lower().replace("-", ""): h for alg, h in digest_all(text_input.encode()).items()}
        return jsonify({"input": text_input, "hashes": hashes})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
