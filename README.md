# Horoscope App

🔮 This is a Streamlit frontend with Flask backend for horoscope predictions

## Overview
This project is a Horoscope Generator API that provides daily horoscopes for all zodiac signs. The API is built with Flask (backend) and Streamlit (frontend), offering features to view, save, and manage your daily horoscopes.

## Setup
1. Create virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r Backend/requirements.txt
   pip install streamlit
   ```

3. Create `.env` file:
   ```env
   GOOGLE_API_KEY=your_key_here
   ```

## Running
```bash
# Terminal 1 (Backend)
cd Backend
flask run

# Terminal 2 (Frontend)
streamlit run Frontend/ui.py
```
## Features
* Daily Horoscope: Get today's horoscope for any zodiac sign

* Save Horoscopes: Save your favorite horoscopes for later viewing

* Manage Saved Horoscopes: View and delete previously saved horoscopes

* User-Friendly Interface: Clean and intuitive Streamlit web interface

  ## API Endpoints
* GET /horoscope/<sign> - Get today's horoscope for a specific zodiac sign

* POST /save_horoscope - Save a horoscope (requires JSON payload)

* GET /saved_horoscopes - Get all saved horoscopes

* DELETE /delete_horoscope/<id> - Delete a saved horoscope by ID
