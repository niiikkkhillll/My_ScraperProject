# MapLead Outscraper Clone 🚀

A premium Google Maps Lead Extraction application built with a **FastAPI** Python backend and a gorgeous, highly interactive **Vanilla HTML/CSS/JS** frontend. It supports both rapid data simulation and real live browser scraping via **Microsoft Playwright**.

---

## 🛠️ Prerequisites
- **Python 3.8 or higher** installed on your system.
- Node.js is **not** required, as the frontend is fully self-contained and served directly by FastAPI!

---

## 🚀 Quick Start Guide (Windows)

Follow these steps in your PowerShell or Command Prompt to set up and launch the application.

### Step 1: Open Terminal and Navigate to Project
Open your terminal (PowerShell or CMD) and navigate to the project subdirectory:
```powershell
cd "c:\Users\admimn\OneDrive\Desktop\MyScraperProject\outscraper-python"
```

### Step 2: Create a Python Virtual Environment (Recommended)
Creating a virtual environment ensures that the project's dependencies do not conflict with your global Python installation.

*   **In PowerShell / CMD:**
    ```powershell
    python -m venv venv
    ```

### Step 3: Activate the Virtual Environment
Activate the environment so that subsequent commands use the virtualized python interpreter:

*   **In PowerShell:**
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```
    *(Note: If you get a policy execution error, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` first)*

*   **In CMD (Command Prompt):**
    ```cmd
    .\venv\Scripts\activate.bat
    ```

### Step 4: Install Dependencies
Install all the required Python libraries listed in `requirements.txt`:
```powershell
pip install -r requirements.txt
```

### Step 5: Install Playwright Browser Binaries
Because the application features a **Real Engine** that scrapes Google Maps live using Playwright, you must install the headless Chromium browser binary:
```powershell
playwright install chromium
```

### Step 6: Start the FastAPI Server
Launch the development server using **Uvicorn**:
```powershell
uvicorn app:app --reload
```

---

## 🌐 Accessing the Application

Once Uvicorn starts, you will see output like this:
```text
INFO:     Will watch for changes in these directories: ['c:\\Users\\admimn\\OneDrive\\Desktop\\MyScraperProject\\outscraper-python']
INFO:     Uvicorn server running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

1. Open your web browser.
2. Navigate to: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**
3. The FastAPI app will serve the gorgeous static dashboard page directly!

---

## ⚡ Scraper Engine Options

In the web interface, you can select between two engines:
1. **Simulated Engine (Default):** Instantly generates highly realistic, correct business data, phone lists, and social media links. Perfect for fast testing without hitting anti-bot limits.
2. **Real Playwright Engine:** Launches a headless Chromium browser using Microsoft Playwright to scrape live listings from Google Maps based on your category and area inputs.
