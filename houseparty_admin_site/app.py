
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/')
def index():
    with open('content.json') as f:
        content = json.load(f)
    return render_template('index.html', content=content)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    with open('content.json') as f:
        content = json.load(f)
    if request.method == 'POST':
        content['about_text'] = request.form['about']
        content['contact']['address'] = request.form['address']
        content['contact']['phone'] = request.form['phone']
        content['contact']['email'] = request.form['email']

        if 'hero' in request.files:
            hero = request.files['hero']
            if hero.filename:
                filename = secure_filename(hero.filename)
                hero.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                content['hero_path'] = f"/static/uploads/{filename}"
        
        with open('content.json', 'w') as f:
            json.dump(content, f, indent=2)
        return redirect(url_for('admin'))
    return render_template('admin.html', content=content)

if __name__ == '__main__':
    app.run(debug=True)
