# StayXB: AI Hotel Booking Assistant

A chat and voice hotel concierge that helps guests find a room, book it, pay and manage the booking. Includes customer accounts and a manager dashboard.

> Portfolio project. Hotels, addresses and photos are fictional (photos are AI-generated). Payments run in demo mode unless Razorpay keys are added.

## Features
- **AI concierge (Riya):** asks questions one by one, answers FAQs (offers, rooms, area), understands English and Hinglish, and uses Claude for open questions. The server, not the AI, decides prices, rooms and booking IDs.
- **Booking flow:** hotel details and live vacancy, 3 room picks, add-ons, coupon, guest details, review, payment, confirmation.
- **Accounts:** sign up, sign in, forgot-password email (Supabase Auth). Guests can book without an account and look up bookings with their mobile number (masked details).
- **No double booking:** a database primary key on (hotel, room, night) blocks two people taking the same room; unpaid holds expire after 10 minutes.
- **Payments:** Razorpay (UPI, cards, net banking) with signature check and webhook, or free demo mode with no keys.
- **Manager dashboard (admin role only):** KPIs, charts, room map (free/booked/maintenance), booking search, CSV export.
- **Voice input and replies** using the browser speech features.

## Tech stack
| Layer | Tools |
|---|---|
| Frontend | HTML, CSS, JavaScript (single file), Supabase JS |
| Backend | Python, FastAPI |
| Database and auth | Supabase (PostgreSQL, Row Level Security, Auth) |
| Payments | Razorpay (optional) |
| AI | Anthropic Claude API (server side) |
| Hosting | Render |

## Project structure
```
stayxb/
  backend/
    main.py        API: auth, bookings, payments, chat, admin
    engine.py      price and room availability rules
    schema.sql     database tables and security rules
    static/index.html   the website (served by FastAPI)
  DEPLOY.md        step by step hosting guide
```

## Run locally
```
cd backend
pip install -r requirements.txt
cp .env.example .env      # fill in your own values
uvicorn main:app --reload
```
Open http://localhost:8000

## Security
Secrets live only in environment variables (`.env` is git-ignored). The browser only gets the public Supabase key. Prices and availability are checked on the server.

## Limitations
Mobile-only lookup should get SMS OTP for stronger privacy. Demo data and fictional hotels.
