from flask import Flask, request, render_template, redirect, flash, session, url_for
from sqlalchemy import create_engine, text
from werkzeug.utils import secure_filename
import pandas as pd
import os
import re
from functools import wraps


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default-dev-key')  # Better key management
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'temp_uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitize_table_name(name):
    """Sanitize table name to prevent SQL injection"""
    return re.sub(r'[^a-zA-Z0-9_]', '', name).lower()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'db_url' not in session:
            flash('Please connect to the database first.', 'error')
            return redirect(url_for('connect_database'))
        return f(*args, **kwargs)
    return decorated_function

def get_db_connection():
    """Create and test database connection"""
    if 'db_url' not in session:
        raise Exception("No database connection configured")
    return create_engine(session['db_url'])

@app.route('/', methods=['GET', 'POST'])
def connect_database():
    if request.method == 'POST':
        # Get form values with proper key names and defaults
        host = request.form.get('host', '').strip()       # Changed from 'localhost'
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        database = request.form.get('database', '').strip()

        # Validate inputs
        if not all([host, username, password, database]):
            flash('All connection fields are required', 'error')
            return render_template('connect.html')

        try:
            # Construct database URL with proper escaping
            from urllib.parse import quote_plus
            password = quote_plus(password)  # Escape special characters in password
            
            # Use SSL if possible
            db_url = f"postgresql://{username}:{password}@{host}/{database}?sslmode=prefer"
            
            # Test connection before saving to session
            engine = create_engine(db_url)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            # Save successful connection to session
            session['db_url'] = db_url
            flash('Successfully connected to database!', 'success')
            return redirect(url_for('upload_file'))

        except Exception as e:
            flash(f'Database connection failed: {str(e)}', 'error')
            return render_template('connect.html')

    return render_template('connect.html')

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        table_name = request.form.get('table_name', '').strip()
        table_name = sanitize_table_name(table_name)
        
        if not table_name:
            flash('Please provide a valid table name (letters, numbers, and underscores only).', 'error')
            return redirect(url_for('upload_file'))
        
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('upload_file'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('upload_file'))
        
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload CSV or XLSX files only.', 'error')
            return redirect(url_for('upload_file'))
        
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Read the file into a DataFrame
            try:
                if filename.endswith('.xlsx'):
                    df = pd.read_excel(filepath)
                else:
                    df = pd.read_csv(filepath)
                
                # Basic data validation
                if df.empty:
                    raise ValueError("The file contains no data")
                
                # Upload to database
                engine = get_db_connection()
                df.to_sql(table_name, engine, if_exists='append', index=False)
                
                flash(f"Successfully uploaded {len(df)} rows to table '{table_name}'!", 'success')
                
            except Exception as e:
                raise Exception(f"Error processing file: {str(e)}")
            
            finally:
                # Clean up temporary file
                if os.path.exists(filepath):
                    os.remove(filepath)
                    
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        
        return redirect(url_for('upload_file'))
    
    return render_template('upload.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Successfully disconnected from database.', 'success')
    return redirect(url_for('connect_database'))

if __name__ == '__main__':
    app.run(debug=False)  # Set to False in production