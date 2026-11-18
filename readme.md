# FreshCart AI — Grocery Sales Assistant

FreshCart AI is an AI-powered grocery shopping and sales assistant. Customers can chat with the assistant to explore grocery products, check prices and discounts, build an order, and move through an order-confirmation and payment flow.

The application uses **FastAPI** for the backend, a lightweight **HTML/CSS/JavaScript** frontend, **LangChain** agents and tools, and an **OpenAI chat model**. Conversation messages are read from and written to a **MySQL** database so the assistant can use earlier messages in the same conversation.

## Features

- Chat-based grocery shopping experience.
- Product search using a predefined grocery catalog.
- Discount lookup through a LangChain tool.
- Order and billing summary displayed in the UI.
- Customer name, email, and phone display.
- Payment-link tool integration point.
- Email tool integration point.
- Conversation ID stored in browser `localStorage`.
- Conversation history loaded from MySQL for each chat request.
- Responsive chat and order-summary interface.
- FastAPI endpoint documentation through Swagger UI.

## Technology Stack

| Area | Technology |
|---|---|
| Backend API | FastAPI |
| ASGI server | Uvicorn |
| Frontend | HTML, CSS, JavaScript |
| LLM framework | LangChain |
| Chat model integration | LangChain OpenAI (`ChatOpenAI`) |
| Agent | LangChain `create_agent` |
| Database | MySQL |
| Database driver | PyMySQL |
| Configuration | `python-dotenv`, Pydantic Settings |

## Project Structure

```text
Genai_project3/
├── app.py
├── requirements.txt
├── .env.example              # Create this file; do not commit your real .env
├── .gitignore
│
├── config/
│   ├── llm_config.py         # Creates the chat model and provides tools
│   └── settings.py           # Loads application settings from .env
│
├── controllers/
│   └── chat_controller.py    # POST /chat endpoint
│
├── models/
│   ├── chat_request.py       # Chat request model
│   └── chat_response.py      # Chat response model
│
├── prompts/
│   └── sales_ai_prompt.py   # Sales assistant instructions and JSON format
│
├── services/
│   ├── chat_service.py       # Conversation history, agent execution, DB access
│   └── calender_service.py   # Currently empty
│
├── tools/
│   ├── product_search_tool.py
│   ├── discounts_tool.py
│   ├── generate_payment_link_tool.py
│   └── email_tool.py
│
└── static/
    ├── index.html
    ├── styles.css
    └── app.js
```

## Prerequisites

Install or prepare the following:

- Python 3.10 or later (the project uses modern Python type-union syntax).
- MySQL Server.
- Node.js is **not required**; the frontend is plain HTML, CSS, and JavaScript.
- An OpenAI API key with access to the chat model configured in your environment.

## Installation and Setup

Run the commands from the `Genai_project3` project root (the folder containing `app.py`).

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Genai_project3
```

If you already have the project locally, open its root directory in your terminal.

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The settings module imports `pydantic_settings`. If installation reports `No module named 'pydantic_settings'`, install it:

```bash
python -m pip install pydantic-settings
```

You can also add `pydantic-settings` to `requirements.txt` so it is installed consistently with the rest of the project.

### 4. Configure environment variables

Create a `.env` file in the project root. Use the following template and fill in your own values:

```env
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
DEFAULT_LLM=openai
DEFAULT_OPENAI_MODEL=your_available_openai_model
DEFAULT_ANTHROPIC_MODEL=your_anthropic_model
```

The current active LLM implementation uses `ChatOpenAI`. The Anthropic client code is commented out, but the settings class currently still requires `ANTHROPIC_API_KEY` and `DEFAULT_ANTHROPIC_MODEL` to be present.

**Important:** Never commit `.env` or publish API keys. The repository's `.gitignore` excludes `.env`. If a real key has ever been committed or shared, revoke it and generate a replacement.

### 5. Set up MySQL

The chat service connects to a local MySQL database named `genai_pro3_db` and reads/writes a table named `conv_messages`.

Create the database:

```sql
CREATE DATABASE genai_pro3_db;
```

The code expects the `conv_messages` table to contain at least these columns:

- `conv_id` — conversation identifier
- `message` — message content
- `message_from` — role, such as `user` or `assistant`

A table compatible with the SQL used by the current service can be created with:

```sql
USE genai_pro3_db;

