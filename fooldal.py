from flask import Flask, redirect, url_for, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def login():
    name = request.args.get('name')
    password = request.args.get('password')
    if name and password:
        return render_template('chat.html', name = name, password = password)
    else:
        return render_template("bejelentkezes2.html")


    #return render_template("bejelentkezes2.html")
	
@app.route('/chat/')
def chat():
    name = request.args.get('name')
    password = request.args.get('password')
    print(f"name: {name} password: {password}")
    if name and password:
        return render_template('chat.html', name = name, password = password)
    else:
        return redirect(url_for('regisztracio2'))

		
if __name__ == "__main__":
	app.run(debug = True)
