import datetime
from include import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) 
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password_hash = db.Column(db.String(60), nullable = False)
    cash = db.Column(db.Float, nullable  = False, default = 10000.0)

    # Specifying how the object is printed whenever we print it out.
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Stock(db.Model):
    symbol = db.Column(db.String(20), primary_key = True)
    company_name = db.Column(db.String(200), nullable = False)

    # Specifying how the object is printed whenever we print it out.
    def __repr__(self):
        return f"User('{self.symbol}', '{self.company_name}')"


class Stocks_Owned(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    stock_id = db.Column(db.String(20), db.ForeignKey('stock.symbol'), primary_key = True)
    shares = db.Column(db.Integer, nullable = False)
    logo = db.Column(db.Text)

    # Specifying how the object is printed whenever we print it out.
    def __repr__(self):
        return f"Stocks_Owned('{self.user_id}', '{self.stock_id}, '{self.shares}')"


class Transaction(db.Model):
    t_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    stock_id = db.Column(db.String(20), db.ForeignKey('stock.symbol'))
    shares = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Float, nullable = False)
    logo = db.Column(db.Text)
    transacted = db.Column(db.DateTime, default = datetime.datetime.now() )

    # Specifying how the object is printed whenever we print it out.
    def __repr__(self):
        return f"Stocks_Owned('{self.t_id}', '{self.user_id}, '{self.stock_id}', '{self.shares}', '{self.price}')"
