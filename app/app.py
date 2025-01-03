from datetime import datetime
import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from .middleware import CurrencyValidationMiddleware
import xml.etree.ElementTree as ET
from .schemas import *

# Environment variables
load_dotenv()
EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL")
API_KEY = os.getenv("API_KEY")
XML_FILE_PATH = "available_combinations.xml"

# API code
app = FastAPI()
app.add_middleware(CurrencyValidationMiddleware)


@app.get("/valid-combinations/")
def get_valid_combinations():
    """
    Returns all valid currency combinations.

    Returns:
        - A dictionary with valid currency pairs and their descriptions.
    """
    try:
        # Load the XML directly
        response = requests.get(
            os.getenv(
                "CURRENCY_XML_URL", "https://economia.awesomeapi.com.br/xml/available"
            )
        )
        response.raise_for_status()

        tree = ET.ElementTree(ET.fromstring(response.content))
        root = tree.getroot()

        # Extract valid currency pairs and their descriptions
        valid_combinations = {child.tag: child.text for child in root}

        if not valid_combinations:
            raise HTTPException(status_code=404, detail="No valid combinations found.")

        return {"valid_combinations": valid_combinations}

    except HTTPException as http_exc:
        raise http_exc
    except requests.RequestException as req_err:
        raise HTTPException(status_code=500, detail=f"Request error: {req_err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@app.get("/exchange-rate/")
def get_exchange_rate(request: ExchangeRateRequest):
    """
    Fetches the current exchange rate between two currencies using the AwesomeAPI.

    Parameters:
        - base_currency: Base currency code (e.g., USD).
        - target_currency: Target currency code (e.g., BRL).

    Returns:
        - Current exchange rate between the specified currencies.
    """
    try:
        headers = {"x-api-key": API_KEY}
        response = requests.get(
            f"{EXTERNAL_API_URL}/last/{request.base_currency}-{request.target_currency}",
            headers=headers,
        )

        if response.status_code == 404:
            raise HTTPException(
                status_code=404, detail="Data not found for the specified currencies."
            )

        # Return exchange rate data
        data = response.json()
        key = f"{request.base_currency}{request.target_currency}"
        exchange_rate = data[key]
        return {
            "base_currency": request.base_currency,
            "target_currency": request.target_currency,
            "exchange_rate": exchange_rate["bid"],
            "timestamp": exchange_rate["create_date"],
        }

    except HTTPException as http_exc:
        raise http_exc
    except requests.RequestException as req_err:
        raise HTTPException(status_code=500, detail=f"Request error: {req_err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@app.get("/exchange-history/")
def get_exchange_history(request: ExchangeHistoryRequest):
    """
    Returns the exchange rate history between two currencies over a date range.

    Parameters:
        - base_currency: Base currency code (e.g., USD).
        - target_currency: Target currency code (e.g., BRL).
        - start_date: Start date in the format YYYY-MM-DD.
        - end_date: End date in the format YYYY-MM-DD.

    Returns:
        - Exchange rate history for the specified range.
    """
    try:
        try:
            start_date_formatted = datetime.strptime(
                request.start_date, "%d%m%Y"
            ).strftime("%Y%m%d")
            end_date_formatted = datetime.strptime(request.end_date, "%d%m%Y").strftime(
                "%Y%m%d"
            )
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Dates must be in the format DDMMYYYY."
            )

        headers = {"x-api-key": API_KEY}
        response = requests.get(
            f"{EXTERNAL_API_URL}/daily/{request.base_currency}-{request.target_currency}/?start_date={start_date_formatted}&end_date={end_date_formatted}",
            headers=headers,
        )

        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="History not found for the provided currencies.",
            )
        response.raise_for_status()

        data = response.json()

        # Return exchange rate history
        return {
            "base_currency": request.base_currency,
            "target_currency": request.target_currency,
            "start_date": start_date_formatted,
            "end_date": end_date_formatted,
            "history": data,
        }

    except HTTPException as http_exc:
        raise http_exc
    except requests.RequestException as req_err:
        raise HTTPException(status_code=500, detail=f"Request error: {req_err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@app.get("/exchange-last-days/")
def get_exchange_last_days(request: ExchangeLastDaysRequest):
    """
    Returns exchange rates for the last X days between two currencies.

    Parameters:
        - base_currency: Base currency code (e.g., USD).
        - target_currency: Target currency code (e.g., BRL).
        - days: Number of days for the history (X).

    Returns:
        - Exchange rate history for the last X days.
    """
    try:
        headers = {"x-api-key": API_KEY} if API_KEY else {}
        response = requests.get(
            f"{EXTERNAL_API_URL}/daily/{request.base_currency}-{request.target_currency}/{request.days}",
            headers=headers,
        )

        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="History not found for the provided currencies.",
            )

        response.raise_for_status()

        data = response.json()

        # Return exchange rate history
        return {
            "base_currency": request.base_currency,
            "target_currency": request.target_currency,
            "days": request.days,
            "history": data,
        }
    except HTTPException as http_exc:
        raise http_exc
    except requests.RequestException as req_err:
        raise HTTPException(status_code=500, detail=f"Request error: {req_err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@app.get("/convert-currency/")
def convert_currency(request: ConvertCurrencyRequest):
    """
    Converts an amount from a base currency to a target currency using the current exchange rate.

    Parameters:
        - base_currency: Base currency code (e.g., USD).
        - target_currency: Target currency code (e.g., BRL).
        - amount: Amount to be converted.

    Returns:
        - Converted amount based on the current exchange rate.
    """
    try:
        headers = {"x-api-key": API_KEY}
        response = requests.get(
            f"{EXTERNAL_API_URL}/last/{request.base_currency}-{request.target_currency}",
            headers=headers,
        )

        if response.status_code == 404:
            raise HTTPException(
                status_code=404, detail="Data not found for the specified currencies."
            )
        response.raise_for_status()

        data = response.json()
        key = f"{request.base_currency}{request.target_currency}"
        exchange_rate = float(data[key]["bid"])
        converted_amount = request.amount * exchange_rate
        return {
            "base_currency": request.base_currency,
            "target_currency": request.target_currency,
            "amount": request.amount,
            "exchange_rate": exchange_rate,
            "converted_amount": converted_amount,
        }

    except HTTPException as http_exc:
        raise http_exc
    except requests.RequestException as req_err:
        raise HTTPException(status_code=500, detail=f"Request error: {req_err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
