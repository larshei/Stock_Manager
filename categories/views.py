from Stock_Manager import app
from categories.models import PartCategory
from flask import render_template, redirect, session, request, url_for, flash

@app.route('/category/showall')
def category_showAll():
    categories = PartCategory.query.order_by(PartCategory.name.asc())
    category_count = PartCategory.query.count()
    return render_template('categories/showAll.html', categories=categories,count=category_count)