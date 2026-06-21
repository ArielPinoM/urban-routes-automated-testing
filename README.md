# Urban Routes Automated Testing

## Descripción breve

Suite pruebas automatizadas flujo completo reserva taxi con validaciones SMS, pago, extras.

## Objetivo

Garantizar la calidad funcional de la aplicación Urban Routes cubriendo escenarios críticos desde el ingreso de direcciones hasta la reserva de taxi. Automatizar la validación end-to-end para reducir regresiones manuales y mejorar la confiabilidad del proceso de reserva.

## Problemática

La validación manual del flujo completo de reserva de taxi resulta lenta, repetitiva y propensa a errores humanos. El código de confirmación SMS es dinámico y requiere extracción desde logs de red. La complejidad de múltiples campos, modales y estados dinámicos demanda una arquitectura mantenible y escalable para las pruebas.

## Aprendizajes clave y logros

Implementación exitosa de Page Object Model para desacoplar selectores de la lógica de pruebas. Dominio de extracción de datos desde logs de performance de Chrome para recuperar códigos SMS dinámicos. Uso efectivo de WebDriverWait para sincronización confiable de elementos dinámicos. Cobertura completa de flujo end-to-end: direcciones, tipos de vehículo, tarifas, confirmación telefónica con SMS, pago con tarjeta, selección de extras y validación de modal de búsqueda de auto. Suite de pruebas funcionales que reproduce comportamientos críticos del usuario.

## Habilidades

**Automatización & QA**
- Diseño de arquitecturas de test (Page Object Model)
- Sincronización de elementos dinámicos (WebDriverWait)
- Inspección de network y extracción de datos en runtime
- Validación de flujos completos end-to-end
- Ejecución parametrizada con Pytest

**Desarrollo & Análisis**
- Python avanzado
- Interacciones complejas con Selenium (ActionChains, Keys)
- Debugging con Chrome DevTools Protocol
- Optimización de localizadores (XPath/CSS)

## Stack tecnológico

Python 3.14+ | Selenium 4.45 | Pytest 9.1 | Chrome DevTools Protocol | XPath/CSS selectors

## Descripción detallada

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