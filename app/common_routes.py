from flask import redirect, url_for


def page_not_found(err):
    return redirect(url_for('dashboard_blueprint.dashboard'))
