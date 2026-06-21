# Proyecto Urban Routes Automated Testing

## Descripción

Este repositorio implementa un conjunto de pruebas automatizadas para la aplicación Urban Routes utilizando Python y Selenium WebDriver. El archivo `main.py` contiene tanto el Page Object Model (`UrbanRoutesPage`) como la clase de pruebas `TestUrbanRoutes`.

El proyecto cubre escenarios como:
- ingreso de direcciones de origen y destino
- selección de modo y tipo de transporte
- elección de tarifa `Comfort`
- flujo de número de teléfono y verificación por SMS
- adición de tarjeta de crédito y validación de datos
- uso del campo de mensaje para el conductor
- selección de extras (`Manta y pañuelos`, helados)
- reserva de taxi y verificación de la aparición del modal de búsqueda de auto
- visualización de detalles del viaje

También incluye un helper para recuperar el código SMS desde los logs de red del navegador, necesario para las pruebas de confirmación de teléfono.

## Tecnologías

| Tecnología      | Propósito                                  |
|:----------------|:-------------------------------------------|
| Python 3.14.5   | Lenguaje de programación principal         |
| Selenium 4.44.0 | Automatización de pruebas web en navegador |

## Técnicas

| Técnica                      | Aplicación en el Proyecto                                                     |
|:-----------------------------|:------------------------------------------------------------------------------|
| Page Object Model            | Organización de selectores y acciones de página en `UrbanRoutesPage`          |
| Pruebas funcionales          | Cobertura de flujos de usuario completos sobre la interfaz de Urban Routes    |
| Manejo de esperas explícitas | Uso de `WebDriverWait` para sincronizar interacciones con elementos dinámicos |

# 🧪 Ejecución de Pruebas

## Requisitos previos

- Python 3.14+
- Entorno virtual activo (`.venv`)
- Dependencias instaladas (`pip install -r requirements.txt`)
- Navegador Chrome y [ChromeDriver](https://chromedriver.chromium.org/) compatibles con tu versión del navegador
- Actualizar `urban_routes_url` en el archivo [data.py](data.py) con una nueva url del servidor de Urban.Routes

## Ejecutar las pruebas con Pytest

### Todas las pruebas del archivo principal
```bash
pytest -s main.py::TestUrbanRoutes
```