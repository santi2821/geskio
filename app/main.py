import flet as ft

# ─── Tokens premium (Figma) ─────────────────────────────────────────────
# Intento importar de dashboard si existe para consistencia; fallback a local.
try:
    from screens.dashboard import COLORS as _DASH_COLORS  # noqa: F401
except Exception:
    try:
        from app.screens.dashboard import COLORS as _DASH_COLORS  # noqa: F401
    except Exception:
        _DASH_COLORS = None

COLORS = {
    "primary": "#16a34a",
    "bg": "#f8fafc",
    "surface": "#ffffff",
    "text": "#0f172a",
    "muted": "#64748b",
    "border": "#e2e8f0",
    "sidebar": "#0f172a",
    "sidebar_active": "#1e293b",
    "grey": "#94a3b8",
}
RADIUS = 16

# ─── Imports screens (proveedores condicional) ──────────────────────────
try:
    from screens.dashboard import PantallaDashboard
except ImportError:
    from app.screens.dashboard import PantallaDashboard

try:
    from screens.caja import PantallaCaja
except ImportError:
    from app.screens.caja import PantallaCaja

try:
    from screens.stock import PantallaStock
except ImportError:
    from app.screens.stock import PantallaStock

try:
    from screens.clientes import PantallaClientes
except ImportError:
    from app.screens.clientes import PantallaClientes

try:
    from screens.fiado import PantallaFiado
except ImportError:
    from app.screens.fiado import PantallaFiado

try:
    from screens.chat import PantallaChat
except ImportError:
    from app.screens.chat import PantallaChat

# proveedores: condicional por spec (si no existe, placeholder)
try:
    from screens.proveedores import PantallaProveedores
except ImportError:
    try:
        from app.screens.proveedores import PantallaProveedores
    except ImportError:
        PantallaProveedores = None


TITLES = {
    "dash": "Dashboard",
    "caja": "Caja",
    "stock": "Stock",
    "clientes": "Clientes",
    "proveedores": "Proveedores",
    "fiado": "Fiado",
    "chat": "Chat IA",
}


