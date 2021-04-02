import os
from src import app
from flask import render_template, url_for, flash, redirect, send_from_directory
from src.forms import RegistrationForm, LoginForm, SearchForm
from src.extractor.scraper_tapaz import Scrape


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    item = form.item.data
    if item:
        scraper = Scrape(form.item.data, 0.4)
        products_api = scraper.api_generator()
    else:
        products_api = []
    return render_template('search.html', title='Search', form=form, products_api=products_api)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
