# app.py - Main Flask Application
# This is our main Python file that creates a web server

# Import the libraries we need
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import hashlib  # Python's built-in library for creating hashes
import os  # For file operations
from datetime import datetime  # To timestamp our hash operations
from database import init_db, save_hash_result, get_hash_history  # Our database functions

# Create our Flask application
# Think of this as creating a web server that can respond to requests
app = Flask(__name__)
app.secret_key = 'your-secret-key-for-security'  # Needed for flash messages

# Initialize our database when the app starts
init_db()

# ROUTE 1: Homepage
# This function runs when someone visits our website's main page
@app.route('/')
def index():
    """
    This is called a 'route' - it tells Flask what to do when someone visits '/'
    render_template() shows our HTML page to the user
    """
    return render_template('index.html')

# ROUTE 2: Hash Text
# This function runs when someone submits text to be hashed
@app.route('/hash_text', methods=['POST'])
def hash_text():
    """
    This handles POST requests (when forms are submitted)
    We get the text from the form and create hashes
    """
    # Get the text that the user submitted
    text_input = request.form.get('text_input')
    
    # Check if user actually entered something
    if not text_input:
        flash('Please enter some text to hash!', 'error')
        return redirect(url_for('index'))
    
    # Create different types of hashes
    # Each hash algorithm creates a unique "fingerprint" of the text
    hashes = {
        'MD5': hashlib.md5(text_input.encode()).hexdigest(),
        'SHA-1': hashlib.sha1(text_input.encode()).hexdigest(),
        'SHA-256': hashlib.sha256(text_input.encode()).hexdigest(),
        'SHA-512': hashlib.sha512(text_input.encode()).hexdigest()
    }
    
    # Save this operation to our database
    for algorithm, hash_value in hashes.items():
        save_hash_result(
            input_type='text',
            input_value=text_input[:50] + ('...' if len(text_input) > 50 else ''),  # Truncate long text
            algorithm=algorithm,
            hash_result=hash_value
        )
    
    # Show the results page with all the hashes
    return render_template('results.html', 
                         input_type='Text', 
                         input_value=text_input, 
                         hashes=hashes)

# ROUTE 3: Hash File
# This function runs when someone uploads a file to be hashed
@app.route('/hash_file', methods=['POST'])
def hash_file():
    """
    This handles file uploads and creates hashes of the file contents
    """
    # Check if a file was uploaded
    if 'file' not in request.files:
        flash('No file selected!', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    # Check if user actually selected a file
    if file.filename == '':
        flash('No file selected!', 'error')
        return redirect(url_for('index'))
    
    try:
        # Read the file contents
        file_content = file.read()
        filename = file.filename
        
        # Create hashes of the file content
        hashes = {
            'MD5': hashlib.md5(file_content).hexdigest(),
            'SHA-1': hashlib.sha1(file_content).hexdigest(),
            'SHA-256': hashlib.sha256(file_content).hexdigest(),
            'SHA-512': hashlib.sha512(file_content).hexdigest()
        }
        
        # Save to database
        for algorithm, hash_value in hashes.items():
            save_hash_result(
                input_type='file',
                input_value=filename,
                algorithm=algorithm,
                hash_result=hash_value
            )
        
        # Show results
        return render_template('results.html', 
                             input_type='File', 
                             input_value=filename, 
                             hashes=hashes)
    
    except Exception as e:
        flash(f'Error processing file: {str(e)}', 'error')
        return redirect(url_for('index'))

# ROUTE 4: View History
# This shows all previous hash operations
@app.route('/history')
def history():
    """
    This shows a page with all the hash operations we've done before
    """
    # Get all hash results from our database
    history_data = get_hash_history()
    return render_template('history.html', history=history_data)

# ROUTE 5: API endpoint for programmatic access
# This allows other programs to use our hash tool
@app.route('/api/hash', methods=['POST'])
def api_hash():
    """
    This is an API endpoint - other programs can send requests here
    It returns JSON data instead of HTML pages
    """
    try:
        data = request.json
        text_input = data.get('text')
        
        if not text_input:
            return jsonify({'error': 'No text provided'}), 400
        
        # Create hashes
        hashes = {
            'md5': hashlib.md5(text_input.encode()).hexdigest(),
            'sha1': hashlib.sha1(text_input.encode()).hexdigest(),
            'sha256': hashlib.sha256(text_input.encode()).hexdigest(),
            'sha512': hashlib.sha512(text_input.encode()).hexdigest()
        }
        
        return jsonify({
            'input': text_input,
            'hashes': hashes
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Start the web server
if __name__ == '__main__':
    # This runs our web server in debug mode (shows errors for development)
    app.run(debug=True, host='0.0.0.0', port=5000)
