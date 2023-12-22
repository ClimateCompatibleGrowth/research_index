from flask import Flask, render_template

from model import AuthorModel, OutputModel

app = Flask(__name__)


author_model = AuthorModel()


@app.route('/authors/<id>')
def author(id: int):
    entity = author_model.get(int(id), collabs=True)
    app.logger.info(entity)
    return render_template('author.html', title='Author', author=entity)


output_model = OutputModel()


@app.route('/outputs/<id>')
def output(id: int):
    entity = output_model.get(int(id))
    app.logger.info(entity)
    return render_template('output.html', title='Output', output=entity)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
