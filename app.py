from flask import Flask, render_template, request, redirect, url_for
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def size(self):
        return len(self.items)

class FoodSupplyChain:
    def __init__(self):
        self.shipments = Stack()

    def receive_shipment(self, shipment):
        self.shipments.push(shipment)

    def distribute_shipment(self):
        return self.shipments.pop()

    def show_supply_chain(self):
        return list(reversed(self.shipments.items))

    def total_shipments(self):
        return self.shipments.size()

app = Flask(__name__)

supply_chain = FoodSupplyChain()

@app.route('/')
def index():
    shipments = supply_chain.show_supply_chain()
    total = supply_chain.total_shipments()
    message = request.args.get('message')  # Capture the message from query parameters
    return render_template('index.html', shipments=shipments, total=total, message=message)

@app.route('/add_shipment', methods=['POST'])
def add_shipment():
    shipment = request.form['shipment']
    if shipment:
        supply_chain.receive_shipment(shipment)
    return redirect(url_for('index'))

@app.route('/distribute_shipment')
def distribute_shipment():
    distributed_shipment = supply_chain.distribute_shipment()
    if distributed_shipment:
        message = f"Distributed: {distributed_shipment}"
    else:
        message = "No shipments available for distribution."
    return redirect(url_for('index', message=message))


if __name__ == '__main__':
    app.run(debug=True)
