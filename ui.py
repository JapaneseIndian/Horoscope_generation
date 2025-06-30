import streamlit as st
import requests
from datetime import datetime

if 'current_prediction' not in st.session_state:
    st.session_state.current_prediction = None

URL = "http://127.0.0.1:5000/"
zodiac = [
    "Aries", "Taurus", "Gemini", "Cancer", "Scorpio", "Leo", 
    "Pisces", "Libra", "Virgo", "Aquarius", "Sagittarius", "Capricorn"
]
CATEGORIES = ["love", "career", "health", "social life", "mind"]

def main():
    st.set_page_config(page_title="Horoscope App", page_icon="🔮")
    st.title("🔮 Mystic Horoscope Reader")
    
    tab1, tab2 = st.tabs(["Get Prediction", "Saved Predictions"])
    
    with tab1:
        st.header("Get Your Horoscope")
        
        col1, col2 = st.columns(2)
        with col1:
            sign = st.selectbox("Your Zodiac Sign", zodiac)
        with col2:
            category = st.selectbox("Category", CATEGORIES)
        
        if st.button("Get Prediction", type="primary"):
            try:
                with st.spinner("Fetching your horoscope..."):
                    response = requests.get(
                        f"{URL}/horoscope",
                        params={"sign": sign, "category": category},
                        timeout=10
                    )
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("✨ Here's your horoscope reading:")
                    st.subheader(f"{sign} - {category.capitalize()}")
                    
                    prediction_text = ""
                    if isinstance(data["prediction"], str):
                        prediction_text = data["prediction"]
                    elif isinstance(data["prediction"], dict):
                        prediction_text = data["prediction"].get('text', 
                                           data["prediction"].get('content', 
                                           str(data["prediction"])))
                    else:
                        prediction_text = str(data["prediction"])
                    
                    st.write(prediction_text)
                    
                    if "lucky_number" in data and "date" in data:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Lucky Number", data["lucky_number"])
                        with col2:
                            st.metric("Date", data["date"])
                    
                    st.session_state.current_prediction = {
                        "sign": sign,
                        "prediction": prediction_text,
                        "category": category
                    }
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")
        
        if st.session_state.current_prediction is not None:
            if st.button("Save This Prediction"):
                try:
                    with st.spinner("Saving prediction..."):
                        save_response = requests.post(
                            f"{URL}/horoscope/save",
                            json=st.session_state.current_prediction,
                            timeout=10
                        )
                    
                    if save_response.status_code == 201:
                        st.success("Prediction saved permanently!")
                        st.session_state.current_prediction = None
                        st.rerun()
                    else:
                        st.error(f"Failed to save. Status code: {save_response.status_code}")
                
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection error: {str(e)}")
    
    with tab2:
        st.header("Your Saved Predictions")
        
        try:
            with st.spinner("Loading saved predictions..."):
                response = requests.get(f"{URL}/horoscope/saved", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if not data or data.get("count", 0) == 0:
                    st.info("No saved predictions yet. Get a prediction and save it!")
                else:
                    st.subheader(f"Total Saved Predictions: {data.get('count', 0)}")
                    
                    for pred in data.get("horoscopes", []):
                        with st.expander(f"{pred.get('sign', 'Unknown')} - {pred.get('category', 'general').capitalize()}"):
                            st.write(pred.get("prediction", "No prediction text"))
                            if 'saved_at' in pred:
                                st.caption(f"Saved on: {pred['saved_at']}")
                            
                            if st.button(f"Delete", key=f"delete_{pred.get('id', '0')}"):
                                try:
                                    del_response = requests.delete(
                                        f"{URL}/horoscope/delete/{pred.get('id', '0')}",
                                        timeout=10
                                    )
                                    if del_response.status_code == 200:
                                        st.rerun()  
                                    else:
                                        st.error("Failed to delete prediction")
                                except requests.exceptions.RequestException as e:
                                    st.error(f"Connection error: {str(e)}")
            else:
                st.error(f"Error fetching saved predictions: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {str(e)}")

if __name__ == "__main__":
    main()
