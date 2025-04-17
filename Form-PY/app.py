from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Load existing data from JSON file
def load_data():
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            return json.load(f)
    return []

# Save new entry to JSON file
def save_data(entry):
    data = load_data()
    data.append(entry)
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    first_name = request.form['first_name']
    email = request.form['email']
    contact_number = request.form['contact_number']
    source = request.form['source']
    other_source = request.form.get('other_source', '')
    reason = request.form['reason']
    payment_screenshot = request.files['payment_screenshot']

    # Save the payment screenshot
    if payment_screenshot:
        screenshot_filename = payment_screenshot.filename
        payment_screenshot.save(os.path.join('static/images', screenshot_filename))
    else:
        screenshot_filename = ''

    entry = {
        "first_name": first_name,
        "email": email,
        "contact_number": contact_number,
        "source": source,
        "other_source": other_source,
        "reason": reason,
        "payment_screenshot": screenshot_filename
    }

    save_data(entry)
    return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)