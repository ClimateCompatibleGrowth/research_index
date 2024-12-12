from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.crud.author import Author
from app.crud.country import Country
from app.crud.graph import Edges, Nodes
from app.crud.output import Output

from app.api import author, output, country, workstream
from app.schemas.author import AuthorListModel, AuthorOutputModel
from app.schemas.country import CountryNodeModel
from app.schemas.output import OutputModel, OutputListModel
from app.schemas.workstream import WorkstreamBase, WorkstreamModel
from app.schemas.topic import TopicBaseModel

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(author.router)
app.include_router(output.router)
app.include_router(country.router)
app.include_router(workstream.router)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
@app.get("/index", response_class=HTMLResponse)
def index(request: Request):
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
def country(request: Request,
            id: str,
            type: str = 'publication',
            skip: int = 0,
            limit: int = 20):
    country_model = Country()
    outputs_model = Output()
    outputs = outputs_model.filter_country(result_type=type,
                                           country=id,
                                           skip=skip,
                                           limit=limit)
    country = country_model.get(id)
    count = country_model.count(id)
    return templates.TemplateResponse(
        "country.html",
        {
            "request": request,
            "title": "Country",
            "outputs": outputs,
            "country": country,
            "count": count,
            "skip": skip,
            "limit": limit,
            "type": type
        },
    )


@app.get("/countries", response_class=HTMLResponse)
def country_list(request: Request):
    country_model = Country()
    entity = country_model.get_all()
    return templates.TemplateResponse(
        "country_list.html",
        {"request": request, "title": "Countries", "countries": entity},
    )


@app.get("/authors/{id}", response_class=HTMLResponse)
def author(request: Request,
           id: str,
           type: str = 'publication',
           skip: int = 0,
           limit: int = 20):
    author_model = Author()
    entity = author_model.get(id, result_type=type, skip=skip, limit=limit)
    count = author_model.count(id)
    return templates.TemplateResponse(
        "author.html",
        {"request": request,
         "title": "Author",
         "author": entity,
         "count": count,
         "skip": skip,
         "limit": limit,
         'type': type},
    )


@app.get("/authors", response_class=HTMLResponse)
def author_list(request: Request, skip: int = 0, limit: int = 20):
    model = Author()
    entity = model.get_all(skip=skip, limit=limit)
    count = model.count_authors()
    return templates.TemplateResponse(
        "authors.html", {"request": request,
                         "title": "Author List",
                         "authors": entity,
                         "skip": skip,
                         "limit": limit,
                         "count": count}
    )


@app.get("/outputs", response_class=HTMLResponse)
def output_list(request: Request,
                type: str = 'publication',
                skip: int = 0,
                limit: int = 20,
                country: str = None):

    model = Output()
    if country:
        results = model.filter_country(result_type=type,
                                       skip=skip,
                                       limit=limit,
                                       country=country)
    else:
        results = model.filter_type(result_type=type,
                                    skip=skip,
                                    limit=limit)

    count = model.count()

    package = {
        "meta": {"count": count,
                 "db_response_time_ms": 0,
                 "page": 0,
                 "per_page": 0},
        "results": results
    }

    return templates.TemplateResponse(
        "outputs.html",
        {"request": request,
         "title": "Output List",
         "outputs": package['results'],
         "count": package['meta']['count'],
         "type": type,
         "skip": skip,
         "limit": limit}
    )


@app.get("/outputs/{id}", response_class=HTMLResponse)
def output(request: Request, id: str):
    output_model = Output()
    entity = output_model.get(id)
    return templates.TemplateResponse(
        "output.html", {"request": request, "title": "Output", "output": entity})