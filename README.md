# Job Application Tracker

## Project Overview

The Job Application Tracker is a full-stack database application developed for COP 4751 – Advanced Database Management.

The application helps users organize job opportunities, companies, contacts, and job applications in one place. It also includes a Job Match feature that compares user-entered skills with job requirements and ranks opportunities by match percentage.

## Technologies Used

- **Backend:** Python 3 and Flask
- **Database:** MySQL
- **Frontend:** HTML and CSS
- **Database Connector:** mysql-connector-python
- **Environment Variables:** python-dotenv
- **Version Control:** GitHub
- **AI Assistance:** ChatGPT

## Main Features

### Dashboard
Displays an overview of the information stored in the database, including the number of companies, jobs, applications, and contacts.

### Companies
Allows users to add, view, edit, and delete company records.

### Jobs
Allows users to manage job opportunities, including job titles, company information, salary details, and job requirements.

### Applications
Allows users to track submitted applications, application dates, status, resume versions, and interview information.

### Contacts
Allows users to manage professional contacts associated with companies.

### Job Match
Allows users to enter skills separated by commas. The application compares those skills with the requirements stored for each job, calculates a match percentage, and ranks matching opportunities from highest to lowest.

## Database Structure

The application uses four MySQL tables:

- `companies`
- `jobs`
- `applications`
- `contacts`

The database includes primary keys, foreign key relationships, and JSON fields for job requirements and interview information.

The database creation script is provided in `schema.sql`.

## Project Structure

job-application-tracker/
│
├── app.py
├── database.py
├── schema.sql
├── requirements.txt
├── README.md
├── AI_USAGE.md
├── .gitignore
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── companies.html
│   ├── jobs.html
│   ├── applications.html
│   ├── contacts.html
│   ├── manage_table.html
│   └── job_match.html
│
└── static/
    └── style.css

## Installation and Setup

### 1. Clone the Repository

git clone https://github.com/isabel0121/job-application-tracker.git
cd job-application-tracker

### 2. Install Python Dependencies

pip install -r requirements.txt

### 3. Create the MySQL Database

Open MySQL Workbench and execute:

CREATE DATABASE job_tracker;

Import the provided `schema.sql` file into MySQL Workbench to create the required tables and database structure.

### 4. Configure Environment Variables

Create a `.env` file in the project root directory with the following settings:

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD
DB_NAME=job_tracker
SECRET_KEY=your-secret-key

Replace `YOUR_MYSQL_PASSWORD` with your local MySQL password.

**Important:** Do not upload the `.env` file or your database password to GitHub.

### 5. Run the Application

Execute:

python app.py

Open your browser and navigate to:

http://127.0.0.1:5000


## Job Match Example

Enter skills such as:

Python, SQL, Java, Excel


The application displays matching jobs with their match percentages and matching skills.

## Course Information

**Course:** COP 4751 – Advanced Database Management

**Project:** Job Application Tracker

**Developer:** Isabel Milian

**GitHub Repository:** https://github.com/isabel0121/job-application-tracker
