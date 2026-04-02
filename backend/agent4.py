
# AGENT 4: Booking & Coordination Agent
# Confirms appointment + sends notifications
# Hybrid approach: Minimal LLM usage (only for message generation)

import json
import uuid
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

# ── In-memory stores (replace with real database later) ─────────────────────
BOOKINGS_DB = {}
NOTIFICATIONS_LOG = []


# ── Core Functions (Deterministic - No LLM) ─────────────────────────────────
def confirm_booking(provider_id: str, slot_id: str, tourist_name: str,
                    tourist_phone: str, tourist_email: str,
                    language_preference: str, symptoms: str,
                    severity_score: int) -> dict:
    
    booking_id = f"BK-{str(uuid.uuid4())[:8].upper()}"
    
    booking = {
        "id": booking_id,
        "provider_id": provider_id,
        "slot_id": slot_id,
        "tourist_name": tourist_name,
        "tourist_phone": tourist_phone,
        "tourist_email": tourist_email,
        "language_preference": language_preference,
        "symptoms": symptoms,
        "severity_score": severity_score,
        "status": "confirmed",
        "created_at": datetime.now().isoformat()
    }
    
    BOOKINGS_DB[booking_id] = booking
    print(f"✅ Booking confirmed: {booking_id}")
    return booking


def send_notification(channel: str, recipient: str, message: str, booking_id: str) -> dict:
    """Send notification and log it"""
    log_entry = {
        "id": f"NOTIF-{str(uuid.uuid4())[:6].upper()}",
        "channel": channel,
        "recipient": recipient,
        "message": message,
        "booking_id": booking_id,
        "sent_at": datetime.now().isoformat(),
        "status": "sent"
    }
    NOTIFICATIONS_LOG.append(log_entry)
    print(f"📨 Notification sent via {channel.upper()} to {recipient}")
    return log_entry


def check_booking_status(booking_id: str) -> dict:
    return BOOKINGS_DB.get(booking_id, {"error": f"Booking {booking_id} not found"})


# ── LLM Only for Message Generation ─────────────────────────────────────────
def generate_confirmation_message(matched_provider: dict, booking_id: str, 
                                  tourist_info: dict) -> str:
    """Use LLM ONLY to generate warm, natural confirmation message"""
    prompt = f"""
Write a short, warm, and reassuring appointment confirmation message in {tourist_info.get('language_preference', 'English')}.

Details:
- Tourist Name: {tourist_info.get('name')}
- Doctor: {matched_provider.get('provider_name')}
- Clinic/Hospital: {matched_provider.get('clinic_name')}
- Address: {matched_provider.get('address')}
- Date & Time: {matched_provider.get('slot_date')} at {matched_provider.get('slot_time')}
- Booking ID: {booking_id}

Rules:
- Keep it under 4 sentences
- Sound friendly and professional
- End with: "Please arrive 10 minutes early with valid ID and insurance card if applicable."
"""

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    except Exception as e:
        # Fallback message if LLM fails
        return f"Dear {tourist_info.get('name')}, your appointment with {matched_provider.get('provider_name')} " \
               f"at {matched_provider.get('clinic_name')} on {matched_provider.get('slot_date')} at " \
               f"{matched_provider.get('slot_time')} has been confirmed. Booking ID: {booking_id}. " \
               f"Please arrive 10 minutes early."


# ── Main Booking Agent (Hybrid - Lightweight) 
class BookingCoordinationAgent:
    def __init__(self):
        pass

    def book(self, matched_provider: dict, triage_result: dict, tourist_info: dict) -> dict:
        """
        Main booking function - Uses minimal LLM (only for message)
        """
        # Step 1: Confirm Booking (Deterministic)
        booking = confirm_booking(
            provider_id=matched_provider["provider_id"],
            slot_id=matched_provider["slot_id"],
            tourist_name=tourist_info["name"],
            tourist_phone=tourist_info.get("phone", ""),
            tourist_email=tourist_info.get("email", ""),
            language_preference=tourist_info.get("language_preference", "English"),
            symptoms=triage_result.get("translated_summary", ""),
            severity_score=triage_result.get("severity_score", 5)
        )

        booking_id = booking["id"]

        confirmation_message = generate_confirmation_message(
            matched_provider, booking_id, tourist_info
        )

        # Step 3: Send Notifications (Deterministic)
        notifications_sent = []
        
        if tourist_info.get("phone"):
            send_notification("sms", tourist_info["phone"], confirmation_message, booking_id)
            notifications_sent.append("sms")

        if tourist_info.get("email"):
            send_notification("email", tourist_info["email"], confirmation_message, booking_id)
            notifications_sent.append("email")

        # Step 4: Return clean result
        return {
            "booking_id": booking_id,
            "status": "confirmed",
            "doctor": matched_provider.get("provider_name"),
            "clinic": matched_provider.get("clinic_name"),
            "address": matched_provider.get("address"),
            "appointment_date": matched_provider.get("slot_date"),
            "appointment_time": matched_provider.get("slot_time"),
            "notifications_sent": notifications_sent,
            "confirmation_message": confirmation_message,
            "booking_details": booking
        }


# Test Entry Point 
if __name__ == "__main__":
    matched_provider = {
        "provider_id": "doc-001",
        "provider_name": "Dr. Priya Sharma",
        "clinic_name": "City Health Clinic",
        "address": "12 Park Street, Kolkata",
        "slot_id": "slot-101",
        "slot_date": "2025-08-05",
        "slot_time": "09:00 AM"
    }

    triage_result = {
        "severity_score": 6,
        "translated_summary": "Fever 102F, body ache, and cough for 2 days."
    }

    tourist_info = {
        "name": "John Smith",
        "language_preference": "English",
        "phone": "+91-9876543210",
        "email": "john.smith@email.com"
    }

    agent = BookingCoordinationAgent()
    result = agent.book(matched_provider, triage_result, tourist_info)

    print("\n" + "="*70)
    print("🎉 BOOKING SUCCESSFUL")
    print("="*70)
    print(json.dumps(result, indent=2))