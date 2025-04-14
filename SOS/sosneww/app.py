from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.message import EmailMessage
import os
from jinja2 import DictLoader

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Predefined sender credentials and default receiver emails
SENDER_EMAIL = "tensortitans2612@gmail.com"
SENDER_PASSWORD = "hjcy lblh gwhv jmzk"
DEFAULT_RECEIVERS = ["siddhantpatil1543@gmail.com", "siddhantpatil1540@gmail.com"]

# ----------------------------
# Templates (Using DictLoader)
# ----------------------------
templates = {
    "base.html": """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tensor Titans SOS Hub</title>
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
      text-align: left;
      font-weight: bold;
      background: rgba(255,255,255,0.05);
      text-decoration: none;
      transition: background 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease, color 0.3s ease;
    }
    .sidenav .nav-link i {
      margin-right: 8px;
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
      display: inline-block;
    }
    .btn-grad:hover {
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
    /* Form Controls with Icons */
    .input-group-text {
      background-color: #1f1f1f;
      border: 1px solid #444444;
      color: #e0e0e0;
    }
    .form-control {
      background-color: #1f1f1f;
      border: 1px solid #444444;
      color: #e0e0e0;
    }
    .form-control:focus {
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
    /* Drag & Drop Upload Area */
    .upload-area {
      margin-top: 1.25rem;
      border: none;
      background-image: url("data:image/svg+xml,%3csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3e%3crect width='100%25' height='100%25' fill='none' stroke='%23ccc' stroke-width='3' stroke-dasharray='6, 14' stroke-dashoffset='0' stroke-linecap='square'/%3e%3c/svg%3e");
      background-color: transparent;
      padding: 3rem;
      width: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      transition: background-image 0.3s;
      cursor: pointer;
    }
    .upload-area:hover, .upload-area:focus {
      background-image: url("data:image/svg+xml,%3csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3e%3crect width='100%25' height='100%25' fill='none' stroke='%232e44ff' stroke-width='3' stroke-dasharray='6, 14' stroke-dashoffset='0' stroke-linecap='square'/%3e%3c/svg%3e");
    }
    .upload-area-icon {
      display: block;
      width: 2.25rem;
      height: 2.25rem;
    }
    .upload-area-icon svg {
      max-height: 100%;
      max-width: 100%;
    }
    .upload-area-title {
      margin-top: 1rem;
      display: block;
      font-weight: 700;
      color: #D3D3D3;
    }
    .upload-area-description {
      display: block;
      color: #6a6b76;
    }
    .upload-area-description strong {
      color: #2e44ff;
      font-weight: 700;
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
    /* Responsive Styles for Mobile Devices */
    @media (max-width: 768px) {
      .sidenav {
        position: relative;
        width: 100%;
        height: auto;
        padding: 10px;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
      }
      .sidenav h3 {
        width: 100%;
        text-align: center;
      }
      .sidenav .nav-link {
        margin: 5px;
        flex: 1 1 auto;
        text-align: center;
      }
      .sidenav .sidebar-footer {
        position: static;
        width: 100%;
        margin-top: 10px;
      }
      .topnav {
        margin-left: 0;
        flex-direction: column;
        align-items: center;
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
    <div class="btn-grad"><b>TensorTitans SOS Hub</b></div>
    <a class="nav-link" href="https://www.google.com" target="_blank"><i class="fas fa-home"></i> Home</a>
    <a class="nav-link" href="{{ url_for('add_travel_details') }}"><i class="fas fa-car"></i> Add Travel Details</a>
    <a class="nav-link" href="{{ url_for('track_location') }}"><i class="fas fa-map-marker-alt"></i> Track Location</a>
    <a class="nav-link" href="{{ url_for('emergency_sos') }}"><i class="fas fa-exclamation-triangle"></i> Emergency SOS</a>
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
      <a href="#"><img src="{{ url_for('static', filename='logo.jpg') }}" alt="Logo" style="height:60px;"></a>
    </div>
  </nav>
  <!-- Main Content -->
  <div class="main-content">
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
            {{ message }}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
        {% endfor %}
      {% endif %}
    {% endwith %}
    {% block content %}{% endblock %}
  </div>
  <!-- Bootstrap JS and dependencies -->
  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
  <!-- Drag & Drop Setup for Upload Areas -->
  <script>
    document.addEventListener("DOMContentLoaded", function() {
      function setupUploadArea(areaId, inputId) {
        var area = document.getElementById(areaId);
        var fileInput = document.getElementById(inputId);
        if (!area || !fileInput) return;
        area.addEventListener("click", function() {
          fileInput.click();
        });
        area.addEventListener("dragover", function(e) {
          e.preventDefault();
          e.stopPropagation();
          area.style.backgroundColor = "#f0f0f0";
        });
        area.addEventListener("dragleave", function(e) {
          e.preventDefault();
          e.stopPropagation();
          area.style.backgroundColor = "transparent";
        });
        area.addEventListener("drop", function(e) {
          e.preventDefault();
          e.stopPropagation();
          fileInput.files = e.dataTransfer.files;
        });
      }
      setupUploadArea("upload-area", "upload-input");
    });
  </script>
  {% block extra_js %}{% endblock %}
</body>
</html>
""",
    "dashboard.html": """
{% extends "base.html" %}
{% block content %}
  <h2>Welcome to Tensor Titans SOS Hub</h2>
  <p>Select an option from the sidebar to get started.</p>
{% endblock %}
""",
    "add_travel_details.html": """
{% extends "base.html" %}
{% block content %}
  <h2>Add Travel Details</h2>
  <form method="POST" enctype="multipart/form-data">
    <!-- Receiver Emails -->
    <div class="form-group">
      <label>Receiver Emails (comma-separated):</label>
      <div class="input-group mb-3">
        <div class="input-group-prepend">
          <span class="input-group-text"><i class="fas fa-envelope"></i></span>
        </div>
        <input type="text" name="receiver_emails" class="form-control" placeholder="e.g., {{ default_receivers }}" required>
      </div>
    </div>
    <!-- Vehicle Number -->
    <div class="form-group">
      <label>Vehicle Number:</label>
      <div class="input-group mb-3">
        <div class="input-group-prepend">
          <span class="input-group-text"><i class="fas fa-car"></i></span>
        </div>
        <input type="text" name="vehicle_number" class="form-control" placeholder="e.g., MH12AB1234" required>
      </div>
    </div>
    <!-- Vehicle Type -->
    <div class="form-group">
      <label>Vehicle Type:</label>
      <div class="input-group mb-3">
        <div class="input-group-prepend">
          <span class="input-group-text"><i class="fas fa-list"></i></span>
        </div>
        <select name="vehicle_type" class="form-control">
          <option>Car</option>
          <option>Bike</option>
          <option>Auto</option>
          <option>Other</option>
        </select>
      </div>
    </div>
    <!-- Vehicle Color -->
    <div class="form-group">
      <label>Vehicle Color:</label>
      <div class="input-group mb-3">
        <div class="input-group-prepend">
          <span class="input-group-text"><i class="fas fa-palette"></i></span>
        </div>
        <input type="text" name="vehicle_color" class="form-control" placeholder="e.g., White, Black, Red" required>
      </div>
    </div>
    <!-- Driver's Name -->
    <div class="form-group">
      <label>Driver's Name:</label>
      <div class="input-group mb-3">
        <div class="input-group-prepend">
          <span class="input-group-text"><i class="fas fa-user"></i></span>
        </div>
        <input type="text" name="driver_name" class="form-control" placeholder="Enter driver's name" required>
      </div>
    </div>
    <!-- Location -->
    <div class="form-group">
      <label>Location:</label>
      <div class="input-group mb-3">
        <div class="input-group-prepend">
          <span class="input-group-text"><i class="fas fa-map-marker-alt"></i></span>
        </div>
        <textarea name="location" class="form-control" placeholder="Enter your current location or Google Maps link" required></textarea>
      </div>
    </div>
    <!-- Additional Message -->
    <div class="form-group">
      <label>Additional Message (Optional):</label>
      <div class="input-group mb-3">
        <div class="input-group-prepend">
          <span class="input-group-text"><i class="fas fa-comment"></i></span>
        </div>
        <textarea name="message" class="form-control" placeholder="Enter any additional details"></textarea>
      </div>
    </div>
    <!-- Drag & Drop Image Upload -->
    <div class="form-group">
      <label>Upload an image (optional):</label>
      <div id="upload-area" class="upload-area">
        <span class="upload-area-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24">
            <path fill="none" d="M0 0h24v24H0V0z"/>
            <path d="M19 9l-7-7-7 7h4v7h6V9h4z" fill="#2e44ff"/>
          </svg>
        </span>
        <span class="upload-area-title">Drag & drop your image here</span>
        <span class="upload-area-description">Or click to select a file</span>
      </div>
      <input type="file" id="upload-input" name="image" accept="image/*" style="display: none;">
    </div>
    <button type="submit" class="btn btn-grad">Send Emergency Report</button>
  </form>
{% endblock %}
""",
    "track_location.html": """
{% extends "base.html" %}
{% block content %}
  <h2>Track Location</h2>
  <form method="POST">
    <!-- User Email -->
    <div class="form-group">
      <label>Your Email:</label>
      <div class="input-group mb-3">
        <div class="input-group-prepend">
          <span class="input-group-text"><i class="fas fa-envelope"></i></span>
        </div>
        <input type="email" name="user_email" class="form-control" placeholder="Enter your email" required>
      </div>
    </div>
    <!-- Password -->
    <div class="form-group">
      <label>Your Email Password:</label>
      <div class="input-group mb-3">
        <div class="input-group-prepend">
          <span class="input-group-text"><i class="fas fa-lock"></i></span>
        </div>
        <input type="password" name="user_password" class="form-control" placeholder="Enter your password" required>
      </div>
    </div>
    <button type="submit" class="btn btn-grad">Track Location</button>
  </form>
{% endblock %}
""",
    "emergency_sos.html": """
{% extends "base.html" %}
{% block content %}
  <h2>Emergency SOS System</h2>
  <form method="POST" enctype="multipart/form-data">
    <!-- Receiver Emails -->
    <div class="form-group">
      <label>Receiver Emails (comma-separated):</label>
      <div class="input-group mb-3">
        <div class="input-group-prepend">
          <span class="input-group-text"><i class="fas fa-envelope"></i></span>
        </div>
        <input type="text" name="receiver_emails" class="form-control" placeholder="e.g., {{ default_receivers }}" required>
      </div>
    </div>
    <!-- Emergency Message -->
    <div class="form-group">
      <label>Message:</label>
      <div class="input-group mb-3">
        <div class="input-group-prepend">
          <span class="input-group-text"><i class="fas fa-exclamation-triangle"></i></span>
        </div>
        <textarea name="message" class="form-control" placeholder="Enter your emergency message" required></textarea>
      </div>
    </div>
    <!-- Drag & Drop Image Upload -->
    <div class="form-group">
      <label>Upload an image (optional):</label>
      <div id="upload-area" class="upload-area">
        <span class="upload-area-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24">
            <path fill="none" d="M0 0h24v24H0V0z"/>
            <path d="M19 9l-7-7-7 7h4v7h6V9h4z" fill="#2e44ff"/>
          </svg>
        </span>
        <span class="upload-area-title">Drag & drop your image here</span>
        <span class="upload-area-description">Or click to select a file</span>
      </div>
      <input type="file" id="upload-input" name="image" accept="image/*" style="display: none;">
    </div>
    <button type="submit" class="btn btn-grad">Send Emergency Email</button>
  </form>
  <br>
  <h5>Need immediate help?</h5>
  <a href="tel:112" class="btn btn-danger">Call Emergency Services (India)</a>
{% endblock %}
"""
}

