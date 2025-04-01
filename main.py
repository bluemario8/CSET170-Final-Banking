from flask import Flask, render_template
from sqlalchemy import create_engine
from scripts.shhhh_its_a_secret import customHash

app = Flask(__name__)                                                                   # initiates flask
conn_str = "mysql://root:cset155@localhost/cset170final"                                # connects to db
engine = create_engine(conn_str, echo=True)                                             # creates engine
conn = engine.connect()                                                                 # connects engine


# --------------- #
# -- HOME PAGE -- #
# --------------- #

@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')