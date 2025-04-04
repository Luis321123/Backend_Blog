from uuid import uuid4
from pydantic import Field, HttpUrl, Optional
from app.models.basemodel import MongoDBModel

class Post(MongoDBModel):
    """
    Modelo de bebida para MongoDB con soft delete
    """
    uuid: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Identificador único adicional"
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Nombre del post"
    )
    title: str = Field(
        min_length=1,
        max_length=255,
        description="Titulo del post"
    )
    desc: str = Field(
        None,
        min_length=1,
        description="previa descripcion del post"
    )

    image_url: Optional[str] = Field(
        None,
        description="url de la imagen del post"
    )

    tags: list[str] = Field(default_factory=list)

    # No necesitamos declarar deleted_at porque viene de MongoDBModel