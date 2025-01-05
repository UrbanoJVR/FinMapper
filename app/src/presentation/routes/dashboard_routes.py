from flask import Blueprint, render_template

dashboard_blueprint = Blueprint('dashboard_blueprint', __name__, url_prefix='')

@dashboard_blueprint.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard/dashboard.html')