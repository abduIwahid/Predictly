import os
import random
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import google.generativeai as genai
import PIL.Image
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def mock_pakistan_price(city, area_marla, property_type, bedrooms, bathrooms, amenities):
    # Dummy average price per marla in PKR (Millions)
    city_rates = {
        'Lahore': 2.5,
        'Karachi': 3.0,
        'Islamabad': 3.5,
        'Rawalpindi': 2.0,
        'Faisalabad': 1.5,
        'Multan': 1.2
    }
    
    rate = city_rates.get(city, 2.0)
    base = area_marla * rate
    
    # Adjustments
    if property_type == 'House':
        base *= 1.2
    elif property_type == 'Farm House':
        base *= 1.5
        
    base += (bedrooms * 0.2) + (bathrooms * 0.1)
    
    # Amenities adjustments
    if 'gated' in amenities:
        base *= 1.05
    if 'metro' in amenities:
        base *= 1.02
    if 'commercial' in amenities:
        base *= 1.03
        
    return base * 1000000 # Return in actual PKR

def analyze_image_with_gemini(filepath):
    try:
        # Mocking the AI response for demonstration
        descriptions = [
            "AI detected a modern 2-story house with a premium exterior and good maintenance.",
            "AI detected a standard single-story property with average exterior condition.",
            "AI detected a luxury multi-level estate with high-end finishing."
        ]
        
        desc = random.choice(descriptions)
        
        if "luxury" in desc:
            adj = 1.20
        elif "modern" in desc:
            adj = 1.10
        else:
            adj = 1.00
            
        return desc, adj
    except Exception as e:
        return "AI analysis unavailable.", 1.0

def format_pkr(amount):
    return "{:,.0f}".format(amount)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    try:
        # Simulate AI processing delay so the loading spinner is visible
        time.sleep(1.5)
        
        city = request.form.get('city')
        area_marla = float(request.form.get('area_marla', 0))
        property_type = request.form.get('property_type')
        bedrooms = int(request.form.get('bedrooms', 0))
        bathrooms = int(request.form.get('bathrooms', 0))
        
        # Amenities
        amenities = []
        if request.form.get('amenity_gated'): amenities.append('gated')
        if request.form.get('amenity_metro'): amenities.append('metro')
        if request.form.get('amenity_commercial'): amenities.append('commercial')

        if area_marla <= 0:
            return render_template('index.html', error="Area must be greater than 0.")

        base_price = mock_pakistan_price(city, area_marla, property_type, bedrooms, bathrooms, amenities)
        
        image_adjustment = 0
        uploaded_image_path = None
        ai_description = None
        
        if 'house_image' in request.files:
            file = request.files['house_image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                uploaded_image_path = f"uploads/{filename}"
                
                # Fetch info using AI
                ai_description, multiplier = analyze_image_with_gemini(filepath)
                image_adjustment = base_price * (multiplier - 1)
        
        final_price = base_price + image_adjustment
        
        breakdown = {
            'city': city,
            'base': format_pkr(base_price),
            'image_adj': format_pkr(image_adjustment),
            'total': format_pkr(final_price),
            'raw_total': final_price # useful for JS calculations
        }
        
        return render_template('index.html', 
                               results=format_pkr(final_price), 
                               breakdown=breakdown, 
                               image_path=uploaded_image_path,
                               ai_description=ai_description,
                               selected_city=city,
                               selected_area=area_marla)

    except Exception as e:
        return render_template('index.html', error=f"An error occurred: {str(e)}")
   

if __name__ == "__main__":
    app.run(debug=True)
