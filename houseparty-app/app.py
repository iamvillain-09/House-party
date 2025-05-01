import os
import logging
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# Simple user class for Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Hardcoded admin user (in a real app this would be from a database)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "houseparty2023"

# Create user loader callback
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Data storage
DATA_FILE = 'site_content.json'

def get_site_content():
    """Load site content from JSON file or return default content"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        logging.error(f"Error loading site content: {e}")
    
    # Default content if file doesn't exist or has an error
    return {
        "hero": {
            "heading": "Welcome to House Party",
            "subheading": "Experience the best nightlife in Hyderabad with our DJ nights, live music, and delicious food & drinks. Join us for an unforgettable night out!"
        },
        "about": {
            "content": "House Party Bar and Kitchen brings the vibrant nightlife experience to Hyderabad with our energetic atmosphere, premium drinks, and delicious food offerings.\n\nEstablished with a passion for creating memorable nights out, we strive to provide a perfect blend of music, food, and drinks that make every visit special. Our venue is designed to create an electrifying ambiance where friends can gather, celebrate, and create lasting memories.\n\nFrom our carefully crafted cocktails to our mouth-watering menu items, every aspect of House Party is curated to ensure you have an amazing time. Our team of experienced bartenders, chefs, and staff are dedicated to providing exceptional service."
        },
        "services": [
            {
                "id": "service1",
                "icon": "fas fa-music",
                "title": "DJ Nights",
                "description": "Experience electrifying music from our resident and guest DJs with the latest tracks and cutting-edge sound systems. Every weekend, our dance floor comes alive with energetic beats."
            },
            {
                "id": "service2",
                "icon": "fas fa-female",
                "title": "Ladies Night",
                "description": "Join us every Wednesday for our special Ladies Night with complimentary drinks, special discounts, and curated music selection. Ladies enjoy priority entry and exclusive offers."
            },
            {
                "id": "service3",
                "icon": "fas fa-rupee-sign",
                "title": "MRP Nights",
                "description": "Enjoy drinks at MRP (Maximum Retail Price) on select nights. Our MRP nights offer premium beverages at store prices, making it a perfect night for budget-friendly gatherings."
            },
            {
                "id": "service4",
                "icon": "fas fa-cocktail",
                "title": "Happy Hour",
                "description": "Visit us between 5PM - 8PM daily for our Happy Hour specials featuring discounted drinks and appetizers. Perfect time to unwind after work with great deals."
            },
            {
                "id": "service5",
                "icon": "fas fa-microphone",
                "title": "Live Music",
                "description": "Enjoy performances from talented local and touring bands and artists. Our live music events feature various genres from rock to jazz to acoustic sets in an intimate setting."
            },
            {
                "id": "service6",
                "icon": "fas fa-utensils",
                "title": "Food & Drinks",
                "description": "Savor our delicious menu featuring a variety of cuisines, from bar snacks to full meals. Pair your food with our extensive selection of cocktails, beers, wines, and spirits."
            }
        ],
        "contact": {
            "address": "1st Floor, Plot No.1/A, Sy. No. 117, Beside Oyo Flagship, Near Hitech City MMTS, KPHB, Hyderabad, Telangana 500072",
            "phone": "+91 96660 22277",
            "email": "info@housepartyhyd.com",
            "hours": "Monday - Sunday: 12:00 PM - 11:30 PM"
        },
        "testimonials": [
            {
                "id": "testimonial1",
                "content": "Amazing place for weekend night outs! The DJ nights are energetic and the drinks selection is impressive. Staff is really friendly too.",
                "author": "Riya S.",
                "position": "Regular Visitor",
                "rating": 5
            },
            {
                "id": "testimonial2",
                "content": "The Happy Hour deals are unbeatable! Great ambiance, awesome music, and the food is surprisingly good for a bar. The chicken wings are a must-try.",
                "author": "Arun P.",
                "position": "Food Enthusiast",
                "rating": 4.5
            },
            {
                "id": "testimonial3",
                "content": "Ladies Night at House Party is the best in Hyderabad! Great deals on drinks, amazing music, and a wonderful atmosphere. My girlfriends and I go every week!",
                "author": "Priya M.",
                "position": "Regular Customer",
                "rating": 5
            }
        ]
    }

def save_site_content(content):
    """Save site content to JSON file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(content, f, indent=2)
        return True
    except Exception as e:
        logging.error(f"Error saving site content: {e}")
        return False

# Main website routes
@app.route('/')
def index():
    content = get_site_content()
    return render_template('index.html', content=content)

# Admin routes
@app.route('/admin')
@login_required
def admin_dashboard():
    content = get_site_content()
    return render_template('admin/dashboard.html', content=content)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            user = User(1)  # User ID 1 for admin
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin/edit/hero', methods=['GET', 'POST'])
@login_required
def edit_hero():
    content = get_site_content()
    
    if request.method == 'POST':
        content['hero'] = {
            'heading': request.form.get('heading'),
            'subheading': request.form.get('subheading')
        }
        
        if save_site_content(content):
            flash('Hero section updated successfully', 'success')
        else:
            flash('Error updating hero section', 'danger')
        
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/edit_hero.html', content=content)

