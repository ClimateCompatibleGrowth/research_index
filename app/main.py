from fastapi.logger import logger
from fastapi import FastAPI, Request, Query, Path, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import Annotated
from uuid import UUID

from app.crud.author import Author
from app.crud.country import Country
from app.crud.output import Output
from app.crud.workstream import Workstream
from app.schemas.query import (FilterWorkstream, FilterParams, FilterBase, FilterOutputList)

from app.api import author, output, country, workstream

import logging

# Add console handler to the fastapi logger
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)

# Use a nice format for the log messages
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)
console_handler.setFormatter(formatter)

# Obtain access loggers for uvicorn
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
        request,
        "index.html",
        {"title": "Home"} | countries
    )


@app.get("/countries/{id}", response_class=HTMLResponse)
def country(request: Request,
            id: Annotated[str, Path(examples=['KEN'], title="Country identifier", pattern="^([A-Z]{3})$")],
            query: Annotated[FilterParams, Query()]
            ):
    country_model = Country()
    try:
        country = country_model.get_country(id, query.skip, query.limit, query.result_type)
    except KeyError:
        raise HTTPException(status_code=404,
                            detail=f"Country with id '{id}' not found")
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Database error: {str(e)}") from e
    else:
        return templates.TemplateResponse(
            request,
            "country.html",
            {"title": "Country"} | country
        )


@app.get("/countries", response_class=HTMLResponse)
def country_list(request: Request,
                 query: Annotated[FilterBase, Query()]

                 ):
    country_model = Country()
    try:
        entity = country_model.get_countries(query.skip, query.limit)
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Server error: {str(e)}") from e
    else:
        return templates.TemplateResponse(
            request,
            "country_list.html",
            {"title": "Countries"} | entity
        )


@app.get("/authors/{id}", response_class=HTMLResponse)
def author(request: Request,
           id: Annotated[UUID, Path(title="Unique author identifier")],
           query: Annotated[FilterParams, Query()]):
    author = Author()
    try:
        entity = author.get_author(
            id,
            result_type=query.result_type,
            skip=query.skip,
            limit=query.limit)
    except KeyError:
        raise HTTPException(status_code=404,
                            detail=f"Author '{id}' not found")
    else:
        return templates.TemplateResponse(
            request,
            "author.html",
            {"title": "Author"} | entity  # Merges dicts
        )


@app.get("/authors", response_class=HTMLResponse)
def author_list(request: Request,
                query: Annotated[FilterWorkstream, Query()]):
    authors = Author()
    try:
        entity = authors.get_authors(skip=query.skip,
                                     limit=query.limit,
                                     workstream=query.workstream)
    except KeyError as ex:
        raise HTTPException(status_code=404,
                            detail=f"Authors not found")
    else:
        return templates.TemplateResponse(
            request,
            "authors.html",
            {"title": "Author List"} | entity  # Merges dicts
        )


@app.get("/outputs", response_class=HTMLResponse)
def output_list(request: Request,
                query: Annotated[FilterOutputList, Query()]
                ):

    model = Output()
    try:
        package = model.get_outputs(skip=query.skip,
                                    limit=query.limit,
                                    result_type=query.result_type,
                                    country=query.country)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    else:
        return templates.TemplateResponse(
            request,
            "outputs.html",
            {"title": "Output List"} | package
        )


@app.get("/outputs/{id}", response_class=HTMLResponse)
def output(request: Request,
           id: Annotated[UUID, Path(title="Unique output identifier")]
           ):
    output_model = Output()
    try:
        entity = output_model.get_output(id)
    except KeyError as e:
        raise HTTPException(
                status_code=404, detail=f"Output with id {id} not found"
            ) from e
    except Exception as e:
        logger.error(f"Error in api_output: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e)) from e
    else:
        return templates.TemplateResponse(
            request,
            "output.html",
            {"title": "Output"} | entity)


@app.get("/workstreams", response_class=HTMLResponse)
def workstream_list(request: Request):
    model = Workstream()
    try:
        all = model.get_all()
    except KeyError as e:
        raise HTTPException(status_code=500,
                            detail=f"Database error: {str(e)}") from e
    else:
        try:
            entity = model.get(all['results'][0]['id'])
        except KeyError as e:
            raise HTTPException(status_code=500,
                                detail=f"Database error: {str(e)}") from e

        else:
            return templates.TemplateResponse(
                request,
                "workstreams.html",
                {"title": "Workstream"} | entity | all
    )


@app.get("/workstreams/{id}", response_class=HTMLResponse)
def workstream(request: Request,
               id: str,
               query: Annotated[FilterBase, Query()]
               ):
    model = Workstream()
    all = model.get_all()
    try:
        entity = model.get(id, skip=query.skip, limit=query.limit)
    except KeyError as e:
        raise HTTPException(status_code=404,
                            detail=f"Workstream '{id}' not found")

    else:
        return templates.TemplateResponse(
            request,
            "workstreams.html",
            {"title": "Workstreams"} | entity | all
        )


if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(uvicorn_access_logger.level)
