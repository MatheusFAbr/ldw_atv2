from pydantic import BaseModel, Field, field_validator


class GameSchema(BaseModel):
    titulo: str = Field(..., min_length=1, description="Título do jogo")
    genero: str = Field(..., min_length=1, description="Gênero do jogo")
    plataforma: str = Field(..., min_length=1, description="Plataforma do jogo")
    nota: float = Field(..., ge=0, le=10, description="Nota de 0 a 10")

    @field_validator("titulo", "genero", "plataforma", mode="before")
    @classmethod
    def nao_pode_ser_vazio(cls, v: str) -> str:
        if isinstance(v, str) and v.strip() == "":
            raise ValueError("Campo não pode ser vazio")
        return v