app.jinja_loader = DictLoader(templates)

# ----------------------------
# Routes
# ----------------------------
@app.route('/')
def dashboard():
    return render_template("dashboard.html", page_title="Dashboard")

@app.route('/add_travel_details', methods=["GET", "POST"])
def add_travel_details():
    if request.method == "POST":
        receiver_emails = request.form.get("receiver_emails")
        vehicle_number = request.form.get("vehicle_number")
        vehicle_type = request.form.get("vehicle_type")
        vehicle_color = request.form.get("vehicle_color")
        driver_name = request.form.get("driver_name")
        location = request.form.get("location")
        message_text = request.form.get("message")
        uploaded_file = request.files.get("image")

        if not (receiver_emails and vehicle_number and vehicle_color and driver_name and location):
            flash("⚠️ Please fill in all required fields before sending.", "warning")
            return redirect(url_for('add_travel_details'))

        email_list = [email.strip() for email in receiver_emails.split(",")]
        email_body = f"""
🚨 Emergency Alert from Tensor Titans SOS Hub

Vehicle Details:
- Vehicle Number: {vehicle_number}
- Vehicle Type: {vehicle_type}
- Vehicle Color: {vehicle_color}

Driver Details:
- Driver Name: {driver_name}

Location:
{location}

Additional Message:
{message_text if message_text else "No additional information provided."}
        """
        msg = EmailMessage()
        msg["From"] = SENDER_EMAIL
        msg["To"] = ", ".join(email_list)
        msg["Subject"] = "🚨 Tensor Titans Emergency Alert"
        msg.set_content(email_body)

        if uploaded_file:
            file_data = uploaded_file.read()
            file_name = uploaded_file.filename
            subtype = file_name.split('.')[-1]
            msg.add_attachment(file_data, maintype="image", subtype=subtype, filename=file_name)

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            server.quit()
            flash(f"✅ Emergency Report sent successfully to: {', '.join(email_list)}", "success")
        except Exception as e:
            flash(f"❌ Failed to send email: {e}", "danger")
        return redirect(url_for('add_travel_details'))

    return render_template("add_travel_details.html", page_title="Add Travel Details", default_receivers=", ".join(DEFAULT_RECEIVERS))

