from sqlalchemy import Column 
from sqlalchemy import String, Integer
from sqlalchemy.orm import declarative_base
# las librerias

Base = declarative_base() # la base para poder configurar el modelo


class Auth_User(Base): # nuestra clase de mapeo relacioandos
    __tablename__ = "auth_user" # nombre de nuestra tabla
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(150))  
    password = Column(String(128))

    
    def __repr__(self):
        return f'auth_user({self.username}, {self.password})'

    def __str__(self):
        return self.username

   