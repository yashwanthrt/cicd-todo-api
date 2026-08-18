from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
import os

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

# In-memory storage (simple for this project)
todos = []
todo_id_counter = 1

def reset_todos():
    """Reset todos for testing"""
    global todos, todo_id_counter
    todos = [
        {
            'id': 1,
            'title': 'Test Todo',
            'completed': True
        }
    ]
    todo_id_counter = 1

@app.route('/', methods=['GET'])
def health_check():
    """
    Health check endpoint
    ---
    responses:
      200:
        description: Service is healthy
        schema:
          properties:
            status:
              type: string
            service:
              type: string
    """
    return jsonify({'status': 'healthy', 'service': 'todo-api'}), 200

@app.route('/todos', methods=['GET'])
def get_todos():
    """
    Get all todos
    ---
    responses:
      200:
        description: List of all todos
        schema:
          properties:
            todos:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  title:
                    type: string
                  completed:
                    type: boolean
            count:
              type: integer
    """
    if len(todos) == 0:
        reset_todos()

    return jsonify({'todos': todos, 'count': len(todos)}), 200

@app.route('/todos', methods=['POST'])
def create_todo():
    """
    Create a new todo
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            title:
              type: string
              example: "Learn github CI/CD"
    responses:
      201:
        description: Todo created successfully
        schema:
          properties:
            id:
              type: integer
            title:
              type: string
            completed:
              type: boolean
      400:
        description: Missing title field
    """
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
    """
    Get a specific todo
    ---
    parameters:
      - name: todo_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Todo found
        schema:
          properties:
            id:
              type: integer
            title:
              type: string
            completed:
              type: boolean
      404:
        description: Todo not found
    """
    todo = next((t for t in todos if t['id'] == todo_id), None)
    
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    return jsonify(todo), 200

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """
    Update a todo
    ---
    parameters:
      - name: todo_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        schema:
          properties:
            title:
              type: string
            completed:
              type: boolean
    responses:
      200:
        description: Todo updated successfully
        schema:
          properties:
            id:
              type: integer
            title:
              type: string
            completed:
              type: boolean
      404:
        description: Todo not found
    """
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
    """
    Delete a todo
    ---
    parameters:
      - name: todo_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Todo deleted successfully
      404:
        description: Todo not found
    """
    global todos
    
    initial_length = len(todos)
    todos = [t for t in todos if t['id'] != todo_id]
    
    if len(todos) == initial_length:
        return jsonify({'error': 'Todo not found'}), 404
    
    return jsonify({'message': 'Todo deleted successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('FLASK_DEBUG', False))