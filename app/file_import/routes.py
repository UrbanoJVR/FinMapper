import os

from flask import request, current_app, redirect, url_for, render_template
from flask_babel import _
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename

from app.file_import import file_import_blueprint
from app.file_import.forms import MovementFileForm


@file_import_blueprint.route('/load', methods=['GET', 'POST'])
def load():
    form = MovementFileForm(CombinedMultiDict((request.files, request.form)))

    if request.method == 'GET':
        return render_template('file_import/load_file.html', form=form, error=None)

    if form.validate_on_submit():
        data_file = form.file.data
        filename = secure_filename(data_file.filename)
        data_file.save(os.path.join(current_app.config['UPLOAD_DIR'], filename))
        return redirect(url_for('file_import_blueprint.load'))
    else:
        error_text = _('FileExtensionNotAllowed')

        return render_template('file_import/load_file.html', form=form, error=error_text)
