# Guerra dos Pombos: O Resgate das Pastas — Jogo Arcade 2D

## Visão geral

**Guerra dos Pombos: O Resgate das Pastas** é um jogo Arcade 2D desenvolvido para a disciplina de **Computação Gráfica**.

O jogador controla um professor que precisa correr de um lado para o outro para **resgatar pastas que estão caindo** enquanto tenta **desviar dos cocôs dos pombos**.

O projeto foi desenvolvido com foco na implementação manual dos principais conceitos de Computação Gráfica estudados na disciplina, incluindo rasterização, preenchimento de regiões, transformações geométricas, animação, Window/Viewport, clipping e mapeamento de textura.

---

## Vídeo de demonstração

Assista ao jogo em execução:



---

## Conceito do jogo

O jogo apresenta uma situação caótica dentro da faculdade: o professor precisa recuperar documentos/pastas importantes para uma reunião.

Ao mesmo tempo, pombos sobrevoam o local e deixam cair cocôs que podem fazer o professor se sujar e perder a reunião.

O jogador precisa equilibrar **movimentação, coleta e desvio de obstáculos** para atingir a meta da dificuldade escolhida.

### Objetivo

Recuperar a quantidade necessária de pastas (conforme a dificuldade) das trinta que vão cair do céu, sem sujar suas roupas (perder todas as vidas).

A partida termina somente depois que as **30 pastas** tiverem caído do céu.

### Dificuldades

A dificuldade é escolhida pelo menu antes do início da partida.

| Dificuldade | Vidas | Meta de pastas | Velocidade das pastas | Frequência dos cocos |
|---|---:|---:|---:|---:|
| **Fácil** | 5 | 30% | 150 | 2,0 s |
| **Normal** | 3 | 50% | 250 | 1,0 s |
| **Difícil** | 1 | 70% | 350 | 0,5 s |

A dificuldade permanece fixa durante a partida.

---

## Controles

- **A / Seta para esquerda:** mover para a esquerda
- **D / Seta para direita:** mover para a direita
- **F3:** mostrar/ocultar as caixas de colisão
- **ENTER:** voltar ao menu em telas que disponibilizam essa opção
- **Mouse:** interagir com os menus
- **Roda do mouse:** rolar o conteúdo da História / Manual

---

## Funcionalidades

### Menu interativo

O jogo possui um menu com:

- Iniciar partida
- Seleção de dificuldade
- História / Manual

A interface é construída utilizando os próprios recursos de rasterização do projeto para os elementos geométricos.

### Sistema de vidas (camisas)

Cada dificuldade possui uma quantidade diferente de camisas.

Quando o professor é atingido por um coco de pombo, uma camisa é perdida.

### Sistema de progressão

A HUD apresenta:

- quantidade de vidas;
- quantidade de pastas recuperadas;
- porcentagem de progresso;
- contador de FPS.

### Minimapa

A partida possui um minimapa que utiliza:

- Window;
- transformação Mundo → Viewport;
- escala/zoom;
- translação;
- Cohen-Sutherland;
- Bresenham.

### Animação

O professor possui uma animação composta por oito imagens de corrida.

As pastas possuem animação contínua de rotação durante a queda.

---

## Recursos de Computação Gráfica implementados

### Set Pixel

Implementado em:

[`src/engine/rasterizacao.py`](src/engine/rasterizacao.py)

Função:

```python
setPixel()
```

A função converte as coordenadas para inteiros, verifica os limites da superfície e escreve o pixel correspondente.

---

### Primitivas de rasterização

Implementadas manualmente em:

[`src/engine/rasterizacao.py`](src/engine/rasterizacao.py)

#### Linha

Algoritmo de **Bresenham**:

```python
bresenham()
desenhar_linha()
```

#### Circunferência

Algoritmo de ponto médio da circunferência:

```python
desenhar_circulo()
```

#### Elipse

Algoritmo de ponto médio da elipse, dividido em duas regiões:

```python
desenhar_elipse()
```

Essas primitivas são utilizadas na tela inicial e em elementos da interface do jogo.

---

## Preenchimento de regiões

### Boundary Fill

Implementado em:

[`src/engine/rasterizacao.py`](src/engine/rasterizacao.py)

Função:

```python
boundary_fill()
```

É utilizado na construção das figuras da tela inicial.

### Scanline Fill

Também implementado manualmente em:

```python
scanline_fill()
```

O algoritmo percorre as linhas horizontais do polígono, encontra as interseções com suas arestas e preenche os intervalos correspondentes.

