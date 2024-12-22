# MySQL Database Connector Web Application

## Overview
This project is a Flask-based web application designed to facilitate seamless integration with a MySQL database. It allows users to connect to a MySQL database by providing connection credentials and upload Excel files, which are then automatically stored in the specified database.

## Interface
![image](https://github.com/user-attachments/assets/dac3fe1c-1565-4e90-883d-285cfb7bbee3)
### Add information to connect MySQL Server
![image](https://github.com/user-attachments/assets/8ffaae04-dd60-4c40-bc4d-c9a167031a98)
## upload Interface
![image](https://github.com/user-attachments/assets/3151a333-c25b-4740-b0da-ea0efa2d845a)
## upload file Successful
![image](https://github.com/user-attachments/assets/01c044f0-8603-4037-8f24-0e6a51ebc8da)
![image](https://github.com/user-attachments/assets/642cbf14-dd3b-4959-9c88-ec7cf16795e0)

## Features

1. **Secure Database Connection**
   - Connect to a MySQL database by providing host, username, password, and database name.
   
2. **Excel File Upload**
   - Supports the upload of `.xlsx` files.
   - Automatically processes and inserts data from Excel into the specified database table.

3. **Dynamic Error Handling**
   - Provides user-friendly error messages for invalid credentials, connection failures, or file format issues.

4. **Responsive User Interface**
   - Simple, intuitive, and responsive web interface for seamless user experience.

5. **Data Validation**
   - Ensures only valid data is inserted into the database.
   - Logs errors and skipped rows for better troubleshooting.

## Benefits

- **Ease of Use**: Simplifies the process of importing Excel data into a MySQL database.
- **Efficiency**: Automates repetitive data entry tasks.
- **Scalability**: Can handle large Excel files and robust database connections.
- **Cross-Platform**: Works on any system with Python and MySQL installed.
- **Secure**: Sensitive credentials are handled securely within the application.

## Prerequisites

- Python 3.10+
- MySQL Server
- Required Python packages:
  - Flask
  - mysql-connector-python
  - pandas

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/mysql-database-connector.git
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd mysql-database-connector
   ```

3. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate # For Linux/Mac
   venv\Scripts\activate   # For Windows
   ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## How to Use

1. **Run the Application**:
   ```bash
   python app.py
   ```

2. **Open in Browser**:
   - Navigate to `http://127.0.0.1:5000/` in your web browser.

3. **Connect to Database**:
   - Enter your MySQL host, username, password, and database name.

4. **Upload Excel File**:
   - Select and upload an Excel file to insert its data into the database.

## License
This project is licensed under the MIT License.

---

Feel free to contribute to this project by submitting issues or pull requests!
