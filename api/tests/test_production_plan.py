"""
test_production_plan.py: Contains endpoint production plan tests.
"""

__author__ = "alvertogit"
__copyright__ = "Copyright 2024"


import json

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_production_plan_payload_3():
    payload_3 = {
        "load": 910,
        "fuels": {
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20,
            "wind(%)": 60,
        },
        "powerplants": [
            {
                "name": "gasfiredbig1",
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460,
            },
            {
                "name": "gasfiredbig2",
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460,
            },
            {
                "name": "gasfiredsomewhatsmaller",
                "type": "gasfired",
                "efficiency": 0.37,
                "pmin": 40,
                "pmax": 210,
            },
            {"name": "tj1", "type": "turbojet", "efficiency": 0.3, "pmin": 0, "pmax": 16},
            {"name": "windpark1", "type": "windturbine", "efficiency": 1, "pmin": 0, "pmax": 150},
            {"name": "windpark2", "type": "windturbine", "efficiency": 1, "pmin": 0, "pmax": 36},
        ],
    }

    response_3 = [
        {"name": "windpark1", "p": 90.0},
        {"name": "windpark2", "p": 21.6},
        {"name": "gasfiredbig1", "p": 460.0},
        {"name": "gasfiredbig2", "p": 338.4},
        {"name": "gasfiredsomewhatsmaller", "p": 0.0},
        {"name": "tj1", "p": 0.0},
    ]

    response = client.post("/productionplan", content=json.dumps(payload_3))
    assert response.status_code == 200
    assert json.loads(response.content) == response_3


def test_production_plan_no_combination_error():
    payload_no_combination = {
        "load": 99999,
        "fuels": {
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20,
            "wind(%)": 60,
        },
        "powerplants": [
            {
                "name": "gasfiredbig1",
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460,
            },
            {"name": "windpark1", "type": "windturbine", "efficiency": 1, "pmin": 0, "pmax": 150},
        ],
    }

    response_no_combination_error = (
        "ValueError: There is no possible combination for the provided payload."
    )

    response = client.post("/productionplan", content=json.dumps(payload_no_combination))
    assert response.status_code == 400
    assert json.loads(response.content) == response_no_combination_error


def test_production_plan_efficiency_error():
    payload_efficiency_error = {
        "load": 150,
        "fuels": {
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20,
            "wind(%)": 60,
        },
        "powerplants": [
            {
                "name": "gasfiredbig1",
                "type": "gasfired",
                "efficiency": 0.0,
                "pmin": 100,
                "pmax": 460,
            },
            {"name": "windpark1", "type": "windturbine", "efficiency": 1, "pmin": 0, "pmax": 150},
        ],
    }

    response_efficiency_error = "ValueError: Wrong efficiency in gasfiredbig1: 0.0"

    response = client.post("/productionplan", content=json.dumps(payload_efficiency_error))
    assert response.status_code == 400
    assert json.loads(response.content) == response_efficiency_error
