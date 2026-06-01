# ScholarIntell
### Intelligent Scholarship Recommendation and Guidance System

---

## About The Project

ScholarIntell is an AI-powered web application that helps students find,
understand, and apply for scholarships based on their academic profile.
Students often miss suitable scholarships due to lack of awareness and scattered
information. ScholarIntell solves this by providing a centralized intelligent
system that recommends scholarships and checks eligibility using AI.

---

## Features

- Student registration and login system
- Academic profile creation (CGPA, degree, field, language certificate)
- Smart recommendation engine matches 295+ scholarships to student profile
- AI Eligibility Checker powered by LLaMA 3 via Groq API
- Search scholarships by keyword, country, or field of study
- Filter by fully funded, degree level, and country
- Scholarship detail page with direct application links
- Admin panel for managing scholarships
- Professional responsive UI with Bootstrap 5

---

## Tech Stack

- Backend  : Python 3, Django
- Database : SQLite
- Frontend : HTML5, Bootstrap 5, Bootstrap Icons
- AI Engine: LLaMA 3.3 70B via Groq API
- Data     : 297 scholarships, 46+ countries

---

## How To Run

1. Activate virtual environment
   source venv/bin/activate

2. Install dependencies
   pip install -r requirements.txt

3. Create .env file with your Groq API key
   GROQ_API_KEY=your_groq_api_key_here
   Get a free key at: https://console.groq.com

4. Run database migrations
   python manage.py migrate

5. Import scholarship data
   python manage.py import_scholarships

6. Create admin account
   python manage.py createsuperuser

7. Start the server
   python manage.py runserver

   Visit: http://127.0.0.1:8000

---

## How The Recommendation Engine Works

The smart recommender filters scholarships by student degree level,
then filters by field of study, then scores each scholarship:
- Fully funded        = +40 points
- Preferred country   = +30 points
- Language score match= +20 points
- No language required= +10 points
Results are sorted by score highest first.

---

## How The AI Eligibility Checker Works

The AI checker sends the student profile and scholarship details
to LLaMA 3.3 70B via Groq API and gets back:
- Verdict: STRONG MATCH / PARTIAL MATCH / NOT ELIGIBLE
- Reasons why the student qualifies
- Concerns or missing requirements
- Honest recommendation on whether to apply

---

## Pages

  /                                Home page
  /accounts/register/              Student registration
  /accounts/login/                 Login
  /accounts/profile/               Academic profile form
  /scholarships/dashboard/         Recommendation dashboard
  /scholarships/search/            Search scholarships
  /scholarships/id/                Scholarship detail
  /scholarships/id/eligibility/    AI eligibility checker
  /admin/                          Admin panel

---

## Scholarship Database

The database contains 297 scholarships with these fields:
- Scholarship ID, Name, Description
- Level (Bachelor, Master, PhD)
- Host Institution and Host Country
- Field of Study
- Fully Funded (Yes or No)
- What It Covers
- Special Requirements
- Application Link and Deadline
- Language Requirements

---

## Student Information

- Name           : Noor ul Huda
- Registration No: F22BSEEN1E02009
- Semester       : 7th Semester
- Project Title  : SCHOLARINTELL
- Year           : 2026

---

## Submission Checklist

- Project runs locally with runserver
- Admin panel accessible at /admin/
- 297 scholarships imported in database
- Student can register, login, and create profile
- Recommendation engine returns matched scholarships
- AI eligibility checker working with Groq API
- Search and filter working
- All pages responsive on mobile and desktop
- requirements.txt included
- README.md included

---

ScholarIntell - Final Year Project - Noor ul Huda - 2026