# modulo para gestionar nuestras acciones
import sqlalchemy as db
from persistence.model import Auth_User
from sqlalchemy.orm import Session


class AuthUserRepository(): # nuestra clase 
     
     def __init__(self):
        self.engine = db.create_engine('sqlite:///db/login.sqlite',
                                       echo=False, future=True)
      # para que se conecte a nuestra clase 
     def getUserByUserName(self, user_name: str):
        user: Auth_User = None
        with Session(self.engine) as session:
            user = session.query(Auth_User).filter_by(
                username=user_name).first()
             # cuando ya estamos conectado al motor  nos genery una consulta y que lo filtr
        return user
        # para obtener nuestro usuarios mediante un filtro de username

     def insertUser(self, user: Auth_User):
        with Session(self.engine) as session:
            #generamos la accion para que agregue los metodos al repositorio
            session.add(user)
            session.commit()
           