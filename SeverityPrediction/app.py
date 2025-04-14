import pickle
import numpy as np
from flask import Flask, render_template, request, flash, redirect, url_for
from jinja2 import DictLoader

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# ------------------------------
# Load Model and Vectorizer
# ------------------------------
with open("incident_severity_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)
with open("tfidf_vectorizer.pkl", "rb") as vec_file:
    vectorizer = pickle.load(vec_file)

def predict_severity(description):
    description_tfidf = vectorizer.transform([description])
    prediction = model.predict(description_tfidf)
    return prediction[0]

# ------------------------------
# Templates (Using DictLoader)
# ------------------------------
# Modified Base Template – note the background image changed to "safe.jpeg" 
# and the sidebar now contains a single navigation link for the severity predictor.
base_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Incident Severity Predictor Dashboard</title>
  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <!-- Font Awesome for icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    /* Global Styles */
    body {
      background: url("{{ url_for('static', filename='apple.jpg') }}") no-repeat center center;
      background-size: cover;
      color: #e0e0e0;
      font-family: 'Inter', sans-serif;
      margin: 0;
      padding: 0;
    }
    /* Sidebar Styling */
    .sidenav {
      position: fixed;
      top: 0;
      left: 0;
      height: 100%;
      width: 250px;
      background: linear-gradient(135deg, #2a2a2a, #1f1f1f);
      padding: 30px 20px;
      overflow-y: auto;
      box-shadow: 2px 0 8px rgba(0, 0, 0, 0.8);
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .sidenav:hover {
      transform: translateX(5px);
      box-shadow: 4px 0 16px rgba(0, 0, 0, 0.9);
    }
    .sidenav h3 {
      margin: 0;
      padding-bottom: 20px;
    }
    .sidenav .nav-link {
      display: block;
      padding: 12px 10px;
      margin-bottom: 12px;
      color: #ffffff;
      border: 1px solid #444444;
      border-radius: 8px;
      text-align: center;
      font-weight: bold;
      background: rgba(255,255,255,0.05);
      text-decoration: none;
      transition: background 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease, color 0.3s ease;
    }
    .sidenav .nav-link:hover {
      background: #03dac6;
      color: #000000;
      transform: translateY(-3px);
      box-shadow: 0 4px 12px rgba(0,0,0,0.7);
    }
    /* Top Navbar */
    .topnav {
      margin-left: 250px;
      background: linear-gradient(135deg, #1f1f1f, #0d0d0d);
      padding: 10px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #444444;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.6);
    }
    .breadcrumb {
      background: transparent;
      margin-bottom: 0;
      font-size: 1.1em;
      color: #aaaaaa;
    }
    /* Main Content */
    .main-content {
      margin: 40px auto;
      max-width: 800px;
      padding: 40px;
      padding-top: 120px;
      background: rgba(0, 0, 0, 0.75);
      border-radius: 15px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.8);
      border: 1px solid rgba(50, 50, 50, 0.8);
      text-align: center;
      position: relative;
      left: 125px;
    }
    /* Button Styles */
    .btn-grad {
      background-image: linear-gradient(to right, #C04848 0%, #480048 51%, #C04848 100%);
      margin: 20px 10px;
      padding: 15px 45px;
      text-align: center;
      text-transform: uppercase;
      transition: 0.5s;
      background-size: 200% auto;
      color: white;            
      box-shadow: 0 0 20px #eee;
      border-radius: 15px;
      display: block;
    }
    .btn-grad:hover {
      background-position: right center;
      color: #fff;
      text-decoration: none;
    }
    .btn-grad-dupe {
        background-image: linear-gradient(to right, #C04848 0%, #480048 51%, #C04848 100%);
        margin: 20px 10px;
        padding: 5px 30px;
        text-align: center;
        text-transform: uppercase;
        transition: 0.5s;
        background-size: 200% auto;
        color: white;            
        border-radius: 5px;
        display: block;
    }
    .btn-grad-dupe:hover {
        background-position: right center;
        color: #fff;
        text-decoration: none;
    }




    .btn {
      all: unset;
      padding: 0.5em 1.5em;
      font-size: 16px;
      background: transparent;
      border: none;
      position: relative;
      color: #f0f0f0;
      cursor: pointer;
      z-index: 1;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      white-space: nowrap;
      user-select: none;
      -webkit-user-select: none;
      touch-action: manipulation;
      transition: color 250ms;
    }
    .btn::after,
    .btn::before {
      content: "";
      position: absolute;
      bottom: 0;
      right: 0;
      z-index: -1;
      transition: all 0.4s;
    }
    .btn::before {
      transform: translate(0%, 0%);
      width: 100%;
      height: 100%;
      background: #28282d;
      border-radius: 10px;
    }
    .btn::after {
      transform: translate(10px, 10px);
      width: 35px;
      height: 35px;
      background: #ffffff15;
      backdrop-filter: blur(5px);
      -webkit-backdrop-filter: blur(5px);
      border-radius: 50px;
    }
    .btn:hover::before {
      transform: translate(5%, 20%);
      width: 110%;
      height: 110%;
    }
    .btn:hover::after {
      border-radius: 10px;
      transform: translate(0, 0);
      width: 100%;
      height: 100%;
    }
    .btn:active::after {
      transition: 0s;
      transform: translate(0, 5%);
    }
    .btn:hover {
      color: #fff;
    }
    /* Form Controls */
    .narrow-field {
      max-width: 400px;
      margin: 10px auto;
    }
    .form-control, .form-control-file, textarea {
      background-color: #1f1f1f;
      border: 1px solid #444444;
      color: #e0e0e0;
      border-radius: 5px;
      transition: box-shadow 0.3s ease;
    }
    .form-control:focus, textarea:focus {
      box-shadow: 0 0 8px rgba(100, 100, 100, 0.8);
    }
    label {
      font-weight: bold;
      color: #ffffff;
      margin-bottom: 5px;
      display: block;
      background: linear-gradient(135deg, #333333, #222222);
      padding: 5px;
      border-radius: 5px;
      border: 1px solid #555555;
    }
    h1, h2, p {
      text-align: center;
    }
    /* Sidebar Footer */
    .sidebar-footer {
      position: absolute;
      bottom: 20px;
      left: 20px;
      right: 20px;
      font-size: 10px;
      color: #aaa;
      text-align: center;
    }
    .sidebar-footer a {
      color: #aaa;
      margin: 0 4px;
      font-size: 14px;
    }
    /* Hamburger Menu - Hidden on Desktop */
    .hamburger {
      display: none;
      cursor: pointer;
    }
    /* Overlay Menu for Mobile */
    .overlay-menu {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.7);
      display: none;
      justify-content: center;
      align-items: center;
      z-index: 9999;
    }
    .overlay-menu.active {
      display: flex;
    }
    .overlay-menu a {
      font-size: 24px;
      color: #fff;
      background: rgba(255, 255, 255, 0.1);
      padding: 15px 30px;
      border-radius: 10px;
      text-decoration: none;
    }
    /* Responsive Styles for Mobile Devices */
    @media (max-width: 768px) {
      .sidenav {
        display: none;
      }
      .topnav {
        margin-left: 0;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
      }
      .hamburger {
        display: block;
      }
      .main-content {
        margin: 20px auto;
        padding: 20px;
        left: 0;
        width: 90%;
        padding-top: 80px;
      }
    }
  </style>
</head>
<body>
  <!-- Sidebar -->
  <aside class="sidenav">
    <div class="btn-grad"><b>Tensor Titans</b></div>
    <a class="nav-link" href="{{ url_for('severity') }}">Incident Severity Predictor</a>
    <div class="sidebar-footer">
       <div>
         <a href="#"><i class="fas fa-cog"></i></a>
         <a href="#"><i class="fab fa-twitter"></i></a>
         <a href="#"><i class="fab fa-facebook"></i></a>
         <a href="#"><i class="fab fa-instagram"></i></a>
       </div>
       <div style="margin-top:5px;">Contact us: tensortitans2612@gmail.com</div>
    </div>
  </aside>
  <!-- Top Navbar -->
  <nav class="topnav">
    <ol class="breadcrumb">
      <li class="breadcrumb-item">Pages</li>
      <li class="breadcrumb-item active">{{ page_title|default("Dashboard") }}</li>
    </ol>
    <div>
      <a href="#"><img src="{{ url_for('static', filename='logo.png') }}" alt="Logo" style="height:60px;"></a>
    </div>
  </nav>
  <!-- Overlay Menu for Mobile -->
  <div id="overlay-menu" class="overlay-menu" onclick="toggleMenu()">
    <a href="{{ url_for('severity') }}" onclick="event.stopPropagation(); toggleMenu();">Incident Severity Predictor</a>
  </div>
  <!-- Main Content -->
  <div class="main-content">
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <div class="alert alert-info" role="alert" style="background: #111111; border: 1px solid #333333;">
          {% for message in messages %}
            <p>{{ message }}</p>
          {% endfor %}
        </div>
      {% endif %}
    {% endwith %}
    {% block content %}{% endblock %}
  </div>
  <!-- Bootstrap JS and dependencies -->
  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
  <script>
    function toggleMenu() {
      var menu = document.getElementById("overlay-menu");
      if (menu.classList.contains("active")) {
        menu.classList.remove("active");
      } else {
        menu.classList.add("active");
      }
    }
  </script>
  {% block extra_js %}{% endblock %}
</body>
</html>
'''

# Severity Prediction Page Template
severity_html = '''
{% extends "base.html" %}
{% block content %}
<h1>Incident Severity Predictor</h1>
<p>AI-Powered Safety Analysis for Women &amp; Children</p>
<!-- Slogans / Awareness -->
<div style="background-color: black; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
  <h3>🔍 Predict, Prevent, and Protect</h3>
  <p>
    🌟 "Your safety matters! Report incidents and raise awareness."<br>
    🛡️ "AI for a safer tomorrow – let's predict, prevent, and protect."<br>
    🔥 "Speak up, stay safe. Together, we build a secure society."
  </p>
</div>
<form action="{{ url_for('severity') }}" method="post" class="narrow-field">
  <div class="form-group">
    <label for="description" class="btn-grad-dupe" style="display:block; margin-bottom:20px;">📝 Describe the incident:</label>
    <textarea id="description" name="description" class="form-control" rows="4" placeholder="Example: A working woman faced molestation near a railway station in Mumbai..."></textarea>
  </div>
  <button type="submit" class="btn">🔍 Predict Severity</button>
</form>
{% if result %}
  <h2 style="text-align: center; color: yellow;">⚠️ Predicted Severity: {{ result }}</h2>
{% endif %}
{% endblock %}
'''

# Register templates via DictLoader
app.jinja_loader = DictLoader({
    'base.html': base_html,
    'severity.html': severity_html,
})

# ------------------------------
# Flask Routes
# ------------------------------
@app.route('/')
def index():
    return redirect(url_for('severity'))

@app.route('/severity', methods=['GET', 'POST'])
def severity():
    result = None
    if request.method == 'POST':
        description = request.form.get('description', '')
        if description.strip():
            result = predict_severity(description)
        else:
            flash("⚠️ Please enter a description of the incident. ⚠️")
    return render_template('severity.html', page_title="Incident Severity Predictor", result=result)

# ------------------------------
# Run the Application
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5004)
