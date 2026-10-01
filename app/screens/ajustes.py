from datetime import date

import flet as ft
import datos
from screen_base import Pantalla
from theme import (
    ACENTOS_PREDETERMINADOS,
    ANCHO_BORDE,
    FS_14,
    R_MD,
    R_SM,
    SP_4,
    SP_8,
    SP_10,
    SP_12,
    colores,
)
from widgets import (
    campo_texto,
    encabezado,
    seccion,
    aviso,
    sincronizar_texto,
    dialogo,
)
from jev.openrouter import configuracion_actual

class PantallaAjustes(Pantalla):
    def __init__(self, page: ft.Page, al_apariencia=None, al_restaurar=None):
        super().__init__(page, "Ajustes")
        self.al_apariencia = al_apariencia
        self.al_restaurar = al_restaurar
        self._hex_value = ""
        self._selector_archivos = ft.FilePicker()
        self._selector_registrado = False

    def build(self):
        paleta = colores.get()
        self._registrar_selector_archivos()
        modo_comercio = (
            "Datos de ejemplo" if datos.MODO_COMERCIO == "demo" else "Comercio vacío"
        )
        self._seg_modo = ft.SegmentedButton(
            segments=[
                ft.Segment(value="light", label=ft.Text("Claro")),
                ft.Segment(value="dark", label=ft.Text("Oscuro")),
            ],
            selected=[colores.mode],
            on_change=self._al_modo,
        )
        tarjetas_marca = ft.Row(
            [
                self._tarjeta_marca("rojo", "Rojo"),
                self._tarjeta_marca("verde", "Verde"),
            ],
            spacing=SP_12,
            wrap=True,
        )
        muestras = ft.Row(
            [self._muestra(hex, etiqueta) for hex, etiqueta in ACENTOS_PREDETERMINADOS],
            spacing=SP_8,
            wrap=True,
        )
        self.campo_hex = campo_texto(
            label="Hex personalizado",
            hint_text="#c81e1e",
            value=self._hex_value or colores.accent_override or "",
            on_submit=lambda _: self.aplicar_hex(),
            width=280,
        )
        sincronizar_texto(self.campo_hex)
        form_acento = ft.Column(
            [
                muestras,
                ft.Row(
                    [
                        self.campo_hex,
                        ft.FilledButton(
                            "Aplicar",
                            on_click=lambda _: self.aplicar_hex(),
                            style=ft.ButtonStyle(
                                bgcolor=paleta.primary,
                                color=paleta.on_primary,
                            ),
                        ),
                        ft.TextButton(
                            "Restablecer", on_click=lambda _: self.restablecer_acento()
                        ),
                    ],
                    spacing=SP_8,
                    wrap=True,
                ),
            ],
            spacing=SP_8,
        )
        personalizar_acento = ft.ExpansionTile(
            title="Color de acento",
            subtitle="Opciones de personalización",
            controls=[form_acento],
            dense=True,
            controls_padding=SP_12,
            tile_padding=ft.Padding.symmetric(horizontal=SP_8, vertical=SP_4),
            collapsed_text_color=paleta.text,
            text_color=paleta.text,
            collapsed_icon_color=paleta.text_muted,
            icon_color=paleta.text_muted,
            collapsed_shape=ft.RoundedRectangleBorder(radius=R_MD),
            shape=ft.RoundedRectangleBorder(radius=R_MD),
            collapsed_bgcolor=paleta.surface,
            bgcolor=paleta.surface,
        )
        return ft.Column(
            [
                encabezado(
                    "Preferencias",
                    al_refrescar=lambda _: self.actualizar(),
                    descripcion="Preferencias visuales y ubicación de los datos de demo.",
                ),
                seccion(
                    "Apariencia",
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text("Modo", size=FS_14, weight=ft.FontWeight.W_600, color=paleta.text),
                                    self._seg_modo,
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ft.Divider(color=paleta.border),
                            ft.Row(
                                [
                                    ft.Text("Color base", size=FS_14, weight=ft.FontWeight.W_600, color=paleta.text),
                                    tarjetas_marca,
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                wrap=True,
                            ),
                            ft.Divider(color=paleta.border),
                            personalizar_acento,
                        ],
                        spacing=SP_10,
                    ),
                ),
                self._seccion_asistente(paleta),
                seccion(
                    "Datos del comercio",
                    ft.Column(
                        [
                            ft.Text(
                                f"Inicio elegido: {modo_comercio}.",
                                size=FS_14,
                                weight=ft.FontWeight.W_600,
                                color=paleta.text,
                            ),
                            ft.Text(
                                "Los datos y el historial se guardan en este equipo. No se sincronizan entre dispositivos.",
                                size=FS_14,
                                color=paleta.text,
                            ),
                            ft.Text(
                                str(datos.RUTA_ARCHIVO_DATOS),
                                size=FS_14,
                                color=paleta.text_muted,
                                selectable=True,
                            ),
                            ft.Text(
                                "Esta ubicación corresponde al archivo JSON local de la demo.",
                                size=FS_14,
                                color=paleta.text_muted,
                            ),
                            ft.Text(
                                "Una copia incluye productos, ventas, clientes, teléfonos y saldos. Guardala en un lugar privado.",
                                size=FS_14,
                                color=paleta.text_muted,
                            ),
                            ft.Row(
                                [
                                    ft.OutlinedButton(
                                        "Crear copia",
                                        icon=ft.Icons.DOWNLOAD,
                                        on_click=self.crear_respaldo,
                                    ),
                                    ft.OutlinedButton(
                                        "Restaurar copia",
                                        icon=ft.Icons.UPLOAD_FILE,
                                        on_click=self.seleccionar_respaldo,
                                    ),
                                ],
                                spacing=SP_8,
                                wrap=True,
                            ),
                        ],
                        spacing=SP_8,
                    ),
                ),
            ],
            spacing=SP_12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    @staticmethod
    def _seccion_asistente(paleta):
        config = configuracion_actual()
        if config.clave_detectada:
            estado = (
                f"Clave de OpenRouter detectada · modelo {config.modelo}. "
                "La clave se valida al enviar una consulta autorizada."
            )
            privacidad = (
                "Antes de cada sesión remota, el Chat pide permiso. Puede enviar la consulta, "
                "hasta 8 mensajes previos y un resumen con nombres/saldos de clientes, catálogo "
                "y ventas agregadas. Excluye teléfonos, IDs y el archivo JSON completo. El historial "
                "del Chat es temporal. OpenRouter puede aplicar cargos por uso."
            )
        else:
            estado = (
                "Modo local · no se detecta OPENROUTER_API_KEY. Las consultas del Chat no se envían "
                "por internet."
            )
            privacidad = (
                f"Si habilitás OpenRouter en el entorno, GesKio usará {config.modelo} salvo que "
                "definas OPENROUTER_MODEL. El permiso se solicita antes de cada sesión. La clave "
                "no se muestra ni se guarda en los datos comerciales."
            )
        return seccion(
            "Asistente",
            ft.Column(
                [
                    ft.Text(
                        estado,
                        size=FS_14,
                        weight=ft.FontWeight.W_600,
                        color=paleta.text,
                    ),
                    ft.Text(privacidad, size=FS_14, color=paleta.text_muted),
                ],
                spacing=SP_8,
            ),
        )

    def _registrar_selector_archivos(self):
        if self._selector_registrado:
            return
        try:
            servicios = self.pagina.services
            if self._selector_archivos not in servicios:
                servicios.append(self._selector_archivos)
            self._selector_registrado = True
        except Exception:
            pass

    async def crear_respaldo(self, e=None):
        self._registrar_selector_archivos()
        try:
            contenido = datos.serializar_respaldo()
            nombre = f"geskio-respaldo-{date.today().isoformat()}.json"
            if bool(getattr(self.pagina, "web", False)):
                await self._selector_archivos.save_file(
                    dialog_title="Guardar copia de GesKio",
                    file_name=nombre,
                    file_type=ft.FilePickerFileType.CUSTOM,
                    allowed_extensions=["json"],
                    src_bytes=contenido,
                )
                aviso(self.pagina, "Se inició la descarga de la copia")
                return
            ruta = await self._selector_archivos.save_file(
                dialog_title="Guardar copia de GesKio",
                file_name=nombre,
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["json"],
            )
            if ruta:
                datos.exportar_respaldo(ruta)
                aviso(self.pagina, "Copia guardada")
        except Exception as ex:
            aviso(self.pagina, f"No se pudo crear la copia: {ex}", rol="danger")

    async def seleccionar_respaldo(self, e=None):
        self._registrar_selector_archivos()
        try:
            es_web = bool(getattr(self.pagina, "web", False))
            archivos = await self._selector_archivos.pick_files(
                dialog_title="Elegir copia de GesKio",
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["json"],
                allow_multiple=False,
                with_data=es_web,
            )
            if not archivos:
                return
            archivo = archivos[0]
            if archivo.size > datos.MAX_BYTES_RESPALDO:
                raise ValueError("El respaldo supera el límite de 16 MB")
            if archivo.bytes is not None:
                estado = datos.leer_respaldo(archivo.bytes)
            elif archivo.path:
                estado = datos.leer_respaldo_archivo(archivo.path)
            else:
                raise ValueError("No se pudo leer el archivo seleccionado")
            self._confirmar_restauracion(estado)
        except ValueError as ex:
            aviso(self.pagina, str(ex), rol="danger")
        except Exception as ex:
            aviso(self.pagina, f"No se pudo abrir la copia: {ex}", rol="danger")

    def _confirmar_restauracion(self, estado):
        sin_costo = sum(
            1
            for venta in estado["ventas"]
            if any(item.get("costo") is None for item in venta.get("items", []))
        )
        resumen = (
            f"{len(estado['productos'])} productos · {len(estado['clientes'])} clientes · "
            f"{len(estado['proveedores'])} proveedores · {len(estado['ventas'])} ventas · "
            f"{len(estado['cuentas'])} cuentas por cobrar."
        )
        detalle = (
            f"\n\n{sin_costo} venta(s) no tienen costo histórico registrado."
            if sin_costo
            else ""
        )
        texto = (
            "Esta acción reemplaza todos los datos que están en esta computadora. "
            "La copia no se combina con el estado actual.\n\n"
            + resumen
            + detalle
        )
        ventana = dialogo(
            "Restaurar copia de GesKio",
            ft.Text(texto, size=FS_14, color=colores.get().text),
            acciones=[
                ft.TextButton("Cancelar", on_click=lambda _: self.cerrar_dialogo(ventana)),
                ft.FilledButton(
                    "Reemplazar datos",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=lambda _: self._aplicar_restauracion(ventana, estado),
                ),
            ],
        )
        self.abrir_dialogo(ventana)

    def _aplicar_restauracion(self, ventana, estado):
        try:
            resumen = datos.restaurar_respaldo(estado)
            self.cerrar_dialogo(ventana)
            if callable(self.al_restaurar):
                self.al_restaurar()
            aviso(
                self.pagina,
                f"Copia restaurada · {resumen['productos']} productos, "
                f"{resumen['proveedores']} proveedores y {resumen['ventas']} ventas",
                rol="success",
            )
        except Exception as ex:
            aviso(self.pagina, f"No se pudieron reemplazar los datos: {ex}", rol="danger")

    def _tarjeta_marca(self, nombre: str, etiqueta: str) -> ft.Container:
        paleta = colores.get()
        activa = colores.theme_name == nombre
        clara, oscura = colores.THEMES[nombre]
        hex_punto = (oscura if colores.mode == "dark" else clara).primary
        return ft.OutlinedButton(
            content=etiqueta,
            icon=ft.Icons.CHECK_CIRCLE if activa else ft.Icons.RADIO_BUTTON_UNCHECKED,
            tooltip=f"Usar marca {etiqueta}",
            on_click=lambda _, n=nombre: self.fijar_marca(n),
            width=150,
            height=48,
            style=ft.ButtonStyle(
                color=paleta.primary if activa else paleta.text,
                icon_color=paleta.primary if activa else hex_punto,
                bgcolor=paleta.accent_soft if activa else paleta.surface,
                side=ft.BorderSide(ANCHO_BORDE, paleta.primary if activa else paleta.border),
                shape=ft.RoundedRectangleBorder(radius=R_SM),
            ),
        )

    def _muestra(self, hex: str, etiqueta: str) -> ft.IconButton:
        paleta = colores.get()
        activa = (colores.accent_override or "").lower() == hex.lower()
        return ft.IconButton(
            icon=ft.Icons.CIRCLE,
            icon_color=hex,
            tooltip=(f"Acento actual: {etiqueta}" if activa else f"Usar acento {etiqueta}"),
            on_click=lambda _, h=hex: self.fijar_acento(h),
            width=40,
            height=40,
            style=ft.ButtonStyle(
                padding=0,
                bgcolor=paleta.accent_soft if activa else paleta.surface,
                side=ft.BorderSide(2 if activa else ANCHO_BORDE, paleta.primary if activa else paleta.border),
                shape=ft.CircleBorder(),
            ),
        )

    def _al_modo(self, e) -> None:
        try:
            elegido = (
                e.control.selected
                if e is not None and hasattr(e, "control")
                else [colores.mode]
            )
            modo = elegido[0] if elegido else colores.mode
        except Exception:
            modo = colores.mode
        self.fijar_modo(modo)

    def fijar_modo(self, modo: str) -> None:
        try:
            colores.set_mode(modo, self.pagina)
        except ValueError:
            return
        self._aplicar("Modo " + ("oscuro" if modo == "dark" else "claro"))

    def fijar_marca(self, nombre: str) -> None:
        try:
            colores.set_theme(nombre, self.pagina)
        except ValueError:
            return
        self._aplicar("Marca " + nombre.capitalize())

    def fijar_acento(self, hex: str) -> None:
        try:
            colores.set_accent(hex, self.pagina)
        except ValueError:
            aviso(self.pagina, "Hex inválido (ej: #c81e1e)")
            return
        self._hex_value = hex
        self._aplicar("Acento " + hex)

    def aplicar_hex(self, e=None) -> None:
        try:
            escrito = (self.campo_hex.value or "").strip()
        except Exception:
            escrito = ""
        if not escrito:
            return
        self.fijar_acento(escrito)

    def restablecer_acento(self, e=None) -> None:
        colores.set_accent(None, self.pagina)
        self._hex_value = ""
        self._aplicar("Acento restablecido")

    def _aplicar(self, texto: str) -> None:
        self.invalidate()
        try:
            if callable(self.al_apariencia):
                self.al_apariencia()
            else:
                self.al_entrar()
        except Exception:
            pass
        try:
            aviso(self.pagina, texto)
        except Exception:
            pass
