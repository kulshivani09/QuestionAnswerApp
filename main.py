from flask import Flask,render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import date
from flask_migrate import Migrate
from flask_login import UserMixin,login_user,login_required,logout_user,current_user,LoginManager

app=Flask(__name__)
app.secret_key = 'srpilusm'
app.config['SQLALCHEMY_DATABASE_URI']=f"postgresql://{'postgres'}:{'Shiva09'}@{'localhost'}:{'5432'}/{'questionanswer'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='secret key'
db=SQLAlchemy(app)
migrate=Migrate(app,db)


#flask_login stuff
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(email_id):
    return User.query.get(email_id)


class User(db.Model,UserMixin):
    __tablename__='User'
    email=db.Column(db.String(50),primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(50),nullable=False)
    date_registered=db.Column(db.Date)
    questions=db.relationship('Questions',backref='user',cascade='all, delete-orphan')

    def get_id(self):
        return str(self.email)

    def __init__(self,email,name,password):
        self.email=email
        self.name=name
        self.password=password
        self.date_registered=date.today()

class Questions(db.Model):
    __tablename__ ='Questions'
    ques_id=db.Column(db.Integer,primary_key=True)
    description=db.Column(db.String(600),nullable=False)
    ques_posted_date=db.Column(db.Date)
    email=db.Column(db.String(50),db.ForeignKey('User.email'),nullable=False)
    answers=db.relationship('Answers',backref='questions',cascade='all, delete-orphan')

    def __init__(self,description,email):
        self.description=description
        self.ques_posted_date=date.today()
        self.email=email

class Answers(db.Model):
    __tablename__ ='Answers'
    ans_id=db.Column(db.Integer,primary_key=True)
    ans_desc=db.Column(db.String(600),nullable=False)
    ans_posted_date=db.Column(db.Date)
    posted_by=db.Column(db.String(600))
    ques_id=db.Column(db.Integer,db.ForeignKey('Questions.ques_id'),nullable=False)

    def __init__(self,ans_desc,posted_by,ques_id):
        self.ans_desc=ans_desc
        self.ans_posted_date=date.today()
        self.posted_by=posted_by
        self.ques_id=ques_id

#login
@app.route("/login",methods=['GET','POST'])
def login():
    try:
        if request.method=='POST':
            email=request.form['email_id']
            password=request.form['password']
            user=User.query.get(email)
            if user is not None:
                if user.password==password:
                    login_user(user)
                    return redirect(url_for('homepage'))
                else:
                    flash("Please enter correct password..")
            else:
                flash("User is not registered..Please register to login")
    except Exception as e:
        print(e)
    return render_template('login.html')

#register
@app.route("/register",methods=['GET','POST'])
def register():
    try:
        if request.method=='POST':
            email=request.form['email_id']
            name=request.form['full_name']
            password=request.form['password']
            user=User.query.get(email)
            if user is not None:
                flash('User already exists with this mail id')
            else:
                user1=User(email,name,password)
                print(user1.name)
                db.session.add(user1)
                db.session.commit()
                flash('Registration successful! You can now log in.', 'success')
                return render_template('login.html')
    except IntegrityError as e:
        flash('User already exists with this mail id', 'error')
    
    return render_template('register.html')

#add question
@app.route("/addQuestion",methods=['GET','POST']) 
@login_required
def add_question():
    try:
        if request.method=='POST':
            user_ques=request.form['user_ques']
            curr_user=current_user.email
            question=Questions(user_ques,curr_user)
            db.session.add(question)
            db.session.commit()
            flash('Question added successfully')
    except Exception as e:
        print(e)
    return redirect(url_for('homepage'))


#dashboard
@app.route("/dashboard",methods=['GET','POST'])
@login_required
def homepage():
    allQuestions=Questions.query.all()
    return render_template('dashboard.html',allQuestions=allQuestions)

#Add Answer
@app.route("/answerQuestion",methods=['GET','POST'])
@login_required
def answer_question():
    try:
        if request.method=='POST':
            user_ans=request.form['user_ans']
            curr_user=current_user.email
            q_id=request.form['q_id']
            answer=Answers(user_ans,curr_user,q_id)
            db.session.add(answer)
            db.session.commit()
            flash('Answer added successfully')
    except Exception as e:
        print(e)
    return redirect(url_for('homepage'))

#View Answers
@app.route("/answer/<int:ques_id>",methods=['GET','POST'])
@login_required
def view_answers(ques_id):
    answers = Answers.query.filter_by(ques_id=ques_id).all()
    questions=Questions.query.get(ques_id)
    return render_template('answers.html',questions=questions,answers=answers)

#Update Answer
@app.route("/updateAnswer",methods=['GET','POST'])
@login_required
def update_answer():
    try:
        if request.method=='POST':
            up_ans=request.form['up_ans']
            ans_id=request.form['a_id']
            updated_answer=Answers.query.get(ans_id)
            updated_answer.ans_desc=up_ans
            updated_answer.ans_posted_date=date.today()
            db.session.add(updated_answer)
            db.session.commit()
            flash('Answer Updated successfully')
    except Exception as e:
        print(e)
    return redirect(url_for('view_answers',ques_id=updated_answer.ques_id))
    #return render_template('answer.html')

#delete Answer
@app.route("/deleteAnswer/<int:ans_id>",methods=['GET','POST'])
@login_required
def delete_answer(ans_id):
    try:
        if request.method=='GET':
            delete_ans=Answers.query.get(ans_id)
            ques_id=delete_ans.ques_id
            db.session.delete(delete_ans)
            db.session.commit()
            flash("Answer deleted successfully")
    except Exception as e:
        print(e)
    return redirect(url_for('view_answers',ques_id=ques_id))

#delete Question
@app.route("/deleteQuestion/<int:ques_id>",methods=['GET','POST'])
@login_required
def delete_question(ques_id):
    try:
        if request.method=='GET':
            delete_ques=Questions.query.get(ques_id)
            db.session.delete(delete_ques)
            db.session.commit()
            flash("Question deleted successfully")
    except Exception as e:
        print(e)
    return redirect(url_for('homepage'))



#logout
@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__== "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)