-- 01_create_tables.sql
-- Creates table `students` per assignment spec.
-- Idempotent: drops table if it already exists (safe for dev demos).

DROP TABLE IF EXISTS students;

CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name  TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    enrollment_date DATE
);
