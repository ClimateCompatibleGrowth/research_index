from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.crud.author import Author, AuthorList
from app.crud.country import Country, CountryList
from app.crud.graph import Edges, Nodes
from app.crud.output import Output, OutputList

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    nodes = Nodes().get()
    edges = Edges().get()
    countries = CountryList().get()
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
    country_model = CountryList()
    entity = country_model.get()
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
    model = AuthorList()
    entity = model.get()
    return templates.TemplateResponse(
        "authors.html", {"request": request, "title": "Author List", "authors": entity}
    )


@app.get("/outputs", response_class=HTMLResponse)
async def output_list(request: Request, type: str = None):
    model = OutputList()
    entity = model.filter_type(result_type=type) if type else model.get()
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
