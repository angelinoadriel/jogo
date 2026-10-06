from dataclasses import dataclass


@dataclass(frozen=True)
class ConfigDificuldade:

    nome: str

    vidas: int

    meta: float

    velocidade_pasta: float

    frequencia_coco: float


DIFICULDADES = {

    1: ConfigDificuldade(
        nome="Fácil",
        vidas=5,
        meta=0.30,
        velocidade_pasta=150.0,
        frequencia_coco=2.0
    ),

    2: ConfigDificuldade(
        nome="Normal",
        vidas=3,
        meta=0.50,
        velocidade_pasta=250.0,
        frequencia_coco=1.0
    ),

    3: ConfigDificuldade(
        nome="Difícil",
        vidas=1,
        meta=0.70,
        velocidade_pasta=350.0,
        frequencia_coco=0.5
    )
}