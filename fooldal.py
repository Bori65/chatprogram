from flask import Flask, redirect, url_for, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def login():
    return render_template("bejelentkezes2.html")
	
@app.route('/chat')
def chat():
    name = request.args.get('name')
	password = request.args.get('password')
	if name and password:
		return render_template('chat.html', name = name, password = password)
	else:
		return redirect(url_for('login'))

		
if __name__ == "__main__":
	app.run(debug = True)
