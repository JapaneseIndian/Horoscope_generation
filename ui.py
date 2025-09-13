import streamlit as st
import requests
from datetime import datetime
import random
import os

st.set_page_config(
    page_title="Mystic Horoscope", 
    page_icon="🔮",
    layout="wide"
)

if 'current_prediction' not in st.session_state:
    st.session_state.current_prediction = None
if 'show_tarot' not in st.session_state:
    st.session_state.show_tarot = False
if 'tarot_reading' not in st.session_state:
    st.session_state.tarot_reading = None
if 'selected_sign' not in st.session_state:
    st.session_state.selected_sign = "Aries"

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5000")
zodiac = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]
CATEGORIES = ["love", "career", "health", "social life", "mind"]


st.markdown("""
    <style>
    .stApp {
        background-color: #0f0c29;
        color: white;
    }
    .stButton>button {
        background-color: #4a148c;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #7b1fa2;
        color: white;
    }
    .stSelectbox>div>div>select {
        background-color: #1a1a2e;
        color: white;
    }
    .horoscope-card {
        background-color: #1a1a2e;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #4a148c;
    }
    .tarot-card {
        background-color: #1a1a2e;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #7b1fa2;
    }
    .error-card {
        background-color: #3a1a1a;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #ff4d4d;
    }
    </style>
    """, unsafe_allow_html=True)

def display_error(message):
    """Display an error message in a styled card"""
    st.markdown(f"""
    <div class='error-card'>
        <h4>🔮 Cosmic Connection Error</h4>
        <p>{message}</p>
    </div>
    """, unsafe_allow_html=True)

def ensure_string(data):
    """Ensure the data is a string, converting if necessary"""
    if isinstance(data, str):
        return data
    elif isinstance(data, dict):
        return data.get('text', str(data))
    elif hasattr(data, 'content'):
        return str(data.content)
    return str(data)

def safe_get(data, key, default="Unknown"):
    """Safely get a value from data, handling both dict and string cases"""
    if isinstance(data, dict):
        return data.get(key, default)
    elif isinstance(data, str):
        return data if key == 'reading' else default
    return default

