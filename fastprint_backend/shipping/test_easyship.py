import requests
import json

url = "https://public-api.easyship.com/2024-09/rates"
headers = {
    "Authorization": "Bearer sand_y34Y0SNhj5SyU/LcDE57P3XOc9pZOp0JWb0DrsEk1SQ=",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

payload = {
    "origin_address": {
        "country_alpha2": "US",
        "state": "CA",
        "city": "Los Angeles",
        "postal_code": "90001"
    },
    "destination_address": {
        "country_alpha2": "GB",
        "state": "England",
        "city": "London",
        "postal_code": "SW1A1AA"
    },
    "incoterms": "DDU",
    "insurance": {"is_insured": False},
    "courier_settings": {
        "show_courier_logo_url": False,
        "apply_shipping_rules": True
    },
    "shipping_settings": {
        "units": {"weight": "kg", "dimensions": "cm"}
    },
    "parcels": [
        {
            "items": [
                {
                    "actual_weight": 1.2,
                    "quantity": 1,
                    "declared_currency": "USD",
                    "declared_customs_value": 100,
                    "origin_country_alpha2": "US",
                    "category": "Toys",
                    "hs_code": "95030039",
                    "dimensions": {
                        "length": 20,
                        "width": 10,
                        "height": 5
                    },
                    "contains_battery_pi966": False,
                    "contains_battery_pi967": False,
                    "contains_liquids": False
                }
            ]
        }
    ]
}

print("DEBUG: Payload being sent:")
print(json.dumps(payload, indent=2))

response = requests.post(url, json=payload, headers=headers)
print("\n== Easyship API Response ==")
print("Status Code:", response.status_code)
try:
    print(json.dumps(response.json(), indent=2))
except Exception:
    print(response.text)
