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

from app.schemas.author import AuthorListModel, AuthorOutputModel
from app.schemas.country import CountryNodeModel
from app.schemas.output import OutputModel, OutputListModel
from app.schemas.workstream import WorkstreamBase, WorkstreamModel
from app.schemas.topic import TopicBaseModel

app = FastAPI()

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
        "output.html", {"request": request, "title": "Output", "output": entity}
    )


@app.get("/api/authors/{id}")
def api_author(id: str, type: str = None) -> AuthorOutputModel:
    author_model = Author()
    results = author_model.get(id, result_type=type)
    count = author_model.count(id)
    results['outputs']['meta'] = {"count": count,
                                  "db_response_time_ms": 0,
                                  "page": 0,
                                  "per_page": 0}

    return results


@app.get("/api/authors")
def api_author_list(skip: int = 0, limit: int = 20) -> AuthorListModel:
    model = Author()
    authors = model.get_all(skip=skip, limit=limit)
    count = model.count_authors()
    return {'meta': {'count': {'total': count}},
            'authors': authors}


@app.get("/api/countries/{id}")
def api_country(id: str)-> CountryNodeModel:
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
    country = country_model.get(id)
    return country


@app.get("/api/countries")
def api_country_list()-> List[CountryNodeModel]:
    country_model = Country()
    results = country_model.get_all()
    return [result['c'] for result in results] # The queries should return a list of dictionaries, each containing a 'c' key with the country information
                                               # This is a temporary workaround but the queries should be updated to return the correct data structure


@app.get("/api/outputs")
def api_output_list(skip: int = 0,
                    limit: int = 20,
                    type: str = 'publication',
                    country: str = None) -> OutputListModel:
    """Return a list of outputs

    Arguments
    ---------
    skip: int, default = 0
    limit: int, default = 20
    type: enum, default = None
    country: str, default = None
    """
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

    return {
        "meta": {"count": count,
                 "db_response_time_ms": 0,
                 "page": 0,
                 "per_page": 0},
        "results": results
    }


@app.get("/api/outputs/{id}")
def api_output(id: str) -> OutputModel:
    output_model = Output()
    results = output_model.get(id)
    return results


@app.get("/api/workstreams")
def api_workstream_list() -> List[WorkstreamBase]:
    model = Workstream()
    return model.get_all()


@app.get("/api/workstreams/{id}")
def api_workstream(id: str) -> WorkstreamModel:
    model = Workstream()
    return model.get(id)


@app.get("/api/topics")
def api_topics_list() -> List[TopicBaseModel]:
    raise NotImplementedError("Have not yet implemented topics in the database")


@app.get("/api/topics/{id}")
def api_topic(id: str) -> TopicBaseModel:
    raise NotImplementedError("Have not yet implemented topics in the database")