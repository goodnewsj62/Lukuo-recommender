from flask import Blueprint, render_template

site = Blueprint('site', __name__)


@site.route('/policy', methods=['GET'])
def policy():
    return render_template('site/policy.html')


@site.route('/about', methods=['GET'])
def about():
    return render_template('site/about.html')