O Scanline é utilizado em:

- polígonos do cenário;
- botões;
- painéis;
- HUD;
- elementos do minimapa;
- preenchimento de objetos.

---

## Gradiente de cores

O projeto implementa **Scanline com interpolação de cores entre os vértices**.

Em:

[`src/engine/rasterizacao.py`](src/engine/rasterizacao.py)

são utilizadas:

```python
interpola_cor()
scanline_fill_gradiente()
```

As cores fornecidas aos vértices são interpoladas ao longo das arestas e também entre as interseções de cada scanline.

O gradiente é utilizado no cenário inicial.

---

## Mapeamento de textura

O mapeamento de textura é implementado em:

[`src/engine/textura.py`](src/engine/textura.py)

Função:

```python
scanline_textura()
```

O algoritmo recebe vértices com coordenadas:

```text
(x, y) + (u, v)
```

e realiza a interpolação das coordenadas UV para determinar qual pixel da imagem corresponde a cada pixel do polígono.

Texturas são utilizadas em:

- professor;
- animação de corrida;
- pastas;
- cocos dos pombos;
- elementos do HUD;
- cenário da partida;
- pombos da tela inicial.

---

## Transformações geométricas

As transformações são implementadas manualmente com matrizes homogêneas 3×3 em:

[`src/engine/transformacoes.py`](src/engine/transformacoes.py)

### Translação

```python
translacao(tx, ty)
```

### Escala

```python
escala(sx, sy)
```

### Rotação

```python
rotacao(angulo_rad)
```

A rotação utiliza ângulos em radianos.

### Multiplicação de matrizes

```python
multiplica_matrizes()
```

### Aplicação da transformação

```python
aplica_transformacao()
```

As transformações são utilizadas diretamente pelas entidades do jogo. A pasta, por exemplo, combina escala, rotação e translação.

---

## Window e Viewport

O sistema de visualização é implementado em:

[`src/engine/viewport.py`](src/engine/viewport.py)

e utilizado pelo:

[`src/ui/minimapa.py`](src/ui/minimapa.py)

O minimapa define uma **Window** no espaço do mundo e transforma suas coordenadas para uma **Viewport** na tela.

O processo utiliza:

```text
Mundo
  ↓
Translação
  ↓
Escala / Zoom
  ↓
Viewport
  ↓
Dispositivo
```

A Window acompanha o jogador e o nível de zoom pode alterar a região observada.

---

## Clipping — Cohen-Sutherland

O recorte de linhas é implementado em:

[`src/engine/recorte.py`](src/engine/recorte.py)

Função:

```python
cohen_sutherland()
```

O algoritmo classifica os pontos usando códigos de região e determina se a linha:

- está totalmente dentro;
- está totalmente fora;
- precisa ser recortada.

No jogo, o Cohen-Sutherland é utilizado no minimapa antes das linhas serem rasterizadas com Bresenham.

---

## Colisões

As colisões são tratadas em:

[`src/engine/colisoes.py`](src/engine/colisoes.py)

O jogo utiliza **AABB (Axis-Aligned Bounding Box)** para verificar colisões.

As entidades possuem geometria visual e uma geometria específica para colisão, permitindo que a área efetiva de colisão seja menor que a área visual da textura.

---

## Arquitetura do projeto

A organização foi dividida em módulos de acordo com suas responsabilidades:

```text
jogo/
│
├── assets/
│   ├── cenario/
│   ├── coco/
│   ├── fonte/
│   ├── pastas/
│   ├── personagem_professor/
│   ├── pombos/
│   └── vidas_camisa/
│
├── src/
│   ├── cenario/
│   │   ├── __init__.py
│   │   └── cenario_menu.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── caminhos.py
│   │   ├── constantes.py
│   │   ├── cores.py
│   │   └── dificuldades.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── entrada.py
│   │   └── recursos.py
│   │
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── colisoes.py
│   │   ├── rasterizacao.py
│   │   ├── recorte.py
│   │   ├── textura.py
│   │   ├── transformacoes.py
│   │   └── viewport.py
│   │
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── coco_pombo.py
│   │   ├── entidade.py
│   │   ├── jogador.py
│   │   └── pasta.py
│   │
│   ├── estados/
│   │   ├── __init__.py
│   │   ├── dificuldade.py
│   │   ├── estado.py
│   │   ├── fim.py
│   │   ├── historia.py
│   │   ├── jogando.py
│   │   └── menu.py
│   │
│   ├── game/
│   │   ├── __init__.py
│   │   └── jogo.py
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── botao.py
│   │   ├── hud.py
│   │   ├── minimapa.py
│   │   └── painel.py
│   │
│   └── main.py
│
├── .gitignore
├── README.md
└── requisitos.txt
```

