"""APEX Digital — FastAPI Backend.

Complete REST API for the AI-powered marketing agency.
Uses Kimi API (OpenAI-compatible) for AI agent operations.
"""
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date, datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
import uuid
import logging

from database import get_db, engine, Base
from config import get_settings

# Create tables on startup
Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="APEX Digital API",
    version="2.0.0",
    description="AI-Powered Digital Marketing Agency Backend",
)

# CORS — allow all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = get_settings()

@app.get("/")
def root():
    return {"message": "APEX Digital API", "version": "2.0.0", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now()}

# Contact Form Endpoint
class ContactForm(BaseModel):
    name: str
    email: str
    company: Optional[str] = None
    phone: Optional[str] = None
    message: str
    service_interest: Optional[str] = None
    industry: Optional[str] = None

@app.post("/contact-form")
def submit_contact_form(form: ContactForm):
    """Receive contact form submission and notify via Telegram"""
    import requests
    
    BOT_TOKEN = '7989235077:AAGtunw3F9RbJHc2rTnlY2idE9wW1yJBNhA'
    CHAT_ID = '627288703'
    
    message = f"""🚨 NEW LEAD FROM WEBSITE!

👤 Name: {form.name}
📧 Email: {form.email}
🏢 Company: {form.company or 'N/A'}
📱 Phone: {form.phone or 'N/A'}
🎯 Service: {form.service_interest or 'Not specified'}
🏭 Industry: {form.industry or 'Not specified'}

💬 Message:
{form.message or 'No message'}

🔗 Respond ASAP!"""
    
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'HTML'}
    
    try:
        response = requests.post(url, data=data, timeout=10); logger.info(f"Telegram status: {response.status_code}")
    except Exception as e:
        logger.error(f"Telegram error: {e}")
    
    return {'success': True, 'message': 'Thank you! We will contact you soon.'}

@app.get("/contact-form")
def contact_form_options():
    """CORS preflight support"""
    return {'status': 'ok'}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Booking endpoint
class BookingRequest(BaseModel):
    name: str
    email: str
    company: Optional[str] = None
    slot: str

@app.post("/booking")
def create_booking(booking: BookingRequest):
    """Handle booking request and notify via Telegram"""
    import requests
    
    BOT_TOKEN = '7989235077:AAGtunw3F9RbJHc2rTnlY2idE9wW1yJBNhA'
    CHAT_ID = '627288703'
    
    message = f"""📅 NEW BOOKING REQUEST!

👤 Name: {booking.name}
📧 Email: {booking.email}
🏢 Company: {booking.company or 'N/A'}
⏰ Slot: {booking.slot}

🔗 Book this in your calendar!"""
    
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'HTML'}
    
    try:
        response = requests.post(url, data=data, timeout=10); logger.info(f"Telegram status: {response.status_code}")
    except Exception as e:
        logger.error(f"Telegram error: {e}")
    
    return {'success': True, 'message': 'Booking request received!'}
