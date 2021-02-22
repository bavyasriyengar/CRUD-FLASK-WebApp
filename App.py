from flask import Flask, render_template,request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import  os


app = Flask(__name__)
app.secret_key = "Secret Key"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///'+ os.path.join(basedir, 'data.db')
#sapp.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amb_id = db.Column(db.Integer)
    queue_id= db.Column(db.Integer)
    amount = db.Column(db.Integer)
    task_count = db.Column(db.Integer)
    state=db.Column(db.Integer)
    reason=db.Column(db.String(100))

    def __init__(self,amb_id,queue_id,amount,task_count,state,reason):
        self.amb_id=amb_id
        self.queue_id=queue_id
        self.amount=amount
        self.task_count=task_count
        self.state=state
        self.reason=reason


#HomePage

@app.route('/')
def Index():
    all_data = Data.query.all()
    return render_template("index.html",records=all_data)

#AddRecords
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        amb_id = request.form['amb_id']
        queue_id = request.form['queue_id']
        state = request.form['state']
        reason = request.form['reason']
        task_count = request.form['task_count']
        amount = 0
        if float(task_count) == 0.5:
            amount = 50
        elif float(task_count) == 1.0:
            amount = 100
        elif float(task_count) == 1.5:
            amount = 150
        elif float(task_count) == 2.0:
            amount = 200
        my_data = Data(amb_id,queue_id,amount,task_count,state,reason)
        db.session.add(my_data)
        db.session.commit()

        flash("Record Inserted Successfully")

        return redirect(url_for('Index'))

#UpdateRecords
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.amb_id = request.form['amb_id']
        my_data.queue_id = request.form['queue_id']
        my_data.amount = request.form['amount']
        my_data.task_count = request.form['task_count']
        my_data.state = request.form['state']
        my_data.reason = request.form['reason']
        db.session.commit()
        flash("Record Updated Successfully!")
        return redirect(url_for('Index'))

#DeletRecords
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Record Deleted Successfully")

    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0',port=3000)


