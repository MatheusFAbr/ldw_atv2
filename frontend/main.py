import flet as ft
import requests

API_URL = "http://localhost:5000/games/"

# ── Paleta gamer dark ─────────────────────────────────────────────────────────
BG_DARK    = "#0d0d0d"
BG_CARD    = "#1a1a2e"
BG_SURFACE = "#16213e"
ACCENT     = "#e94560"
ACCENT2    = "#0f3460"
TEXT_PRI   = "#eaeaea"
TEXT_SEC   = "#a0a0b0"
SUCCESS    = "#00d97e"
ERROR      = "#ff4757"
BORDER     = "#2a2a4a"


def buscar_games() -> list[dict]:
    try:
        r = requests.get(API_URL, timeout=5)
        r.raise_for_status()
        return r.json().get("games", [])
    except Exception:
        return []


def cadastrar_game(dados: dict) -> tuple[bool, str]:
    try:
        r = requests.post(API_URL, json=dados, timeout=5)
        if r.status_code == 201:
            return True, r.json().get("mensagem", "Cadastrado com sucesso!")
        detalhes = r.json().get("detalhes", [])
        if detalhes:
            msgs = ", ".join(f"{d['campo']}: {d['mensagem']}" for d in detalhes)
            return False, f"Dados inválidos — {msgs}"
        return False, r.json().get("erro", "Erro desconhecido")
    except requests.exceptions.ConnectionError:
        return False, "Não foi possível conectar ao backend. Certifique-se que o servidor está rodando."
    except Exception as e:
        return False, str(e)


def card_game(game: dict) -> ft.Container:
    nota = game.get("nota", 0)
    cor_nota = SUCCESS if nota >= 8 else (ACCENT if nota >= 6 else ERROR)

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(game.get("titulo", ""), size=16, weight=ft.FontWeight.BOLD,
                                color=TEXT_PRI),
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Text(game.get("genero", ""), size=11, color=TEXT_SEC),
                                    bgcolor="#2a2a4a", border_radius=4,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                ),
                                ft.Container(
                                    content=ft.Text(game.get("plataforma", ""), size=11, color=TEXT_SEC),
                                    bgcolor="#1e3a5f", border_radius=4,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                ),
                            ],
                            spacing=6,
                        ),
                    ],
                    spacing=6,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Text(f"{nota:.1f}", size=22, weight=ft.FontWeight.BOLD, color=cor_nota),
                    width=56,
                    alignment=ft.alignment.center,
                    border=ft.border.all(2, cor_nota),
                    border_radius=8,
                    padding=6,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=BG_CARD,
        border_radius=10,
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        border=ft.border.all(1, BORDER),
        margin=ft.margin.only(bottom=8),
    )


