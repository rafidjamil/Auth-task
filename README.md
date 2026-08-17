# Auth Practice API (FastAPI + Supabase)

A secure RESTful API built with **FastAPI** and **Supabase Auth** that handles user registration, authentication, session management, and route protection using JSON Web Tokens (JWT) with HTTP Bearer authentication.

---

## Features

* **User Authentication:** Complete Sign Up, Log In, and Log Out flow powered by Supabase Auth.
* **JWT Token Security:** Dependency-based middleware for token extraction and verification.
* **Interactive API Docs:** Built-in Swagger UI with HTTP Bearer security scheme.
* **Environment Configuration:** Sensitive credentials secured using `.env` variables.

---

## Tech Stack

* **Language:** Python 3.10+
* **Framework:** FastAPI
* **Auth Provider:** Supabase Auth (`supabase-py`)
* **ASGI Server:** Uvicorn

---

## Getting Started

### Prerequisites

* Python 3.10+ installed
* Git
* A active Supabase project with API credentials

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <YOUR_GITHUB_REPOSITORY_URL>
   cd auth-practice