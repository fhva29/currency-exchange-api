# **Currency Exchange API**

A robust API for retrieving exchange rates, historical data, and performing currency conversions in real-time.

---

## **Features**
- **Current Exchange Rate**: Get the latest exchange rate between two currencies.
- **Historical Exchange Rates**: View exchange rates for a specific date range or the last X days.
- **Currency Conversion**: Convert amounts between different currencies using the latest exchange rates.
- **Validation**: Ensures only valid currency pairs are processed.

---

## **Getting Started**

### **Prerequisites**
- Python 3.9+
- [Git](https://git-scm.com/)
- An IDE or text editor (e.g., VS Code)

### **Installation**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/fhva29/currency-exchange-api
   cd currency-exchange-api
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate   # Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the root directory with the following content:
   ```env
   CURRENCY_API_URL=https://economia.awesomeapi.com.br/json
   CURRENCY_API_KEY=your_api_key_here
   CURRENCY_XML_URL=https://economia.awesomeapi.com.br/xml/available
   ```

---

## **Usage**

### **Run the Server**
Start the FastAPI server using `uvicorn`:
```bash
uvicorn app:app --reload
```

The server will be available at:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## **API Endpoints**

### **1. Get Current Exchange Rate**
Retrieve the latest exchange rate between two currencies.

- **Endpoint**: `/exchange-rate/`
- **Method**: `GET`
- **Query Parameters**:
  - `base_currency`: The base currency (e.g., `USD`).
  - `target_currency`: The target currency (e.g., `BRL`).

**Example**:
```bash
GET /exchange-rate/?base_currency=USD&target_currency=BRL
```

**Response**:
```json
{
    "base_currency": "USD",
    "target_currency": "BRL",
    "exchange_rate": 5.123,
    "timestamp": "2023-01-01 12:34:56"
}
```

---

### **2. Get Historical Exchange Rates**
Retrieve exchange rates for a specific date range.

- **Endpoint**: `/exchange-history/`
- **Method**: `GET`
- **Query Parameters**:
  - `base_currency`: The base currency (e.g., `USD`).
  - `target_currency`: The target currency (e.g., `BRL`).
  - `start_date`: Start date in `DDMMYYYY` format.
  - `end_date`: End date in `DDMMYYYY` format.

**Example**:
```bash
GET /exchange-history/?base_currency=USD&target_currency=BRL&start_date=01012023&end_date=07012023
```

**Response**:
```json
{
    "base_currency": "USD",
    "target_currency": "BRL",
    "start_date": "2023-01-01",
    "end_date": "2023-01-07",
    "history": [
        {
            "date": "2023-01-01",
            "rate": 5.123
        },
        {
            "date": "2023-01-02",
            "rate": 5.234
        }
    ]
}
```

---

### **3. Get Exchange Rates for the Last X Days**
Retrieve exchange rates for the last X days.

- **Endpoint**: `/exchange-last-days/`
- **Method**: `GET`
- **Query Parameters**:
  - `base_currency`: The base currency (e.g., `USD`).
  - `target_currency`: The target currency (e.g., `BRL`).
  - `days`: The number of days for which to retrieve data.

**Example**:
```bash
GET /exchange-last-days/?base_currency=USD&target_currency=BRL&days=7
```

**Response**:
```json
{
    "base_currency": "USD",
    "target_currency": "BRL",
    "days": 7,
    "history": [
        {
            "date": "2023-01-01",
            "rate": 5.123
        },
        {
            "date": "2023-01-02",
            "rate": 5.234
        }
    ]
}
```

---

### **4. Convert Currency**
Convert an amount from one currency to another using the latest exchange rates.

- **Endpoint**: `/convert-currency/`
- **Method**: `GET`
- **Query Parameters**:
  - `base_currency`: The base currency (e.g., `USD`).
  - `target_currency`: The target currency (e.g., `BRL`).
  - `amount`: The amount to convert.

**Example**:
```bash
GET /convert-currency/?base_currency=USD&target_currency=BRL&amount=100
```

**Response**:
```json
{
    "base_currency": "USD",
    "target_currency": "BRL",
    "amount": 100,
    "exchange_rate": 5.123,
    "converted_value": 512.3
}
```

---

### **5. Get Valid Currency Pairs**
Retrieve all valid currency pairs and their descriptions.

- **Endpoint**: `/valid-combinations/`
- **Method**: `GET`

**Example**:
```bash
GET /valid-combinations/
```

**Response**:
```json
{
    "valid_combinations": {
        "USD-BRL": "US Dollar / Brazilian Real",
        "EUR-BRL": "Euro / Brazilian Real"
    }
}
```
---

## **Contributing**
Contributions are welcome! Please open an issue or submit a pull request with suggestions or improvements.

---

## **License**
This project is licensed under the [MIT License](LICENSE).

