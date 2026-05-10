<div align="center">
  
# 📅 SkipSmart Timetable Service

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

*A lightweight, dedicated Python microservice for seamless Edupage integration.*

</div>

---

## 📖 Overview

The **SkipSmart Timetable Service** is a specialized component of the broader SkipSmart ecosystem. Built to assist UFAZ University students in managing their absence limits effectively, this service acts as the bridge between the core SkipSmart application and the Edupage system. 

By leveraging a custom implementation of the `edupage-api` Python package, this Flask-based service reliably extracts, processes, and delivers accurate timetable data and working day calculations to the main .NET backend.

## ✨ Key Features

- **🎓 Edupage Integration**: Directly connects to Edupage to fetch real-time scheduling data.
- **📅 Daily Timetables**: Retrieves detailed class schedules for any specific date and student group.
- **⏱️ Working Days Calculation**: Accurately computes working days within a given date range, accounting for specific language and faculty subgroups.
- **🔒 Secure Access**: Endpoints are protected via static API keys and strict CORS configurations to ensure only authorized requests from the Core Service are processed.
- **🐳 Docker Ready**: Fully containerized using Gunicorn for robust, production-ready deployments.

## 🛠️ Tech Stack

- **Language:** Python 3.10
- **Framework:** Flask
- **Integration:** Modified `edupage-api` (via pip)
- **Deployment:** Docker, Gunicorn

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- [Docker](https://www.docker.com/) (optional, for containerized deployment)

### Installation & Setup

1. **Clone the repository** (if not already done within the SkipSmart monorepo/ecosystem).
2. **Navigate to the service directory**:
   ```bash
   cd skipsmart-backend-v2-timetable-service
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Environment Variables**:
   Create a `.env` file in the root directory and configure the following variables:
   ```env
   EDUPAGE_USERNAME=your_edupage_username
   EDUPAGE_PASSWORD=your_edupage_password
   EDUPAGE_DOMAIN=your_school_domain # e.g., ufaz
   PASSWORD_KEY=your_secret_api_key
   ALLOWED_ORIGIN=https://your-core-service-url.com
   ```

### Running Locally

To start the Flask development server:
```bash
python app.py
```
*The service will be available at `http://localhost:5435`.*

### Running with Docker

To build and run the containerized version (uses Gunicorn on port 8000):
```bash
docker build -t skipsmart-timetable-service .
docker run -p 8000:8000 --env-file .env skipsmart-timetable-service
```

## 🔌 API Endpoints

All endpoints require the `key` parameter (matching the `PASSWORD_KEY` environment variable) for authorization.

### 1. Get Timetable for Date
Retrieves the class schedule for a specific date and group.

- **URL:** `/api/timetable-service/v1/timetable-for-date`
- **Method:** `GET`
- **Query Parameters:**
  - `key` (string): API access key.
  - `date` (string): Target date in `YYYY-MM-DD` format.
  - `group_id` (integer): The Edupage internal ID for the student group.

### 2. Calculate Working Days
Calculates the active academic working days over a specific period for a student.

- **URL:** `/api/timetable-service/v1/working-days`
- **Method:** `POST`
- **Body Data (JSON):**
  - `key` (string): API access key.
  - `start_date` (string): Period start date in `YYYY-MM-DD`.
  - `end_date` (string): Period end date in `YYYY-MM-DD`.
  - `group_id` (integer): The Edupage group ID.
  - `language_subgroup` (integer): ID representing the student's language subgroup.
  - `faculty_subgroup` (integer): ID representing the student's faculty subgroup.
  - `courses` (string, optional): Specific courses filter.

## 🔗 Related Repositories

- **[Backend Core Service](https://github.com/Camrado/skipsmart-backend-v2-core-service)**: The primary REST API for SkipSmart, built with .NET 10, which consumes this timetable microservice.
