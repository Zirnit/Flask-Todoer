from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from Todo.auth import login_required
from Todo.db import get_db

bp = Blueprint("todo", __name__)

@bp.route("/")
@login_required
def index():
    db, c = get_db()
    c.execute(
        'SELECT t.id, t.description, u.username, t.completed, t.created_at FROM todo t JOIN user u ON t.created_by=u.id ORDER BY created_at DESC'
    )
    todos = c.fetchall()
    return render_template("todo/index.html", todos=todos)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        description = request.form['description']
        error = None
        if not description:
            error='La descripción es requerida'
        if error is not None:
            flash(error)
        else:
            db, c=get_db()
            c.execute(
                'INSERT INTO todo (description, completed, created_by)'
                ' values(%s, %s, %s)',
                (description, False, g.user['id'])
            )
            db.commit()
            return redirect(url_for('todo.index'))
    return render_template('todo/create.html')

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    return render_template('todo/update.html', todo={
        "description" : "Mi todo",
        "id" : 2,
        "completed" : 0
    })

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete():
    return ""#render_template('todo/delete.html', todo=todo)
    