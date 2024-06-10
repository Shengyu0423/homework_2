from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monster_warehouse.db'
db = SQLAlchemy(app)

# Database model for Monster
class Monster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flavor = db.Column(db.String(50), nullable=False)
    price_per_unit = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Global variable for balance and history
current_balance = 1000.0 # initial balance with a default value
history = []

@app.route('/')
def index():
    monsters = Monster.query.all()
    return render_template('index.html', monsters=monsters, balance=current_balance)

@app.route('/balance')
def balance_view():
    global current_balance
    return render_template('balance.html', balance=current_balance)

@app.route('/submit_balance', methods=['POST'])
def submit_balance():
    global current_balance
    operation = request.form.get('operation')
    amount = float(request.form.get('amount'))

    if operation == 'add':
        current_balance += amount
        history.append({'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'operation': 'add', 'total_amount': amount})
    elif operation == 'substract':
        current_balance -= amount
        history.append({'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'operation': 'substract', 'total_amount': amount})    

    return redirect(url_for('index'))

@app.route('/purchase')
def purchase():
    return render_template('purchase.html', balance=current_balance)

@app.route('/submit_purchase', methods=['POST'])
def submit_purchase():
    global current_balance
    flavor = request.form.get('flavor')
    price_per_unit = request.form.get('price per unit')
    quantity = request.form.get('quantity')

    # Validate the input
    if not flavor.isalpha() or not flavor.replace(' ', '').isalpha():
        return "Invalid flavor. Flavor should only contain alphabets.", 400
    try:
        price_per_unit = float(price_per_unit)
        quantity = int(quantity)
        if price_per_unit <= 0 or quantity <= 0:
            return "Price per unit and quantity should be greater than 0.", 400
    except ValueError:
        return "Invalid price per unit or quantity. Please enter a valid number", 400
    
    total_amount = price_per_unit * quantity
    current_balance -= total_amount

    # Check if the flavor exists in the database
    monster = Monster.query.filter_by(flavor=flavor).first()
    if monster:
        # Update existing monster
        monster.quantity += quantity
    else:
        # Add new monster
        new_monster = Monster(flavor=flavor, price_per_unit=price_per_unit, quantity=quantity)
        db.session.add(new_monster)
    
    db.session.commit()

    history.append({'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'operation': 'purchase', 'flavor': flavor, 'price_per_unit': price_per_unit, 'quantity': quantity, 'total_amount': total_amount})
    return redirect(url_for('index'))

@app.route('/sale')
def sale():
    return render_template('sale.html', balance=current_balance)

@app.route('/submit_sale', methods=['POST'])
def submit_sale():
    global current_balance
    flavor = request.form.get('flavor')
    price_per_unit = float(request.form.get('price per unit'))
    quantity = int(request.form.get('quantity'))

    # Validate the input
    if not flavor.isalpha() or not flavor.replace(' ', '').isalpha():
        return "Invalid flavor. Flavor should only contain alphabets.", 400
    try:
        price_per_unit = float(price_per_unit)
        quantity = int(quantity)
        if price_per_unit <= 0 or quantity <= 0:
            return "Price per unit and quantity should be greater than 0.", 400
    except ValueError:
        return "Invalid price per unit or quantity. Please enter a valid number"

    # Check if the flavor exists in the database
    monster = Monster.query.filter_by(flavor=flavor).first()
    if monster and monster.quantity >= quantity:
        total_amount = price_per_unit * quantity
        current_balance += total_amount
        monster.quantity -= quantity
        db.session.commit()

        history.append({'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'operation': 'sale', 'flavor': flavor, 'price_per_unit': price_per_unit, 'quantity': quantity, 'total_amount': total_amount})
        return redirect('/')
    else:
        return "Flavor not found or not enough quantity to sell", 400

@app.route('/history')
def history_view():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    operation = request.args.get('operation')
    flavor = request.args.get('flavor')
    price_per_unit = request.args.get('price_per_unit')
    quantity = request.args.get('quantity')
    total_amount = request.args.get('total_amount')

    # Initialize filtered_history
    filtered_history = history

    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            filtered_history = [record for record in filtered_history if datetime.strptime(record['timestamp'], "%Y-%m-%d %H:%M:%S") >= start_date]
        except ValueError:
            pass

    if end_date:
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            filtered_history = [record for record in filtered_history if datetime.strptime(record['timestamp'], "%Y-%m-%d %H:%M:%S") <= end_date]
        except ValueError:
            pass

    if operation:
        filtered_history = [record for record in filtered_history if record['operation'] == operation]

    if flavor:
        filtered_history = [record for record in filtered_history if record.get('flavor') and flavor.lower() in record['flavor'].lower()]

    if price_per_unit:
        try:
            price_per_unit = float(price_per_unit)
            filtered_history = [record for record in filtered_history if record.get('price_per_unit') and record['price_per_unit'] == price_per_unit]
        except ValueError:
            pass

    if quantity:
        try:
            quantity = int(quantity)
            filtered_history = [record for record in filtered_history if record.get('quantity') and record['quantity'] == quantity]
        except ValueError:
            pass

    if total_amount:
        try:
            total_amount = float(total_amount)
            filtered_history = [record for record in filtered_history if record.get('total_amount') == total_amount]
        except ValueError:
            pass

    return render_template('history.html', balance=current_balance, history=filtered_history)

# Create the database and the db table
with app.app_context():
    db.create_all()

if __name__ =="__main__":
    app.run(debug=True, port=5500)



