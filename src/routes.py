from src import app
from flask import render_template, url_for, flash, redirect, request
from src.forms import RegistrationForm, LoginForm, SearchForm
# from src.extractor.scraper_tapaz import Scrape_tapaz
# from src.extractor.scraper_amazon import Scrape_amazon
from src.extractor.distributor import Distributor


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    mode = 'fast'
    item = form.item.data
    min_price = form.min_price.data
    max_price = form.max_price.data
    sort_option = None
    currency = None
    websites = [
        i
        for i in ['amazon', 'tapaz', 'aliexpress']
        if request.form.getlist(i) == ['on']
    ]

    if request.method == 'POST':
        sort_option = request.form['sort']
        currency = request.form['currency']

    products_api = Distributor(websites=websites, mode=mode, item=item, timeout=0.4, min_price=min_price,
                               max_price=max_price, sort_option=sort_option, currency=currency).get_apis()

    return render_template('search.html', title='Search', form=form, products_api=products_api)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)
