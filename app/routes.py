from flask import render_template
from app import functions
from app import app

@app.route('/')
@app.route('/index')
def index():
    stores_list = functions.all_stores
    return render_template('index.html', stores=stores_list)

