from fastapi.logger import logger
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.crud.author import Author
from app.crud.country import Country
from app.crud.output import Output

from app.api import author, output, country, workstream

import logging

uvicorn_access_logger = logging.getLogger("uvicorn.access")
logger.handlers = uvicorn_access_logger.handlers

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
    countries = Country().get_countries(skip=0, limit=200)
    return templates.TemplateResponse(
        "index.html",
        {"request": request,
         "title": "Home"} | countries
    )

@app.get("/countries/{id}", response_class=HTMLResponse)
def country(request: Request,
            id: str,
            result_type: str = 'publication',
            skip: int = 0,
            limit: int = 20):
    country_model = Country()
    country = country_model.get_country(id, skip, limit, result_type)
    return templates.TemplateResponse(
        "country.html",
        {
            "request": request,
            "title": "Country"} | country
    )


@app.get("/countries", response_class=HTMLResponse)
def country_list(request: Request,
                 skip: int = 0,
                 limit: int = 20):
    country_model = Country()
    entity = country_model.get_countries(skip, limit)
    return templates.TemplateResponse(
        "country_list.html",
        {"request": request, "title": "Countries"} | entity
    )


@app.get("/authors/{id}", response_class=HTMLResponse)
def author(request: Request,
           id: str,
           result_type: str = 'publication',
           skip: int = 0,
           limit: int = 20):
    author = Author()
    entity = author.get_author(id,
                               result_type=result_type,
                               skip=skip,
                               limit=limit)
    return templates.TemplateResponse(
        "author.html",
        {"request": request,
         "title": "Author"} | entity  # Merges dicts
    )


@app.get("/authors", response_class=HTMLResponse)
def author_list(request: Request, skip: int = 0, limit: int = 20):
    authors = Author()
    entity = authors.get_authors(skip=skip, limit=limit)
    return templates.TemplateResponse(
        "authors.html", {"request": request,
                         "title": "Author List"} | entity  # Merges dicts
    )


@app.get("/outputs", response_class=HTMLResponse)
def output_list(request: Request,
                result_type: str = 'publication',
                skip: int = 0,
                limit: int = 20,
                country: str = None):

    model = Output()
    package = model.get_outputs(skip=skip,
                                limit=limit,
                                result_type=result_type,
                                country=country)
    return templates.TemplateResponse(
        "outputs.html",
        {"request": request,
         "title": "Output List"} | package
    )


@app.get("/outputs/{id}", response_class=HTMLResponse)
def output(request: Request, id: str):
    output_model = Output()
    entity = output_model.get_output(id)
    return templates.TemplateResponse(
        "output.html",
        {"request": request, "title": "Output"} | entity )


if __name__ != "main":
    logger.setLevel(uvicorn_access_logger.level)
else:
    logger.setLevel(logging.DEBUG)
