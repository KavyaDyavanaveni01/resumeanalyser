# SkillGraph AI – Resume Skill Gap Analyzer

SkillGraph AI is a full-stack web application designed to help tech candidates align their resumes with target career goals. By extracting professional competencies from uploaded resumes (PDF/DOCX) using a Python spaCy NLP module, the application runs a gap-analysis against selected career tracks, visualizes stats using Chart.js, creates step-by-step learning roadmaps, recommends industry certifications, and exports custom ReportLab PDF reports.

---

## Technical Stack & Architecture

- **Frontend**: HTML5, Vanilla CSS3 (with Custom Theme tokens & Glassmorphic styling), Bootstrap 5, Chart.js, and client-side JavaScript.
- **Backend Service**: Java 21, Spring Boot 3, Hibernate 6, Maven, and SQLite (for database storage).
- **AI Microservice**: Python 3, Flask, PyPDF2 (for PDF extraction), python-docx (for Word document extraction), spaCy (for Natural Language Processing & NLP parsing), and ReportLab (for custom formatted PDF document generation).

---

## Directory Structure

```text
skillgraph-ai/
├── ai_module/
│   ├── app.py                     # Flask entry point and ReportLab PDF compiler
│   ├── resume_parser.py           # Text extraction logic for PDF & DOCX
│   ├── analyzer.py                # Regex-based spaCy NLP parser & roadmap metrics
│   ├── requirements.txt           # Python package requirements
│   └── resume_sample.docx         # Sample resume containing matching/missing developer skills
├── backend/
│   ├── pom.xml                    # Maven POM dependency definition (Spring Boot 3, SQLite)
│   └── src/
│       └── main/
│           ├── java/com/skillgraph/ai/
│           │   ├── SkillGraphApplication.java # Spring Boot application entry point
│           │   ├── config/
│           │   │   └── CorsConfig.java        # Cross-Origin resource sharing mapping
│           │   ├── controller/
│           │   │   ├── AuthController.java    # Registration, Login, Logout APIs
│           │   │   ├── UserController.java    # Get profile & change career goals
│           │   │   └── ResumeController.java  # Parse uploads, get analysis, fetch reports
│           │   ├── dto/                       # Request/Response data transfer objects
│           │   │   ├── RegisterRequest.java
│           │   │   ├── LoginRequest.java
│           │   │   ├── LoginResponse.java
│           │   │   ├── ProfileResponse.java
│           │   │   ├── GoalRequest.java
│           │   │   ├── AnalysisResponse.java
│           │   │   └── FlaskParseResponse.java
│           │   ├── entity/                    # Database models mapped to SQLite
│           │   │   ├── User.java
│           │   │   ├── UserSession.java
│           │   │   └── AnalysisResult.java
│           │   ├── repository/                # Data layers
│           │   │   ├── UserRepository.java
│           │   │   ├── UserSessionRepository.java
│           │   │   └── AnalysisResultRepository.java
│           │   ├── service/                   # Business rules
│           │   │   ├── AuthService.java
│           │   │   ├── UserService.java
│           │   │   └── ResumeService.java     # Calls Flask microservice and manages logs
│           │   └── util/
│           │       └── PasswordUtil.java      # SHA-256 Hashing helper
│           └── resources/
│               └── application.properties     # DB URL, limits, and Flask URL
├── database/
│   └── schema.sql                 # SQLite schema mapping reference
├── frontend/
│   ├── login.html                 # Login and register interfaces
│   ├── dashboard.html             # Analysis view, upload zone, timeline, and charts
│   ├── css/
│   │   └── style.css              # Custom styling (dark theme, glassmorphic glass card, timeline)
│   └── js/
│       └── app.js                 # Network controller, cookie-less session, Chart.js rendering
└── README.md                      # Comprehensive Setup and user guidelines (This file)
```

---

## Setup & Running Instructions

Follow these steps to launch the application:

### Step 1: Run the Python AI Microservice
The Python microservice handles text extraction, spaCy NLP matching, and PDF building.

1. Navigate to the `ai_module` directory:
   ```bash
   cd ai_module
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the Flask server:
   ```bash
   python app.py
   ```
   *The Flask microservice will run locally on `http://127.0.0.1:5000`.*

---

### Step 2: Run the Java Backend
The Spring Boot backend manages credentials, logs active sessions, cache results in SQLite, and communicates with the Python Flask app.

1. Open a new terminal and navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Build and compile the project using Maven:
   ```bash
   mvn clean install
   ```
3. Run the Spring Boot application:
   ```bash
   mvn spring-boot:run
   ```
   *The backend server will run on `http://localhost:8080`.*
   *Upon launch, Hibernate will automatically connect to `database/skillgraph.db` and initialize tables based on `schema.sql`.*

---

### Step 3: Launch the Frontend
Since the application uses local routing and handles CORS headers natively, you can run the client without setting up a secondary web server.

1. Navigate to the `frontend` folder.
2. Double-click `login.html` to open it in your browser (or use the VS Code Live Server extension).
3. Switch to **Sign Up** to create an account. Make sure to choose a career goal (e.g., *Full Stack Developer*).
4. Log in to access the main Dashboard page.
5. In the file upload box, select or drop the pre-packaged test resume: `ai_module/resume_sample.docx`.
6. Click **Analyze Resume** to view the Chart.js doughnut score, matched vs missing skills list, timeline learning roadmap, and certification recommendations.
7. Click **Download PDF Report** to save a generated, professionally styled ReportLab PDF.
