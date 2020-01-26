from CodeCompany import db,login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

##############################################################################

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

##############################################################################

class User(db.Model,UserMixin):

    __tablename__= "users"

    id=db.Column(db.Integer,primary_key=True)
    profile_image=db.Column(db.String(128),nullable=False,default="default_profile.jpg")
    email=db.Column(db.String(64),unique=True,nullable=False,index=True)
    username=db.Column(db.String(64),unique=True,nullable=False,index=True)
    password_hash=db.Column(db.String(128),nullable=False)
    post=db.relationship('CodePost',backref="author",lazy=True)

    def __init__(self,email,username,password):
        self.email=email
        self.username=username
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return "Username:{}".format(self.username)

##############################################################################

class CodePost(db.Model):

    users=db.relationship(User)

    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    title=db.Column(db.String(140),nullable=False)
    code=db.Column(db.Text, nullable=False)

    def __init__(self,title,code,user_id):
        self.title=title
        self.code=code
        self.user_id=user_id

    def __repr(self):
        return f"Post ID:{self.id}"