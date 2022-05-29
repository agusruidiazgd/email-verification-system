from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_marshmallow import Marshmallow
from flask_mail import Mail, Message
import psycopg2
import psycopg2.extras
import os

load_dotenv()

app = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}
app.config.update(mail_settings)

mail = Mail(app)
ma = Marshmallow(app)
DB_HOST = "localhost"
DB_NAME = "accounts"
DB_USER = "postgres"
DB_PASS = "admin"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

class userSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'verified_email')

users_schema = userSchema(many=True)

@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route('/sendemail/<email>', methods=['GET'])
def send_mail(email):
    msg = Message(subject="Hello",
                    sender=app.config.get("MAIL_USERNAME"),
                    recipients=[os.environ['EMAIL_RECIPIENT']], # replace with your email for testing
                    body="This is a test email I sent with Gmail and Python!")
    msg.html = "<p>Hi user,</br>We just need to verify your email address.</br>Verify your email address <a href='http://127.0.0.1:5000//verification/%s'>here</a></p><div>Thanks! </div>"%email          
    mail.send(msg)
    return "Message sent!"

@app.route('/verification/<email>', methods=['GET'])
def verify_email(email):
    key = os.urandom(24)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        UPDATE users
        SET key = %s, is_verified = 'true'
        WHERE email = %s
    """, (key, email))
    conn.commit()
    return 'Account successfully verified'

@app.route('/account', methods=['POST'])
def add_account():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        username = request.json['username']
        email = request.json['email']
        cur.execute("INSERT INTO users (username, email) VALUES (%s,%s)", (username, email))
        conn.commit()
        return 'User successfully Added'

@app.route('/accounts', methods=['GET'])
def get_account():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM users"
    cur.execute(s) 
    list_users = cur.fetchall()
    result = users_schema.dump(list_users)
    return jsonify(result)

@app.route('/account/<id>', methods = ['GET', 'POST'])
def update_account(id):
    if request.method == 'POST':
        username = request.json['username']
        email = request.json['email']
         
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE users
            SET username = %s,
                email = %s
            WHERE id = %s
        """, (username, email, id))
        conn.commit()
        return 'Account Updated Successfully'
    else:    
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        cur.execute('SELECT * FROM users WHERE id = %s', (id))
        data = cur.fetchall()
        cur.close()
        result = users_schema.dump(data)
    return jsonify(result)

@app.route('/delete/<id>', methods = ['POST','GET'])
def delete_account(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('DELETE FROM users WHERE id = %s', (id))
    conn.commit()
    return 'Account Removed Successfully'


if __name__ == "__main__":
    app.run(debug=True)