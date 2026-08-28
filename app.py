from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from datetime import date

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'project_manager_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    search_query = request.args.get('search', '')
    status_filter = request.args.get('status', '')

    cur = mysql.connection.cursor()

    sql = "SELECT * FROM projects WHERE 1=1"
    params = []

    if search_query:
        sql += " AND (client_name LIKE %s OR project_title LIKE %s)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])

    if status_filter:
        sql += " AND status = %s"
        params.append(status_filter)

    sql += " ORDER BY created_at DESC"

    cur.execute(sql, tuple(params))
    projects = cur.fetchall()

    cur.execute("SELECT COUNT(*) AS total FROM projects")
    total = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS completed FROM projects WHERE status = 'completed'")
    completed = cur.fetchone()['completed']

    cur.execute("SELECT COUNT(*) AS in_progress FROM projects WHERE status = 'in-progress'")
    in_progress = cur.fetchone()['in_progress']

    cur.execute("SELECT COUNT(*) AS pending FROM projects WHERE status = 'pending'")
    pending = cur.fetchone()['pending']

    cur.close()

    completion_rate = round((completed / total) * 100) if total > 0 else 0

    return render_template(
        'index.html',
        projects=projects,
        search_query=search_query,
        status_filter=status_filter,
        total=total,
        completed=completed,
        in_progress=in_progress,
        pending=pending,
        completion_rate=completion_rate
    )

@app.route('/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        client_name = request.form['client_name']
        project_title = request.form['project_title']
        dataset_type = request.form['dataset_type']
        status = request.form['status']
        deadline = request.form['deadline'] or None
        notes = request.form['notes']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO projects
            (client_name, project_title, dataset_type, status, deadline, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (client_name, project_title, dataset_type, status, deadline, notes))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    return render_template('add_project.html', today=date.today().isoformat())

@app.route('/edit/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        client_name = request.form['client_name']
        project_title = request.form['project_title']
        dataset_type = request.form['dataset_type']
        status = request.form['status']
        deadline = request.form['deadline'] or None
        notes = request.form['notes']

        cur.execute("""
            UPDATE projects
            SET client_name=%s, project_title=%s, dataset_type=%s,
                status=%s, deadline=%s, notes=%s
            WHERE id=%s
        """, (client_name, project_title, dataset_type, status, deadline, notes, project_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    cur.execute("SELECT * FROM projects WHERE id = %s", (project_id,))
    project = cur.fetchone()
    cur.close()
    return render_template('edit_project.html', project=project)

@app.route('/delete/<int:project_id>')
def delete_project(project_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM projects WHERE id = %s", (project_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)