from flask import Flask,render_template,flash,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_wtf import FlaskForm,CsrfProtect
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:mysql@localhost:3306/todo_demo?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key="newmore"
db=SQLAlchemy(app)
csrf=CsrfProtect(app)
class AddForm(FlaskForm):
    thing=StringField("事件:",validators=[DataRequired()])
    submit=SubmitField("添加")

class TodoTable(db.Model):
    __tablename__="todo"
    thing_id=db.Column(db.Integer,primary_key=True)
    thing=db.Column(db.String(32),unique=True)
    date=db.Column(db.DateTime,default=datetime.datetime.now())
    is_done=db.Column(db.String(16),default="NO")
    def __repr__(self):
        return "<thing:%s date:%s is_done:%s>"%(self.thing,self.date,self.is_done)

@app.route('/',methods=["POST","GET"])
def hello_world():
    add_form =AddForm()
    todo=TodoTable.query.all()
    if add_form.validate_on_submit():
        data=add_form.thing.data
        print(data)
        new_Todo=TodoTable()
        new_Todo.thing=data
        try:
            db.session.add(new_Todo)
            db.session.commit()
            redirect(url_for("hello_world"))
            print("success")
        except Exception as e:
            print(e)
            db.session.rollback()
    else:
        if request.method=="POST":
            flash("参数不完整请重试")
    return render_template("index.html", todo=todo,add_form=add_form)
@app.route('/delete/<int:id>')
def deleteL(id):
    print(id);
    L=TodoTable.query.get(id)
    try:
        db.session.delete(L)
        db.session.commit()
    except Exception as e:
        print(e)
        flash("删除失败")
        db.session.rollback()
    return redirect(url_for("hello_world"))
@app.route('/change/<int:id>')
def change_statue(id):
    toL=TodoTable.query.get(id)
    if toL.is_done=="NO":
        toL.is_done="YES"
        db.session.commit()
    else:
        toL.is_done="NO"
        db.session.commit()
    return redirect(url_for("hello_world"))


if __name__ == '__main__':
    app.run()
