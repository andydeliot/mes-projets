from flask import Flask
import os


app = Flask(__name__)

@app.route('/')
def index():
    status_fourmizzz = os.popen("journalctl -u fourmizzzing --merge").readlines()
    status_fourmizzz = "<br>".join(status_fourmizzz)
    return status_fourmizzz

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
















