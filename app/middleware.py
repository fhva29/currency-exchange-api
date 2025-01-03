from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import requests
import os
import xml.etree.ElementTree as ET


class CurrencyValidationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.xml_url = os.getenv(
            "CURRENCY_XML_URL", "https://economia.awesomeapi.com.br/xml/available"
        )
        self.valid_pairs = self.load_valid_pairs()

    def load_valid_pairs(self) -> set:
        try:
            response = requests.get(self.xml_url)
            response.raise_for_status()

            tree = ET.ElementTree(ET.fromstring(response.content))
            root = tree.getroot()
            valid_pairs = {child.tag for child in root}
            return valid_pairs
        except requests.RequestException as e:
            raise Exception(f"Erro ao carregar o XML da URL: {e}")
        except ET.ParseError as e:
            raise Exception(f"Erro ao analisar o XML: {e}")

    async def dispatch(self, request: Request, call_next):
        try:
            query_params = request.query_params
            base_currency = query_params.get("base_currency")
            target_currency = query_params.get("target_currency")

            if base_currency and target_currency:
                pair = f"{base_currency}-{target_currency}"
                if pair not in self.valid_pairs:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Par de moedas inválido: {pair}. Verifique as combinações válidas.",
                    )

            response = await call_next(request)
            return response
        except HTTPException as exc:
            # Aqui convertemos o HTTPException em uma resposta que
            # o Starlette/FastAPI entenda corretamente
            return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


app = FastAPI()
app.add_middleware(CurrencyValidationMiddleware)
