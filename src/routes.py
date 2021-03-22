from src import app
from flask import render_template, url_for, flash, redirect
from src.forms import RegistrationForm, LoginForm, SearchForm
from src.models import User


results = [
    {
        'title': 'Laptop Stand for desk, Detachable Laptop Riser Notebook Holder Stand Ergonomic Aluminum Laptop '
                 'Mount Computer Stand, Compatible with MacBook Air Pro, Dell XPS, Lenovo More 10-18" Laptops  ',
        'price': '$22.99',
        'rating': '4.6/5',
        'url': 'https://www.amazon.com/Detachable-Notebook-Ergonomic-Aluminum-Compatible/dp/B08DD82FRR/ref=sr_1_3'
               '?dchild=1&keywords=notebook+stand&qid=1616432225&sr=8-3',
        'short_url': 'https://www.amazon.com/'
    },
    {
        'title': 'Global ROM Oneplus 8 5G Mobile Phone 12GB 256GB /8GB 128GB 6.55" 90Hz Snapdragon 865 48MP 30W '
                 '4300mAh NFC 5G Smartphone',
        'price': '$485.56 - 559.56',
        'rating': '4.6/5',
        'url': 'https://www.aliexpress.com/item/4001263945664.html?spm=a2g0o.productlist.0.0.4e222876npEmQo&algo_pvid'
               '=44651afa-e2e7-48a1-b206-6d7e416144d5&algo_expid=44651afa-e2e7-48a1-b206-6d7e416144d5-0&btsid'
               '=0bb0623a16164323935431321ec84e&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_',
        'short_url': 'https://www.aliexpress.com/'
    },
    {
        'title': 'Monitor “Acer EK220Q”',
        'price': '185AZN',
        'rating': '0',
        'url': 'https://tap.az/elanlar/elektronika/komputer-avadanliqi/21120675',
        'short_url': 'https://www.tap.az/'
    }
]


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
    return render_template('search.html', title='Search', form=form, res=results)


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

