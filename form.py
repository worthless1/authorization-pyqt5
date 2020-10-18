from PyQt5 import QtWidgets
from design import Ui_MainWindow as Win1  # импорт нашего сгенерированного файла
from design2 import Ui_MainWindow as Win2
from design3 import Ui_MainWindow as Win3

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm.session import sessionmaker
import sys
Base = declarative_base()

engine = create_engine('postgresql://postgres:1234@localhost/Python')
connection = engine.connect()
session = sessionmaker(bind=engine)()



class User(Base):
     __tablename__ = 'users'
     id = Column(Integer, primary_key=True)
     username = Column(String)
     password = Column(String)


class Mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Mywindow, self).__init__()
        self.ui = Win1()
        self.ui.setupUi(self)
        self.ui.signup_btn.clicked.connect(self.signin)
        self.ui.signin_btn.clicked.connect(self.login)

    def login(self):
        username = self.ui.login_lineEdit.text()
        password = self.ui.pass_lineEdit.text()
        result = session.query(User).filter_by(username=username, password=password)
        if (result.first()):
            self.hide()
            self.ui = Mywindow3()
            self.ui.show()
        else:
            self.ui.label_5.setText("Неправильный логин или пароль")

    def signin(self):
        self.hide()
        self.ui = Mywindow2()
        self.ui.show()



class Mywindow2(QtWidgets.QMainWindow):
    def __init__(self):
        super(Mywindow2, self).__init__()
        self.ui = Win2()
        self.ui.setupUi(self)
        self.ui.ca_btn.clicked.connect(self.reg)

    def reg(self):
        login = self.ui.login_lineEdit.text()
        password = self.ui.pass_lineEdit.text()
        s_password = self.ui.s_pass_lineEdit.text()
        if len(password) >= 8:
            res = session.query(User).filter_by(username=login, password=password)
            if not(res.first()):
                if password == s_password:
                    session.add(User(username=login, password=password))
                    session.commit()
                    self.hide()
                    self.ui = Mywindow()
                    self.ui.show()
                else:
                    self.ui.label_6.setText("Пароли не совпадают")
            else:
                self.ui.label_6.setText("Пользователь уже существует")
        else:
            self.ui.label_6.setText("Пароль должен быть не меньше 8 символов")


class Mywindow3(QtWidgets.QMainWindow):
    def __init__(self):
        super(Mywindow3, self).__init__()
        self.ui = Win3()
        self.ui.setupUi(self)

Base.metadata.create_all(engine)
app = QtWidgets.QApplication([])
application = Mywindow()
application.show()

sys.exit(app.exec())
