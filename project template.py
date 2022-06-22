import sys

from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
# moment = Moment(app)
# db = db_setup(app)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Enable debug mode.
app.config['DEBUG'] = True

db = SQLAlchemy(app)
Migrate(app, db)


# def db_setup(app):
#     app.config.from_object('config')
#     db.app = app
#     db.init_app(app)
#     migration = Migrate(app, db)
#     return db


# class Person(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(), nullable=False)
#     description = db.Column(db.String(), nullable=False)
#     completed = db.Column(db.Boolean, nullable=True)
#
#     def __int__(self, id, name, description, completed):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.completed = completed
#
#     def __repr__(self):
#         return f' {self.id} {self.name}'


class Todolist(db.Model):
    __tablename__ = 'todolist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    todos = db.relationship('Todo', backref='list', lazy=True)


class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolist.id'), nullable=False)

    def __int__(self, id, description, completed):
        self.id = id
        self.description = description
        self.completed = completed

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


@app.route('/todos/update/<todo_id>/set-complete', methods=['POST'])
def update_todo(todo_id):
    error = False
    try:
        complete = request.get_json()['complete']
        todo = Todo.query.get(todo_id)
        print('Todo: ', todo)
        todo.complete = complete
        db.session.commit()
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return redirect(url_for('create'))


@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        # Todo.query.filter_by(id=todo_id).delete()
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    return jsonify({'success': True})


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    error = False
    try:
        completed = request.get_json()['completed']
        print('completed', completed)
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return '', 200
    # return redirect(url_for('create'))


@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    lists = Todolist.query.all()
    active_list = Todolist.query.get(list_id)
    todos = Todo.query.filter_by(list_id=list_id).order_by('id').all()
    return render_template('create.html', todos=todos, lists=lists, active_list=active_list)


@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']
        todo = Todo(description=description, list_id=list_id, completed=False)
        db.session.add(todo)
        db.session.commit()
        body['id'] = todo.id
        body['completed'] = todo.completed
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)


@app.route('/lists/create', methods=['POST'])
def create_list():
    error = False
    body = {}
    try:
        name = request.get_json()['name']
        todolist = Todolist(name=name)
        db.session.add(todolist)
        db.session.commit()
        body['id'] = todolist.id
        body['name'] = todolist.name
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info)
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify(body)


@app.route('/lists/<list_id>/delete', methods=['DELETE'])
def delete_list(list_id):
    error = False
    try:
        list = Todolist.query.get(list_id)
        for todo in list.todos:
            db.session.delete(todo)

        db.session.delete(list)
        db.session.commit()
    except():
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({'success': True})


@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('create.html',
                           lists=Todolist.query.all(),
                           active_list=Todolist.query.get(list_id),
                           todos=Todo.query.filter_by(list_id=list_id).order_by('id').all()
                           )


@app.route('/lists/<list_id>/set-completed', methods=['POST'])
def set_completed_list(list_id):
    error = False
    try:
        list = Todolist.query.get(list_id)
        for todo in list.todos:
            todo.completed = True
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return '', 200


@app.route('/')
def create():
    return redirect(url_for('get_list_todos', list_id=1))


if __name__ == '__main__':
    # app.run(host="0.0.0.0")
    app.run()
