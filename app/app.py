from flask import Flask, render_template, request

from model import (Author, Output, AuthorList, OutputList, Nodes, Edges,
                   CountryList, Country)

from logging import getLogger, basicConfig, DEBUG

logger = getLogger(__name__)
basicConfig(filename='example.log', filemode='w', encoding='utf-8', level=DEBUG)


app = Flask(__name__)



@app.route('/countries/<id>')
def country(id: str):
    country_model = Country()
    outputs, country = country_model.get(id)
    return render_template('country.html', title='Country', outputs=outputs, country=country)


@app.route('/countries')
def country_list():
    country_model = CountryList()
    entity = country_model.get()
    return render_template('country_list.html', title='Countries', countries=entity)


@app.route('/authors/<id>')
def author(id: str):
    author_model = Author()
    entity = author_model.get(id)
    return render_template('author.html', title='Author', author=entity)


@app.route('/authors')
def author_list():
    model = AuthorList()
    entity = model.get()
    return render_template('authors.html', title='Author List', authors=entity)


@app.route('/outputs')
def output_list():
    model = OutputList()
    result_type = request.args.get('type')
    logger.debug(f"Obtained filter {result_type}")
    if result_type:
        logger.info(f"Filtering outputs on {result_type}")
        entity = model.filter_type(result_type=result_type)
    else:
        entity = model.get()
    return render_template('outputs.html', title='Output List', outputs=entity)


@app.route('/outputs/<id>')
def output(id: str):
    output_model = Output()

    entity = output_model.get(id)
    return render_template('output.html', title='Output', output=entity)


@app.route('/outputs/<id>/popup')
def output_popup(id: str):
    output_model = Output()
    entity = output_model.get(id)
    return render_template('output_popup.html', title='Output', output=entity)


@app.route('/')
@app.route('/index')
def index():
    nodes = Nodes().get()
    edges = Edges().get()
    countries = CountryList().get()
    return render_template('index.html', title='Home',
                           nodes=nodes, links=edges, countries=countries)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
