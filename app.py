"""
app.py
------
A minimal, well-documented CLI app demonstrating CRUD on a PostgreSQL `students` table.

Functions implemented (matching assignment names):
- getAllStudents(): retrieve and display all students
- addStudent(first_name, last_name, email, enrollment_date): insert a new row
- updateStudentEmail(student_id, new_email): update email by id
- deleteStudent(student_id): delete row by id

Run `python app.py -h` for usage.
"""

import os
import argparse
from contextlib import contextmanager
from typing import Any, Iterable, Optional, Tuple, List

from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from tabulate import tabulate

# Load environment variables from .env if present (PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE)
load_dotenv()

def get_db_params() -> dict:
    """Collect DB connection params from environment variables. Fail early if missing."""
    required = ["PGHOST", "PGPORT", "PGUSER", "PGPASSWORD", "PGDATABASE"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise SystemExit(f"Missing environment variables: {', '.join(missing)}. "
                         "Copy .env.example to .env and fill in your credentials.")
    return {
        "host": os.getenv("PGHOST"),
        "port": int(os.getenv("PGPORT")),
        "user": os.getenv("PGUSER"),
        "password": os.getenv("PGPASSWORD"),
        "dbname": os.getenv("PGDATABASE"),
    }

@contextmanager
def get_conn():
    """Context manager to acquire a DB connection and ensure proper cleanup on exit."""
    params = get_db_params()
    conn = psycopg2.connect(**params)
    try:
        yield conn
    finally:
        conn.close()

def getAllStudents() -> List[dict]:
    """Fetch and return all students as a list of dicts (for easy display)."""
    with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT student_id, first_name, last_name, email, enrollment_date FROM students ORDER BY student_id;")
        rows = cur.fetchall()
        return [dict(r) for r in rows]

def addStudent(first_name: str, last_name: str, email: str, enrollment_date: Optional[str]) -> int:
    """
    Insert a new student. Returns the generated student_id.

    Args:
        first_name: non-empty text
        last_name: non-empty text
        email: unique, non-empty text
        enrollment_date: optional ISO date 'YYYY-MM-DD' or None
    """
    sql = """
        INSERT INTO students (first_name, last_name, email, enrollment_date)
        VALUES (%s, %s, %s, %s)
        RETURNING student_id;
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (first_name, last_name, email, enrollment_date))
        new_id = cur.fetchone()[0]
        conn.commit()
        return new_id

def updateStudentEmail(student_id: int, new_email: str) -> int:
    """
    Update the email for a given student_id.
    Returns the number of rows updated (0 or 1).
    """
    sql = "UPDATE students SET email = %s WHERE student_id = %s;"
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (new_email, student_id))
        updated = cur.rowcount
        conn.commit()
        return updated

def deleteStudent(student_id: int) -> int:
    """
    Delete the student row for the given student_id.
    Returns the number of rows deleted (0 or 1).
    """
    sql = "DELETE FROM students WHERE student_id = %s;"
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (student_id,))
        deleted = cur.rowcount
        conn.commit()
        return deleted

def print_table(rows: List[dict]) -> None:
    """Nicely print result rows in a table using 'tabulate'."""
    if not rows:
        print("(no rows)")
        return
    headers = rows[0].keys()
    data = [list(r.values()) for r in rows]
    print(tabulate(data, headers=headers, tablefmt="github"))

def main():
    parser = argparse.ArgumentParser(description="PostgreSQL CRUD app for `students` table.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # get-all
    sub.add_parser("get-all", help="Retrieve and display all students.")

    # add
    p_add = sub.add_parser("add", help="Insert a new student.")
    p_add.add_argument("--first", required=True, help="First name")
    p_add.add_argument("--last", required=True, help="Last name")
    p_add.add_argument("--email", required=True, help="Email (must be unique)")
    p_add.add_argument("--date", required=False, help="Enrollment date (YYYY-MM-DD)")

    # update-email
    p_upd = sub.add_parser("update-email", help="Update a student's email by id.")
    p_upd.add_argument("--id", required=True, type=int, help="Student ID")
    p_upd.add_argument("--email", required=True, help="New email")

    # delete
    p_del = sub.add_parser("delete", help="Delete a student by id.")
    p_del.add_argument("--id", required=True, type=int, help="Student ID")

    args = parser.parse_args()

    try:
        if args.cmd == "get-all":
            rows = getAllStudents()
            print_table(rows)

        elif args.cmd == "add":
            new_id = addStudent(args.first, args.last, args.email, args.date)
            print(f"Inserted student_id={new_id}")
            rows = getAllStudents()
            print_table(rows)

        elif args.cmd == "update-email":
            updated = updateStudentEmail(args.id, args.email)
            if updated == 0:
                print(f"No student found with id {args.id}")
            else:
                print(f"Updated email for student_id={args.id}")
            rows = getAllStudents()
            print_table(rows)

        elif args.cmd == "delete":
            deleted = deleteStudent(args.id)
            if deleted == 0:
                print(f"No student found with id {args.id}")
            else:
                print(f"Deleted student_id={args.id}")
            rows = getAllStudents()
            print_table(rows)

    except psycopg2.errors.UniqueViolation as e:
        # Common error: duplicate email
        print("Error: Email must be unique. Choose a different email.")
    except Exception as e:
        # Generic error handler to keep demo flowing while surfacing the issue
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
