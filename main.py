from flask import Flask,render_template,request,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app=Flask(__name__)
app.secret_key = 'srpilusm'
app.config['SQLALCHEMY_DATABASE_URI']=f"postgresql://{'postgres'}:{'Shiva09'}@{'localhost'}:{'5432'}/{'questionanswer'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class User(db.Model):
    __tablename__='User'
    email=db.Column(db.String(50),primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(50),nullable=False)
    date_registered=db.Column(db.Date)

    def __init__(self,email,name,password):
        self.email=email
        self.name=name
        self.password=password
        self.date_registered=date.today()

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=='POST':
        email=request.form['email_id']
        name=request.form['full_name']
        password=request.form['password']
        user=User(email,name,password)
        print(user.name)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
    return render_template('register.html')

if __name__== "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)