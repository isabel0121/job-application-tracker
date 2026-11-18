
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

ALLOWED_TABLES = {
    "companies",
    "jobs",
    "applications",
    "contacts"
}


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "job_tracker")
    )


def get_columns(table):
    if table not in ALLOWED_TABLES:
        raise ValueError("Invalid table")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(f"SHOW COLUMNS FROM `{table}`")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def get_primary_key(table):
    for column in get_columns(table):
        if column["Key"] == "PRI":
            return column["Field"]

    raise ValueError("Primary key not found")


def get_records(table):
    if table not in ALLOWED_TABLES:
        raise ValueError("Invalid table")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(f"SELECT * FROM `{table}`")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def add_record(table, data):
    columns = get_columns(table)

    allowed = {
        column["Field"]
        for column in columns
        if "auto_increment" not in column["Extra"].lower()
        and "generated" not in column["Extra"].lower()
    }

    values = {
        key: value.strip()
        for key, value in data.items()
        if key in allowed and value.strip() != ""
    }

    if not values:
        raise ValueError("Please enter at least one value.")

    names = ", ".join(f"`{name}`" for name in values)
    placeholders = ", ".join(["%s"] * len(values))

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            f"INSERT INTO `{table}` ({names}) VALUES ({placeholders})",
            list(values.values())
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def update_record(table, record_id, data):
    primary_key = get_primary_key(table)
    columns = get_columns(table)

    allowed = {
        column["Field"]
        for column in columns
        if column["Field"] != primary_key
        and "auto_increment" not in column["Extra"].lower()
        and "generated" not in column["Extra"].lower()
    }

    values = {
        key: value.strip()
        for key, value in data.items()
        if key in allowed and value.strip() != ""
    }

    if not values:
        raise ValueError("No fields to update.")

    assignments = ", ".join(
        f"`{name}` = %s" for name in values
    )

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            f"UPDATE `{table}` SET {assignments} "
            f"WHERE `{primary_key}` = %s",
            list(values.values()) + [record_id]
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def delete_record(table, record_id):
    primary_key = get_primary_key(table)

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            f"DELETE FROM `{table}` WHERE `{primary_key}` = %s",
            (record_id,)
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()
