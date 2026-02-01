#import os
# app/main.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3

from app.scraper import scrape_trends
from app.llm_engine import summarize_trends
from app.semantic_search import semantic_search, CURRENCY_RATES
from app.database import init_db, add_user, get_user

# ✅ Create FastAPI app BEFORE using decorators
app = FastAPI(title="Data Driven Fashion Trend Aggregator")

# ✅ Templates directory
templates = Jinja2Templates(directory="app/templates")

# ✅ Initialize database
init_db()

# Helper: get last inserted user ID
def get_last_user_id():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT MAX(id) FROM users")
    user_id = c.fetchone()[0]
    conn.close()
    return user_id

# Homepage: scraped trends + AI summary
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    trends = scrape_trends()
    summary = summarize_trends(trends)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "trends": trends, "summary": summary}
    )

# Profile creation: includes gender + currency
@app.post("/create_profile", response_class=HTMLResponse)
def create_profile(
    request: Request,
    name: str = Form(...),
    gender: str = Form(...),
    style_pref: str = Form(...),
    budget: float = Form(...),
    currency: str = Form(...),
    occasion: str = Form(...)
):
    add_user(name, gender, style_pref, budget, currency, occasion)
    user_id = get_last_user_id()
    return templates.TemplateResponse(
        "profile_created.html",
        {"request": request, "name": name, "user_id": user_id}
    )

# Recommendations: filtered by gender, budget, currency, occasion
@app.get("/recommend/{user_id}", response_class=HTMLResponse)
def recommend(request: Request, user_id: int):
    user = get_user(user_id)
    if not user:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "message": "User not found"}
        )
    _, name, gender, style_pref, budget, currency, occasion = user
    results = semantic_search(
        style_pref,
        gender=gender,
        budget=budget,
        currency=currency,
        occasion=occasion
    )
    return templates.TemplateResponse(
        "recommend.html",
        {
            "request": request,
            "user": name,
            "recommendations": results,
            "currency": currency,
            "CURRENCY_RATES": CURRENCY_RATES   # ✅ Added this
        }
    )
#