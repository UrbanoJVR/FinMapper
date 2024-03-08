import os

from flask import request, current_app, redirect, url_for, render_template
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename

from . import file_import
from movement_file_form import MovementFileForm


@file_import.route('/load', methods=['GET', 'POST'])
def load():
    form = MovementFileForm(CombinedMultiDict((request.files, request.form)))

    if form.validate_on_submit():
        data_file = form.file.data
        filename = secure_filename(data_file.filename)
        data_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('load'))

    return render_template('file_import/load_file.html', form=form)