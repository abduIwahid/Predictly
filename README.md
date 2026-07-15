# Predictly: Intelligent Pakistan Property Valuation

**Predictly** is a state-of-the-art, AI-powered real estate valuation dashboard specifically tailored for the Pakistan housing market. It features a premium, responsive monochrome user interface and uses **on-device AI image analysis** (no API key required) alongside structured valuation logic to provide comprehensive property assessments.

---

## 🌟 Key Features

*   **🇵🇰 Localized Valuation Logic:** Predicts housing prices across major Pakistani cities (Lahore, Karachi, Islamabad, Rawalpindi, Faisalabad, Multan) based on Area (Marlas), Property Type, Bedrooms, and Bathrooms.
*   **🧠 On-Device AI Vision Analysis:** Upload a photo of the property — the backend analyzes it locally using **pixel-level image processing** (brightness, color richness, contrast, and sharpness) to determine condition and generate an independent AI price estimate. **No API key or internet connection required.**
*   **💰 Dual Price Estimation:** Shows both a structured form-based valuation and a separate AI-generated visual price estimate side by side.
*   **🌗 Monochrome Light/Dark Mode:** A highly polished, distraction-free UI that seamlessly toggles between dark and light glassmorphism themes.
*   **📄 PDF Report Generation:** Instantly generate and download sleek, branded PDF valuation reports using `html2pdf.js`.
*   **📊 Market Trends Analytics:** Visualize 5-year historical price trends for selected cities via an interactive `Chart.js` graph.
*   **🗺️ Interactive Mapping:** Integrated `Leaflet.js` map that automatically flies to and pins the selected city during valuation.
*   **🏘️ Comparable Properties (Comps):** Displays mock comparable properties based on the user's location and area inputs.
*   **💳 Mortgage Estimator:** Built-in EMI calculator for estimating monthly installments based on down payment and loan term.
*   **✅ Amenity Adjustments:** Dynamic toggles for neighborhood amenities (Gated Community, Commercial Area, Near Metro) that adjust the base price.

---

## 🧠 How the AI Image Analysis Works

No external AI service is used. The analysis runs entirely on your machine using **PIL (Pillow)**:

| Signal | What it measures |
|--------|-----------------|
| **Brightness** | How well-lit and presentable the property looks |
| **Color Richness** | Vibrancy and appeal of the property's exterior |
| **Contrast** | Architectural definition and visual clarity |
| **Sharpness** | Detail level and image quality proxy |

These signals are combined into a **Visual Score (0–100)** which maps to a condition tier and price range:

| Score | Condition | AI Price Range (PKR) |
|-------|-----------|----------------------|
| 65–100 | ✨ Luxury | 15M – 80M |
| 42–64 | 🏡 Modern | 6M – 15M |
| 0–41 | 🏠 Standard | 2M – 6M |

---

## 🛠️ Tech Stack

*   **Backend:** Python 3, Flask, Werkzeug
*   **AI / Image Analysis:** Pillow (PIL) — fully on-device, no external API
*   **Frontend:** HTML5, CSS3 (Custom Variables), Bootstrap 5, JavaScript
*   **Data Visualization & Mapping:** Chart.js, Leaflet.js
*   **Document Generation:** html2pdf.js

---

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/abduIwahid/Predictly.git
   cd Predictly
   ```

2. **Set up a Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```
   Open `http://127.0.0.1:5000` in your web browser.

> **No API key needed.** The AI image analysis runs completely offline using local pixel analysis. Simply upload any house photo and get an instant AI visual estimate.

---

## 👨‍💻 Developer

**Abdul Wahid**
*   **GitHub:** [github.com/abduIwahid](https://github.com/abduIwahid)
*   **Email:** [contact@abdulwahid.in](mailto:contact@abdulwahid.in)

*This project demonstrates full-stack development, on-device AI image processing, and modern UI/UX design — all without relying on paid external APIs.*
