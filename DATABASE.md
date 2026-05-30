# База данных интернет-магазина игрушек

## 📊 Общая информация

- **Тип БД:** SQLite
- **Файл:** `shop.db`
- **ORM:** SQLAlchemy
- **Автоматическое создание:** Да (при первом запуске)

## 🗂️ Структура таблиц

### Таблица `User` (пользователи)
Хранит информацию о зарегистрированных пользователях.

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | Integer | Уникальный идентификатор (первичный ключ) |
| `username` | String(80) | Имя пользователя (уникальное) |
| `email` | String(120) | Email адрес (уникальный) |
| `password` | String(200) | Хэшированный пароль |

### Таблица `Product` (товары)
Хранит информацию о товарах в магазине.

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | Integer | Уникальный идентификатор (первичный ключ) |
| `name` | String(100) | Название товара |
| `price` | Float | Цена в рублях |
| `description` | Text | Описание товара |
| `category` | String(50) | Категория товара |
| `stock` | Integer | Количество на складе |

### Таблица `Order` (заказы)
Хранит информацию о заказах пользователей.

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | Integer | Уникальный идентификатор (первичный ключ) |
| `user_id` | Integer | ID пользователя (внешний ключ → User) |
| `total` | Float | Общая сумма заказа |
| `status` | String(20) | Статус заказа (pending/completed) |
| `created_at` | DateTime | Дата и время создания |

### Таблица `OrderItem` (товары в заказе)
Хранит информацию о товарах в каждом заказе.

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | Integer | Уникальный идентификатор (первичный ключ) |
| `order_id` | Integer | ID заказа (внешний ключ → Order) |
| `product_id` | Integer | ID товара (внешний ключ → Product) |
| `quantity` | Integer | Количество товара |
| `price` | Float | Цена товара в момент заказа |

## 🔗 Связи между таблицами


## 📦 Тестовые данные

При первом запуске автоматически создаются следующие товары:

| ID | Название | Цена | Категория | В наличии |
|----|----------|------|-----------|-----------|
| 1 | Медвежонок Бамбл | 1500 ₽ | мягкие | 10 шт |
| 2 | Лего Конструктор | 2500 ₽ | конструкторы | 5 шт |
| 3 | Кукла Маша | 1200 ₽ | куклы | 8 шт |
| 4 | Мяч футбольный | 900 ₽ | спорт | 15 шт |
| 5 | Пазл 1000 деталей | 800 ₽ | пазлы | 12 шт |
| 6 | Робот-трансформер | 3200 ₽ | роботы | 3 шт |

## 🛠️ Полезные SQL-запросы

### Показать все товары:
```sql
SELECT * FROM Product;

SELECT name, price FROM Product WHERE price > 1000;

SELECT * FROM Product WHERE category = 'мягкие';

SELECT category, COUNT(*) as count FROM Product GROUP BY category;

SELECT u.username, o.total, o.created_at 
FROM Order o 
JOIN User u ON o.user_id = u.id 
ORDER BY o.created_at DESC 
LIMIT 5;

from app import Product, app

with app.app_context():
    products = Product.query.all()
    for p in products:
        print(f"{p.name} - {p.price}₽")

from app import db, Product

with app.app_context():
    new_product = Product(
        name='Новая игрушка',
        price=1000,
        description='Описание',
        category='мягкие',
        stock=10
    )
    db.session.add(new_product)
    db.session.commit()

from app import User

with app.app_context():
    user = User.query.filter_by(username='admin').first()
    if user:
        print(f"Найден: {user.email}")
   