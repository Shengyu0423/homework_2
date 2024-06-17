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

# Database model for Balance
class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False, default=0.0)

# Database model for History
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    operation = db.Column(db.String(50), nullable=False)
    flavor = db.Column(db.String(50))
    price_per_unit = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    total_amount = db.Column(db.Float)

@app.route('/')
def index():
    monsters = Monster.query.all()
    balance = Balance.query.first()
    return render_template('index.html', monsters=monsters, balance=balance.amount)

@app.route('/balance')
def balance_view():
    balance = Balance.query.first()
    return render_template('balance.html', balance=balance.amount)

@app.route('/submit_balance', methods=['POST'])
def submit_balance():
    balance = Balance.query.first()
    operation = request.form.get('operation')
    amount = float(request.form.get('amount'))

    if operation == 'add':
        balance.amount += amount
        timestamp = datetime.now()
        history_record = History(timestamp=timestamp, operation='add', total_amount=amount)
        db.session.add(history_record)
    elif operation == 'substract':
        balance.amount -= amount
        timestamp = datetime.now()
        history_record = History(timestamp=timestamp, operation='substract', total_amount=amount)
        db.session.add(history_record)

    db.session.commit()    

    return redirect(url_for('index'))

@app.route('/purchase')
def purchase():
    balance = Balance.query.first()
    return render_template('purchase.html', balance=balance.amount)

@app.route('/submit_purchase', methods=['POST'])
def submit_purchase():
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
    balance = Balance.query.first()
    
    # Check if the balance is enough to purchase
    if balance.amount < total_amount:
        return "Not enough balance to purchase", 400
    
    balance.amount -= total_amount

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

    timestamp = datetime.now()
    history_record = History(timestamp=timestamp, operation='purchase', flavor=flavor, price_per_unit=price_per_unit, quantity=quantity, total_amount=total_amount)
    db.session.add(history_record)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/sale')
def sale():
    balance = Balance.query.first()
    return render_template('sale.html', balance=balance.amount)

@app.route('/submit_sale', methods=['POST'])
def submit_sale():
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
        return "Invalid price per unit or quantity. Please enter a valid number"
    
    balance = Balance.query.first()

    # Check if the flavor exists in the database
    monster = Monster.query.filter_by(flavor=flavor).first()
    if monster and monster.quantity >= quantity:
        total_amount = price_per_unit * quantity
        balance.amount += total_amount
        monster.quantity -= quantity
        db.session.commit()

        timestamp = datetime.now()
        history_record = History(timestamp=timestamp, operation='sale', flavor=flavor, price_per_unit=price_per_unit, quantity=quantity, total_amount=total_amount)
        db.session.add(history_record)
        db.session.commit()

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

    # Initialize query
    history_query = History.query

    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            history_query = history_query.filter(History.timestamp >= start_date)
        except ValueError:
            pass

    if end_date:
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            history_query = history_query.filter(History.timestamp <= end_date)
        except ValueError:
            pass

    if operation:
        history_query = history_query.filter_by(operation=operation)

    if flavor:
        history_query = history_query.filter(History.flavor.ilike(f"%{flavor}%"))

    if price_per_unit:
        try:
            price_per_unit = float(price_per_unit)
            history_query = history_query.filter_by(price_per_unit=price_per_unit)
        except ValueError:
            pass

    if quantity:
        try:
            quantity = int(quantity)
            history_query = history_query.filter_by(quantity=quantity)
        except ValueError:
            pass

    if total_amount:
        try:
            total_amount = float(total_amount)
            history_query = history_query.filter_by(total_amount=total_amount)
        except ValueError:
            pass
        
    balance = Balance.query.first()    
    return render_template('history.html', balance=balance.amount, history=history_query.all())

# Create the database and the db table
with app.app_context():
    db.create_all()

    # Initialize the balance if it does not exist
    if not Balance.query.first():
        balance = Balance(amount=0.0)
        db.session.add(balance)
        db.session.commit()

if __name__ =="__main__":
    app.run(debug=True, port=5500)




