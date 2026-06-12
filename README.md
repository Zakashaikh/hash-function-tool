# Hash Function Tool

A small Flask web app for generating and comparing cryptographic hashes
(MD5, SHA-1, SHA-256, SHA-512) of text and files, with an operation history
stored in SQLite and a JSON API.

I built this early in my MSc to get hands-on with hash functions, then came
back to it later and security-audited my own code. The fixes are in the
commit history — see [Self-audit](#self-audit) below.

## Run it

```bash
pip install -r requirements.txt
python app.py
# http://127.0.0.1:5000
```

## What it does

- **Hash text or files** — paste text or upload a file (16 MB cap), get all
  four digests with one-click copy.
- **Compare** — paste a known hash on the results page to verify integrity.
- **History** — every operation is stored in SQLite and filterable by
  algorithm, type, or content.
- **API** — `POST /api/hash` with `{"text": "..."}` returns all digests as JSON:

```bash
curl -X POST http://127.0.0.1:5000/api/hash \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World"}'
```

## Algorithm notes

| Algorithm | Bits | Status | Sensible use |
|-----------|------|--------|--------------|
| MD5 | 128 | broken (collisions) | non-security checksums only |
| SHA-1 | 160 | broken (collisions) | legacy comparison only |
| SHA-256 | 256 | current standard | integrity verification |
| SHA-512 | 512 | current standard | integrity verification |

MD5 and SHA-1 are included deliberately so the tool can verify checksums
published by older sources — not as an endorsement. None of these are
suitable for password storage; that needs a slow KDF (bcrypt, scrypt,
Argon2), which is a different problem than file integrity.

## Self-audit

After shipping the first version I reviewed it the way I'd review someone
else's code, and found four real issues:

1. **Hardcoded secret key** — a placeholder string committed to the repo.
   Now read from the `SECRET_KEY` environment variable.
2. **`debug=True` on `0.0.0.0`** — the Werkzeug debugger is remote code
   execution if it ever faces a network. Now loopback-only, debug off.
3. **Raw exception text returned to clients** — information disclosure.
   Error responses are now generic, and the API validates input properly.
4. **No upload size limit** — unbounded memory use per request. Capped at
   16 MB.

There was also a SQLite database committed to the repo (with the
`.gitignore` rule for it commented out) — runtime state doesn't belong in
version control.

What the first version got right: parameterized SQL throughout, and file
contents are hashed in memory, never executed or written to disk.

## Stack

Python 3.8+, Flask, SQLite, vanilla HTML/CSS/JS.
