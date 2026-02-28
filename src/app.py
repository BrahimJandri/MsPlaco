from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, g
from flask_mail import Mail, Message
from dotenv import load_dotenv
from functools import wraps
import os
import re
import json
import requests as http_requests
from datetime import datetime
from pathlib import Path

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-secret-key")

SUPPORTED_LANGS = ("fr", "ar")


@app.before_request
def set_lang():
    g.lang = session.get("lang", "fr")


@app.route("/set-lang/<lang>")
def set_language(lang):
    if lang in SUPPORTED_LANGS:
        session["lang"] = lang
    return redirect(request.referrer or url_for("home"))


# ── MAIL CONFIG
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")

mail = Mail(app)

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
QUOTES_FILE = Path("data/quotes.json")
QUOTES_FILE.parent.mkdir(exist_ok=True)

# ── CALLMEBOT WHATSAPP CONFIG
# Your WhatsApp number (e.g. +212659715906)
CALLMEBOT_PHONE = os.getenv("CALLMEBOT_PHONE")
# API key received from CallMeBot
CALLMEBOT_APIKEY = os.getenv("CALLMEBOT_APIKEY")


def send_whatsapp_notification(first_name, last_name, email, phone, project, description, date):
    """Send a WhatsApp message via CallMeBot when a new quote is received."""
    if not CALLMEBOT_PHONE or not CALLMEBOT_APIKEY:
        print(
            "[WHATSAPP] Skipped – missing config (CALLMEBOT_PHONE or CALLMEBOT_APIKEY)")
        return

    message = (
        f"📩 *Nouveau devis MsPlaco*\n"
        f"──────────────────\n"
        f"*Nom :* {first_name} {last_name}\n"
        f"*Email :* {email}\n"
        f"*Tel :* {phone}\n"
        f"*Projet :* {project}\n"
        f"*Date :* {date}\n"
        f"──────────────────\n"
        f"*Description :*\n{description}"
    )
    try:
        resp = http_requests.get(
            "https://api.callmebot.com/whatsapp.php",
            params={
                "phone": CALLMEBOT_PHONE,
                "text": message,
                "apikey": CALLMEBOT_APIKEY,
            },
            timeout=15,
        )
        resp.raise_for_status()
        print(f"[WHATSAPP] Message sent successfully to {CALLMEBOT_PHONE}")
    except Exception as e:
        print(f"[WHATSAPP ERROR] {e}")


def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def load_quotes():
    if not QUOTES_FILE.exists():
        return []
    try:
        return json.loads(QUOTES_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def save_quotes(quotes):
    QUOTES_FILE.write_text(json.dumps(
        quotes, ensure_ascii=False, indent=2), encoding="utf-8")


def next_id(quotes):
    return max((q["id"] for q in quotes), default=0) + 1


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated

# ── PUBLIC ROUTES


@app.route("/")
def home():
    if g.lang == "ar":
        return render_template("index_ar.html")
    return render_template("index.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

# ── CONTACT FORM


@app.route("/send-contact", methods=["POST"])
def send_contact():
    first_name = request.form.get("first_name",  "").strip()
    last_name = request.form.get("last_name",   "").strip()
    email = request.form.get("email",       "").strip()
    phone = request.form.get("phone",       "").strip() or "Non renseigne"
    project = request.form.get("project",     "").strip()
    description = request.form.get("description", "").strip()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    errors = []
    if not first_name:
        errors.append("Le prenom est obligatoire.")
    if not last_name:
        errors.append("Le nom est obligatoire.")
    if not email or not is_valid_email(email):
        errors.append("Email invalide.")
    if not description:
        errors.append("Veuillez decrire votre projet.")
    if errors:
        if is_ajax:
            return jsonify({"success": False, "errors": errors}), 400
        return redirect(url_for("home") + "#contact")

    quotes = load_quotes()
    quote = {
        "id": next_id(quotes),
        "first_name": first_name,
        "last_name":  last_name,
        "email":      email,
        "phone":      phone,
        "project":    project,
        "description": description,
        "date":       now,
        "status":     "new"
    }
    quotes.insert(0, quote)
    save_quotes(quotes)

    owner_email = os.getenv("OWNER_EMAIL", os.getenv("MAIL_USERNAME"))
    try:
        mail.send(Message(
            subject=f"[MsPlaco] Nouveau devis - {first_name} {last_name}",
            recipients=[owner_email],
            body=f"Nouveau devis de {first_name} {last_name}\nEmail: {email}\nTel: {phone}\nProjet: {project}\nDate: {now}\n\n{description}",
            reply_to=email
        ))
        mail.send(Message(
            subject="MsPlaco - Votre demande de devis a bien ete recue",
            recipients=[email],
            body=f"Bonjour {first_name},\n\nMerci pour votre demande. Nous vous repondrons sous 24h.\n\nProjet: {project}\n\nL'equipe MsPlaco"
        ))
    except Exception as e:
        print(f"[MAIL ERROR] {e}")

    # Send WhatsApp notification
    send_whatsapp_notification(
        first_name, last_name, email, phone, project, description, now)

    if is_ajax:
        return jsonify({"success": True, "message": "Votre demande a bien ete envoyee ! Nous vous repondrons sous 24h."})
    flash("Votre demande a bien ete envoyee !", "success")
    return redirect(url_for("home") + "#contact")

# ── ADMIN ROUTES


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        error = "Mot de passe incorrect."
    return render_template("admin_login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))


@app.route("/admin")
@admin_required
def admin_dashboard():
    return render_template("admin.html")


@app.route("/api/quotes")
@admin_required
def api_quotes():
    return jsonify(load_quotes())


@app.route("/api/quotes/<int:qid>/status", methods=["PATCH"])
@admin_required
def api_update_status(qid):
    status = request.json.get("status")
    if status not in ("new", "progress", "done", "archive"):
        return jsonify({"error": "Invalid status"}), 400
    quotes = load_quotes()
    for q in quotes:
        if q["id"] == qid:
            q["status"] = status
            save_quotes(quotes)
            return jsonify({"success": True, "quote": q})
    return jsonify({"error": "Not found"}), 404


@app.route("/api/quotes/<int:qid>", methods=["DELETE"])
@admin_required
def api_delete_quote(qid):
    quotes = [q for q in load_quotes() if q["id"] != qid]
    save_quotes(quotes)
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
