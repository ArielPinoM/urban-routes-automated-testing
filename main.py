import data
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for _ in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if code is not None:
            return code
    raise Exception("No se encontró el código de confirmación del teléfono.\n"
                    "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")


class UrbanRoutesPage:
    # Localizadores
    # Direcciones
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    # Contenedor del selector de "Modo" y "Tipo"
    type_picker_shown_div = (By.CSS_SELECTOR, ".type-picker.shown")
    # Botón de selección de modo "Personal"
    personal_mode_button = (By.XPATH, "//div[text()='Personal']")
    # Tipo
    # Se busca el div contenedor de los tipos y se ubica el 3er tipo (Taxi)
    taxi_type_button = (By.XPATH, "//div[contains(@class, 'types-container')]/div[3]")
    # Botón "Pedir un Taxi" - Se localiza seleccionando el botón dentro del div .results-text.
    request_taxi_button = (By.XPATH, "//div[contains(@class, 'results-text')]/button")
    # Contenedor de selección de tarifas
    tariff_picker_container = (By.CLASS_NAME, "tariff-picker")
    # Tarifa Comfort
    # comfort_tariff_button = (By.XPATH, "//button[@data-for='tariff-card-4']")
    comfort_tariff_button = (By.XPATH, "//div[@class='tariff-cards']/div[5]")
    # Botón numero de teléfono
    phone_number_button = (By.CLASS_NAME, "np-button")
    # Modal para introducir el número de teléfono
    phone_number_modal = (By.CLASS_NAME, "number-picker")
    # Campo número de teléfono dentro del modal de Número de teléfono
    phone_number_field = (By.XPATH, "//input[@id='phone']")
    # Botón siguiente dentro del modal de número de teléfono
    next_button_phone_number = (By.XPATH, "//div[@class='number-picker open']//button[contains(text(), 'Siguiente')]")
    # Header del modal "Introduce el código del SMS"
    sms_code_modal_header = (By.XPATH, "//div[contains(text(), 'Introduce el código del SMS')]")
    # Botón número de teléfono con clase "filled"
    filled_phone_number_button = (By.CSS_SELECTOR, ".np-button.filled")
    # Campo "Código"
    code_field = (By.ID, "code")
    # Botón "Confirmar" código del SMS
    confirm_button_sms_code = (By.XPATH, "//div[@class='number-picker open']//button[contains(text(), 'Confirmar')]")
    # Botón método de pago
    payment_method_button = (By.CLASS_NAME, "pp-button")
    # Modal para seleccionar el método de pago
    payment_method_modal = (By.CLASS_NAME, "payment-picker")
    # Botón "Agregar tarjeta" del modal para seleccionar el método de pago
    add_card_button = (By.XPATH, "//div[@class='pp-title' and contains(text(), 'Agregar tarjeta')]")
    # Header del modal para agregar tarjeta
    header_add_card_modal = (By.XPATH, "//div[@class='head' and contains(text(), 'Agregar tarjeta')]")
    # Input número de tarjeta
    card_number_field = (By.ID, "number")
    # Input CVV
    cvv_field = (By.XPATH, "//input[@id='code' and @class='card-input']")
    # Botón "Agregar" tarjeta
    add_data_card_button = (By.XPATH, "//div[@class='pp-buttons']//button[contains(text(), 'Agregar')]")
    # Fila que representa la ultima tarjeta agregada
    last_added_card_row = (By.XPATH, "//div[contains(@class, 'pp-title') and text()='Tarjeta']")
    # Botón de cierre "X" del modal "Método de pago"
    payment_method_modal_close_button = (By.XPATH, "//div[contains(@class, 'payment-picker')]//div[contains(@class, 'section active')]//button[contains(@class, 'close-button')]")
    # Campo de comentario para el conductor
    comment_field = (By.ID, "comment")
    # Contenedor que se actualiza con la clase "error" cuando se ingresa un comentario inválido
    comment_field_container = (By.XPATH, "//input[@id='comment']/..")
    # Checkbox "Manta y Pañuelos"
    blanket_and_tissues_checkbox = (By.XPATH, "//div[contains(text(), 'Manta y pañuelos')]/following-sibling::div[@class='r-sw']//input")
    # Contenedor padre del checkbox
    blanket_and_tissues_checkbox_container = (By.XPATH, "//div[contains(text(), 'Manta y pañuelos')]/following-sibling::div[@class='r-sw']//input/..")
    # Valor actual del contador de Helado
    ice_cream_current_counter_value = (By.XPATH, "//div[contains(text(), 'Helado')]/following-sibling::div[@class='r-counter']//div[@class='counter-value']")
    # Contador (+1) Helado
    ice_cream_increase_counter_button = (By.XPATH, "//div[contains(text(), 'Helado')]/following-sibling::div[@class='r-counter']//div[@class='counter-plus']")
    # Botón de reserva "Pedir un taxi"
    reservation_button = (By.XPATH, "//button[@class='smart-button']")
    # Modal que muestra la búsqueda de un taxi y posteriormente la información del conductor
    looking_for_taxi_modal = (By.CLASS_NAME, ".order")
    # Para comprobar que el modal despliega la búsqueda verificamos que el encabezado coincida con "Buscar automóvil"
    searching_car_header = (By.XPATH, "//div[@class='order-header-title' and contains(text(), 'Buscar automóvil')]")
    # Temporizador de búsqueda de automóvil
    searching_car_timer = (By.CLASS_NAME, "order-header-time")
    # Encabezado "El conductor llegará en..."
    driver_arrive_header = (By.XPATH, "//div[@class='order-header-title' and contains(text(), 'El conductor llegará en')]")
    # Botón "Detalles" del modal "Order"
    order_details_button = (By.XPATH, "//div[@class='order shown']//div[text()='Detalles']/parent::div/button")
    # Contenedor de los detalles del viaje con clase 'shown'. Implica que el contenedor esté visible en pantalla.
    order_details_shown_div = (By.CSS_SELECTOR, ".order-details.shown")


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate_to_urban_routes(self):
        self.driver.get(data.urban_routes_url)

    def _find_element_presence(self, by, value, timeout=None) -> WebElement:
        """
        Localiza un elemento en el DOM esperando a que esté presente.

        Busca un elemento en la página utilizando la estrategia y el valor especificados.
        Si se proporciona un tiempo de espera (`timeout`), crea una instancia temporal de
        WebDriverWait; de lo contrario, utiliza la instancia por defecto configurada en la
        clase (`self.wait`).

        Args:
            by (str): La estrategia de localización a utilizar
                (ej. By.XPATH, By.CSS_SELECTOR, By.ID).
            value (str): El localizador o selector del elemento a buscar.
            timeout (int | float, optional): Tiempo máximo en segundos a esperar antes de lanzar una excepción. Si es None, se usa el wait por defecto de la clase.

        Returns:
            WebElement: El objeto de Selenium correspondiente al elemento encontrado en el DOM.

        Raises:
            TimeoutException: Si transcurre el tiempo límite sin encontrar el elemento.
        """
        if timeout:
            wait = WebDriverWait(self.driver, timeout)
        else:
            wait = self.wait
        return wait.until(EC.presence_of_element_located((by, value)))

    def _find_element_clickable(self, by: str, value: str) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable((by, value)), f"❌ Error Element to be clickable: {value}")

    def _find_element_visibility(self, locator, timeout=None) -> WebElement:
        """
        Check that an element is visible (present in DOM and width/height greater than zero) for a period of time (timeout).

        Args:
            locator (tuple[str, str]): Localizador
            timeout (int | float, optional): Tiempo máximo en segundos a esperar antes de lanzar una excepción. Si es None, se usa el wait por defecto de la clase.
        Returns:
            WebElement: Elemento visible
        """
        if timeout:
            wait = WebDriverWait(self.driver, timeout)
        else:
            wait = self.wait
        return wait.until(EC.visibility_of_element_located(locator))

    def is_element_present(self, by: str, value: str) -> bool:
        return len(self.driver.find_elements(by, value)) > 0

    def is_button_disabled(self, locator):
        """
        Verifica si un botón está deshabilitado.
        Args:
            locator: Tuple (By, value) que identifica el elemento.
        Returns:
            bool: True si el botón está deshabilitado, False en caso contrario.
        """
        button = self._find_element_presence(*self.add_data_card_button)
        return not button.is_enabled()

    def set_from(self, from_address):
        from_field = self._find_element_clickable(*self.from_field)
        from_field.clear()
        from_field.send_keys(from_address)

    def set_to(self, to_address):
        to_field = self._find_element_clickable(*self.to_field)
        to_field.clear()
        to_field.send_keys(to_address)

    def get_from(self):
        return self._find_element_presence(*self.from_field).get_property('value')

    def get_to(self):
        return self._find_element_presence(*self.to_field).get_property('value')

    def click_request_taxi(self):
        """Selecciona el modo 'Personal', tipo 'taxi' y hace clic en 'Pedir un taxi'"""
        self._find_element_clickable(*self.personal_mode_button).click()
        self._find_element_clickable(*self.taxi_type_button).click()
        self._find_element_clickable(*self.request_taxi_button).click()

    def set_route(self, address_from, address_to):
        """
        Llena los campos "Desde" y "Hasta" con direcciones dadas.

        Args:
            address_from (str): Dirección de partida
            address_to (str): Dirección de destino
        """
        self.set_from(address_from)
        self.set_to(address_to)

    def is_type_picker_shown(self):
        """
            Checa que el contenedor type-picker contenga la clase 'shown'.
            Returns:
                bool: True o False si contiene la clase o no.
        """
        try:
            self._find_element_presence(*self.type_picker_shown_div, timeout=1)
            return True
        except:
            return False

    def is_tariff_container_visible(self) -> bool:
        try:
            self._find_element_visibility(self.tariff_picker_container)
            return True
        except:
            return False

    def click_comfort_tariff_button(self):
        self._find_element_clickable(*self.comfort_tariff_button).click()

    def click_phone_number_button(self):
        self._find_element_clickable(*self.phone_number_button).click()

    def is_phone_number_modal_visible(self) -> bool:
        try:
            self._find_element_visibility(self.phone_number_modal, 1)
            return True
        except:
            return False

    def set_phone_number(self, phone_number: str) -> None:
        phone_number_field = self._find_element_clickable(*self.phone_number_field)
        phone_number_field.clear()
        phone_number_field.send_keys(phone_number)

    def get_phone_number(self):
        return self._find_element_presence(*self.phone_number_field).get_property('value')

    def click_next_button_phone_modal(self) -> None:
        self._find_element_clickable(*self.next_button_phone_number).click()

    def is_sms_code_header_modal_visible(self):
        """
        Checa si el header del modal para introducir el código del SMS es visible.
        Returns:
            bool: True o False si es visible o no.
        """
        try:
            self._find_element_visibility(self.sms_code_modal_header, 1)
            return True
        except:
            return False

    def fill_sms_code_field(self, code) -> None:
        code_field = self._find_element_clickable(*self.code_field)
        code_field.clear()
        code_field.send_keys(code)

    def click_confirm_button_verification_code(self) -> None:
        self._find_element_clickable(*self.confirm_button_sms_code).click()

    def add_phone_number(self, phone_number) -> None:
        """
        Agrega un numero de teléfono.
        Pasos:
            1. Clic en el botón "Número de teléfono"
            2. Llenar el campo "Número de teléfono"
            3. Clic en "Siguiente"
            4. Llenar el campo código del SMS
            5. Clic en "Confirmar"
        """
        self.click_phone_number_button()
        self.set_phone_number(phone_number)
        self.click_next_button_phone_modal()
        self.fill_sms_code_field(retrieve_phone_code(self.driver))
        self.click_confirm_button_verification_code()

    def click_payment_method_button(self) -> None:
        """
        Hace clic en el botón "Método de pago" que despliega el modal "Método de pago".
        """
        self._find_element_clickable(*self.payment_method_button).click()

    def is_payment_method_modal_visible(self) -> bool:
        try:
            self._find_element_visibility(self.payment_method_modal)
            return True
        except:
            return False

    def click_add_card_button(self) -> None:
        """
        Hace clic en "Agregar tarjeta" dentro del modal "Método de pago".
        """
        self._find_element_clickable(*self.add_card_button).click()

    def is_add_card_modal_visible(self) -> bool:
        try:
            self._find_element_visibility(self.header_add_card_modal, 1)
            return True
        except:
            return False

    def fill_card_number_field(self, card_number) -> None:
        """
        Llena el campo "Número de tarjeta" con un numero dado.

        params:
            card_number: Numero de tarjeta
        """
        card_number_field = self._find_element_clickable(*self.card_number_field)
        card_number_field.clear()
        card_number_field.send_keys(card_number)

    def fill_cvv_field(self, cvv) -> None:
        """
        Llena el campo "Código" con un código dado.

        params:
            cvv: Código de la tarjeta
        """
        cvv_field = self._find_element_clickable(*self.cvv_field)
        cvv_field.clear()
        cvv_field.send_keys(cvv)

    def press_tab(self):
        ActionChains(self.driver).send_keys(Keys.TAB).perform()

    def click_add_card_filled_fields_button(self) -> None:
        """
        Hace clic en el botón "Agregar" del modal "Agregar tarjeta. El botón se habilita cuando se han ingresado datos validos y se quita el foco del campo."
        """
        # Antes de hacer clic en el botón, hay que quitar el foco del campo
        self.press_tab()
        # Hacer clic en el botón de agregar tarjeta
        self._find_element_clickable(*self.add_data_card_button).click()

    def is_new_card_added(self) -> bool:
        try:
            self._find_element_presence(*self.last_added_card_row)
            return True
        except:
            return False

    def close_payment_method_modal(self) -> None:
        self._find_element_clickable(*self.payment_method_modal_close_button).click()

    def add_new_card(self, card_number, cvv):
        """
        Agrega una tarjeta de crédito.
        Pasos:
            1. Clic en el botón "Método de pago"
            2. Clic en "Agregar tarjeta"
            3. Llenar el campo "Numero de tarjeta"
            4. Llenar el campo "Código"
            5. Clic en "Agregar"
        """
        self.click_payment_method_button()
        self.click_add_card_button()
        self.fill_card_number_field(card_number)
        self.fill_cvv_field(cvv)
        self.click_add_card_filled_fields_button()

    def fill_driver_message_field(self, message):
        message_field = self._find_element_clickable(*self.comment_field)
        message_field.clear()
        message_field.send_keys(message)

    def get_driver_message(self):
        return self._find_element_presence(*self.comment_field).get_property('value')

    def is_driver_message_field_invalid(self) -> bool:
        """Valida que el div contenedor del campo 'Mensaje para el conductor' tiene la clase 'error' cuando se ingresa un comentario con más de 24 caracteres"""
        message_field_container = self._find_element_presence(*self.comment_field_container)
        container_class = message_field_container.get_attribute("class")
        if container_class:
            return "error" in container_class
        else:
            return False

    def is_blanket_and_tissues_selected(self) -> bool:
        """Devuelve True si el checkbox está seleccionado. False en caso contrario."""
        checkbox = self._find_element_presence(*self.blanket_and_tissues_checkbox)
        return checkbox.is_selected()

    def click_blanket_and_tissues(self) -> None:
        self._find_element_presence(*self.blanket_and_tissues_checkbox_container).click()

    def get_ice_cream_current_counter_value(self) -> int:
        """Devuelve el valor actual del contador de helado"""
        return int(self._find_element_presence(*self.ice_cream_current_counter_value).text)

    def click_plus_one_ice_cream_button(self, quantity: int) -> None:
        for _ in range(quantity):
            self._find_element_clickable(*self.ice_cream_increase_counter_button).click()

    def click_reservation_button(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.reservation_button)).click()

    def reserve_taxi(self):
        """
        Reserva un taxi con los siguientes pasos:
            1. Establece la dirección "desde" y "hasta"
            2. Selecciona el modo "personal", tipo "Taxi" y hace clic en "Pedir un taxi"
            3. Agrega un numero de teléfono
            4. Hace clic en "Pedir un taxi"
        """
        self.set_route(data.address_from, data.address_to)
        self.click_request_taxi()
        self.add_phone_number(data.phone_number)
        self.click_reservation_button()

    def is_searching_for_a_car_modal_visible(self) -> bool:
        try:
            self._find_element_visibility(self.searching_car_header)
            return True
        except:
            return False

    def get_searching_for_a_car_timer(self) -> int:
        import time
        time.sleep(1)
        seconds = self._convert_timer_str_to_seconds(self._find_element_visibility(self.searching_car_timer).text)
        print(f"⌛ Tiempo de espera para buscar un automóvil: {seconds} segundos.")
        return seconds

    @staticmethod
    def _convert_timer_str_to_seconds(time_str: str) -> int:
        """
        Convierte una cadena en formato 'MM:SS' a segundos totales.

        Ejemplo:
            '05:30' -> 330
        """
        minutes, seconds = time_str.split(':')
        return int(minutes) * 60 + int(seconds)

    def is_driver_arriving_header_visible(self) -> bool:
        """
        Verifica que el header sea visible con un timeout igual al contador de búsqueda de automóvil.
        """
        timer = int(self.get_searching_for_a_car_timer())
        wait = WebDriverWait(self.driver, timer)
        try:
            wait.until(EC.visibility_of_element_located(self.driver_arrive_header))
            return True
        except:
            return False

    def click_order_details_button(self):
        """
        Hace clic en el botón "Detalles" que muestra los datos del viaje.
        """
        self._find_element_clickable(*self.order_details_button).click()

    def are_order_details_shown(self):
        """
        Checa que el elemento con las clases "order-details shown" sea visible.
        Returns:
            bool: True o False si es visible o no.
        """
        try:
            self._find_element_visibility(self.order_details_shown_div)
            return True
        except:
            return False


