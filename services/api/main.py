import uuid
from datetime import datetime

from flask import Flask, request
from flask_cors import CORS

import woody

app = Flask('my_api')
cors = CORS(app)

# redis_db = redis.Redis(host='redis', port=6379, db=0)


@app.get('/api/ping')
def ping():
    return 'ping'


# ### 1. Misc service ### (note: la traduction de miscellaneous est 'divers'
@app.route('/api/misc/time', methods=['GET'])
def get_time():
    return f'misc: {datetime.now()}'


@app.route('/api/misc/heavy/', methods=['GET'])
def get_heavy():
    # TODO TP9: cache ?
    name = request.args.get('name')
    r = woody.make_some_heavy_computation(name)
    return f'{datetime.now()}: {r}'


# ### 2. Product Service ###
@app.route('/api/products', methods=['POST'])
def add_product():
    product = request.json.get('product', '')
    woody.add_product(product)


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    return "not yet implemented"


@app.route('/api/products/last', methods=['GET'])
def get_last_product():
    # TODO TP9: put in cache ? cache duration ?
    last_product = woody.get_last_product()  # note: it's a very slow db query
    return f'db: {datetime.now()} - {last_product}'


# ### 3. Order Service
@app.route('/api/orders', methods=['POST'])
def create_order():
    # very slow process because some payment validation is slow (maybe make it asynchronous ?)
    order = request.get_json()
    order_id = str(uuid.uuid4())

    # TODO TP10: this next line is long, intensive and can be done asynchronously ... maybe use a message broker ?
    process_order(order_id, order)

    return "Your process {order_id} has been created"


@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    status = woody.get_order(order_id)

    return f'order "{order_id}": {status}'


# #### 4. internal Services
def process_order(order_id, order):
    # ...
    # ... do many check and stuff
    status = woody.make_heavy_validation(order)

    woody.save_order(order_id, status, order)


if __name__ == "__main__":
    woody.launch_server(app, host='0.0.0.0', port=5000)
