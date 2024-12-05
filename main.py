from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.crud.author import Author
from app.crud.country import Country
from app.crud.graph import Edges, Nodes
from app.crud.output import Output
from app.crud.workstream import Workstream

from app.schemas.author import AuthorModel
from app.schemas.country import CountryNodeModel
from app.schemas.output import OutputModel, OutputListModel
from app.schemas.workstream import WorkstreamBase, WorkstreamModel

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    nodes = Nodes().get()
    edges = Edges().get()
    countries = Country().get_all()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Home",
            "nodes": nodes,
            "links": edges,
            "countries": countries,
        },
    )


@app.get("/countries/{id}", response_class=HTMLResponse)
async def country(request: Request, id: str, type: str = None):
    country_model = Country()
    outputs, country = country_model.get(id, result_type=type)
    count = country_model.count(id)
    return templates.TemplateResponse(
        "country.html",
        {
            "request": request,
            "title": "Country",
            "outputs": outputs,
            "country": country,
            "count": count,
        },
    )


@app.get("/countries", response_class=HTMLResponse)
async def country_list(request: Request):
    country_model = Country()
    entity = country_model.get_all()
    return templates.TemplateResponse(
        "country_list.html",
        {"request": request, "title": "Countries", "countries": entity},
    )


@app.get("/authors/{id}", response_class=HTMLResponse)
async def author(request: Request, id: str, type: str = None):
    author_model = Author()
    entity = author_model.get(id, result_type=type)
    count = author_model.count(id)
    return templates.TemplateResponse(
        "author.html",
        {"request": request, "title": "Author", "author": entity, "count": count},
    )


@app.get("/authors", response_class=HTMLResponse)
async def author_list(request: Request):
    model = Author()
    entity = model.get_all()
    return templates.TemplateResponse(
        "authors.html", {"request": request, "title": "Author List", "authors": entity}
    )


@app.get("/outputs", response_class=HTMLResponse)
async def output_list(request: Request, type: str = None):
    model = Output()
    entity = model.filter_type(result_type=type) if type else model.get_all()
    count = model.count()
    return templates.TemplateResponse(
        "outputs.html",
        {"request": request, "title": "Output List", "outputs": entity, "count": count},
    )


@app.get("/outputs/{id}", response_class=HTMLResponse)
async def output(request: Request, id: str):
    output_model = Output()
    entity = output_model.get(id)
    return templates.TemplateResponse(
        "output.html", {"request": request, "title": "Output", "output": entity}
    )


@app.get("/outputs/{id}/popup", response_class=HTMLResponse)
async def output_popup(request: Request, id: str):
    output_model = Output()
    entity = output_model.get(id)
    return templates.TemplateResponse(
        "output_popup.html", {"request": request, "title": "Output", "output": entity}
    )


@app.get("/api/authors/{id}")
async def author(id: str, type: str = None) -> AuthorModel:
    author_model = Author()
    return author_model.get(id, result_type=type)


@app.get("/api/authors")
async def api_author_list()-> List[AuthorModel]:
    model = Author()
    return model.get_all()

@app.get("/api/countries/{id}")
async def api_country(id: str, type: str = None)-> OutputListModel:
    """Return a list of outputs filtered by the country id provided

    Arguments
    ---------
    id: str
        The 3-letter ISO country code
    type: str
        One of "dataset", "publication", "tools", "other"

    Returns
    -------
    OutputListModel schema

    """
    country_model = Country()
    outputs, country = country_model.get(id, result_type=type)
    count = country_model.count(id)
    return {"outputs": outputs, "country": country, "count": count}


@app.get("/api/countries")
async def api_country_list()-> List[CountryNodeModel]:
    country_model = Country()
    results = country_model.get_all()
    return [result['c'] for result in results] # The queries should return a list of dictionaries, each containing a 'c' key with the country information
                                               # This is a temporary workaround but the queries should be updated to return the correct data structure

@app.get("/api/outputs")
async def api_output_list(type: str = None) -> OutputListModel:
    model = Output()
    results = model.filter_type(result_type=type) if type else model.get_all()
    return [result['outputs'] for result in results]


@app.get("/api/outputs/{id}")
async def api_output(id: str) -> OutputModel:
    output_model = Output()
    return output_model.get(id)

@app.get("/api/workstreams")
async def api_workstream_list() -> List[WorkstreamBase]:
    model = Workstream()
    return model.get_all()

@app.get("/api/workstreams/{id}")
async def api_workstream(id: str) -> WorkstreamModel:
    model = Workstream()
    return model.get(id)
