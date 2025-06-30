from flask import Flask, request, jsonify
from dotenv import load_dotenv
from datetime import datetime
import random as r
from pathlib import Path
from flask_cors import CORS
import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
import google.generativeai as genai

app = Flask(__name__)
CORS(app)
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)
DATA_FILE = "horoscope_data.json"

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY") 
)

embed = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

vector_path_store="horo_vectors"
if not os.path.exists(vector_path_store):
    astro_knowledge = [
        "Aries (March 21-April 19) are known for their fiery energy and leadership qualities.",
        "Taurus (April 20-May 20) values stability and sensual pleasures.",
        "Gemini (May 21-June 20) are communicative and adaptable air signs.",
        "Cancer (June 21-July 22) are nurturing water signs deeply connected to emotions.",
        "Leo (July 23-August 22) are confident fire signs that crave attention.",
        "Virgo (August 23-September 22) are analytical earth signs focused on details.",
        "Libra (September 23-October 22) seek balance and harmony in relationships.",
        "Scorpio (October 23-November 21) are intense water signs with transformative energy.",
        "Sagittarius (November 22-December 21) are adventurous fire signs seeking truth.",
        "Capricorn (December 22-January 19) are disciplined earth signs focused on goals.",
        "Aquarius (January 20-February 18) are innovative air signs with humanitarian ideals.",
        "Pisces (February 19-March 20) are compassionate water signs with strong intuition.",
        "Mercury retrograde periods often cause communication challenges for all signs.",
        "Venus governs love and beauty, influencing relationships when it transits signs.",
        "Mars energizes action and passion, affecting motivation in different zodiac signs."
    ]
    vector_store=FAISS.from_texts(astro_knowledge,embedding=embed)
    vector_store.save_local(vector_path_store)
else:
    vector_store=FAISS.load_local(vector_path_store,embed,allow_dangerous_deserialization=True)

RAG_PROMPT = ChatPromptTemplate.from_messages([
    SystemMessage(content="""You are a mystical astrologer. Generate horoscopes by combining:
    - The user's zodiac sign characteristics
    - Current astrological transits and aspects
    - General astrological knowledge
    - The specific category requested
    
    Make it 3-4 sentences, poetic but not vague. Include astrological terminology where appropriate."""),
    ("human", """Context information:
    {context}

    Generate a {category} horoscope for {sign} today ({current_date}).
    Tone: {tone}""")
])

def format_docs(docs):
    """Properly format retrieved documents for context"""
    if not docs:
        return "No astrological context available"
    try:
        if hasattr(docs[0], 'page_content'):  
            return "\n\n".join(doc.page_content for doc in docs)
        elif isinstance(docs[0], str): 
            return "\n\n".join(docs)
        else:  
            return str(docs)
    except Exception as e:
        print(f"Error formatting docs: {e}")
        return "Astrological context currently unavailable"

retriever=vector_store.as_retriever(search_kwargs={"k":3})
ragchain=(
    {"context": retriever | format_docs, 
     "sign": RunnablePassthrough(),
     "category": RunnablePassthrough(),
     "current_date": RunnablePassthrough(),
     "tone": RunnablePassthrough()}
    | RAG_PROMPT
    | llm
    | StrOutputParser()
)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"savedscope": [], "next_id": 1}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

zodiac = ["Aries","Taurus","Gemini","Cancer","Scorpio","Leo","Pisces","Libra","Virgo","Aquarius","Sagittarius","Capricorn"]

def generate(sign: str, category: str) -> str:
    """Generate a horoscope using RAG with Gemini"""
    try:
        formatted_prompt = RAG_PROMPT.format(
            context=format_docs(retriever.invoke(sign)),
            sign=sign,
            category=category,
            current_date=datetime.now().strftime("%Y-%m-%d"),
            tone="mystical, soothing and magical"
        )
        response = llm.invoke(formatted_prompt)
        
        if hasattr(response, 'content'):
            return response.content
        elif isinstance(response, dict):
            return response.get('text', str(response))
        return str(response)
        
    except Exception as e:
        error_msg = f"The stars are not aligned properly today. (Error: {str(e)})"
        print(f"Generation Error: {error_msg}")
        return error_msg

@app.route('/horoscope', methods=['GET'])
def horoscope():
    sign = request.args.get('sign', '').capitalize()
    category = request.args.get('category', 'career').lower()
    
    if not sign or sign not in zodiac:
        return jsonify({
            "error": "Please provide a valid zodiac sign",
            "valid_signs": zodiac
        }), 400
    
    try:
        prediction = generate(sign, category)
        return jsonify({
            "sign": sign,
            "category": category,
            "prediction": prediction,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "lucky_number": r.randint(1, 100)
        })
    except Exception as e:
        return jsonify({
            "error": "Our celestial connection failed",
            "details": str(e)
        }), 500

@app.route('/horoscope/save', methods=['POST'])
def save_horoscope():
    data = request.get_json()
    if not data or 'prediction' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    db = load_data()
    new_entry = {
        "id": db["next_id"],
        "sign": data["sign"],
        "prediction": data["prediction"],
        "category": data.get("category", "general"),
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    db["savedscope"].append(new_entry)
    db["next_id"] += 1
    save_data(db)
    
    return jsonify(new_entry), 201
@app.route('/horoscope/delete/<int:pred_id>', methods=['DELETE'])
def delete_horoscope(pred_id):
    db = load_data()
    for i, pred in enumerate(db["savedscope"]):
        if pred["id"] == pred_id:
            db["savedscope"].pop(i)
            save_data(db)
            return jsonify({"message": "Prediction deleted"}), 200
    
    return jsonify({"error": "Prediction not found"}), 404
@app.route('/horoscope/saved', methods=['GET'])
def list_saved():
    db = load_data()
    return jsonify({
        "count": len(db["savedscope"]),
        "horoscopes": db["savedscope"]
    })


if __name__ == '__main__':
    app.run(debug=True)
