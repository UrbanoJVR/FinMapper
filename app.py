import os

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename

from file_import.movement_file_form import MovementFileForm
from flask_babel import Babel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NOBODY_KNOWS'
app.config['UPLOAD_FOLDER'] = '/Users/urbano.villanueva/PycharmProjects/FinMapper/upload'


def get_locale():
    return 'en'


babel = Babel(app, locale_selector=get_locale)


@app.route('/')
def hello_world():
    return render_template('base.html')


@app.route('/load', methods=['GET', 'POST'])
def load():
    form = MovementFileForm(CombinedMultiDict((request.files, request.form)))

    if form.validate_on_submit():
        data_file = form.file.data
        filename = secure_filename(data_file.filename)
        data_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('load'))

    return render_template('file_import/load_file.html', form=form)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
    # app.run()
    babel.init_app(app)
