from flask import Flask, redirect, render_template, request, url_for, session
import sqlite3
app = Flask(__name__)
app.secret_key = "ashim_inventory_2024"

def get_db():
    conn = sqlite3.connect("inventory.db")
    conn.row_factory = sqlite3.Row 
    return conn
@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close() 
    return render_template("home.html", products=products)
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone() 
        conn.close()
        if user:
            session["user"] = username  
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid username or password!")
    
    return render_template("login.html")
@app.route("/logout")
def logout():
    session.pop("user", None)  
    return redirect(url_for("login"))
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                          (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except:
            conn.close()
            return render_template("register.html", error="Username already exists!")
    
    return render_template("register.html")
@app.route("/add", methods=["GET", "POST"])
def add():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        quantity = request.form["quantity"]
        price = request.form["price"]
        low_stock_alert = request.form["low_stock_alert"]
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (name, category, quantity, price, low_stock_alert)
            VALUES (?, ?, ?, ?, ?)""",
            (name, category, int(quantity), float(price), int(low_stock_alert)))
        conn.commit()
        conn.close()
        return redirect(url_for("home"))
    return render_template("add.html")
@app.route("/edit/<int:id>")
@app.route("/edit/<int:id>")
def edit(id):
    if "user" not in session:
        return redirect(url_for("login"))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (id,))
    product = cursor.fetchone()
    conn.close()
    return render_template("edit.html", product=product)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    if "user" not in session:
        return redirect(url_for("login"))
    name = request.form["name"]
    category = request.form["category"]
    quantity = request.form["quantity"]
    price = request.form["price"]
    low_stock_alert = request.form["low_stock_alert"]
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE products 
        SET name=?, category=?, quantity=?, price=?, low_stock_alert=?
        WHERE id=?""",
        (name, category, int(quantity), float(price), int(low_stock_alert), id))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))
@app.route("/delete/<int:id>")
def delete(id):
    if "user" not in session:
        return redirect(url_for("login"))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(""" DELETE FROM products 
                   WHERE id = ?""",(id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))
@app.route("/search")
def search():
    query = request.args.get("q")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE name LIKE ?", (f"%{query}%",))
    products = cursor.fetchall()
    conn.close()
    return render_template("home.html", products=products, query=query)

if __name__ == "__main__":
    app.run(debug=True)