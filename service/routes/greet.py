from spanserver import (
    SpanRoute,
    Request,
    Response,
    MimeType,
    RecordType,
    DocInfo,
    DocRespInfo,
)
from isleservice_objects import models, errors, schemas

from service.api import api


class SchemaCache:
    ENEMY_FULL = schemas.EnemySchema()
    ENEMY_POST = schemas.EnemySchema(exclude=["rank"])


@api.route("/greet")
class Greet(SpanRoute):
    """
    Bellow a greeting at an enemy.
    """

    @api.use_schema(req=SchemaCache.ENEMY_FULL, resp=MimeType.TEXT)
    async def on_get(
        self, req: Request[RecordType, models.Enemy], resp: Response
    ) -> None:
        """
        Get a greeting.
        """
        data = await req.media_loaded()
        resp.media = f"{data.addressable.upper()}!"

    @api.use_schema(req=SchemaCache.ENEMY_POST, resp=MimeType.TEXT)
    async def on_post(
        self, req: Request[RecordType, models.Enemy], resp: Response
    ) -> None:
        """
        Send a greeting to an Enemy.
        """
        resp.status_code = 201
        raise errors.CoughError("HACK! COUGH! HCCCCKKK!!!")

    class Document:
        example_enemy = models.Enemy("General", models.Name("Obi-wan", "Kenobi"))
        get = DocInfo(
            req_example=example_enemy,
            responses={200: DocRespInfo(example="GENERAL KENOBI!")},
        )

        # We can use the full model here, the excluded field will get ignored when
        # marshmallow dumps the schema (no validation happens on a dump)
        post = DocInfo(
            req_example=example_enemy,
            responses={201: DocRespInfo(example="GENERAL KENOBI!")},
        )
