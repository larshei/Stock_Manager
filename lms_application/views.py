from Stock_Manager import app, db
from part_mng.forms import PartAddForm
from part_mng.models import Part
from package_mng.models import Package
from flask import render_template, redirect, session, request, url_for, flash

@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")