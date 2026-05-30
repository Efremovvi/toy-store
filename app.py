from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Модели
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, default=0)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Создаем базу данных и тестовые товары
with app.app_context():
    db.create_all()
    
    if Product.query.count() == 0:
        products = [
            Product(name='Медвежонок Бамбл', price=1500, description='Мягкая игрушка 30 см', category='мягкие', stock=10),
            Product(name='Лего Конструктор', price=2500, description='200 деталей', category='конструкторы', stock=5),
            Product(name='Кукла Маша', price=1200, description='С аксессуарами', category='куклы', stock=8),
            Product(name='Мяч футбольный', price=900, description='Размер 4', category='спорт', stock=15),
            Product(name='Пазл 1000 деталей', price=800, description='С животными', category='пазлы', stock=12),
            Product(name='Робот-трансформер', price=3200, description='Свет и звук', category='роботы', stock=3),
        ]
        for p in products:
            db.session.add(p)
        db.session.commit()
        print("База данных создана!")

# Маршруты
@app.route('/')
def index():
    products = Product.query.limit(6).all()
    return render_template('index.html', products=products)

@app.route('/catalog')
def catalog():
    category = request.args.get('category', 'all')
    if category == 'all':
        products = Product.query.all()
    else:
        products = Product.query.filter_by(category=category).all()
    categories = ['все', 'мягкие', 'конструкторы', 'куклы', 'спорт', 'пазлы', 'роботы']
    return render_template('catalog.html', products=products, categories=categories, current_category=category)

@app.route('/product/<int:id>')
def product(id):
    product = Product.query.get_or_404(id)
    return render_template('product.html', product=product)

@app.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    flash('Товар добавлен в корзину!', 'success')
    return redirect(request.referrer or url_for('catalog'))

@app.route('/cart')
def cart():
    cart_items = []
    total = 0
    cart = session.get('cart', {})
    
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart
    flash('Товар удален', 'info')
    return redirect(url_for('cart'))

@app.route('/checkout')
@login_required
def checkout():
    session.pop('cart', None)
    flash('Заказ оформлен! Спасибо за покупку!', 'success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        
        if User.query.filter_by(username=username).first():
            flash('Пользователь уже существует', 'danger')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        
        flash('Регистрация успешна! Войдите в систему', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Добро пожаловать!', 'success')
            return redirect(url_for('index'))
        
        flash('Неверное имя или пароль', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)