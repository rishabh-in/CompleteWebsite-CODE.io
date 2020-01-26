## CodeCompany/Error_pages/handler.py

from flask import Blueprint,render_template

error=Blueprint('error',__name__)

@error.app_errorhandler(404)
def error_404(error):
    return render_template("error_handler/404.html"),404