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

    def get_shipments(self):
        return list(reversed(self.shipments.items))  # Display in LIFO order


app = Flask(__name__)

supply_chain = FoodSupplyChain()

@app.route('/')
def index():
    shipments = supply_chain.get_shipments()
    return render_template('index.html', shipments=shipments)

@app.route('/add_shipment', methods=['POST'])
def add_shipment():
    shipment_name = request.form['shipment']
    if shipment_name:
        supply_chain.receive_shipment(shipment_name)
    return redirect(url_for('index'))

@app.route('/distribute_shipment')
def distribute_shipment():
    distributed_shipment = supply_chain.distribute_shipment()
    if distributed_shipment:
        return f"Distributed: {distributed_shipment}", 200
    return "No shipments available for distribution", 400


if __name__ == '__main__':
    app.run(debug=True)
