from ast import match_case
import subprocess, sys


def run_development_server():
    subprocess.run(["pg_ctl", "-D", "C:\\Program Files\\PostgreSQL\\17\\data", "start"])
    subprocess.run(["uv", "run", "manage.py", "runserver"])


def make_migrations_and_migrate():
    subprocess.run(["uv", "run", "manage.py", "makemigrations"])
    subprocess.run(["uv", "run", "manage.py", "migrate"])


def start_database():
    subprocess.run(["pg_ctl", "-D", "C:\\Program Files\\PostgreSQL\\17\\data", "start"])


def stop_database():
    subprocess.run(["pg_ctl", "-D", "C:\\Program Files\\PostgreSQL\\17\\data", "stop"])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        match (sys.argv[1]):
            case "dev":
                run_development_server()
            case "migrate":
                make_migrations_and_migrate()
            case "startdb":
                start_database()
            case "stopdb":
                stop_database()
