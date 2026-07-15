# Predictly: Intelligent Pakistan Property Valuation

**Predictly** is a state-of-the-art, AI-powered real estate valuation dashboard specifically tailored for the Pakistan housing market. It features a premium, responsive monochrome user interface and leverages advanced machine learning techniques alongside Google's Gemini Vision AI to provide comprehensive property assessments.

---

## 🌟 Key Features

*   **🇵🇰 Localized Valuation Logic:** Predicts housing prices across major Pakistani cities (Lahore, Karachi, Islamabad, etc.) based on Area (Marlas), Property Type, Bedrooms, and Bathrooms.
*   **👁️ AI Vision Assessment:** Upload a picture of a property, and the backend utilizes the **Google Gemini API** to analyze its exterior condition, luxury level, and number of stories, dynamically adjusting the valuation.
*   **🌗 Monochrome Light/Dark Mode:** A highly polished, distraction-free UI that seamlessly toggles between dark and light glassmorphism themes.
*   **📄 PDF Report Generation:** Instantly generate and download sleek, branded PDF valuation reports of the property using `html2pdf.js`.
*   **📊 Market Trends Analytics:** Visualize 5-year historical price trends for selected cities via an interactive `Chart.js` graph.
*   **🗺️ Interactive Mapping:** Integrated `Leaflet.js` map that automatically flies to and pins the selected city during valuation.
*   **🏘️ Comparable Properties (Comps):** Automatically fetches and displays mock comparable properties based on the user's location and area inputs.
*   **💰 Mortgage Estimator:** Built-in EMI calculator allowing users to estimate monthly installments based on down payment and loan term preferences.
*   **✅ Amenity Adjustments:** Dynamic toggles for neighborhood amenities (Gated Community, Commercial Area, Near Metro) that adjust the base price in real-time.

---

## 🛠️ Tech Stack

*   **Backend:** Python 3, Flask, Werkzeug
*   **Artificial Intelligence:** Google Generative AI (`google-generativeai`)
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

4. **Configure API Keys (Optional)**
   To enable true AI image processing, open `app.py`, uncomment the Gemini configuration lines, and add your free Google Gemini API Key:
   ```python
   # os.environ["GEMINI_API_KEY"] = "YOUR_API_KEY_HERE"
   # genai.configure(api_key=os.environ["GEMINI_API_KEY"])
   ```
   *(Note: The application includes a smart fallback mock handler if no API key is provided, ensuring the demo always works.)*

5. **Run the Application**
   ```bash
   python app.py
   ```
   Open `http://127.0.0.1:5000` in your web browser.

---

## 👨‍💻 Developer

**Abdul Wahid**
*   **GitHub:** [github.com/abduIwahid](https://github.com/abduIwahid)
*   **Email:** [contact@abdulwahid.in](mailto:contact@abdulwahid.in)

*This project is designed as a robust portfolio demonstration of full-stack development, AI API integration, and modern UI/UX design.*
