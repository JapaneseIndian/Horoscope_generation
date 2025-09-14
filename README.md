# 🔮Horoscope App

A full-stack web application that provides AI-powered horoscope predictions and tarot card readings based on zodiac signs. Built with Flask backend and Streamlit frontend.

## Overview
This project is a Horoscope Generator API that provides daily horoscopes for all zodiac signs. The API is built with Flask (backend) and Streamlit (frontend), offering features to view, save, and manage your daily horoscopes.

## Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd Backend 
   ```

2. Create `.env` file:
   ```env
   GOOGLE_API_KEY=your_key_here
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
   
## Frontend Setup
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd Frontend
   ```
2. Run the Streamlit application:
   ```bash
   streamlit run ui.py
   ```

## 🏗️ Architecture
```
horoscope/
├── Backend/
│   ├── app.py                 # Flask application with all API endpoints
│   ├── horoscope_data.json    # Database for saved predictions
│   ├── tarot_cards.json       # Tarot card definitions and meanings
│   └── requirements.txt       # Python dependencies
├── Frontend/
│   └── app.py                # Streamlit frontend application
└── README.md
```

## Features
* Personalized Horoscopes: Get daily horoscopes for all 12 zodiac signs across multiple categories (love, career, health, etc.)

* AI-Powered Predictions: Uses Google's Gemini AI with RAG (Retrieval Augmented Generation) for accurate astrological insights

* Tarot Card Readings: Receive mystical tarot card interpretations tailored to your zodiac sign

* Tarot Card Readings: Receive mystical tarot card interpretations tailored to your zodiac sign

## Horoscope Endpoints
* GET /horoscope?sign=<sign>&category=<category> - Get a horoscope for a specific sign and category

* POST /horoscope/save - Save a horoscope prediction

* GET /horoscope/saved - Retrieve all saved predictions

* DELETE /horoscope/delete/<id> - Delete a saved prediction

## Taror Endpoints
* GET /tarot/daily?sign=<sign> - Get a daily tarot reading for a specific sign

* GET /horoscope/tarot?sign=<sign>&category=<category> - Get combined horoscope and tarot reading

## 🐛 Troubleshooting
### Common Issues
1. API Key Errors: Ensure your Google API key is valid and properly set in the .env file

2. Connection Errors: Verify the backend is running before starting the frontend

3. Module Not Found: Ensure all dependencies are installed from requirements.txt

