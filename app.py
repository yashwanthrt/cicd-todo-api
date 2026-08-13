from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# In-memory storage (simple for this project)
todos = []
todo_id_counter = 1

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'todo-api'}), 200

@app.route('/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    return jsonify({'todos': todos}), 200

@app.route('/todos', methods=['POST'])
def create_todo():
    """Create a new todo"""
    global todo_id_counter
    
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    new_todo = {
        'id': todo_id_counter,
        'title': data['title'],
        'completed': False
    }
    
    todos.append(new_todo)
    todo_id_counter += 1
    
    return jsonify(new_todo), 201

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Get a specific todo"""
    todo = next((t for t in todos if t['id'] == todo_id), None)
    
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    return jsonify(todo), 200

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update a todo"""
    todo = next((t for t in todos if t['id'] == todo_id), None)
    
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        todo['title'] = data['title']
    if 'completed' in data:
        todo['completed'] = data['completed']
    
    return jsonify(todo), 200

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo"""
    global todos
    
    initial_length = len(todos)
    todos = [t for t in todos if t['id'] != todo_id]
    
    if len(todos) == initial_length:
        return jsonify({'error': 'Todo not found'}), 404
    
    return jsonify({'message': 'Todo deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', False))