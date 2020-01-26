## CodeCompany/CodePost/views.py


from flask import render_template,flash,redirect,url_for,abort,Blueprint,request
from flask_login import login_required,current_user
from CodeCompany import db
from CodeCompany.models import CodePost
from CodeCompany.CodePost.forms import CodePostForm

code_posts=Blueprint("code_posts",__name__)

# CREATE
@code_posts.route("/create",methods=["GET","POST"])
@login_required
def create():
    form = CodePostForm()

    if form.validate_on_submit():

        code_post=CodePost(title=form.title.data,
                           code=form.code.data,
                           user_id=current_user.id)

        db.session.add(code_post)
        db.session.commit()

        flash("Post created")

        return redirect(url_for("core.index"))

    return render_template("create_post.html",form=form)

# BLOGPOST VIEW
@code_posts.route("/<int:code_post_id>")
def code_post(code_post_id):
    code_post=CodePost.query.get_or_404(code_post_id)
    return render_template("code_post.html",title=code_post.title,date=code_post.date,post=code_post)

# UPDATE
@code_posts.route("/<int:code_post_id>/update",methods=["GET","POST"])
@login_required
def update(code_post_id):
    code_post=CodePost.query.get_or_404(code_post_id)

    if code_post.author!=current_user:
        abort(403)

    form=CodePostForm()
    if form.validate_on_submit():
        code_post.title=form.title.data
        code_post.code=form.code.data
        db.session.commit()
        flash("Updated")

        return redirect(url_for("code_posts.code_post", code_post_id=code_post_id))

    elif request.method== "GET":
        form.title.data=code_post.title
        form.code.data=code_post.code

    return render_template("create_post.html",title="Updating",form=form)

# DELETING
@code_posts.route("/<int:code_post_id>/delete",methods=["GET","POST"])
@login_required
def delete(code_post_id):

    code_post=CodePost.query.get_or_404(code_post_id)

    if code_post.author!=current_user:
        abort(403)

    db.session.delete(code_post)
    db.session.commit()
    flash("Blog post deleted")
    return redirect(url_for("core.index"))
