from flask import Flask, render_template
from sqlalchemy import create_engine, text
from scripts.shhhh_its_a_secret import customHash

app = Flask(__name__)                                                                   # initiates flask
conn_str = "mysql://root:cset155@localhost/cset170final"                                # connects to db
engine = create_engine(conn_str, echo=True)                                             # creates engine
conn = engine.connect()                                                                 # connects engine


# --------------- #
# -- HOME PAGE -- #
# --------------- #

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')


# ------------------ #
# -- ACCOUNT PAGE -- #
# ------------------ #

@app.route('/account', methods=['GET'])
def account():
    current = getCurrentUser()
    users = list(conn.execute(text('SELECT acc_num, CONCAT(first_name, " ", last_name), username, phone_num FROM users WHERE acc_num = :current;'), {'current': current}).fetchone())
    address = list(conn.execute(text('SELECT CONCAT(street_addr, ", ", city, ", ", state, " ", zip_code, " ", country) FROM addresses WHERE acc_num = :current;'), {'current': current}).fetchone())
    print(current)
    print(users)
    print(address)
    return render_template('account.html', accounts = users, address = address)


# --------------- #
# -- FUNCTIONS -- # 
# --------------- #

def getCurrentUser():                                                                   # FUNCTION gets current user id
    user = conn.execute(text('SELECT * FROM loggedin;')).all()                          # gets data from loggedin table

    if loggedIntoType() == 'user':                                                      # if user type account
        return user[0][0]                                                               # return acc_num
    elif loggedIntoType() == 'admin':                                                   # elif admin type account
        return user[0][1]                                                               # return admin_id

def loggedIntoType():                                                                   # FUNCTION checks user type that is logged in 
    value = conn.execute(text("SELECT * FROM loggedin")).all()
    
    if value[0][0]:                                                                     # returns user type if 
        return "user"                                                                   # acc_num is not null 
    elif value[0][1]:                                                                   # returns admin type if
        return "admin"                                                                  # admin_id is not null
    else:                                                                               # else both are null and 
        return None                                                                     # is therefore not signed in



if __name__ == '__main__':
    app.run(debug=True)