import subprocess, sys


def run_development_server():
    subprocess.run(["pg_ctl", "-D", "C:\\Program Files\\PostgreSQL\\17\\data", "start"])
    subprocess.run(["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"])


def run_production_server():
    subprocess.run(["python", "createsuperuser.py"])
    subprocess.run(["python", "manage.py", "makemigrations"])
    subprocess.run(["python", "manage.py", "migrate"])
    subprocess.run(["python", "manage.py", "collectstatic"])
    subprocess.run(["gunicorn", "real_estate_api.wsgi:application"])


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
            case "prod":
                run_production_server()
            case "migrate":
                make_migrations_and_migrate()
            case "startdb":
                start_database()
            case "stopdb":
                stop_database()
