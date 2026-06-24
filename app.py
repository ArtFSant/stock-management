from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
import mysql.connector
import datetime

app = Flask(__name__)
app.secret_key = 'secret_key_example_123'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="1234",
        database="stock_db"
    )

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    alert = ''
    if request.method == 'POST' and 'login' in request.form and 'password' in request.form:
        login = request.form['login']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE login = %s AND password = %s', (login, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['name']
            return redirect(url_for('home'))
        else:
            alert = 'Login or Password Incorrect'
    return render_template('login.html', alert=alert)

@app.route('/home', methods=['GET'])
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM products WHERE quantity <= minimal_stock')
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    if products:
        runningout = 'Running out'
        show_p_table = True
    else:
        runningout = 'No products running out on stock'
        show_p_table = False
    return render_template('index.html', products=products, runningout=runningout, show_p_table=show_p_table)

@app.route('/stock', methods=['GET'])
def stock():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('stock.html', products=products)

@app.route('/update-stock', methods=['POST'])
def update_stock():
    product_id = request.form['hidden-id']
    amount = request.form['amount']
    user_id = session['id']
    ac_type = request.form['ac-type']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if ac_type == 'buy':
        update_products = ('UPDATE products SET quantity = quantity + %s WHERE id = %s')
        insert_into_orders = ('INSERT INTO orders (type, quantity, date, users_id, products_id) VALUES (%s, %s, %s, %s, %s)')
        cursor.execute(update_products, (amount, product_id))
        cursor.execute(insert_into_orders, ('buy', amount, datetime.date.today(), user_id, product_id,))
        conn.commit()
        cursor.close()
        conn.close()
    else:
        update_products = ('UPDATE products SET quantity = quantity - %s WHERE id = %s')
        insert_into_orders = ('INSERT INTO orders (type, quantity, date, users_id, products_id) VALUES (%s, %s, %s, %s, %s)')
        cursor.execute(update_products, (amount, product_id))
        cursor.execute(insert_into_orders, ('sell', amount, datetime.date.today(), user_id, product_id,))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('stock'))

if __name__ == '__main__':
    app.run(debug=True)