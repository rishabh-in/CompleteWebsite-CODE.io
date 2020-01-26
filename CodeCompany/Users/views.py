from flask import render_template,redirect,url_for,Blueprint,flash,request
from flask_login import login_user,current_user,logout_user,login_required
from CodeCompany import db
from CodeCompany.models import User,CodePost
from CodeCompany.Users.forms import LoginForm,RegistrationForm,UpdateUserForm
from CodeCompany.Users.picture_handler import add_profile_picture

##########################################################################################

users=Blueprint("users",__name__)

##########################################################################################

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))

@users.route("/registration",methods=["GET","POST"])
def registration():

    form=RegistrationForm()

    if form.validate_on_submit():
        user=User(email=form.email.data,
                  username=form.username.data,
                  password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash("Registered Successfully")

        return redirect(url_for("users.login"))

    return render_template("registration.html",form=form)

@users.route("/login",methods=["GET","POST"])
def login():

    form=LoginForm()

    if form.validate_on_submit():

        user=User.query.filter_by(email=form.email.data).first()

        if user:

            if user.check_password(form.password.data) and user is not None:

                login_user(user)
                flash("You are logged in")

                next=request.args.get("next")

                if next==None or not next[0]=="/":

                    return redirect(url_for("users.account"))

                return redirect("next")
        else:
            return render_template("error_handler/user_not_found.html"), 404


    return render_template("login.html",form=form)

@users.route("/account",methods=["GET","POST"])
@login_required
def account():

    form=UpdateUserForm()

    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username

            pic = add_profile_picture(form.picture.data, username)

            current_user.profile_image = pic     ## Here pic is the returned value of add_profile_picture
                                                 ## It is the storage_filename ex=(rishabh.jpg)

        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()
        flash("User account Updated")

        return redirect(url_for("users.account"))

    elif request.method=="GET":

        form.username.data=current_user.username
        form.email.data=current_user.email

    profile_image = url_for("static",filename="profile_pics/"+current_user.profile_image)
    return render_template("account.html",profile_image=profile_image,form=form)

@users.route("/<username>")
def user_posts(username):

    page=request.args.get('page',type=int)

    user=User.query.filter_by(username=username).first_or_404()

    code_post=CodePost.query.filter_by(author=user).order_by(CodePost.date.desc()).paginate(page=page, per_page=8)

    return render_template("user_blog_post.html",code_post=code_post,user=user)

