from flask import Flask, render_template, request
from file_import.movement_file_form import MovementFileForm
from flask_babel import Babel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NOBODY_KNOWS'


def get_locale():
    return 'en'


babel = Babel(app, locale_selector=get_locale)


@app.route('/')
def hello_world():
    return render_template('base.html')


@app.route('/load', methods=['GET', 'POST'])
def load():
    if request.method == 'POST':
        print(request)
        return render_template('file_import/load_file.html')

    if request.method == 'GET':
        form = MovementFileForm()
        return render_template('file_import/load_file.html', form = form)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
    # app.run()
    babel.init_app(app)