def main(page: ft.Page) -> None:
    page.title = "GameVault — Catálogo de Jogos"
    page.bgcolor = BG_DARK
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.fonts = {"Inter": "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap"}

    # ── Estado ────────────────────────────────────────────────────────────────
    lista_column = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)
    feedback_text = ft.Text("", size=13, text_align=ft.TextAlign.CENTER)
    loading = ft.ProgressRing(width=24, height=24, stroke_width=2, color=ACCENT, visible=False)

    def atualizar_lista():
        lista_column.controls.clear()
        games = buscar_games()
        if not games:
            lista_column.controls.append(
                ft.Text("Nenhum game encontrado.", color=TEXT_SEC, size=14,
                        text_align=ft.TextAlign.CENTER)
            )
        else:
            for g in games:
                lista_column.controls.append(card_game(g))
        page.update()

    # ── Formulário ────────────────────────────────────────────────────────────
    field_style = {
        "bgcolor": BG_SURFACE,
        "border_color": BORDER,
        "focused_border_color": ACCENT,
        "color": TEXT_PRI,
        "cursor_color": ACCENT,
        "label_style": ft.TextStyle(color=TEXT_SEC),
        "border_radius": 8,
    }

    tf_titulo    = ft.TextField(label="Título do Jogo", **field_style)
    tf_genero    = ft.TextField(label="Gênero", **field_style)
    tf_plataforma = ft.TextField(label="Plataforma", **field_style)
    tf_nota      = ft.TextField(label="Nota (0 – 10)", keyboard_type=ft.KeyboardType.NUMBER, **field_style)

    def limpar_form():
        for f in (tf_titulo, tf_genero, tf_plataforma, tf_nota):
            f.value = ""
            f.error_text = None

    def enviar_form(e):
        # Limpa apenas os erros — não os valores dos campos
        for f in (tf_titulo, tf_genero, tf_plataforma, tf_nota):
            f.error_text = None
        feedback_text.color = TEXT_SEC
        feedback_text.value = ""

        erros = False
        if not tf_titulo.value.strip():
            tf_titulo.error_text = "Obrigatório"
            erros = True
        if not tf_genero.value.strip():
            tf_genero.error_text = "Obrigatório"
            erros = True
        if not tf_plataforma.value.strip():
            tf_plataforma.error_text = "Obrigatório"
            erros = True

        nota_str = tf_nota.value.strip().replace(",", ".")
        try:
            nota_val = float(nota_str)
            if not (0 <= nota_val <= 10):
                raise ValueError
        except ValueError:
            tf_nota.error_text = "Digite um número entre 0 e 10"
            erros = True

        if erros:
            page.update()
            return

        loading.visible = True
        page.update()

        sucesso, msg = cadastrar_game({
            "titulo": tf_titulo.value.strip(),
            "genero": tf_genero.value.strip(),
            "plataforma": tf_plataforma.value.strip(),
            "nota": nota_val,
        })

        loading.visible = False
        feedback_text.value = msg
        feedback_text.color = SUCCESS if sucesso else ERROR

        if sucesso:
            limpar_form()
            atualizar_lista()
        page.update()

    btn_enviar = ft.ElevatedButton(
        text="Cadastrar Game",
        on_click=enviar_form,
        bgcolor=ACCENT,
        color=TEXT_PRI,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        height=44,
        expand=True,
    )

    formulario = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Cadastrar Novo Game", size=18, weight=ft.FontWeight.BOLD,
                        color=TEXT_PRI),
                tf_titulo,
                tf_genero,
                tf_plataforma,
                tf_nota,
                ft.Row(controls=[btn_enviar, loading], spacing=10,
                       vertical_alignment=ft.CrossAxisAlignment.CENTER),
                feedback_text,
            ],
            spacing=12,
        ),
        bgcolor=BG_CARD,
        border_radius=12,
        padding=20,
        border=ft.border.all(1, BORDER),
        width=380,
    )

    # ── Header ────────────────────────────────────────────────────────────────
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text("GAMEVAULT", size=28, weight=ft.FontWeight.BOLD, color=ACCENT),
                        ft.Text("Catálogo de Jogos", size=13, color=TEXT_SEC),
                    ],
                    spacing=2,
                ),
                ft.IconButton(
                    icon=ft.Icons.REFRESH,
                    icon_color=ACCENT,
                    tooltip="Atualizar lista",
                    on_click=lambda _: atualizar_lista(),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=BG_SURFACE,
        padding=ft.padding.symmetric(horizontal=24, vertical=16),
        border=ft.border.only(bottom=ft.border.BorderSide(1, BORDER)),
    )

    # ── Painel da lista ───────────────────────────────────────────────────────
    painel_lista = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Jogos Cadastrados", size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRI),
                ft.Divider(color=BORDER, height=1),
                lista_column,
            ],
            spacing=12,
            expand=True,
        ),
        bgcolor=BG_CARD,
        border_radius=12,
        padding=20,
        border=ft.border.all(1, BORDER),
        expand=True,
    )

    # ── Layout principal ──────────────────────────────────────────────────────
    body = ft.Container(
        content=ft.Row(
            controls=[painel_lista, formulario],
            spacing=20,
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        ),
        padding=24,
        expand=True,
    )

    page.add(
        ft.Column(
            controls=[header, body],
            spacing=0,
            expand=True,
        )
    )

    atualizar_lista()


ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)
