from flask import render_template

from app.transactions import transactions_blueprint


@transactions_blueprint.route('/transactions', methods=['GET'])
def dashboard():
    return render_template('transactions/transactions_dashboard.html')
