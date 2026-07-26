<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/GesKio-gesti%C3%B3n%20de%20negocio-22c55e?style=for-the-badge&logo=store&logoColor=white">
    <img alt="GesKio" src="https://img.shields.io/badge/GesKio-gesti%C3%B3n%20de%20negocio-22c55e?style=for-the-badge&logo=store&logoColor=white">
  </picture>
</p>

# GesKio

**App de gestión de negocio para emprendedores + Landing promocional.** CRUD de productos, ventas, clientes, caja, fiado, stock y chat integrado. App Flet multiplataforma con landing page web.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Flet](https://img.shields.io/badge/Flet-0.24-00B4AB?logo=flutter&logoColor=white)

## Modules

| Module | Descripcion |
|---|---|
| Dashboard | Resumen del negocio, KPIs |
| Stock | Gestion de productos e inventario |
| Caja | Registro de ventas y cobros |
| Clientes | CRUD de clientes con historial |
| Fiado | Control de creditos y pagos |
| Chat | Comunicacion interna |

## Tech Stack

| Capa | Tecnologia |
|---|---|
| App | Python 3.11 + Flet |
| Landing | HTML5, CSS3, JavaScript |
| Persistencia | SQLite |

## Quick Start

`ash
cd app
pip install flet
flet run main.py
`

La landing se abre con landing/index.html en cualquier navegador.

## Project Structure

`
geskio/
├── app/                # App Flet
│   ├── main.py         # Entry point
│   ├── datos.py        # Manejo de datos
│   ├── screen_base.py  # Clase base de pantallas
│   └── screens/        # Modulos (caja, stock, etc.)
├── landing/            # Landing promocional
│   ├── index.html
│   ├── styles.css
│   └── script.js
└── README.md
`

## License

[MIT](LICENSE) © 2026 Santino Avila
