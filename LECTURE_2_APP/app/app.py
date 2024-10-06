from azure.cosmos import CosmosClient, exceptions
from flask import Flask, jsonify, request
import os

# Create Flask application
app = Flask(__name__)

# Retrieve Cosmos DB environment variables
cosmosdb_uri = os.getenv('COSMOSDB_URI')
cosmosdb_key = os.getenv('COSMOSDB_PRIMARY_KEY')
database_name = os.getenv('COSMOSDB_DATABASE_NAME')
container_name = "my-container"

# Initialize Cosmos DB client
client = CosmosClient(cosmosdb_uri, credential=cosmosdb_key)
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

# Base route to check API status
@app.route('/')
def home():
    return jsonify({'message': 'API connected to Cosmos DB is running!'})

# Route to insert data into Cosmos DB
@app.route('/items', methods=['POST'])
def create_item():
    try:
        item = request.json
        container.create_item(body=item)
        return jsonify({'message': 'Item created successfully!'}), 201
    except exceptions.CosmosResourceExistsError:
        return jsonify({'error': 'Item already exists!'}), 409

# Route to list all items in Cosmos DB
@app.route('/items', methods=['GET'])
def list_items():
    query = "SELECT * FROM c"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    return jsonify(items)

# Route to retrieve a specific item by ID
@app.route('/items/<item_id>', methods=['GET'])
def get_item(item_id):
    try:
        item = container.read_item(item=item_id, partition_key=item_id)
        return jsonify(item)
    except exceptions.CosmosResourceNotFoundError:
        return jsonify({'error': 'Item not found!'}), 404

# Route to update an item by ID
@app.route('/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    try:
        item = container.read_item(item=item_id, partition_key=item_id)
        updated_data = request.json
        for key in updated_data:
            item[key] = updated_data[key]
        container.upsert_item(body=item)
        return jsonify({'message': 'Item updated successfully!'})
    except exceptions.CosmosResourceNotFoundError:
        return jsonify({'error': 'Item not found!'}), 404

# Route to delete an item by ID
@app.route('/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        container.delete_item(item=item_id, partition_key=item_id)
        return jsonify({'message': 'Item deleted successfully!'})
    except exceptions.CosmosResourceNotFoundError:
        return jsonify({'error': 'Item not found!'}), 404

# Start the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
