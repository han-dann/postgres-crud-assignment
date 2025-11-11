# Assignment (3) - Q(1): PostgreSQL CRUD App

This repository implements a simple PostgreSQL-backed application that performs CRUD on a `students` table using **Python 3** and **psycopg2**.

> ✅ Matches the rubric:
> - Database created with correct schema & constraints
> - Initial data inserted
> - Functions implemented: `getAllStudents`, `addStudent`, `updateStudentEmail`, `deleteStudent`
> - Clear comments, error handling, and README instructions
> - Demo instructions and video script provided

---

## 🧱 Project Structure

```
postgres-crud-assignment/
├─ app.py                 # Main CLI app with CRUD functions
├─ requirements.txt       # Python dependencies
├─ .env.example           # Example environment variables
├─ sql/
│  ├─ 01_create_tables.sql
│  └─ 02_seed.sql
├─ scripts/
│  ├─ demo_commands.sh    # macOS/Linux demo helper
│  └─ demo_commands.ps1   # Windows PowerShell demo helper
└─ README.md
```

---

## 🗄️ Database Setup (pgAdmin or psql)

1. **Create the database (once):**
   - In **pgAdmin**: Right-click *Databases* → *Create* → *Database...* → Name: `school_db` → Save.
   - Or with **psql**:
     ```sql
     CREATE DATABASE school_db;
     ```

2. **Create the table & constraints:**
   - In **pgAdmin**: Open `school_db` → *Query Tool* → open `sql/01_create_tables.sql` → Run.
   - Or with **psql**:
     ```bash
     psql -U <your_user> -h <host> -d school_db -f sql/01_create_tables.sql
     ```

3. **Insert initial data:**
   - In **pgAdmin**: Run `sql/02_seed.sql`.
   - Or with **psql**:
     ```bash
     psql -U <your_user> -h <host> -d school_db -f sql/02_seed.sql
     ```

> Tip: If you re-run the seed and get duplicate emails, either truncate the table or use fresh emails for testing.

---

## ⚙️ App Setup

### 1) Prerequisites
- Python 3.10+
- PostgreSQL 14+ installed and running
- A database user with access to `school_db`

### 2) Clone & install
```bash
git clone <your-repo-url>.git
cd postgres-crud-assignment
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3) Configure environment
Copy the example env file and fill in your details:
```bash
cp .env.example .env
```
Open `.env` and set your real PostgreSQL credentials.

---

## 🚀 Run the App (CLI)

The app exposes subcommands for each function.

```bash
# List all students
python app.py get-all

# Add a student
python app.py add --first "Alice" --last "Wonder" --email "alice.wonder@example.com" --date 2023-09-03

# Update a student's email by id
python app.py update-email --id 1 --email "johnny.doe@example.com"

# Delete a student by id
python app.py delete --id 2
```

> After each INSERT/UPDATE/DELETE, verify the effect in **pgAdmin → Tables → students → View Data** (as requested).

---

## 📄 Demo Video (Add your link here)
- URL:(https://youtu.be/dsvpm7K-hs8)

---

## 🧪 Troubleshooting

- **`psycopg2` build error** → Use `psycopg2-binary` (already in `requirements.txt`).
- **Cannot connect (ECONNREFUSED)** → Check host/port, Postgres service, and your firewall.
- **`unique_violation` on email** → Use a different email or delete existing row.
- **Timezone/Date parsing** → Use ISO date format `YYYY-MM-DD`.

---

