
from flask import Flask
from flask.ext.mysql import MySQL

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'websysS16GB2'
app.config['MYSQL_DATABASE_PASSWORD'] = 'websysS16GB2!!'
app.config['MYSQL_DATABASE_DB'] = 'websysS16GB2'
mysql = MySQL(app)

@app.route('/')
def users():
        cur = mysql.connect().cursor()
        cur.execute('''SELECT userID FROM users''')
        data = cur.fetchall()
        return str(data)

        # def show_user(userID):
        #       user = user.query.filter_by(userID=niharika).first_or_404()
        #       if user:
        #               return {'userID':'success'}
        #       else:
        #               return {'userID':'failure'}

#api.add_resource(users, '/users')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7002,debug=True)