CREATE TABLE conv_messages (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    conv_id VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    message_from VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_conv_id (conv_id)
);
```

This schema is a setup template based on the columns queried and inserted by `services/chat_service.py`. The ZIP does not include a database dump or migration script, so check your existing database before creating the table.

**Database credentials:** The current `get_db_connection()` implementation has the MySQL host, username, password, port, and database name written directly in Python source. Move these values into environment variables before sharing or deploying the project. Do not publish a real database password in source control.

### 6. Start the FastAPI server

From the project root, with the virtual environment activated:

```bash
python -m uvicorn app:app --reload
```

Open these URLs:

- **FreshCart AI UI:** http://127.0.0.1:8000
- **Swagger API documentation:** http://127.0.0.1:8000/docs
- **ReDoc API documentation:** http://127.0.0.1:8000/redoc

The frontend is served directly by FastAPI from the `static/` directory. There is no separate frontend development server or build step in this project.

## API

### `POST /chat`

Processes one customer message for a conversation.

**Request body:**

```json
{
  "user_message": "I need 2 kg of rice and 1 litre of milk",
  "conv_id": "a-conversation-uuid"
}
```

Both `user_message` and `conv_id` are required by `ChatRequestModel`.

**Response shape:**

```json
{
  "ai_reply": {
    "message": "Assistant response shown in the chat",
    "status": "collecting details",
    "customer": {
      "name": null,
      "phone": null,
      "email": null
    },
    "products": [],
    "billing": {
      "subtotal": 0,
      "discount": 0,
      "delivery_fee": 0,
      "tax": 0,
      "total": 0
    },
    "order": {
      "order_id": null,
      "confirmed": false
    },
    "payment": {
      "payment_link": null,
      "payment_status": "not_created"
    },
    "actions": {
      "email_sent": false,
      "crm_lead_updated": false,
      "crm_sale_updated": false
    },
    "missing_information": [],
    "error": null
  }
}
```

The example illustrates the response structure requested in the system prompt. Actual values depend on the model's response and tool execution.

## How the Application Works

1. **Open the UI:** FastAPI serves `static/index.html`, along with the CSS and JavaScript files under `/static`.
2. **Create a conversation ID:** The browser creates a UUID for a new conversation and saves it in `localStorage`. The same ID is sent with later messages.
3. **Send a message:** The frontend sends `user_message` and `conv_id` to `POST /chat`.
4. **Load history:** `ChatService` queries MySQL for previous messages belonging to that conversation ID.
5. **Build agent input:** The service combines the sales-assistant prompt, conversation history, and latest user message.
6. **Create the agent:** `LLMClient` creates a `ChatOpenAI` client and provides the available LangChain tools to `create_agent`.
7. **Use tools:** The agent can call the product search, discount, payment-link, and email tools as appropriate.
8. **Parse the response:** The service expects the final assistant message to contain valid JSON and parses it with `json.loads`.
9. **Save messages:** The current user message and the assistant's `message` field are inserted into `conv_messages`.
10. **Update the UI:** The browser displays the assistant's message and renders product, billing, customer, order-status, and payment-link information from `ai_reply`.

## Available LangChain Tools

| Tool | Purpose | Current implementation |
|---|---|---|
| `search_products` | Returns the grocery catalog and prices | Returns a predefined in-code product list |
| `get_available_discounts` | Returns available discount rules | Returns two predefined discount entries |
| `generate_payment_link` | Supplies a payment link for an order | Currently returns a fixed example URL |
| `send_email` | Represents sending the bill/payment link by email | Currently returns a text confirmation; it does not send an actual email |

The product catalog and discounts are currently hardcoded in their respective tool files. They are not loaded from MySQL.

## Current Implementation Notes and Limitations

These notes describe what is present in the supplied source code; they are important when evaluating the project as a prototype:

- **No CRM tool is implemented.** The prompt mentions creating/updating a CRM lead and sale, and the response JSON contains CRM action flags, but no CRM integration tool is included in the project.
- **Email is a placeholder.** `send_email` returns a string; it does not connect to an email provider or send a real message.
- **Payment link is a placeholder.** `generate_payment_link` returns a fixed example URL; it does not create a live payment link with a payment gateway.
- **MySQL credentials are hardcoded.** Move them to environment variables and rotate any credential that has been exposed.
- **Database schema is not included.** The project contains SQL queries for `conv_messages`, but no SQL migration or database dump.
- **Anthropic support is not active.** The Anthropic client code is commented out; the active implementation creates `ChatOpenAI`.
- **Calendar service is empty.** `services/calender_service.py` currently contains no implementation.
- **Order/cart state is not stored in dedicated database tables.** The service stores conversation messages. The order details shown in the UI are rendered from the latest model response.
- **The new-chat action creates a new conversation ID in the browser.** It does not delete old conversation records from MySQL.
- **The service expects JSON from the model.** It calls `json.loads` on the agent's final content, so malformed JSON can cause a request to fail.
- **No authentication or user-specific access control is implemented** in the provided code.

## Troubleshooting

### `ModuleNotFoundError: No module named 'pydantic_settings'`

Install the missing dependency:

```bash
python -m pip install pydantic-settings
```

Add it to `requirements.txt` as well.

### MySQL connection error

Check that:

- MySQL Server is running.
- The `genai_pro3_db` database exists.
- The `conv_messages` table exists with the expected columns.
- The connection settings in `get_db_connection()` match your local MySQL configuration.

### OpenAI authentication or model error

Check that:

- `.env` is in the project root.
- `OPENAI_API_KEY` is valid.
- `DEFAULT_LLM=openai`.
- `DEFAULT_OPENAI_MODEL` names a model available to your API account.

### `uvicorn` is not recognized

Run Uvicorn through the active Python interpreter:

```bash
python -m uvicorn app:app --reload
```

If it is not installed in the active environment:

```bash
python -m pip install uvicorn
```

### Static files or page not found

Run Uvicorn from the project root—the directory containing both `app.py` and `static/`—because the app uses relative paths for the static directory and index file.

## Security Checklist Before Publishing

- [ ] Remove secrets and credentials from Python source code.
- [ ] Put database connection settings in `.env` and read them through application settings.
- [ ] Keep `.env` out of Git.
- [ ] Rotate any API key or database password that was previously exposed.
- [ ] Replace the placeholder email and payment tools before using the app with real customers.
- [ ] Add authentication, authorization, input validation, and appropriate database error handling before production use.
