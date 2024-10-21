"""
production_plan.py: Contains production plan functions.
"""

__author__ = "alvertogit"
__copyright__ = "Copyright 2024"

from itertools import combinations


def get_powerplants_data(payload: dict) -> list:
    """
    Parses payload and returns powerplants data.
    """

    co2_euro_mwh = payload["fuels"]["co2(euro/ton)"] * 0.3
    # gasfired and turbojet generate co2
    type_euro_mwh = {
        "gasfired": payload["fuels"]["gas(euro/MWh)"] + co2_euro_mwh,
        "turbojet": payload["fuels"]["kerosine(euro/MWh)"] + co2_euro_mwh,
        "windturbine": 0,
    }
    wind_percentage = payload["fuels"]["wind(%)"] * 0.01
    powerplants_data = []
    for powerplant in payload["powerplants"]:
        efficiency = powerplant["efficiency"]
        # avoid division by 0
        if efficiency <= 0 or efficiency > 1:
            raise ValueError(f'Wrong efficiency in {powerplant["name"]}: {efficiency}')
        powerplant_data = {
            "name": powerplant["name"],
            "cost": type_euro_mwh[powerplant["type"]] / efficiency,
        }
        if powerplant["type"] == "windturbine":
            powerplant_data["pmin"] = round(powerplant["pmin"] * wind_percentage, 1)
            powerplant_data["pmax"] = round(powerplant["pmax"] * wind_percentage, 1)
        else:
            powerplant_data["pmin"] = powerplant["pmin"]
            powerplant_data["pmax"] = powerplant["pmax"]
        powerplants_data.append(powerplant_data)
    return powerplants_data


def calculate_production_plan(payload: dict) -> list:
    """
    Returns cheapest calculated production plan from payload if it exists.
    """

    load = payload["load"]
    powerplants_data = get_powerplants_data(payload)
    total_cost = 0
    posible_combination = []
    final_result = []

    # check all combinations of powerplants
    for r in range(1, len(powerplants_data) + 1):
        for comb in combinations(powerplants_data, r):
            list_comb = list(comb)
            list_comb.sort(key=lambda x: x["cost"])

            if (
                sum([item["pmax"] for item in list_comb]) >= load
                and sum([item["pmin"] for item in list_comb]) <= load
            ):
                cost = 0
                result = []
                remaining_load = load
                # first step consider pmin values for cost and load
                for powerplant in list_comb:
                    cost = cost + powerplant["cost"] * powerplant["pmin"]
                    remaining_load = remaining_load - powerplant["pmin"]
                # values from pmin to pmax starting with cheaper powerplants until remaining_load 0
                for powerplant in list_comb:
                    p_above_pmin = min(remaining_load, powerplant["pmax"] - powerplant["pmin"])
                    cost = cost + powerplant["cost"] * p_above_pmin
                    remaining_load = remaining_load - p_above_pmin
                    result.append(
                        {
                            "name": powerplant["name"],
                            "p": float(p_above_pmin) + float(powerplant["pmin"]),
                        }
                    )
                # if combination is cheaper than existing one then save it
                if not posible_combination or total_cost > cost:
                    total_cost = cost
                    posible_combination = list_comb
                    final_result = result

    if posible_combination == [] and load != 0:
        raise ValueError("There is no possible combination for the provided payload.")

    # add powerplants not included in final result
    result_names = [item["name"] for item in final_result]
    for powerplant in powerplants_data:
        if powerplant["name"] not in result_names:
            final_result.append({"name": powerplant["name"], "p": 0.0})
    return final_result
