from flask import Flask
from flask_restful import Resource, Api

from flask.ext.sqlalchemy import SQLAlchemy
from userLogin import app
import userLogin 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7002)
