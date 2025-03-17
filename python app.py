from flask import Flask
import os
import subprocess
import pytz
from datetime import datetime

app = Flask(__name__)

@app.route('/htop')
def htop():
    # Hard-coded values per requirement
    full_name = "Gnanavijay"
    system_username = "Gnanavijay Panthagani"
    
    # Get current server time in IST
    ist = pytz.timezone('Asia/Kolkata')
    server_time_ist = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S.%f')
    
    # Get output of the 'top' command
    try:
        top_output = subprocess.check_output(
            ["top", "-b", "-n", "1"], 
            stderr=subprocess.STDOUT
        ).decode("utf-8")
    except subprocess.CalledProcessError as e:
        top_output = f"Failed to get top output:\n{e.output.decode('utf-8')}"
    except FileNotFoundError:
        top_output = "Error: 'top' command not found. Ensure it's available in the environment."
    except Exception as e:
        top_output = f"Unexpected error: {str(e)}"
    
    # Construct the HTML response
    html_response = f"""
    <html>
        <body>
            <h1>Name: {full_name}</h1>
            <h2>Username: {system_username}</h2>
            <h2>Server Time (IST): {server_time_ist}</h2>
            <h3>Top output:</h3>
            <pre>{top_output}</pre>
        </body>
    </html>
    """
    return html_response

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, threaded=True)
    except OSError as e:
        print(f"Error starting server: {e}")
