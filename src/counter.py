from flask import Flask

from src import status

app = Flask(__name__)

COUNTERS = {}


# We will use the app decorator and create a route called slash counters.
# specify the variable in route <name>
# let Flask know that the only methods that is allowed to called
# on this function is "POST".
@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    app.logger.info(f"Request to create counter: {name}")
    global COUNTERS

    if name in COUNTERS:
        return {"Message": f"Counter {name} already exists"}, status.HTTP_409_CONFLICT

    COUNTERS[name] = 0
    return {name: COUNTERS[name]}, status.HTTP_201_CREATED


# this will be the same for everyone
@app.route('/counters/<name>', methods=['PUT'])
def update_counter(name):
    """Update a counter"""
    # create a route for method PUT on endpoint /counters/<name>
    app.logger.info(f"Request to update counter: {name}")

    # create a function to implement that route
    global COUNTERS

    # check if the counter exists
    if name not in COUNTERS:
        return {"Message": f"Counter {name} does not exist"}, status.HTTP_404_NOT_FOUND

    # if the counter does exist, increment it by 1
    COUNTERS[name] += 1

    # return the new counter and a 200_OK return code
    return {name: COUNTERS[name]}, status.HTTP_200_OK


# this will be the same for everyone
@app.route('/counters/<name>', methods=['GET'])
def read_counter(name):
    # create a route for method GET on endpoint /counters/<name>
    app.logger.info(f"Request to read counter: {name}")

    # create a function to implement that route
    global COUNTERS

    # check if the counter exists
    if name not in COUNTERS:
        return {"Message": f"Counter {name} does not exist"}, status.HTTP_404_NOT_FOUND

    # if the counter does exist, read it and return its value and a 200_OK return code
    return {name: COUNTERS[name]}, status.HTTP_200_OK
