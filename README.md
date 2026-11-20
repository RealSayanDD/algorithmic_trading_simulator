
<div align="center">

# ⚡ Algorithmic Trading Simulator

### A virtual trading platform built with Python & FastAPI

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&size=20&pause=1000&color=00D4AA&center=true&vCenter=true&width=650&lines=Simulate+the+Stock+Market;Build+Virtual+Portfolios;Execute+Buy+%26+Sell+Trades;Track+Your+Financial+Performance" alt="Typing animation" />

<br/>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Async_API-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)

<br/>

![Status](https://img.shields.io/badge/Project-In_Development-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## 📈 Overview

**Algorithmic Trading Simulator** is a backend-driven virtual trading platform designed to simulate financial market interactions without using real money.

The application allows users to explore trading workflows, manage virtual funds, interact with market data, execute simulated trades, and monitor their portfolio performance through a structured REST API.

The project focuses on building a reliable trading backend with asynchronous operations, secure authentication, financial transaction integrity, and real-time market data capabilities.

> 💡 Learn how trading systems work — experiment with markets — manage risk — without risking real capital.

---

## ✨ Core Features

<table>
<tr>
<td width="50%">

### 🔐 Authentication
Secure user registration and login with token-based authentication.

</td>
<td width="50%">

### 💰 Virtual Wallet
Manage simulated funds and monitor available trading balance.

</td>
</tr>

<tr>
<td width="50%">

### 📊 Market Data
Retrieve stock information and market prices through external market data APIs.

</td>
<td width="50%">

### ⚡ Trade Execution
Simulate buy and sell operations with balance and asset validation.

</td>
</tr>

<tr>
<td width="50%">

### 📁 Portfolio Management
Track holdings, invested capital, available cash, and portfolio value.

</td>
<td width="50%">

### 🔄 Real-Time Updates
WebSocket-based market price streaming for live price updates.

</td>
</tr>
</table>

---

## 🏗️ Architecture

The project follows a modular, layered architecture to separate API endpoints, business logic, database operations, and external service integrations.

```mermaid
flowchart TD

    A[Client / Frontend] --> B[FastAPI Application]

    B --> C[API Layer]

    C --> D[Authentication]
    C --> E[Market Data]
    C --> F[Trading]
    C --> G[Portfolio]
    C --> H[WebSocket]

    D --> I[Service Layer]
    E --> I
    F --> I
    G --> I
    H --> I

    I --> J[SQLAlchemy ORM]

    J --> K[(PostgreSQL)]

    E --> L[External Market API]
    H --> M[Real-Time Price Stream]
```

### Architecture Principles

- **Separation of Concerns** — API routes, services, models, and schemas have distinct responsibilities.
- **Transactional Integrity** — financial operations should be handled atomically.
- **Concurrency Safety** — prevent conflicting trades from modifying the same wallet simultaneously.
- **Asynchronous Processing** — use async operations for external API calls and concurrent workloads.
- **Scalability** — maintain a modular structure that supports future extensions.

---

## 🛠️ Tech Stack

<div align="center">

| Technology | Purpose |
|---|---|
| 🐍 Python | Core programming language |
| 🚀 FastAPI | Backend REST API framework |
| 🗄️ PostgreSQL | Relational database |
| 🔗 SQLAlchemy 2.0 | Database ORM |
| 📦 Pydantic v2 | Validation and data schemas |
| 🔑 JWT | Authentication and authorization |
| 🔒 Passlib | Password hashing |
| 🌐 HTTPX | Async external API requests |
| 📡 WebSockets | Real-time price communication |
| 🧪 Pytest | Testing framework |
| 🛠️ Alembic | Database migrations |

</div>

---

## 📂 Project Structure

```text
algorithmic-trading-simulator/
│
├── src/
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── wallet.py
│   │   ├── asset.py
│   │   └── transaction.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── wallet.py
│   │   ├── asset.py
│   │   └── transaction.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── pricing_service.py
│   │   ├── trade_service.py
│   │   └── portfolio_service.py
│   │
│   ├── api/
│   │   ├── auth.py
│   │   ├── assets.py
│   │   ├── trading.py
│   │   ├── portfolio.py
│   │   └── websocket.py
│   │
│   └── main.py
│
├── tests/
│
├── alembic/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔄 Trading Workflow

### Buy Assets

```mermaid
flowchart TD

    A[User Requests Buy Order] --> B[Validate User]
    B --> C[Fetch Market Price]
    C --> D[Calculate Total Cost]
    D --> E{Sufficient Balance?}

    E -->|No| F[Reject Transaction]
    E -->|Yes| G[Lock Wallet]

    G --> H[Deduct Virtual Balance]
    H --> I[Update Asset Holdings]
    I --> J[Create Transaction Record]
    J --> K[Commit Database Transaction]
    K --> L[Trade Successful]
```

### Sell Assets

```mermaid
flowchart TD

    A[User Requests Sell Order] --> B[Validate Asset Holdings]
    B --> C[Fetch Current Price]
    C --> D[Calculate Sale Value]

    D --> E{Sufficient Holdings?}

    E -->|No| F[Reject Transaction]
    E -->|Yes| G[Lock Wallet & Asset]

    G --> H[Update Asset Quantity]
    H --> I[Credit Virtual Balance]
    I --> J[Create Transaction Record]
    J --> K[Commit Transaction]
    K --> L[Trade Successful]
```

---

## 📡 API Overview

The application exposes RESTful endpoints for user authentication, market data, trading operations, and portfolio management.

| Module | Endpoint | Method | Description |
|---|---|---|---|
| Authentication | `/auth/register` | `POST` | Register a new user |
| Authentication | `/auth/login` | `POST` | Authenticate user |
| Assets | `/assets` | `GET` | List supported assets |
| Market Data | `/assets/{symbol}/price` | `GET` | Retrieve market price |
| Trading | `/trades/buy` | `POST` | Execute simulated buy |
| Trading | `/trades/sell` | `POST` | Execute simulated sell |
| Portfolio | `/portfolio` | `GET` | Retrieve user portfolio |
| Portfolio | `/portfolio/history` | `GET` | Retrieve trade history |
| WebSocket | `/ws/prices` | `WS` | Stream real-time prices |

> 📝 Endpoint paths may evolve as the implementation progresses.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/algorithmic-trading-simulator.git

cd algorithmic-trading-simulator
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://username:password@localhost:5432/trading_db

SECRET_KEY=your_secret_key

ALPHA_VANTAGE_API_KEY=your_market_api_key
```

### 5. Run the application

```bash
uvicorn src.main:app --reload
```

The backend will start at:

```text
http://127.0.0.1:8000
```

### 6. Explore the API documentation

FastAPI automatically generates interactive API documentation.

| Documentation | URL |
|---|---|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

---

## 🧪 Testing

Tests are written using **Pytest** to validate business logic, API behavior, transaction integrity, and edge cases.

Run the test suite:

```bash
pytest -v
```

Run with coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

### Testing Focus

- Authentication and authorization
- Wallet balance validation
- Invalid trading inputs
- Buy and sell calculations
- Concurrent trade execution
- Transaction consistency
- Market API failure handling
- Portfolio calculations
- WebSocket connections

---

## 🛡️ Financial Integrity

Financial operations require special care to prevent inconsistent data.

The simulator aims to maintain:

- Atomic buy and sell transactions
- Accurate wallet balances
- Valid asset holdings
- Consistent transaction records
- Protection against concurrent balance updates
- Decimal-based financial calculations

A trade should never partially complete.

For example, if a buy order deducts the user's wallet balance but fails to update their holdings, the entire database transaction should roll back.

---

## 🗺️ Development Roadmap

```mermaid
timeline
    title Algorithmic Trading Simulator Development

    Week 1 : Project Foundation
            : Authentication
            : Database Models
            : Wallet System

    Week 2 : Market Data Integration
            : Pricing Service
            : External API Handling

    Week 3 : Trading Engine
            : Buy & Sell Operations
            : Portfolio Management

    Week 4 : WebSocket Streaming
            : Integration Testing
            : Error Handling
            : Final Documentation
```

<table>
<tr>
<td>

### 🟢 Week 1
**Foundation**

- Project architecture
- Database configuration
- User authentication
- Wallet creation
- Core models

</td>
<td>

### 🔵 Week 2
**Market Data**

- Stock price API
- Async HTTP requests
- Price validation
- API failure handling

</td>
</tr>

<tr>
<td>

### 🟣 Week 3
**Trading Engine**

- Buy and sell operations
- Wallet locking
- Transaction ledger
- Portfolio calculation

</td>
<td>

### 🟠 Week 4
**Integration**

- WebSocket streaming
- Integration tests
- Error handling
- Performance improvements

</td>
</tr>
</table>

---

## 👥 Team & Contributions

This project is developed collaboratively with responsibilities divided across independent modules.

| Role | Responsibility |
|---|---|
| Project Lead & Integration | Architecture, coordination, integration, code review |
| Database & Authentication | Models, database relationships, JWT authentication |
| Market Data & Pricing | External API integration and price retrieval |
| Trading Engine & Portfolio | Buy/sell logic and portfolio calculations |
| WebSocket & QA | Real-time streaming, automated testing, quality assurance |

---

## 🤝 Development Workflow

We follow a collaborative Git workflow with feature branches and pull requests.

### Branch Naming

```text
feature/authentication
feature/pricing-service
feature/trading-engine
feature/websocket-streaming
```

### Commit Convention

We use Conventional Commits:

```text
feat: add stock price retrieval
fix: correct wallet balance validation
test: add pricing service tests
docs: update api documentation
refactor: improve trade service structure
chore: initialize project configuration
```

---

## 📌 Future Enhancements

- 📉 Historical price charts
- 📊 Advanced portfolio analytics
- 🧮 Profit and loss calculations
- 🏆 Trading performance rankings
- 📈 Multiple asset classes
- 🔔 Price alerts
- 🧠 Algorithmic trading strategies
- ⚡ Redis-based market data caching
- 📱 Frontend dashboard integration

---

## ⚠️ Disclaimer

This application is designed strictly for educational and simulation purposes.

It does not execute real financial transactions and should not be considered financial advice.

All trades, balances, and investment activities are virtual.

---

<div align="center">

### Built with ⚡, Python, and a passion for financial technology.

**Algorithmic Trading Simulator**

*Simulate. Analyze. Trade. Learn.*

</div>
