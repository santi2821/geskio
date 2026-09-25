import flet as ft
from screen_base import Pantalla
from datos import proveedores, crear_proveedor, actualizar_proveedor, eliminar_proveedor
from theme import ICON_SM, SP_4, SP_8, SP_10, SP_12, colores
from widgets import (
    campo_texto,
    dialogo,
    encabezado,
    seccion,
    confirmar_eliminar,
    moneda,
    sincronizar_texto,
)


class PantallaProveedores(Pantalla):
    def __init__(self, page: ft.Page):
        super().__init__(page, "Proveedores")
        self._busqueda = ""

    def actualizar(self):
        self.filtrar_datos()

    def build(self):
        paleta = colores.get()
        self._columnas = [
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Email")),
            ft.DataColumn(ft.Text("Rubro")),
            ft.DataColumn(ft.Text("")),
        ]
        # Tabla real (no espejo) para compat con la suite main-only:
        # los tests leen s.tabla_datos.columns/.rows directamente.
        self.tabla_datos = ft.DataTable(
            columns=self._columnas,
            rows=[],
            column_spacing=16,
            expand=True,
            heading_row_height=36,
            data_row_min_height=40,
            heading_text_style=ft.TextStyle(
                size=12, weight=ft.FontWeight.BOLD, color=paleta.text_muted
            ),
            data_text_style=ft.TextStyle(size=14, color=paleta.text),
        )
        self.campo_buscar = campo_texto(hint_text="Buscar proveedor...", expand=True)
        sincronizar_texto(self.campo_buscar)
        # La barra newer avisa via on_change; se conecta al filtro view-side.
        self.campo_buscar.on_change = self._al_buscar_evento

        self.campo_nombre = campo_texto(label="Nombre", expand=True)
        self.campo_telefono = campo_texto(label="Teléfono", expand=True)
        self.campo_email = campo_texto(label="Email", expand=True)
        self.campo_rubro = campo_texto(label="Rubro", expand=True)
        for _campo in (
            self.campo_buscar,
            self.campo_nombre,
            self.campo_telefono,
            self.campo_email,
            self.campo_rubro,
        ):
            sincronizar_texto(_campo)
        # Re-conectar el filtro tras sincronizar (sincronizar_texto pisa on_change).
        self.campo_buscar.on_change = self._al_buscar_evento

        tabla_scroll = ft.Container(
            content=ft.Row([self.tabla_datos], scroll=ft.ScrollMode.AUTO, expand=True),
            expand=True,
            bgcolor=paleta.surface,
            border=ft.Border.all(1, paleta.border),
            border_radius=8,
            padding=8,
        )
        form = ft.Row(
            [
                self.campo_nombre,
                self.campo_telefono,
                self.campo_email,
                self.campo_rubro,
                ft.FilledButton(
                    "Agregar",
                    on_click=self.guardar_nuevo,
                    style=ft.ButtonStyle(
                        bgcolor=paleta.primary, color=paleta.on_primary
                    ),
                ),
            ],
            spacing=SP_8,
            scroll=ft.ScrollMode.AUTO,
        )

        # El build renderiza los datos actuales: entran montados con la pantalla.
        self._cargar_filas()

        return ft.Column(
            [
                encabezado(
                    "Proveedores",
                    al_refrescar=lambda _: self.filtrar_datos(),
                    descripcion="Distribuidores y contactos de tu comercio.",
                ),
                self.campo_buscar,
                tabla_scroll,
                seccion("Nuevo proveedor", form),
            ],
            spacing=SP_10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    # ─── filtro ───────────────────────────────────────────────────────

    def _al_buscar_evento(self, e=None):
        # El .value del campo llega viejo en 0.84; el estado nuevo viene en el evento.
        dato = getattr(e, "data", None)
        if isinstance(dato, str):
            self._busqueda = dato
            try:
                self.campo_buscar.value = dato
            except Exception:
                pass
        else:
            try:
                self._busqueda = self.campo_buscar.value or ""
            except Exception:
                self._busqueda = ""
        self.filtrar_datos()

    def _cargar_filas(self):
        # Arma las filas filtradas en la tabla real, sin update.
        q = (getattr(self, "_busqueda", "") or "").lower()
        # Compat tests: escriben s.campo_buscar.value y llaman filtrar_datos()
        # sin pasar por el evento; el campo manda sobre el estado interno.
        try:
            valor_campo = (self.campo_buscar.value or "").lower()
            if valor_campo != q:
                q = valor_campo
                self._busqueda = self.campo_buscar.value or ""
        except Exception:
            pass
        filas = []
        for pr in proveedores:
            if q:
                hay = (
                    q in pr["nombre"].lower()
                    or q in pr.get("telefono", "").lower()
                    or q in pr.get("email", "").lower()
                    or q in pr.get("rubro", "").lower()
                )
                if not hay:
                    continue
            pid = pr["id"]
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(pr["nombre"], weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(pr.get("telefono", "—"))),
                        ft.DataCell(ft.Text(pr.get("email", "—"))),
                        ft.DataCell(ft.Text(pr.get("rubro", "—"))),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(
                                        ft.Icons.EDIT,
                                        icon_size=ICON_SM,
                                        tooltip="Editar",
                                        on_click=lambda _, x=pid: self.editar_proveedor(x),
                                    ),
                                    ft.IconButton(
                                        ft.Icons.DELETE_OUTLINE,
                                        icon_size=ICON_SM,
                                        tooltip="Eliminar",
                                        icon_color=colores.get().danger,
                                        on_click=lambda _, x=pid: self.eliminar_proveedor(x),
                                    ),
                                ],
                                spacing=SP_4,
                            )
                        ),
                    ]
                )
            )
        if not filas:
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Sin resultados", italic=True))
                        for _ in range(5)
                    ]
                )
            )
        self.tabla_datos.rows = filas
        # Deuda total informativa (usa moneda del kit newer).
        try:
            self._deuda_texto = moneda(
                sum(p.get("deuda", 0) for p in proveedores if isinstance(p, dict))
            )
        except Exception:
            pass

    def filtrar_datos(self):
        try:
            self._cargar_filas()
        except Exception as ex:
            print(f"Error en filtrar_datos proveedores: {ex}")
            return
        # Refresco post-acción: update si está montado, rearmar si no.
        try:
            self.tabla_datos.update()
        except Exception:
            try:
                self.rearmar()
            except Exception:
                pass

    # ─── nuevo ───────────────────────────────────────────────────────

    def guardar_nuevo(self, e=None):
        try:
            nombre = (self.campo_nombre.value or "").strip()
            if not nombre:
                return
            crear_proveedor(
                nombre,
                (self.campo_telefono.value or "").strip(),
                (self.campo_email.value or "").strip(),
                (self.campo_rubro.value or "").strip(),
            )
            self.campo_nombre.value = ""
            self.campo_telefono.value = ""
            self.campo_email.value = ""
            self.campo_rubro.value = ""
            self.filtrar_datos()
            self.mostrar_alerta("Proveedor agregado")
        except Exception as ex:
            print(f"Error guardar_nuevo proveedor: {ex}")

    # ─── editar ──────────────────────────────────────────────────────

    def editar_proveedor(self, pid):
        try:
            pr = next((x for x in proveedores if x["id"] == pid), None)
            if not pr:
                return

            campo_nombre = campo_texto(label="Nombre", value=pr["nombre"])
            campo_telefono = campo_texto(label="Teléfono", value=pr.get("telefono", ""))
            campo_email = campo_texto(label="Email", value=pr.get("email", ""))
            campo_rubro = campo_texto(label="Rubro", value=pr.get("rubro", ""))
            for _campo in (campo_nombre, campo_telefono, campo_email, campo_rubro):
                sincronizar_texto(_campo)

            def guardar(e):
                try:
                    actualizar_proveedor(
                        pid,
                        (campo_nombre.value or "").strip() or pr["nombre"],
                        (campo_telefono.value or "").strip(),
                        (campo_email.value or "").strip(),
                        (campo_rubro.value or "").strip(),
                    )
                    self.cerrar_dialogo(ventana)
                    self.filtrar_datos()
                    self.mostrar_alerta("Proveedor actualizado")
                except Exception as ex:
                    print(f"Error guardar editar proveedor: {ex}")

            ventana = dialogo(
                "Editar proveedor",
                ft.Column(
                    [campo_nombre, campo_telefono, campo_email, campo_rubro],
                    spacing=SP_12,
                    tight=True,
                ),
                acciones=[
                    ft.TextButton(
                        "Cancelar", on_click=lambda e: self.cerrar_dialogo(ventana)
                    ),
                    ft.ElevatedButton("Guardar", on_click=guardar),
                ],
            )
            self.abrir_dialogo(ventana)
        except Exception as ex:
            print(f"Error editar_proveedor: {ex}")

    # ─── eliminar ────────────────────────────────────────────────────

    def eliminar_proveedor(self, pid):
        try:
            pr = next((x for x in proveedores if x["id"] == pid), None)
            if not pr:
                return

            def confirmar(e):
                try:
                    eliminar_proveedor(pid)
                    self.filtrar_datos()
                    self.mostrar_alerta(f"'{pr['nombre']}' eliminado")
                except Exception as ex:
                    print(f"Error confirmar eliminar proveedor: {ex}")

            confirmar_eliminar(
                self.pagina,
                confirmar,
                nombre=pr["nombre"],
                titulo="Eliminar proveedor",
                mensaje=f"¿Eliminar a '{pr['nombre']}'?\nNo se puede deshacer.",
            )
        except Exception as ex:
            print(f"Error eliminar_proveedor: {ex}")

    # ─── helpers: heredados de Pantalla (dual 0.84 runtime + Mock/0.28.3).
    # mostrar_alerta/abrir_dialogo/cerrar_dialogo viven en screen_base y
    # usan page.snack_bar/page.open cuando existen, con fallback a overlay.
