
import os
import json

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from dotenv import load_dotenv

from database import (
    get_records,
    get_columns,
    add_record,
    update_record,
    delete_record
)


# Load environment variables
load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "job-tracker-development-key"
)


# Database tables and display names
TABLES = {
    "companies": "Companies",
    "jobs": "Jobs",
    "applications": "Applications",
    "contacts": "Contacts"
}


# Dashboard
@app.route("/")
def dashboard():
    counts = {}

    for table in TABLES:
        counts[table] = len(get_records(table))

    applications = get_records("applications")

    recent_applications = sorted(
        applications,
        key=lambda item: str(
            item.get("application_date") or ""
        ),
        reverse=True
    )[:5]

    return render_template(
        "dashboard.html",
        counts=counts,
        recent_applications=recent_applications
    )


# CRUD operations for Companies, Jobs, Applications and Contacts
@app.route("/<table>", methods=["GET", "POST"])
def manage_table(table):

    if table not in TABLES:
        return "Page not found", 404

    columns = get_columns(table)

    primary_key = next(
        (
            column["Field"]
            for column in columns
            if column["Key"] == "PRI"
        ),
        None
    )

    if primary_key is None:
        return "Primary key not found", 500

    if request.method == "POST":

        action = request.form.get("action")

        try:

            if action == "add":

                add_record(table, request.form)

                flash(
                    "Record added successfully.",
                    "success"
                )

            elif action == "update":

                record_id = request.form.get("record_id")

                update_record(
                    table,
                    record_id,
                    request.form
                )

                flash(
                    "Record updated successfully.",
                    "success"
                )

            elif action == "delete":

                record_id = request.form.get("record_id")

                delete_record(
                    table,
                    record_id
                )

                flash(
                    "Record deleted successfully.",
                    "success"
                )

            else:

                flash(
                    "Invalid action.",
                    "error"
                )

        except Exception as error:

            flash(
                f"Error: {error}",
                "error"
            )

        return redirect(
            url_for(
                "manage_table",
                table=table
            )
        )

    records = get_records(table)

    editable_columns = [
        column
        for column in columns
        if column["Field"] != primary_key
        and "auto_increment" not in column["Extra"].lower()
        and "generated" not in column["Extra"].lower()
        and column["Field"] != "created_at"
    ]

    form_columns = [
        column
        for column in columns
        if column["Field"] != primary_key
        and "auto_increment" not in column["Extra"].lower()
        and "generated" not in column["Extra"].lower()
        and column["Field"] != "created_at"
    ]

    return render_template(
        f"{table}.html",
        records=records,
        columns=columns,
        editable_columns=editable_columns,
        form_columns=form_columns,
        primary_key=primary_key,
        page_title=TABLES[table]
    )


# Job Match
@app.route("/job-match", methods=["GET", "POST"])
def job_match():

    matches = []
    skills = ""

    if request.method == "POST":

        skills = request.form.get("skills", "")

        user_skills = {
            skill.strip().lower()
            for skill in skills.split(",")
            if skill.strip()
        }

        if user_skills:

            jobs = get_records("jobs")
            companies = get_records("companies")

            company_names = {
                company["company_id"]: company["company_name"]
                for company in companies
            }

            for job in jobs:

                requirements = job.get("requirements")

                # MySQL may return JSON as a string
                if isinstance(requirements, str):
                    try:
                        requirements = json.loads(requirements)
                    except json.JSONDecodeError:
                        requirements = []

                if not isinstance(requirements, list):
                    continue

                required_skills = {
                    str(skill).strip().lower()
                    for skill in requirements
                    if skill
                }

                if not required_skills:
                    continue

                matched_skills = sorted(
                    user_skills.intersection(required_skills)
                )

                percentage = round(
                    len(matched_skills)
                    / len(required_skills)
                    * 100
                )

                if percentage > 0:

                    matches.append({
                        "job": job,

                        "company_name": company_names.get(
                            job.get("company_id"),
                            "Unknown"
                        ),

                        "percentage": percentage,

                        "matched_skills": matched_skills
                    })

            # Highest match first
            matches.sort(
                key=lambda item: item["percentage"],
                reverse=True
            )

    return render_template(
        "job_match.html",
        matches=matches,
        skills=skills
    )


# Run application
if __name__ == "__main__":

    app.run(
        debug=True
    )