@app.route('/track_location', methods=["GET", "POST"])
def track_location():
    if request.method == "POST":
        return redirect("https://1543siddhant.github.io/live-location-tracking-magnitude/")
    return render_template("track_location.html", page_title="Track Location")

@app.route('/emergency_sos', methods=["GET", "POST"])
def emergency_sos():
    if request.method == "POST":
        receiver_emails = request.form.get("receiver_emails")
        message_text = request.form.get("message")
        uploaded_file = request.files.get("image")

        if not (receiver_emails and message_text):
            flash("⚠️ Please ensure all fields are filled before sending.", "warning")
            return redirect(url_for('emergency_sos'))

        email_list = [email.strip() for email in receiver_emails.split(",")]
        msg = EmailMessage()
        msg["From"] = SENDER_EMAIL
        msg["To"] = ", ".join(email_list)
        msg["Subject"] = "🚨 URGENT: Emergency Assistance Needed!"
        msg.set_content(message_text)

        if uploaded_file:
            file_data = uploaded_file.read()
            file_name = uploaded_file.filename
            subtype = file_name.split('.')[-1]
            msg.add_attachment(file_data, maintype="image", subtype=subtype, filename=file_name)

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            server.quit()
            flash(f"✅ Emergency Email sent successfully to: {', '.join(email_list)}", "success")
        except Exception as e:
            flash(f"❌ Failed to send email: {e}", "danger")
        return redirect(url_for('emergency_sos'))

    return render_template("emergency_sos.html", page_title="Emergency SOS", default_receivers=", ".join(DEFAULT_RECEIVERS))

if __name__ == '__main__':
    app.run(debug=True, port=5007)
