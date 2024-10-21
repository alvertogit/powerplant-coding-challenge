"""
main.py: Contains api endpoint productionplan.
"""

__author__ = "alvertogit"
__copyright__ = "Copyright 2024"


import logging
from typing import Annotated

from fastapi import Body, FastAPI, Request
from fastapi.responses import JSONResponse
from production_plan import calculate_production_plan

logger = logging.getLogger("uvicorn.error")


app = FastAPI()


@app.exception_handler(ValueError)
def value_error_exception_handler(request: Request, exc: ValueError) -> JSONResponse:
    error_msg = f"ValueError: {str(exc)}"
    logger.error(error_msg)
    return JSONResponse(status_code=400, content=error_msg)


@app.post("/productionplan")
def production_plan(data: Annotated[dict, Body()]) -> JSONResponse:
    try:
        response = calculate_production_plan(data)
    except KeyError as exc:
        error_msg = f"KeyError: {str(exc)} field is required."
        logger.error(error_msg)
        return JSONResponse(status_code=404, content=error_msg)
    return JSONResponse(status_code=200, content=response)
