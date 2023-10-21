from os import abort
from flask import Flask, jsonify, request

app = Flask(__name__)

# пример базы данных (например список дел)
tasks = [
    {
        'id': 1,
        'title': 'Сходить в ВУЗ',
        'description': 'Посетить пары по математике и программированию',
        'done': False
    },
    {
        'id': 2,
        'title': 'Убраться в доме',
        'description': 'Помыть пол, протереть пыль',
        'done': False
    },
    {
        'id': 3,
        'title': 'Сделать ужин',
        'description': 'Приготовить котлеты',
        'done': False
    }
]

# обработчик для получения списка дел
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

# обработчик для получения определенной задачи
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_specific_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)  # если задача не найдена, возвращаем ошибку 404
    return jsonify({'task': task[0]})

# обработчик для создания новой задачи
@app.route('/api/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400)  # если не указан параметр задачи, возвращаем ошибку 400
    task = {
        'id': tasks[-1]['id'] + 1,  # генерируем новый ID для задачи
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201  # возвращаем созданную задачу и код 201

# обработчик для обновления задачи
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

# обработчик для удаления задачи
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
