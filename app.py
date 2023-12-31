from flask import Flask , render_template , request , redirect , url_for 
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///users.db' # flask innitialises sqlalchemy for db operations , it will use the specified db sqlite files for storage (users.db)
db = SQLAlchemy(app) #binding sql to flask app

class User(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(80), unique= True, nullable= False)
    password = db.Column(db.String(20), nullable= False)
    email = db.Column(db.String(50), unique= True, nullable= False)
    role = db.Column(db.String(10), nullable= False , default='user')

class Artist(db.Model):
    id =  db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    albums = db.relationship('Album', backref='artist', lazy=True) #In SQLAlchemy,backref used to create a back reference in the related model. It provides a way to access the related model from the other side of the relationship

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup' , methods = ['GET', 'POST']) #when you define a route or view function, you can use the methods attribute to specify which HTTP methods the route should handle. GET :Used to retrieve information from the server. POST : Used to submit data to be processed to a specified resource. Often used for creating or updating a resource on the server.
def signup():
    print(request.form)
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
    
if __name__=='__main__':
    app.run(debug=True)