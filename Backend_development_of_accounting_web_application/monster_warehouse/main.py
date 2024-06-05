from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

monsters = [
    {
        'flavor': 'Original',
        'batches': [
            {'price per unit': 2.0, 'quantity': 50}
        ]
    },
    {
        'flavor': 'Passionfruit',
        'batches': [
            {'price per unit': 2.5, 'quantity': 30}
        ]
    },
    {
        'flavor': 'Mango',
        'batches': [
            {'price per unit': 2.5, 'quantity': 30}
        ]
    },
    {
        'flavor': 'Kiwi',
        'batches': [
            {'price per unit': 3.0, 'quantity': 20}
        ]
    },
    {
        'flavor': 'Citrus',
        'batches': [
            {'price per unit': 3.5, 'quantity': 15}
        ]
    }
]

current_balance = 1000.0 # initial balance with a default value

history = []

@app.route('/')
def index():
    return render_template('index.html', monsters=monsters, balance=current_balance)

@app.route('/balance')
def balance_view():
    global current_balance
    return render_template('balance.html', balance=current_balance)

@app.route('/submit_balance', methods=['POST'])
def submit_balance():
    global current_balance # Ensure can modify the global balance variable
    operation = request.form.get('operation')
    amount = float(request.form.get('amount'))

    if operation == 'add':
        current_balance += amount
        history.append({'timestamp': datetime.now(), 'operation': 'add', 'total_amount': amount})
    elif operation == 'substract':
        current_balance -= amount
        history.append({'timestamp': datetime.now(), 'operation': 'substract', 'total_amount': amount})    

    print(f"Updated balance: {current_balance}")
    return redirect('/')

@app.route('/purchase')
def purchase():
    return render_template('purchase.html', balance=current_balance)

@app.route('/submit_purchase', methods=['POST'])
def submit_purchase():
    global current_balance
    flavor = request.form.get('flavor')
    price_per_unit = float(request.form.get('price per unit'))
    quantity = int(request.form.get('quantity'))
    total_amount = price_per_unit * quantity
    current_balance -= total_amount

    print(f"Received purchase request: flavor={flavor}, price_per_unit={price_per_unit}, quantity={quantity}")

    # Search the flavor in the monsters list
    for monster in monsters:
        if monster['flavor'] == flavor:
            monster['batches'].append({'price per unit': price_per_unit, 'quantity': quantity})
            break
    else:
        return "Flavor not found in the list"

    print("Current monsters list:", monsters)
    history.append({'timestamp': datetime.now(), 'operation': 'purchase', 'flavor': flavor, 'price_per_unit': price_per_unit, 'quantity': quantity, 'total_amount': total_amount})

    return redirect('/')

@app.route('/sale')
def sale():
    return render_template('sale.html', balance=current_balance)

@app.route('/submit_sale', methods=['POST'])
def submit_sale():
    global current_balance
    flavor = request.form.get('flavor')
    price_per_unit = float(request.form.get('price per unit'))
    quantity = int(request.form.get('quantity'))

    print(f"Received sale request: flavor={flavor}, price_per_unit={price_per_unit}, quantity={quantity}")

    # Search the flavor in the monsters list
    for monster in monsters:
        if monster['flavor'] == flavor:
            total_quantity = sum(batch['quantity'] for batch in monster['batches'])
            if total_quantity >=quantity:
                total_amount = price_per_unit * quantity
                current_balance += total_amount
                for batch in monster['batches']:
                    if batch['quantity'] >= quantity:
                        batch['quantity'] -= quantity
                        break
                    else:
                        quantity -= batch['quantity']
                        batch['quantity'] = 0
                break
            else:
                return "Not enough quantity to sell"   
    else:
        return "Flavor not found in the list"

    print("Current monsters list:", monsters)
    history.append({'timestamp': datetime.now(), 'operation': 'sale', 'flavor': flavor, 'price_per_unit': price_per_unit, 'quantity': quantity, 'total_amount': total_amount})
    return redirect('/')

@app.route('/history')
def history_view():
    for entry in history:
        entry['timestamp'] = entry['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    
    return render_template('history.html', balance=current_balance, history=history)

if __name__ =="__main__":
    app.run(debug=True, port=5500)


