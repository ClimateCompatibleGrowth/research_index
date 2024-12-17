from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.crud.author import Author
from app.crud.country import Country
from app.crud.graph import Edges, Nodes
from app.crud.output import Output

from app.api import author, output, country, workstream

app = FastAPI()

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
    countries = Country().get_countries()
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
            result_type: str = 'publication',
            skip: int = 0,
            limit: int = 20):
    country_model = Country()
    outputs_model = Output()
    outputs = outputs_model.filter_country(result_type=result_type,
                                           country=id,
                                           skip=skip,
                                           limit=limit)
    country = country_model.fetch_country_node(id)
    count = country_model.count_country_outputs(id)
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
            "result_type": result_type
        },
    )


@app.get("/countries", response_class=HTMLResponse)
def country_list(request: Request):
    country_model = Country()
    entity = country_model.get_countries()
    return templates.TemplateResponse(
        "country_list.html",
        {"request": request, "title": "Countries", "countries": entity},
    )


@app.get("/authors/{id}", response_class=HTMLResponse)
def author(request: Request,
           id: str,
           result_type: str = 'publication',
           skip: int = 0,
           limit: int = 20):
    author = Author()
    entity = author.get_author(id, result_type=result_type, skip=skip, limit=limit)
    return templates.TemplateResponse(
        "author.html",
        {"request": request,
         "title": "Author",
         "author": entity,
         "count":  entity['outputs']['meta']['count'],
         "skip": skip,
         "limit": limit,
         'result_type': result_type},
    )


@app.get("/authors", response_class=HTMLResponse)
def author_list(request: Request, skip: int = 0, limit: int = 20):
    authors = Author()
    entity = authors.get_authors(skip=skip, limit=limit)
    return templates.TemplateResponse(
        "authors.html", {"request": request,
                         "title": "Author List",
                         "authors": entity['authors'],
                         "skip": skip,
                         "limit": limit,
                         "count": entity['meta']['count']['total']}
    )


@app.get("/outputs", response_class=HTMLResponse)
def output_list(request: Request,
                result_type: str = 'publication',
                skip: int = 0,
                limit: int = 20,
                country: str = None):

    model = Output()
    package = model.get_outputs(skip=skip, limit=limit, result_type=result_type, country=country)
    return templates.TemplateResponse(
        "outputs.html",
        {"request": request,
         "title": "Output List",
         "outputs": package['results'],
         "count": package['meta']['count'],
         "result_type": result_type,
         "skip": skip,
         "limit": limit}
    )


@app.get("/outputs/{id}", response_class=HTMLResponse)
def output(request: Request, id: str):
    output_model = Output()
    entity = output_model.get_output(id)
    return templates.TemplateResponse(
        "output.html", {"request": request, "title": "Output", "output": entity})