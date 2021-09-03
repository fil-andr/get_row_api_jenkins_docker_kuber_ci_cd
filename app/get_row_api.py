import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker

from flask import Flask
from flask_restful import Api, Resource, reqparse
import math
import socket

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)



def func1(x,y):
    return x * y

def cnt_letters(word):
    return len(word)

def fact(x):
    return math.factorial(x)



app = Flask(__name__)
api = Api(app)


engine = sa.create_engine('postgresql://postgres:pswd_123@postgrapi/postgres')

base = declarative_base()

class Company(base):
    __tablename__ = 'company'
    id = sa.Column(sa.Integer,primary_key=True)
    name = sa.Column(sa.String)
    age = sa.Column(sa.Integer)
    address = sa.Column(sa.String)
    salary = sa.Column(sa.Integer)

class Sss(Resource):
    def get(self,id_num):
        session_postg = sessionmaker(bind=engine)()
        try:
            d = session_postg.query(Company).filter_by(id=id_num).one()
        except sa.exc.NoResultFound:
            return f'no row with id: {id_num}'
        return f'This is deploy from jenkins pipeline FINAL TEST ansible k8s -  name: {d.name}, salary: {d.salary}  {host_ip}', 200

api.add_resource(Sss, "/<int:id_num>")


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
