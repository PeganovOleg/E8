from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from app import routes, models, forms

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.debug = True
    return app

app = create_app()
db = SQLAlchemy(app)
db.create_all()


@app.route('/', methods=['POST', 'GET'])
def index():
	""" Index page """
	return render_template('index.html')


if __name__ == "__main__":
	app.run(debug=True)