def main():
    st.title("✨ Mystic Horoscope Reader")
    
    tab1, tab2, tab3 = st.tabs(["🔮 Daily Horoscope", "📚 Saved Predictions", "🃏 Tarot Reading"])
    
    with tab1:
        st.header("Your Daily Cosmic Guidance")
        
        cols = st.columns(4)
        for i, sign in enumerate(zodiac):
            with cols[i % 4]:
                if st.button(sign):
                    st.session_state.selected_sign = sign
                    st.rerun()
        
        st.subheader(f"Selected: {st.session_state.selected_sign}")
        

        category = st.selectbox("Select Category", CATEGORIES)
        

        if st.button("Get Your Horoscope", type="primary"):
            try:
                with st.spinner("Consulting the stars..."):
                    response = requests.get(
                        f"{BACKEND_URL}/horoscope",
                        params={
                            "sign": st.session_state.selected_sign,
                            "category": category
                        },
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        if data.get("status") == "error":
                            display_error(data.get("message", "The stars are not aligned properly today."))
                        else:
                            prediction_text = ensure_string(data["prediction"])
                            
                            st.session_state.current_prediction = {
                                "sign": st.session_state.selected_sign,
                                "prediction": prediction_text,
                                "category": category,
                                "date": data.get("date", datetime.now().strftime("%Y-%m-%d")),
                                "lucky_number": data.get("lucky_number", random.randint(1, 100))
                            }
                            st.session_state.show_tarot = True
                            st.rerun()
                    else:
                        error_data = response.json() if response.content else {}
                        display_error(error_data.get("error", "Failed to connect with the cosmic realm. Please try again."))
            
            except requests.exceptions.RequestException as e:
                display_error(f"Celestial connection failed: {str(e)}")
        

        if st.session_state.current_prediction:
            st.markdown(f"""
            <div class='horoscope-card'>
                <h3>{st.session_state.current_prediction['category'].capitalize()} Horoscope</h3>
                <p>{st.session_state.current_prediction['prediction']}</p>
                <div style='display: flex; gap: 20px; margin-top: 15px;'>
                    <div><b>Lucky Number:</b> {st.session_state.current_prediction['lucky_number']}</div>
                    <div><b>Date:</b> {st.session_state.current_prediction['date']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Save This Prediction"):
                try:
                    with st.spinner("Saving to your cosmic journal..."):
                        save_response = requests.post(
                            f"{BACKEND_URL}/horoscope/save",
                            json={
                                "sign": st.session_state.selected_sign,
                                "prediction": st.session_state.current_prediction["prediction"],
                                "category": category
                            },
                            timeout=10
                        )
                    
                    if save_response.status_code == 201:
                        st.success("Prediction saved in the stars!")
                    else:
                        error_data = save_response.json() if save_response.content else {}
                        display_error(error_data.get("error", "Failed to save your prediction"))
                
                except requests.exceptions.RequestException as e:
                    display_error(f"Failed to connect with the cosmic archive: {str(e)}")
            
            if st.session_state.show_tarot and st.button("Get Tarot Reading"):
                try:
                    with st.spinner("Shuffling the cards..."):
                        tarot_response = requests.get(
                            f"{BACKEND_URL}/tarot/daily",
                            params={"sign": st.session_state.selected_sign},
                            timeout=10
                        )
                        
                        if tarot_response.status_code == 200:
                            st.session_state.tarot_reading = tarot_response.json()
                            st.rerun()
                        else:
                            error_data = tarot_response.json() if tarot_response.content else {}
                            display_error(error_data.get("error", "The tarot cards refused to reveal themselves"))
                
                except requests.exceptions.RequestException as e:
                    display_error(f"The tarot deck is unavailable: {str(e)}")
    
    with tab2:
        st.header("Your Saved Predictions")
        
        try:
            with st.spinner("Consulting your cosmic archive..."):
                response = requests.get(f"{BACKEND_URL}/horoscope/saved", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if not data or data.get("count", 0) == 0:
                    st.info("No saved predictions yet. Your cosmic journal is empty.")
                else:
                    for pred in data.get("horoscopes", []):
                        with st.expander(f"{pred.get('sign', 'Unknown')} - {pred.get('category', 'general').capitalize()} - {pred.get('saved_at', 'No date')}"):
                            st.markdown(f"""
                            <div style='background-color: #1a1a2e; padding: 15px; border-radius: 5px;'>
                                {ensure_string(pred.get("prediction", "No prediction text"))}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button(f"Delete", key=f"delete_{pred.get('id', '0')}"):
                                try:
                                    del_response = requests.delete(
                                        f"{BACKEND_URL}/horoscope/delete/{pred.get('id', '0')}",
                                        timeout=10
                                    )
                                    if del_response.status_code == 200:
                                        st.success("Prediction vanished into the cosmos!")
                                        st.rerun()
                                    else:
                                        error_data = del_response.json() if del_response.content else {}
                                        display_error(error_data.get("error", "Failed to erase from the cosmic records"))
                                except requests.exceptions.RequestException as e:
                                    display_error(f"Cosmic deletion failed: {str(e)}")
            else:
                error_data = response.json() if response.content else {}
                display_error(error_data.get("error", "Failed to access your cosmic journal"))
        
        except requests.exceptions.RequestException as e:
            display_error(f"Cosmic archive unavailable: {str(e)}")
    
    with tab3:
        st.header("Daily Tarot Reading")
        
        if st.session_state.tarot_reading:
            reading = st.session_state.tarot_reading
            
            if "error" in reading:
                display_error(reading["error"])
                if st.button("Try Again"):
                    st.session_state.tarot_reading = None
                    st.rerun()
            else:
                sign = safe_get(reading, 'sign', st.session_state.selected_sign)
                st.subheader(f"Reading for {sign}")
                
                cards = safe_get(reading, 'cards', [])
                if cards and isinstance(cards, list) and len(cards) > 0:
                    st.subheader("Your Cards")
                    cols = st.columns(min(3, len(cards)))
                    for i, card in enumerate(cards):
                        with cols[i % 3]:
                            if isinstance(card, dict):
                                st.markdown(f"""
                                <div class='tarot-card'>
                                    <h4>{card.get('name', 'Mystery Card')}</h4>
                                    <p><em>{card.get('meaning_up', 'The cards are silent')}</em></p>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                <div class='tarot-card'>
                                    <h4>Mystery Card</h4>
                                    <p><em>{str(card)}</em></p>
                                </div>
                                """, unsafe_allow_html=True)
                
                reading_text = safe_get(reading, 'reading', 'No reading available')
                st.markdown(f"""
                <div class='horoscope-card'>
                    <h3>Your Reading</h3>
                    {reading_text}
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Get New Reading"):
                    st.session_state.tarot_reading = None
                    st.rerun()
        else:
            st.info("Get a tarot reading from the horoscope page or select a sign below")
            
            sign = st.selectbox("Select Sign", zodiac, key="tarot_sign")
            if st.button("Get Tarot Reading", key="tarot_button"):
                try:
                    with st.spinner("The cards are whispering..."):
                        response = requests.get(
                            f"{BACKEND_URL}/tarot/daily",
                            params={"sign": sign},
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            st.session_state.tarot_reading = response.json()
                            st.rerun()
                        else:
                            error_data = response.json() if response.content else {}
                            display_error(error_data.get("error", "The cards refused to reveal themselves"))
                
                except requests.exceptions.RequestException as e:
                    display_error(f"The tarot deck is unavailable: {str(e)}")

if __name__ == "__main__":
    main()
