from flask import render_template


def page_not_found(e):
    return render_template('error_pages/404.html'), 404


def page_forbidden(e):
    return render_template('error_pages/403.html'), 403


def internal_server_error(e):
    return render_template('error_pages/500.html'), 500
