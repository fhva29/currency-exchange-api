from pydantic import BaseModel, Field, ValidationError
from fastapi import Query


# Models for validation
class ExchangeRateRequest(BaseModel):
    base_currency: str = Field(
        ..., pattern="^[A-Z]{3}$", description="Base currency code (e.g., USD)"
    )
    target_currency: str = Field(
        ..., pattern="^[A-Z]{3}$", description="Target currency code (e.g., BRL)"
    )


class ExchangeHistoryRequest(BaseModel):
    base_currency: str = Field(
        ..., pattern="^[A-Z]{3}$", description="Base currency code (e.g., USD)"
    )
    target_currency: str = Field(
        ..., pattern="^[A-Z]{3}$", description="Target currency code (e.g., BRL)"
    )
    start_date: str = Field(
        ...,
        pattern="^\\d{2}\\d{2}\\d{4}$",
        description="Start date in the format DDMMYYYY",
    )
    end_date: str = Field(
        ...,
        pattern="^\\d{2}\\d{2}\\d{4}$",
        description="End date in the format DDMMYYYY",
    )


class ExchangeLastDaysRequest(BaseModel):
    base_currency: str = Field(
        ..., pattern="^[A-Z]{3}$", description="Base currency code (e.g., USD)"
    )
    target_currency: str = Field(
        ..., pattern="^[A-Z]{3}$", description="Target currency code (e.g., BRL)"
    )
    days: int = Field(
        ..., gt=0, description="Number of days for the history (must be greater than 0)"
    )


class ConvertCurrencyRequest(BaseModel):
    base_currency: str = Field(
        ..., pattern="^[A-Z]{3}$", description="Base currency code (e.g., USD)"
    )
    target_currency: str = Field(
        ..., pattern="^[A-Z]{3}$", description="Target currency code (e.g., BRL)"
    )
    amount: float = Field(
        ..., gt=0, description="Amount to be converted (must be greater than 0)"
    )