def main(page: ft.Page):
    # ─── Page config (Flet 0.28.3) ─────────────────────────────────────
    page.title = "GesKio"
    try:
        page.window.width = 1200
        page.window.height = 800
        page.window.min_width = 900
        page.window.min_height = 600
    except Exception:
        pass

    try:
        page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN, use_material3=True)
    except Exception:
        pass

    # theme_mode con storage
    try:
        saved = page.client_storage.get("theme")  # type: ignore[attr-defined]
        if saved == "dark":
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
    except Exception:
        try:
            page.theme_mode = ft.ThemeMode.LIGHT
        except Exception:
            pass

    page.padding = 0
    try:
        page.bgcolor = COLORS["bg"]
    except Exception:
        pass

    # ─── Body (container de screens) ────────────────────────────────────
    body = ft.Column(expand=True, spacing=0, scroll=ft.ScrollMode.AUTO)

    # ─── Screens dict ──────────────────────────────────────────────────
    screens: dict[str, ft.Control] = {}
    try:
        screens["dash"] = PantallaDashboard(page)
        screens["caja"] = PantallaCaja(page)
        screens["stock"] = PantallaStock(page)
        screens["clientes"] = PantallaClientes(page)
        screens["fiado"] = PantallaFiado(page)
        screens["chat"] = PantallaChat(page)
        if PantallaProveedores is not None:
            screens["proveedores"] = PantallaProveedores(page)
        else:
            # placeholder si no existe
            screens["proveedores"] = ft.Container(
                content=ft.Text("Proveedores no disponible", color=COLORS["muted"]),
                expand=True,
                alignment=ft.alignment.center,
                bgcolor=COLORS["surface"],
            )
    except Exception as ex:
        print(f"Error creando screens: {ex}")
        # fallback vacío para no crashear mock
        pass

    # ─── Nav items (7) ─────────────────────────────────────────────────
    nav_items = [
        ("dash", ft.Icons.DASHBOARD, "Dashboard"),
        ("caja", ft.Icons.POINT_OF_SALE, "Caja"),
        ("stock", ft.Icons.INVENTORY_2, "Stock"),
        ("clientes", ft.Icons.PEOPLE, "Clientes"),
        ("proveedores", ft.Icons.LOCAL_SHIPPING, "Proveedores"),
        ("fiado", ft.Icons.RECEIPT_LONG, "Fiado"),
        ("chat", ft.Icons.SMART_TOY, "Chat IA"),
    ]

    active_key = ft.Text("dash", visible=False)  # holder

    # ─── Header superior ───────────────────────────────────────────────
    header_title = ft.Text(
        TITLES.get("dash", "Dashboard"),
        size=20,
        weight=ft.FontWeight.BOLD,
        color=COLORS["text"],
    )

    search_btn = ft.IconButton(
        icon=ft.Icons.SEARCH,
        tooltip="Buscar",
        icon_color=COLORS["muted"],
        on_click=lambda e: None,
    )
    notif_btn = ft.IconButton(
        icon=ft.Icons.NOTIFICATIONS_OUTLINED,
        tooltip="Notificaciones",
        icon_color=COLORS["muted"],
        on_click=lambda e: None,
    )

    # theme toggle icon depende del modo actual
    _initial_theme_icon = ft.Icons.DARK_MODE
    try:
        if getattr(page, "theme_mode", None) == ft.ThemeMode.DARK:
            _initial_theme_icon = ft.Icons.LIGHT_MODE
    except Exception:
        pass

    theme_btn = ft.IconButton(
        icon=_initial_theme_icon,
        tooltip="Cambiar tema",
        icon_color=COLORS["muted"],
    )

    avatar = ft.CircleAvatar(
        content=ft.Text("S", color="white", weight=ft.FontWeight.BOLD, size=14),
        bgcolor=COLORS["primary"],
        radius=18,
    )

    def toggle_theme(e):
        try:
            # switch
            if getattr(page, "theme_mode", ft.ThemeMode.LIGHT) == ft.ThemeMode.LIGHT:
                page.theme_mode = ft.ThemeMode.DARK
                new_val = "dark"
                theme_btn.icon = ft.Icons.LIGHT_MODE
            else:
                page.theme_mode = ft.ThemeMode.LIGHT
                new_val = "light"
                theme_btn.icon = ft.Icons.DARK_MODE
            try:
                page.client_storage.set("theme", new_val)  # type: ignore[attr-defined]
            except Exception:
                pass
            page.update()
        except Exception as ex:
            print(f"Error toggle_theme: {ex}")

    theme_btn.on_click = toggle_theme

    header = ft.Row(
        [
            header_title,
            ft.Container(expand=True),
            search_btn,
            notif_btn,
            theme_btn,
            ft.Container(width=8),
            avatar,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=4,
    )

    header_container = ft.Container(
        content=header,
        padding=ft.padding.symmetric(horizontal=20, vertical=12),
        bgcolor=COLORS["surface"],
        border=ft.border.only(bottom=ft.BorderSide(1, COLORS["border"])),
    )

    # ─── Sidebar premium ───────────────────────────────────────────────
    logo = ft.Row(
        [
            ft.Container(
                content=ft.Icon(ft.Icons.STORE_ROUNDED, color="white", size=20),
                width=36,
                height=36,
                bgcolor=COLORS["primary"],
                border_radius=10,
                alignment=ft.alignment.center,
            ),
            ft.Text("GesKio", size=20, weight=ft.FontWeight.BOLD, color="white"),
        ],
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # nav refs: key -> Container
    nav_refs: dict[str, ft.Container] = {}

    nav_column_controls: list[ft.Control] = []

    # placeholder para mostrar/actualizar (definidas luego, pero refs necesarias)
    # Crearemos contenedores; on_click asignado después de definir mostrar.

    # Necesitamos forward declaration: mostrar y actualizar_nav usarán nav_refs y header_title
    # Creamos contenedores vacíos primero, luego asignamos on_click.

    for key, icon, label in nav_items:
        # Row interno
        icon_ctrl = ft.Icon(icon, size=18, color=COLORS["grey"])
        label_ctrl = ft.Text(label, size=13, weight=ft.FontWeight.W_500, color=COLORS["grey"])
        row = ft.Row([icon_ctrl, label_ctrl], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        cont = ft.Container(
            content=row,
            padding=ft.padding.symmetric(horizontal=12, vertical=10),
            border_radius=12,
            ink=True,
            bgcolor=None,
            border=None,
        )
        nav_refs[key] = cont
        nav_column_controls.append(cont)

    nav_column = ft.Column(nav_column_controls, spacing=4, tight=False)

    footer = ft.Container(
        content=ft.Row(
            [
                ft.CircleAvatar(
                    content=ft.Text("S", color="white", weight=ft.FontWeight.BOLD, size=12),
                    bgcolor=COLORS["primary"],
                    radius=16,
                ),
                ft.Column(
                    [
                        ft.Text("Santi", size=13, weight=ft.FontWeight.BOLD, color="white"),
                        ft.Text("Administrador", size=11, color=COLORS["grey"]),
                    ],
                    spacing=2,
                    expand=True,
                    tight=True,
                ),
                ft.Icon(ft.Icons.MORE_VERT, size=16, color=COLORS["grey"]),
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=12,
        bgcolor=COLORS["sidebar_active"],
        border_radius=12,
    )

    sidebar = ft.Container(
        width=240,
        bgcolor=COLORS["sidebar"],
        padding=16,
        content=ft.Column(
            [
                logo,
                ft.Container(height=12),
                ft.Divider(height=1, color="#1e293b"),
                ft.Container(height=8),
                ft.Text("NAVEGACIÓN", size=10, weight=ft.FontWeight.BOLD, color=COLORS["grey"]),
                ft.Container(height=4),
                nav_column,
                ft.Container(expand=True),
                ft.Divider(height=1, color="#1e293b"),
                ft.Container(height=8),
                footer,
            ],
            spacing=0,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    # ─── Lógica mostrar / actualizar_nav ───────────────────────────────

    def actualizar_nav():
        for key, cont in nav_refs.items():
            is_active = key == active_key.value
            row = cont.content  # type: ignore
            try:
                if is_active:
                    cont.bgcolor = COLORS["sidebar_active"]
                    # spec: activo con border left 3px green
                    cont.border = ft.border.only(left=ft.BorderSide(3, COLORS["primary"]))
                    # icon/text white + bold
                    if isinstance(row, ft.Row) and len(row.controls) >= 2:
                        row.controls[0].color = "white"  # type: ignore
                        row.controls[1].color = "white"  # type: ignore
                        row.controls[1].weight = ft.FontWeight.BOLD  # type: ignore
                else:
                    cont.bgcolor = None
                    cont.border = None
                    if isinstance(row, ft.Row) and len(row.controls) >= 2:
                        row.controls[0].color = COLORS["grey"]  # type: ignore
                        row.controls[1].color = COLORS["grey"]  # type: ignore
                        row.controls[1].weight = ft.FontWeight.W_500  # type: ignore
            except Exception as ex:
                print(f"Error actualizar_nav {key}: {ex}")
        try:
            page.update()
        except Exception:
            pass

    def mostrar(nombre: str):
        try:
            # actualizar header title dinámico
            header_title.value = TITLES.get(nombre, nombre.capitalize())
        except Exception:
            pass
        s = screens.get(nombre)
        if s is None:
            print(f"Screen no encontrada: {nombre}")
            return
        try:
            # visible handling
            for k, scr in screens.items():
                try:
                    scr.visible = (k == nombre)
                except Exception:
                    pass
            body.controls = [s]  # property setter
            try:
                s.al_entrar()  # type: ignore
            except AttributeError:
                pass
            except Exception as ex:
                print(f"Error al_entrar {nombre}: {ex}")
            active_key.value = nombre
            actualizar_nav()
            # header ya actualizado, pero actualizar_nav ya hace page.update
            try:
                page.update()
            except Exception:
                pass
        except Exception as ex:
            print(f"Error mostrar {nombre}: {ex}")

    # asignar on_click ahora que mostrar existe
    for key, _, _ in nav_items:
        cont = nav_refs.get(key)
        if cont is not None:
            # capturar key correctamente
            cont.on_click = lambda e, k=key: mostrar(k)

    # ─── Layout principal ──────────────────────────────────────────────
    # Columna principal (header + body)
    main_column = ft.Column(
        [
            header_container,
            ft.Container(content=body, expand=True, padding=ft.padding.all(0), bgcolor=COLORS["bg"]),
        ],
        expand=True,
        spacing=0,
    )

    main_row = ft.Row(
        [
            sidebar,
            ft.VerticalDivider(width=1, color=COLORS["border"]),
            main_column,
        ],
        expand=True,
        spacing=0,
    )

    # ─── Add a page ────────────────────────────────────────────────────
    try:
        page.add(main_row)
    except Exception as ex:
        print(f"Error page.add: {ex}")
        # fallback para mocks que usan controls
        try:
            page.controls.append(main_row)  # type: ignore
        except Exception:
            pass

    # inicializar activo
    try:
        actualizar_nav()
    except Exception:
        pass

    # mostrar dash inicial
    try:
        mostrar("dash")
    except Exception as ex:
        print(f"Error mostrar inicial: {ex}")


if __name__ == "__main__":
    ft.app(target=main)
