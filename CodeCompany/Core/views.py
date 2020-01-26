## PuppuCompanyBlog/Core/views.py

from flask import render_template,redirect,Blueprint,request
from CodeCompany.models import CodePost

core=Blueprint("core",__name__)

@core.route("/",methods=["GET","POST"])
def index():
    page=request.args.get("page",1,type=int)
    code_post=CodePost.query.order_by(CodePost.date.desc()).paginate(page=page, per_page=8)
    return render_template("home.html",code_post=code_post)

@core.route("/info")
def info():
    return render_template("info.html")