### Responsabilidades

**`engine/`**

Contém os algoritmos e ferramentas de Computação Gráfica, procurando manter a implementação reutilizável e independente da lógica específica da partida.

**`entities/`**

Contém as entidades do jogo e seus comportamentos:

- `Entidade`
- `Jogador`
- `Pasta`
- `CocoPombo`

**`estados/`**

Controla os diferentes estados da aplicação:

- menu;
- escolha de dificuldade;
- história/manual;
- partida;
- fim de jogo.

**`ui/`**

Contém componentes reutilizáveis da interface:

- botão;
- painel;
- HUD;
- minimapa.

**`core/`**

Contém a infraestrutura compartilhada, incluindo entrada do usuário e gerenciamento/cache de recursos.

**`config/`**

Centraliza caminhos, cores, constantes e configurações de dificuldade.

**`cenario/`**

Responsável pelo cenário visual compartilhado das telas de menu.

**`game/`**

Contém a classe principal que inicializa o jogo e coordena o loop principal.

---

## Desempenho e otimizações

O projeto foi desenvolvido considerando o custo das operações de rasterização por software.

Algumas decisões adotadas incluem:

- cache de imagens e fontes por meio do `GerenciadorRecursos`;
- cenário do menu pré-renderizado uma única vez;
- pré-renderização das linhas de texto da História / Manual;
- uso de `PixelArray` para acesso direto aos pixels durante o mapeamento de textura;
- separação entre lógica de atualização e desenho;
- utilização de `dt` para movimentação e animação independente do FPS;
- remoção de carregamentos repetidos de imagens e fontes;
- remoção de bibliotecas/dependências não utilizadas.

Como a rasterização e o mapeamento de textura são implementados em Python, o desempenho pode variar de acordo com a quantidade de operações por frame e com o hardware utilizado.

---

## Tecnologias

- **Python**
- **Pygame Community Edition (pygame-ce)**

Dependências:

```text
pygame-ce>=2.5.0
```

---

## Restrições acadêmicas

Os principais algoritmos de Computação Gráfica exigidos pela disciplina foram implementados manualmente no projeto, incluindo:

- rasterização de reta;
- rasterização de circunferência;
- rasterização de elipse;
- Boundary Fill;
- Scanline;
- gradiente por vértices;
- transformações geométricas;
- Window / Viewport;
- Cohen-Sutherland;
- mapeamento de textura.

O Pygame é utilizado como infraestrutura da aplicação para recursos como criação da janela, entrada do usuário, superfícies, fontes e acesso aos pixels. A lógica dos algoritmos gráficos exigidos é implementada no código do projeto.

---

## Como executar

### Requisitos

Tenha o Python instalado e disponível no terminal.

### Instalação

Na raiz do projeto:

```bash
pip install -r requisitos.txt
```

### Execução

Ainda na raiz do projeto:

```bash
python src/main.py
```

O jogo será iniciado no menu principal.

---

## Estrutura de apresentação

Durante a apresentação, os principais recursos de Computação Gráfica podem ser demonstrados por meio das seguintes partes do projeto:

| Recurso | Local principal |
|---|---|
| Set Pixel | `src/engine/rasterizacao.py` |
| Bresenham | `src/engine/rasterizacao.py` |
| Círculo | `src/engine/rasterizacao.py` |
| Elipse | `src/engine/rasterizacao.py` |
| Boundary Fill | `src/engine/rasterizacao.py` |
| Scanline | `src/engine/rasterizacao.py` |
| Gradiente | `src/engine/rasterizacao.py` |
| Textura | `src/engine/textura.py` |
| Transformações | `src/engine/transformacoes.py` |
| Window / Viewport | `src/engine/viewport.py` e `src/ui/minimapa.py` |
| Cohen-Sutherland | `src/engine/recorte.py` |
| Colisões | `src/engine/colisoes.py` |
| Animação | `src/entities/jogador.py` e `src/entities/pasta.py` |

---

## Observações finais

O projeto prioriza:

- clareza didática;
- implementação manual dos algoritmos da disciplina;
- organização modular;
- reutilização de componentes;
- separação entre engine gráfica, entidades, interface e estados do jogo;
- desempenho compatível com uma aplicação 2D em software rasterizer.

