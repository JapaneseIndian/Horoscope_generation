# Horoscope App

🔮 This is a Streamlit frontend with Flask backend for horoscope predictions

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
