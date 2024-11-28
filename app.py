from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

DATABASE = 'students.db'

# Database connection function
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

@app.route('/')
def index():
    if 'username' in session:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students')
        students = cursor.fetchall()
        conn.close()
        return render_template('index.html', students=students)
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_student():
    if 'username' in session:
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        course = request.form['course']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO students (name, email, phone, course) VALUES (?, ?, ?, ?)', 
                       (name, email, phone, course))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/delete/<int:id>')
def delete_student(id):
    if 'username' in session:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    if 'username' in session:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            course = request.form['course']

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE students
                SET name = ?, email = ?, phone = ?, course = ?
                WHERE id = ?
            ''', (name, email, phone, course, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        else:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM students WHERE id = ?', (id,))
            student = cursor.fetchone()
            conn.close()
            return render_template('update.html', student=student)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            session['role'] = user['role']
            return redirect(url_for('index'))
        else:
            return "Invalid credentials, please try again."

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