@app.route('/admin/edit/about', methods=['GET', 'POST'])
@login_required
def edit_about():
    content = get_site_content()
    
    if request.method == 'POST':
        content['about'] = {
            'content': request.form.get('content')
        }
        
        if save_site_content(content):
            flash('About section updated successfully', 'success')
        else:
            flash('Error updating about section', 'danger')
        
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/edit_about.html', content=content)

@app.route('/admin/edit/services', methods=['GET'])
@login_required
def edit_services():
    content = get_site_content()
    return render_template('admin/edit_services.html', content=content)

@app.route('/admin/edit/service/<service_id>', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    content = get_site_content()
    
    # Find the service with the given ID
    service = next((s for s in content['services'] if s['id'] == service_id), None)
    
    if not service:
        flash('Service not found', 'danger')
        return redirect(url_for('edit_services'))
    
    if request.method == 'POST':
        service_index = next((i for i, s in enumerate(content['services']) if s['id'] == service_id), None)
        
        if service_index is not None:
            content['services'][service_index] = {
                'id': service_id,
                'icon': request.form.get('icon'),
                'title': request.form.get('title'),
                'description': request.form.get('description')
            }
            
            if save_site_content(content):
                flash('Service updated successfully', 'success')
            else:
                flash('Error updating service', 'danger')
            
            return redirect(url_for('edit_services'))
    
    return render_template('admin/edit_service.html', service=service)

@app.route('/admin/add/service', methods=['GET', 'POST'])
@login_required
def add_service():
    if request.method == 'POST':
        content = get_site_content()
        
        new_service = {
            'id': f"service{uuid.uuid4().hex[:8]}",
            'icon': request.form.get('icon'),
            'title': request.form.get('title'),
            'description': request.form.get('description')
        }
        
        content['services'].append(new_service)
        
        if save_site_content(content):
            flash('Service added successfully', 'success')
        else:
            flash('Error adding service', 'danger')
        
        return redirect(url_for('edit_services'))
    
    return render_template('admin/add_service.html')

@app.route('/admin/delete/service/<service_id>', methods=['POST'])
@login_required
def delete_service(service_id):
    content = get_site_content()
    
    # Filter out the service with the given ID
    content['services'] = [s for s in content['services'] if s['id'] != service_id]
    
    if save_site_content(content):
        flash('Service deleted successfully', 'success')
    else:
        flash('Error deleting service', 'danger')
    
    return redirect(url_for('edit_services'))

@app.route('/admin/edit/contact', methods=['GET', 'POST'])
@login_required
def edit_contact():
    content = get_site_content()
    
    if request.method == 'POST':
        content['contact'] = {
            'address': request.form.get('address'),
            'phone': request.form.get('phone'),
            'email': request.form.get('email'),
            'hours': request.form.get('hours')
        }
        
        if save_site_content(content):
            flash('Contact information updated successfully', 'success')
        else:
            flash('Error updating contact information', 'danger')
        
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/edit_contact.html', content=content)

@app.route('/admin/edit/testimonials', methods=['GET'])
@login_required
def edit_testimonials():
    content = get_site_content()
    return render_template('admin/edit_testimonials.html', content=content)

@app.route('/admin/edit/testimonial/<testimonial_id>', methods=['GET', 'POST'])
@login_required
def edit_testimonial(testimonial_id):
    content = get_site_content()
    
    # Find the testimonial with the given ID
    testimonial = next((t for t in content['testimonials'] if t['id'] == testimonial_id), None)
    
    if not testimonial:
        flash('Testimonial not found', 'danger')
        return redirect(url_for('edit_testimonials'))
    
    if request.method == 'POST':
        testimonial_index = next((i for i, t in enumerate(content['testimonials']) if t['id'] == testimonial_id), None)
        
        if testimonial_index is not None:
            content['testimonials'][testimonial_index] = {
                'id': testimonial_id,
                'content': request.form.get('content'),
                'author': request.form.get('author'),
                'position': request.form.get('position'),
                'rating': float(request.form.get('rating'))
            }
            
            if save_site_content(content):
                flash('Testimonial updated successfully', 'success')
            else:
                flash('Error updating testimonial', 'danger')
            
            return redirect(url_for('edit_testimonials'))
    
    return render_template('admin/edit_testimonial.html', testimonial=testimonial)

@app.route('/admin/add/testimonial', methods=['GET', 'POST'])
@login_required
def add_testimonial():
    if request.method == 'POST':
        content = get_site_content()
        
        new_testimonial = {
            'id': f"testimonial{uuid.uuid4().hex[:8]}",
            'content': request.form.get('content'),
            'author': request.form.get('author'),
            'position': request.form.get('position'),
            'rating': float(request.form.get('rating'))
        }
        
        content['testimonials'].append(new_testimonial)
        
        if save_site_content(content):
            flash('Testimonial added successfully', 'success')
        else:
            flash('Error adding testimonial', 'danger')
        
        return redirect(url_for('edit_testimonials'))
    
    return render_template('admin/add_testimonial.html')

@app.route('/admin/delete/testimonial/<testimonial_id>', methods=['POST'])
@login_required
def delete_testimonial(testimonial_id):
    content = get_site_content()
    
    # Filter out the testimonial with the given ID
    content['testimonials'] = [t for t in content['testimonials'] if t['id'] != testimonial_id]
    
    if save_site_content(content):
        flash('Testimonial deleted successfully', 'success')
    else:
        flash('Error deleting testimonial', 'danger')
    
    return redirect(url_for('edit_testimonials'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
