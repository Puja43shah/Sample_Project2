from flask import Flask, render_template, abort, request, redirect, url_for
from db_connect import connection
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    if request.method=='POST':
        s_name = request.form.get('student_name')
        s_dob = request.form.get('student_dob')
        s_email = request.form.get('student_email')
        with connection.cursor() as cur:
            sql_stmt = "INSERT INTO student (student_name,student_dob,student_email) values (?,?,?)"
            cur.execute(sql_stmt,(s_name,s_dob,s_email))
            connection.commit()
        return redirect(url_for('index'))
    
    with connection.cursor() as cur:
        cur.execute("SELECT * FROM student")
        res = cur.fetchall()
    return render_template('index.html',student_details=res)

@app.route("/student/<int:student_id>")
def get_student_detail(student_id):
    with connection.cursor() as cur:
        cur.execute("select * from student where id=?",(student_id,))
        res = cur.fetchone()
        if res:
            return render_template('student_detail.html',student=res)
        else:
            abort(404)

@app.route("/delete/<int:student_id>")
def delete_student(student_id):
    with connection.cursor() as cur:
        cur.execute("select * from student where id=?",(student_id,))
        res = cur.fetchone()
        if res:
            cur.execute("DELETE FROM student where id=?",(student_id,))
            connection.commit()
            return redirect(url_for('index'))
        else:
            abort(400)

@app.route("/edit/<int:student_id>",methods=["GET","POST"])
def update_student(student_id):
    if request.methods=="POST":
        s_name = request.form.get('student_name')
        s_dob = request.form.get('student_dob')
        s_email = request.form.get('student_email')
        with connection.cursor() as cur:
            cur.execute("update student set student_name=?,student_dob=?, student_email=?", s_name, s_dob, s_email,student_id)
            connection.commit()
        return redirect(url_for('index'))    
    

    with connection.cursor() as cur:
        cur.execute("select * from student where id=?",(student_id,))
        student = cur.fetchone()

    if student:
        return render_template('edit.html',student=student)
    else:abort(400)
        

if __name__=='__main__':
    app.run(debug=True)

    