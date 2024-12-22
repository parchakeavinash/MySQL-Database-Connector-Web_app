from flask import Flask, request, render_template, redirect, flash, session, url_for
from sqlalchemy import create_engine, text
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default-dev-key')

@app.route('/', methods=['GET', 'POST'])
def connect_database():
    if request.method == 'POST':
        host = request.form.get('host', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        database = request.form.get('database', '').strip()
        
        if not all([host, username, password, database]):
            flash('All connection fields are required', 'error')
            return render_template('connect.html')

        try:
            db_url = f"mysql+pymysql://{username}:{password}@{host}/{database}"
            engine = create_engine(db_url)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            session['db_url'] = db_url
            flash('Successfully connected to database!', 'success')
            return redirect(url_for('upload_file'))

        except Exception as e:
            flash(f'Database connection failed: {str(e)}', 'error')
            return render_template('connect.html')

    return render_template('connect.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'db_url' not in session:
        flash('Please connect to database first', 'error')
        return redirect(url_for('connect_database'))
        
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('upload_file'))
            
        file = request.files['file']
        table_name = request.form.get('table_name', '').strip()
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('upload_file'))
            
        if not table_name:
            flash('Please provide a table name', 'error')
            return redirect(url_for('upload_file'))
            
        try:
            # Read the file based on its extension
            if file.filename.endswith('.xlsx'):
                df = pd.read_excel(file)
            elif file.filename.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                flash('Invalid file type. Please upload CSV or XLSX file', 'error')
                return redirect(url_for('upload_file'))
                
            # Connect to database and upload
            engine = create_engine(session['db_url'])
            df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
            
            flash(f'Successfully uploaded data to table {table_name}!', 'success')
            return redirect(url_for('upload_file'))
            
        except Exception as e:
            flash(f'Error uploading file: {str(e)}', 'error')
            return redirect(url_for('upload_file'))
            
    return render_template('upload.html')

# Add the logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('Successfully disconnected from database', 'success')
    return redirect(url_for('connect_database'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)