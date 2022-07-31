import click
from sqlalchemy.exc import IntegrityError

from api.v1.users import user_blueprint
from config import BASE_DIR
from db.base import engine
from db.base import init_db as init
from db.controllers.users import UserController
from utils.password import PasswordHasher


@user_blueprint.command("createsuperuser")
@click.argument(
    "login",
)
@click.argument("email")
@click.argument("password")
def create_superuser(login, email, password):
    payload = dict(login=login, email=email, password_hash=PasswordHasher.hash_password(password))
    role_id = 5
    UserController().create(payload, role_id)


@user_blueprint.command("init_db")
def init_db():
    init()
    with open(BASE_DIR.joinpath("db/scripts/1_base_data.sql"), "r") as file:
        commands = file.read().split("\n")
    with engine.connect() as connection:
        for command in commands:
            if command.startswith("--"):
                continue
            try:
                connection.execute(command)
            except IntegrityError:
                pass
