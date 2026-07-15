import os
import statistics
import time
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import PIL.Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def mock_pakistan_price(city, area_marla, property_type, bedrooms, bathrooms, amenities):
    # Average price per marla in PKR (Millions)
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

    if property_type == 'House':
        base *= 1.2
    elif property_type == 'Farm House':
        base *= 1.5

    base += (bedrooms * 0.2) + (bathrooms * 0.1)

    if 'gated' in amenities:
        base *= 1.05
    if 'metro' in amenities:
        base *= 1.02
    if 'commercial' in amenities:
        base *= 1.03

    return base * 1_000_000  # Return in PKR


def analyze_image_locally(filepath):
    """
    Analyze a house image using PIL pixel statistics.
    Returns a condition label, description, score (0-100),
    and a standalone AI-estimated price in PKR.
    No API or internet connection required.
    """
    img = PIL.Image.open(filepath).convert("RGB")
    img = img.resize((200, 200))
    pixels = list(img.getdata())

    r_vals = [p[0] for p in pixels]
    g_vals = [p[1] for p in pixels]
    b_vals = [p[2] for p in pixels]

    brightness = (sum(r_vals) + sum(g_vals) + sum(b_vals)) / (3 * len(pixels))

    # Color richness: standard deviation across all channel values
    richness = statistics.stdev(r_vals + g_vals + b_vals)

    # Luminance-based contrast
    luma = [p[0] * 0.299 + p[1] * 0.587 + p[2] * 0.114 for p in pixels]
    contrast = max(luma) - min(luma)

    # Edge-like sharpness proxy: variance of luma
    avg_luma = sum(luma) / len(luma)
    sharpness = statistics.variance(luma)

    # Composite score (0–100)
    score = (
        (brightness / 255) * 30 +
        (min(richness, 80) / 80) * 25 +
        (min(contrast, 255) / 255) * 25 +
        (min(sharpness, 3000) / 3000) * 20
    )

    # Determine condition tier
    if score >= 65:
        condition = "Luxury"
        emoji = "✨"
        desc = (
            "This property exhibits exceptional visual quality — vibrant color palette, "
            "high contrast, and sharp architectural details suggest a luxury, well-maintained residence "
            "with premium finishes and strong market appeal."
        )
        # AI price range: high-end (PKR 15M – 80M)
        ai_price = 15_000_000 + (score - 65) / 35 * 65_000_000
    elif score >= 42:
        condition = "Modern"
        emoji = "🏡"
        desc = (
            "The property image reflects a modern, good-condition home with clean aesthetics, "
            "balanced lighting, and decent curb appeal — typical of a well-kept mid-range residence "
            "in an established neighborhood."
        )
        # AI price range: mid-range (PKR 6M – 15M)
        ai_price = 6_000_000 + (score - 42) / 23 * 9_000_000
    else:
        condition = "Standard"
        emoji = "🏠"
        desc = (
            "The image indicates a standard or older-style property with modest visual characteristics — "
            "lower brightness and reduced color richness suggest an older build or a property "
            "that may benefit from renovation."
        )
        # AI price range: budget (PKR 2M – 6M)
        ai_price = 2_000_000 + (score / 42) * 4_000_000

    return {
        "condition": condition,
        "emoji": emoji,
        "description": desc,
        "score": round(score, 1),
        "ai_price": round(ai_price, -4),  # round to nearest 10,000
    }


def format_pkr(amount):
    return "{:,.0f}".format(amount)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def predict():
    try:
        time.sleep(1.0)

        city = request.form.get('city')
        area_marla = float(request.form.get('area_marla', 0))
        property_type = request.form.get('property_type')
        bedrooms = int(request.form.get('bedrooms', 0))
        bathrooms = int(request.form.get('bathrooms', 0))

        amenities = []
        if request.form.get('amenity_gated'):
            amenities.append('gated')
        if request.form.get('amenity_metro'):
            amenities.append('metro')
        if request.form.get('amenity_commercial'):
            amenities.append('commercial')

        if area_marla <= 0:
            return render_template('index.html', error="Area must be greater than 0.")

        base_price = mock_pakistan_price(city, area_marla, property_type, bedrooms, bathrooms, amenities)

        uploaded_image_path = None
        ai_analysis = None

        if 'house_image' in request.files:
            file = request.files['house_image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                uploaded_image_path = f"uploads/{filename}"

                # Local AI image analysis — no API needed
                ai_analysis = analyze_image_locally(filepath)

        breakdown = {
            'city': city,
            'base': format_pkr(base_price),
            'total': format_pkr(base_price),
            'raw_total': base_price
        }

        if ai_analysis:
            breakdown['ai_price_fmt'] = format_pkr(ai_analysis['ai_price'])

        return render_template(
            'index.html',
            results=format_pkr(base_price),
            breakdown=breakdown,
            image_path=uploaded_image_path,
            ai_analysis=ai_analysis,
            selected_city=city,
            selected_area=area_marla
        )

    except Exception as e:
        return render_template('index.html', error=f"An error occurred: {str(e)}")


if __name__ == "__main__":
    app.run(debug=True)
