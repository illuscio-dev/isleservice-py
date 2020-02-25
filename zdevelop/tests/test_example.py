from spanserver import test_utils

from service.api import api
from isleservice_objects import models, schemas, errors


def test_greeting():

    # We have to use a context manager here to trigger startup and shutdown events.
    # This is not in responder's documentation.
    with api.requests as client:
        enemy = models.Enemy("General", models.Name("Obi-Wan", "Kenobi"))

        data = schemas.EnemySchema().dump(enemy)
        r = client.get("/greet", json=data)

        test_utils.validate_response(response=r, text_value="GENERAL KENOBI!")


def test_error():

    with api.requests as client:
        enemy = models.Enemy("General", models.Name("Obi-Wan", "Kenobi"))

        data = schemas.EnemySchema(exclude=["rank"]).dump(enemy)
        r = client.post("/greet", json=data)

        test_utils.validate_error(r, errors.CoughError)
