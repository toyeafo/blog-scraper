from flask import Flask, render_template, request
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/scrape', methods=['POST'])
def scrape():
    # Get start url from form
    start_url = request.form['start_url']

    print(f"Start URL submitted through form: {start_url}")

    return

if __name__ == '__main__':
    app.run(debug=True)