class TestUrbanRoutes:

    driver = None

    # @classmethod
    # def setup_class(cls):
    #     # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
    #     # Código que causa la advertencia "unexpected arguments"
    #     """from selenium.webdriver import DesiredCapabilities
    #     capabilities = DesiredCapabilities.CHROME
    #     capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
    #     cls.driver = webdriver.Chrome(desired_capabilities=capabilities)"""

    @classmethod
    def setup_method(cls):
        # Código corregido (Selenium 4+)
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)
        cls.routes_page = UrbanRoutesPage(cls.driver)
        cls.routes_page.navigate_to_urban_routes()

    # Test 1.1: Los campos "desde" y "hasta" reciben las direcciones exitosamente
    def test_set_route(self):
        print(f"\n🧪 Testing set_route")
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_route(address_from, address_to)
        assert self.routes_page.get_from() == address_from, f"🐛 Se esperaba: {address_from}, se obtuvo {self.routes_page.get_from()}"
        print(f"✅ Dirección 'desde' establecida con éxito")
        assert self.routes_page.get_to() == address_to, f"🐛 Se esperaba: {address_to}, se obtuvo {self.routes_page.get_to()}"
        print(f"✅ Dirección 'hasta' establecida con éxito")

    # Test 1.2: Llenar ambos campos con direcciones válidas despliegan el contenedor de selector de modo
    def test_set_valid_route_displays_mode_selector(self):
        print(f"\n🧪 Testing set_valid_route_displays_mode_selector")
        self.routes_page.set_route(data.address_from, data.address_to)
        assert self.routes_page.is_type_picker_shown(), f"🐛 No se despliega el contenedor de selector de 'Modo'"
        print(f"✅ Se despliega el contenedor de selector de 'Modo'")

    # Test 1.3: Dirección "Desde" valida y vacío "Hasta" no despliega el contenedor de selector de modo
    def test_set_valid_from_address_empty_to_address_dont_display_mode_selector(self):
        print(f"\n🧪 Testing set_valid_from_address_empty_to_address_dont_display_mode_selector")
        self.routes_page.set_route(data.address_from, "")
        assert self.routes_page.is_type_picker_shown() == False, f"🐛 Se despliega el contenedor de selector de 'Modo'"
        print(f"✅ No se despliega el contenedor de selector de 'Modo'")
    # Test 1.4: Dirección "Hasta" valida y vacío "Desde" no despliega el contenedor de selector de modo
    def test_set_valid_to_address_empty_from_address_dont_display_mode_selector(self):
        print(f"\n🧪 Testing set_valid_to_address_empty_from_address_dont_display_mode_selector")
        self.routes_page.set_route("", data.address_to)
        assert self.routes_page.is_type_picker_shown() == False, f"🐛 Se despliega el contenedor de selector de 'Modo'"
        print(f"✅ No se despliega el contenedor de selector de 'Modo'")
    # Test 1.5: Dirección "Hasta" inválida y valida "Desde" no despliega el contenedor de selector de modo
    def test_set_invalid_to_address_valid_from_address_dont_display_mode_selector(self):
        print(f"\n🧪 Testing set_invalid_to_address_valid_from_address_dont_display_mode_selector")
        self.routes_page.set_route(data.address_from, "invalid address")
        assert self.routes_page.is_type_picker_shown() == False, f"🐛 Se despliega el contenedor de selector de 'Modo'"
        print(f"✅ No se despliega el contenedor de selector de 'Modo'")
    # Test 1.6: Dirección "Desde" inválida y valida "Hasta" no despliega el contenedor de selector de modo
    def test_set_invalid_from_address_valid_to_address_dont_display_mode_selector(self):
        print(f"\n🧪 Testing set_invalid_from_address_valid_to_address_dont_display_mode_selector")
        self.routes_page.set_route("invalid address", data.address_to)
        assert self.routes_page.is_type_picker_shown() == False, f"🐛 Se despliega el contenedor de selector de 'Modo'"
        print(f"✅ No se despliega el contenedor de selector de 'Modo'")

    # Test 2.1: Seleccionar el modo "Personal" > tipo "Taxi" y hacer clic en el botón "Pedir un taxi" despliega el selector de tarifas
    def test_personal_taxi_request_displays_tariff_picker(self):
        print(f"\n🧪 Testing personal_taxi_request_displays_tariff_picker")
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        assert self.routes_page.is_tariff_container_visible(), "🐛 El contenedor de tarifas no se esta mostrando"
        print(f"✅ El contenedor de tarifas se muestra")

    # Test 3.1: Hacer clic en el campo "Número de teléfono" despliega el modal para introducir el número de teléfono
    def test_click_phone_number_button_opens_modal(self):
        print(f"\n🧪 Testing click_phone_number_button_opens_modal")
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        self.routes_page.click_comfort_tariff_button()
        self.routes_page.click_phone_number_button()
        assert self.routes_page.is_phone_number_modal_visible(), "🐛 El modal para introducir numero de teléfono no se esta mostrando"
        print(f"✅ El modal para introducir numero de teléfono se muestra")

    # Test 3.2: El campo "Número de teléfono" recibe el teléfono exitosamente
    def test_set_phone_number(self):
        print(f"\n🧪 Testing set_phone_number")
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        self.routes_page.click_comfort_tariff_button()
        self.routes_page.click_phone_number_button()

        phone_number = data.phone_number
        self.routes_page.set_phone_number(phone_number)

        assert self.routes_page.get_phone_number() == phone_number, f"🐛 Se esperaba: {phone_number}, se obtuvo {self.routes_page.get_phone_number()}"
        print(f"✅ Numero teléfono '{phone_number}' ingresado con éxito")

    # Test 3.3: Al llenar el campo "Número de teléfono" y hacer clic en el botón "Siguiente" despliega el modal "Introduce el código del SMS"
    def test_phone_number_next_shows_sms_code_modal(self):
        print(f"\n🧪 Testing phone_number_next_shows_sms_code_modal")


        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        self.routes_page.click_comfort_tariff_button()
        self.routes_page.click_phone_number_button()

        phone_number = data.phone_number
        self.routes_page.set_phone_number(phone_number)
        # Hacer clic en "Siguiente"
        self.routes_page.click_next_button_phone_modal()
        assert self.routes_page.is_sms_code_header_modal_visible(), f"🐛 El modal para introducir el código del SMS no se muestra en pantalla"
        print(f"✅ El modal para introducir el código del SMS se muestra en pantalla")


    # Test 3.4: Al llenar el campo "Número de teléfono" con un número inválido y hacer clic en el botón "Siguiente" no abre el modal para introducir el código del SMS
    def test_invalid_phone_number_next_does_not_open_sms_modal(self):
        print("\n🧪 Testing invalid_phone_number_next_does_not_open_sms_modal")
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        self.routes_page.click_phone_number_button()
        self.routes_page.set_phone_number("+1123")
        self.routes_page.click_next_button_phone_modal()
        assert self.routes_page.is_sms_code_header_modal_visible() == False, "🐛 Se abre el modal para introducir el código del SMS"
        print("✅ No se abre el modal para introducir el código del SMS")
    # Test 3.5: Al dejar vacío el campo "Número de teléfono" y hacer clic en el botón "Siguiente" no abre el modal para introducir el código del SMS
    def test_empty_phone_number_next_does_not_open_sms_modal(self):
        print("\n🧪 Testing empty_phone_number_next_does_not_open_sms_modal")
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        self.routes_page.click_phone_number_button()
        self.routes_page.set_phone_number("")
        self.routes_page.click_next_button_phone_modal()
        assert self.routes_page.is_sms_code_header_modal_visible() == False, "🐛 Se abre el modal para introducir el código del SMS"
        print("✅ No se abre el modal para introducir el código del SMS")

    # Test 3.6: Al llenar el campo y hacer clic en siguiente, se recibe un código de verificación
    def test_sms_code_is_4_digit_string(self):
        print("\n🧪 Testing sms_code_is_4_digit_string")
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        self.routes_page.click_comfort_tariff_button()
        self.routes_page.click_phone_number_button()
        phone_number = data.phone_number
        self.routes_page.set_phone_number(phone_number)
        self.routes_page.click_next_button_phone_modal()
        code = retrieve_phone_code(self.driver)
        assert isinstance(code, str), "🐛 El código no es un string"
        assert len(code) == 4, f"🐛 Se esperaban 4 dígitos, pero se obtuvo: {code}"
        assert code.isdigit(), "🐛 El código contiene caracteres no numéricos: {code}"
        print(f"✅ El código SMS es un string numérico de 4 dígitos: {code}")

    # Test 3.7: Introducir el código en campo "código" y hacer clic en "Confirmar" cierra el modal y se agrega la clase "filled" al botón para ingresar un número de teléfono
    def test_confirm_sms_code_closes_modal_and_marks_phone_filled(self):
        print(f"\n🧪 Testing confirm_sms_code_closes_modal_and_marks_phone_filled")
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        self.routes_page.click_comfort_tariff_button()
        self.routes_page.click_phone_number_button()
        phone_number = data.phone_number
        self.routes_page.set_phone_number(phone_number)
        self.routes_page.click_next_button_phone_modal()
        code = retrieve_phone_code(self.driver)
        self.routes_page.fill_sms_code_field(code)
        self.routes_page.click_confirm_button_verification_code()
        assert self.routes_page.is_sms_code_header_modal_visible() == False, f"🐛 El modal para introducir el código del SMS es visible en pantalla"
        assert self.routes_page.is_element_present(*self.routes_page.filled_phone_number_button), f"🐛 El botón para ingresar un numero de teléfono no indica que se ha aceptado el numero de teléfono"
        print("✅ Se agrego exitosamente el numero de teléfono")

    # Test 3.8: Introducir un código incorrecto y hacer clic en "Confirmar" no cierra el modal para ingresar el código del sms
    def test_confirm_wrong_sms_code_doesnt_closes_modal(self):
        print(f"\n🧪 Testing confirm_wrong_sms_code_doesnt_closes_modal")
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        self.routes_page.click_comfort_tariff_button()
        self.routes_page.click_phone_number_button()
        phone_number = data.phone_number
        self.routes_page.set_phone_number(phone_number)
        self.routes_page.click_next_button_phone_modal()
        code = retrieve_phone_code(self.driver)
        wrong_code = int(code) + 1
        self.routes_page.fill_sms_code_field(wrong_code)
        self.routes_page.click_confirm_button_verification_code()
        assert self.routes_page.is_sms_code_header_modal_visible, f"🐛 Se cerro el modal para introducir el código del SMS"
        print("✅ Hacer clic en confirmar con un código incorrecto no cierra el modal para ingresar el código del SMS")

    # Test 4.1: Hacer clic en el botón de método de pago despliega el modal de método de pago
    def test_click_payment_method_button_opens_modal(self):
        print(f"\n🧪 Testing click_payment_method_button_opens_modal")

        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        self.routes_page.click_payment_method_button()
        assert self.routes_page.is_payment_method_modal_visible(), f"🐛 El modal método de pago no es visible en pantalla"
        print("✅ Se desplegó el modal método de pago")

    # Test 4.2: Hacer clic en el botón "Agregar tarjeta" despliega el modal "Agregar tarjeta"
    def test_click_add_card_button_opens_modal(self):
        print(f"\n🧪 Testing click_payment_method_button_opens_modal")
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        self.routes_page.click_payment_method_button()
        self.routes_page.click_add_card_button()
        assert self.routes_page.is_add_card_modal_visible(), f"🐛 El modal 'Agregar tarjeta' no es visible en pantalla"
        print("✅ Se desplegó el modal 'Agregar tarjeta'")

    # Test 4.3: Agregar una tarjeta con número válido y código válido
    def test_add_valid_card_number_and_cvv(self):
        """Comprueba que se agrega una nueva tarjeta con datos válidos"""
        print(f"\n🧪 Testing add_valid_card_number_and_cvv")

        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        card_number = data.valid_card_number
        cvv = data.valid_card_code
        self.routes_page.add_new_card(card_number, cvv)
        # Verificar que aparece una fila con el texto "Tarjeta"
        assert self.routes_page.is_new_card_added(), f"🐛 No se agrego la tarjeta"
        print(f"✅ Se agrego la tarjeta con numero: {card_number}, cvv: {cvv}")

    # Test 4.4: Hacer clic en "Agregar" en el modal de agregar tarjeta con un numero valido y código inválido no hace nada
    def test_add_valid_card_number_and_invalid_cvv_does_nothing(self):
        """Comprueba que ingresar un numero valido y código inválido y hacer clic en 'Agregar' no sucede nada."""
        print(f"\n🧪 Testing add_valid_card_number_and_invalid_cvv")
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        card_number = data.valid_card_number
        cvv = data.invalid_card_code
        self.routes_page.add_new_card(card_number, cvv)
        # Verificar que el modal sigue abierto
        assert self.routes_page.is_add_card_modal_visible(), f"🐛 El modal para agregar la tarjeta se cerró"
        print("✅ No ocurrió nada. El modal para agregar la tarjeta sigue abierto")
    # Test 4.5: No es posible hacer clic en el botón de agregar tarjeta cuando se ingresa una tarjeta con número inválido y código válido
    def test_add_invalid_card_number_and_valid_cvv_does_nothing(self):
        """Comprueba que ingresar un numero invalido y código válido y hacer clic en 'Agregar' no sucede nada."""
        print(f"\n🧪 Testing add_invalid_card_number_and_valid_cvv_does_nothing")
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        card_number = data.invalid_card_number
        cvv = data.valid_card_code
        self.routes_page.add_new_card(card_number, cvv)
        # Verificar que el modal sigue abierto
        assert self.routes_page.is_add_card_modal_visible(), f"🐛 El modal para agregar la tarjeta se cerró"
        print("✅ No ocurrió nada. El modal para agregar la tarjeta sigue abierto")
    # Test 4.6: El botón "Agregar" esta deshabilitado cuando se dejan los campos vacíos para agregar una nueva tarjeta
    def test_add_button_disabled_when_empty_card_number_and_empty_cvv(self):
        """
        Comprueba el estado `disabled` del botón cuando se dejan los campos vacíos al agregar una nueva tarjeta.
        """
        print(f"\n🧪 Testing add_button_disabled_when_empty_card_number_and_empty_cvv")
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        self.routes_page.click_payment_method_button()
        self.routes_page.click_add_card_button()
        self.routes_page.fill_card_number_field("")
        self.routes_page.fill_cvv_field("")
        # Hacer un tab
        self.routes_page.press_tab()
        # Verificar que el botón esté deshabilitado
        assert self.routes_page.is_button_disabled(self.routes_page.add_data_card_button), "🐛 El botón 'Agregar' esta habilitado."
        print("✅ El botón 'Agregar' esta deshabilitado")
    # Test 5.1: El campo "Mensaje para el conductor" permite agregar un mensaje con longitud menor o igual a 24 caracteres
    def test_driver_message_field_accepts_24_characters(self):
        print(f"\n🧪 Testing driver_message_field_accepts_24_characters")

        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        message = data.message_for_driver_24_chars
        self.routes_page.fill_driver_message_field(message)
        assert self.routes_page.get_driver_message() == message, f"🐛 No se agrego el mensaje en el campo"
        print(f"✅ Se agrego el mensaje en el campo: {message}")

    # Test 5.2: El campo "Mensaje para el conductor" marca como invalido un mensaje con mayor de 24 caracteres
    def test_driver_message_field_doesnt_accept_more_than_24_chars(self):
        print(f"\n🧪 Testing driver_message_field_shows_invalid_more_than_24_chars")

        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        message = data.message_for_driver_28_chars
        self.routes_page.fill_driver_message_field(message)
        assert self.routes_page.is_driver_message_field_invalid(), f"🐛 El campo debería marcarse como invalido con mas de 24 caracteres. len: {len(message)}"
        print(f"✅ El campo se marca como invalido con el mensaje: {message}")

    # Test 6.1: El estado del checkbox "Manta y pañuelos" cambia correctamente
    def test_blanket_and_tissues_checkbox_changes_state(self):
        print(f"\n🧪 Testing blanket_and_tissues_checkbox_changes_state")

        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        self.routes_page.click_comfort_tariff_button()
        # Estado inicial
        initial_state = self.routes_page.is_blanket_and_tissues_selected()
        # Hacer clic/seleccionar
        self.routes_page.click_blanket_and_tissues()
        # Verificar que cambio
        new_state = self.routes_page.is_blanket_and_tissues_selected()
        assert new_state != initial_state, f"🐛 El checkbox no cambio de estado"
        print("✅ El checkbox cambio de estado")

    # Test 7.1: Hacer clic en el botón '+' aumenta el contador en 1 del helado
    def test_ice_cream_plus_button_increases_counter_by_one(self):
        print(f"\n🧪 Testing ice_cream_plus_button_increases_counter_by_one")

        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        self.routes_page.click_comfort_tariff_button()
        # Aumentar el contador en 1
        self.routes_page.click_plus_one_ice_cream_button(1)
        # Estado final del contador
        current_counter_value = self.routes_page.get_ice_cream_current_counter_value()
        # Verificar que el valor del contador actual es igual a 1
        assert current_counter_value == 1, f"🐛 El valor del contador actual no coincide con el esperado. Valor actual: {current_counter_value}, esperado: {1}"
        print(f"✅ Hacer clic en el botón '+' aumenta en 1 el contador de helados. Valor actual: {current_counter_value}, esperado: {1}")

    # Test 7.2: Se agregan 2 helados al hacer clic en el botón '+' 2 veces
    def test_two_clicks_adds_two_ice_creams(self):
        print(f"\n🧪 Testing two_clicks_adds_two_ice_creams")

        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        self.routes_page.click_comfort_tariff_button()
        # Aumentar el contador en 2
        self.routes_page.click_plus_one_ice_cream_button(2)
        # Estado del contador
        current_counter_value = self.routes_page.get_ice_cream_current_counter_value()
        # Verificar que el valor del contador actual es igual a 2
        assert current_counter_value == 2, f"🐛 Se esperaba que se agregaran 2 helados. Se agregaron {current_counter_value}"
        print(
            f"✅ Se agregaron 2 helados")

    # Test 8.1: Al establecer las direcciones, elegir la tarifa "Comfort", agregar un número de teléfono, agregar una tarjeta de crédito, ingresar el mensaje para el conducir, seleccionar "Manta y pañuelos", agregar 2 helados y hacer clic en el botón de reserva "Pedir un taxi" se muestra el modal "Buscar automóvil"
    def test_complete_comfort_order_shows_searching_car_modal(self):
        """
        Se muestra el modal de búsqueda de automóvil al hacer clic en el botón 'Pedir un taxi' después de haber hecho los siguientes pasos:
            1. Ingresar las direcciones "desde" y "hasta"
            2. Seleccionar modo "Personal"
            3. Seleccionar tipo "Taxi" y hacer clic en "Pedir un Taxi"
            4. Seleccionar la tarifa "Comfort"
            5. Ingresar un numero de teléfono valido
            6. Ingresar una tarjeta de crédito valida
            7. Cerrar el modal "Método de pago"
            8. Ingresar un mensaje valido para el conductor
            9. Seleccionar "Manta y pañuelos"
            10. Agregar 2 helados
        """
        print(f"\n🧪 Testing complete_comfort_order_shows_searching_car_modal")

        # Paso 1
        self.routes_page.set_route(data.address_from, data.address_to)
        # Paso 2 y 3
        self.routes_page.click_request_taxi()
        # Paso 4
        self.routes_page.click_comfort_tariff_button()
        # Paso 5
        self.routes_page.add_phone_number(data.phone_number)
        # Paso 6
        self.routes_page.add_new_card(data.valid_card_number, data.valid_card_code)
        # Paso 7
        self.routes_page.close_payment_method_modal()
        # Paso 8
        self.routes_page.fill_driver_message_field(data.message_for_driver_24_chars)
        # Paso 9
        self.routes_page.click_blanket_and_tissues()
        # Paso 10
        self.routes_page.click_plus_one_ice_cream_button(2)
        # Hacer clic en el botón de reserva "Pedir un Taxi"
        self.routes_page.click_reservation_button()
        assert self.routes_page.is_searching_for_a_car_modal_visible(), f"🐛 No se desplegó el modal 'Buscar automóvil'"
        print(f"✅ Se desplegó el modal 'Buscar automóvil'")

    # Test 8.2: Reservar un taxi sin ingresar un numero de teléfono despliega el modal para agregar un numero de teléfono
    def test_book_taxi_without_phone_opens_phone_modal(self):
        print("\n🧪 Testing book_taxi_without_phone_opens_phone_modal")
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        self.routes_page.click_reservation_button()
        assert self.routes_page.is_phone_number_modal_visible(), "🐛 El modal para ingresar numero de teléfono no está visible"
        print("✅ El modal para ingresar numero de teléfono está visible")

    # Test 9.1: Aparece la información del conductor en el modal "Buscar un automóvil" al terminar el temporizador
    def test_driver_info_appears_after_timer_ends(self):
        """
        Verifica que aparezca la información del conductor al terminar el temporizador de búsqueda de automóvil.
        """
        print(f"\n🧪 Testing driver_info_appears_after_timer_ends")

        self.routes_page.reserve_taxi()
        assert self.routes_page.is_driver_arriving_header_visible(), f"🐛 No se mostró la información del conductor"
        print(f"✅ Se mostró la información del conductor")

    # Test 9.2: Hacer clic en el botón "Detalles" muestra los detalles del viaje
    def test_click_details_shows_trip_details(self):
        print("\n🧪 Testing click_details_shows_trip_details")
        self.routes_page.reserve_taxi()
        self.routes_page.click_order_details_button()
        assert self.routes_page.are_order_details_shown(), "🐛 Los detalles del viaje no son visibles al hacer clic en el botón 'Detalles'"
        print("✅ Los detalles del viaje son visibles al hacer clic en 'Detalles'")

    @classmethod
    def teardown_method(cls):
        if cls.driver is not None:
            try:
                cls.driver.quit()
            finally:
                cls.driver = None
