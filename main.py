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
login_manager.login_view='/login'

@login_manager.user_loader
def load_user(email_id):
    return User.query.get(email_id)


class User(db.Model,UserMixin):
    __tablename__='User'
    email=db.Column(db.String(50),primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(50),nullable=False)
    date_registered=db.Column(db.Date)

    def get_id(self):
        return str(self.email)

    def __init__(self,email,name,password):
        self.email=email
        self.name=name
        self.password=password
        self.date_registered=date.today()

#login
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        print("Request received for login(post)")
        email=request.form['email_id']
        password=request.form['password']
        user=User.query.get(email)
        if user is not None:
            print('User found')
            if user.password==password:
                login_user(user)
                print('inside password')
                return redirect(url_for('homepage'))
    return render_template('login.html')

#register
@app.route("/register",methods=['GET','POST'])
def register():
    try:
        if request.method=='POST':
            email=request.form['email_id']
            name=request.form['full_name']
            password=request.form['password']
            user=User(email,name,password)
            print(user.name)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
    except IntegrityError as e:
        flash('User already exists with this mail id', 'error')
        
    return render_template('register.html')

#home

@app.route("/dashboard",methods=['GET','POST'])
@login_required
def homepage():
    return render_template('dashboard.html')

# 
@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



if __name__== "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)