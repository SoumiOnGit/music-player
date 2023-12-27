from flask import Flask , render_template , request , redirect , url_for 
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite://users.db' # flask innitialises sqlalchemy for db operations , it will use the specified db sqlite files for storage (users.db)
db = SQLAlchemy(app) #binding sql to flask app

class User(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.string(80), unique= True, nullable= False)
    password = db.Column(db.string(20), nullable= False)
    email = db.Column(db.string(50), unique= True, nullable= False)

db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup' , methods = ['GET', 'POST']) #when you define a route or view function, you can use the methods attribute to specify which HTTP methods the route should handle. GET :Used to retrieve information from the server. POST : Used to submit data to be processed to a specified resource. Often used for creating or updating a resource on the server.
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if User.query.filter_by(username=username).first():  #query means to query the database for a user with a specific username . .first() means to retrieve the first result of query 
            return 'username already exists , please choose another username '
        new_user = User(username=username , password= password , email = email)
        db.session.add(new_user)
        db.session.commit()   

        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login' , methods = ['GET', 'POST'])
def login():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            return f'Welcome , {user.username} !!'
        else:
            return 'Invalid login Credentials :( '
        
    return render_template('login.html')
    
if __name__=='main':
    app.run(debug=True)