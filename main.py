from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, text, insert, Table, MetaData, update
from scripts.shhhh_its_a_secret import customHash
# from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)                                                                   # initiates flask
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:cset155@localhost/cset170final"


conn_str = "mysql://root:cset155@localhost/cset170final"                                
engine = create_engine(conn_str, echo=True)                                             
conn = engine.connect()                                                                 


# For login session. Will continue to try and get this to work if we have extra time
"""
login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)
class User(UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
"""

# --------------- #
# -- HOME PAGE -- #
# --------------- #

@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    return "signup"

# ---------------- #
# -- LOGIN PAGE -- #
# ---------------- #

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        admin_username = dict( conn.execute(text("SELECT username, password FROM admin")).all() )
        users_username = dict( conn.execute(text("SELECT username, password FROM users")).all() )
        
        if username in admin_username.keys() and admin_username[username] == password:
            print(logIntoDB('admin', username, password))

        elif username in users_username.keys() and users_username[username] == password:
            logIntoDB('user', username, password)
        else:
            return render_template("login.html", error="Error: Invalid username or password")
        
        return render_template("login.html", success="Login success")


def logIntoDB(accType, username=None, password=None):                                    
        """
        Logs the user into the DB. Needs accType ('admin', 'user', or None)
        You need an username and password if you are logging into an account or
        nothing if you are logging out
        """
        if accType is None:                                                           
            conn.execute(text("UPDATE loggedin "                                      
                            f"SET acc_num = NULL, admin_id = NULL"))
            conn.commit()                                                             
            return "logged out"
        
        if accType == 'admin':
            result = conn.execute(text( "SELECT admin_id FROM admin "
                                       f"WHERE username = '{username}' AND password = '{password}'")).all()
        elif accType == 'user':
            result = conn.execute(text( "SELECT acc_num FROM users "
                                       f"WHERE username = '{username}' AND password = '{password}'")).all()

        print(f"logIntoDB result variable = {result}")
        
        if not result:                                                                
            return "no users"
        
        stored_id = result[0][0]                                                      

        conn.execute(                                                                 
            text("UPDATE loggedin SET acc_num = :acc_num, admin_id = :admin_id"),
                {'acc_num': stored_id if accType == 'user' else None,
                'admin_id': stored_id if accType == 'admin' else None}
        )                                             
        conn.commit()                                                                 

        return "Executed function logIntoDB fully"

def loggedIntoType():                                                                    
    """Returns either 'user', 'admin', or None"""
    value = conn.execute(text("SELECT * FROM loggedin")).all()
    
    if value[0][0]:                                                                      
        return "user"                                                                
    elif value[0][1]:                                                              
        return "admin"                                                          
    else:                                                                               
        return None                                                                     

def getCurrentUser():                                                                   
    """Returns either the admin_id, acc_num, or None"""
    user = conn.execute(text('SELECT * FROM loggedin;')).all()                          

    if loggedIntoType() == 'user':                                               
        return user[0][0]                                                               
    elif loggedIntoType() == 'admin':                                             
        return user[0][1]                                                               


if __name__ == "__main__":
    app.run(debug=True)