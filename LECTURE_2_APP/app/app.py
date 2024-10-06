from azure.cosmos import CosmosClient, exceptions
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

cosmosdb_uri = os.getenv('COSMOSDB_URI')
cosmosdb_key = os.getenv('COSMOSDB_PRIMARY_KEY')
database_name = os.getenv('COSMOSDB_DATABASE_NAME')
container_name = "my-container"

client = CosmosClient(cosmosdb_uri, credential=cosmosdb_key)
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

@app.route('/')
def home():
    return jsonify({'message': 'API connected to Cosmos DB is running!'})

@app.route('/items', methods=['POST'])
def create_item():
    try:
        item = request.json
        container.create_item(body=item)
        return jsonify({'message': 'Item created successfully!'}), 201
    except exceptions.CosmosResourceExistsError:
        return jsonify({'error': 'Item already exists!'}), 409

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443)
