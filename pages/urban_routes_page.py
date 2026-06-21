import json
import time
import data
from selenium.common import WebDriverException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def retrieve_phone_code(driver) -> str:
    """Recupera el código SMS desde los logs de performance del navegador."""
    code = None
    for _ in range(10):
        try:
            logs = [
                log["message"]
                for log in driver.get_log("performance")
                if log.get("message") and "api/v1/number?number" in log.get("message")
            ]
            for entry in reversed(logs):
                message_data = json.loads(entry)["message"]
                body = driver.execute_cdp_cmd(
                    "Network.getResponseBody",
                    {"requestId": message_data["params"]["requestId"]},
                )
                code = "".join([x for x in body["body"] if x.isdigit()])
                if code:
                    return code
        except WebDriverException:
            time.sleep(1)
            continue
    raise Exception(
        "No se encontró el código de confirmación del teléfono.\n"
        "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación."
    )


class UrbanRoutesPage:
    # Localizadores
    from_field = (By.ID, "from")
    to_field = (By.ID, "to")
    type_picker_shown_div = (By.CSS_SELECTOR, ".type-picker.shown")
    personal_mode_button = (By.XPATH, "//div[text()='Personal']")
    taxi_type_button = (By.XPATH, "//div[contains(@class, 'types-container')]/div[3]")
    request_taxi_button = (By.XPATH, "//div[contains(@class, 'results-text')]/button")
    tariff_picker_container = (By.CLASS_NAME, "tariff-picker")
    comfort_tariff_button = (By.XPATH, "//div[@class='tariff-cards']/div[5]")
    phone_number_button = (By.CLASS_NAME, "np-button")
    phone_number_modal = (By.CLASS_NAME, "number-picker")
    phone_number_field = (By.XPATH, "//input[@id='phone']")
    next_button_phone_number = (
        By.XPATH,
        "//div[@class='number-picker open']//button[contains(text(), 'Siguiente')]",
    )
    sms_code_modal_header = (
        By.XPATH,
        "//div[contains(text(), 'Introduce el código del SMS')]",
    )
    filled_phone_number_button = (By.CSS_SELECTOR, ".np-button.filled")
    code_field = (By.ID, "code")
    confirm_button_sms_code = (
        By.XPATH,
        "//div[@class='number-picker open']//button[contains(text(), 'Confirmar')]",
    )
    payment_method_button = (By.CLASS_NAME, "pp-button")
    payment_method_modal = (By.CLASS_NAME, "payment-picker")
    add_card_button = (
        By.XPATH,
        "//div[@class='pp-title' and contains(text(), 'Agregar tarjeta')]",
    )
    header_add_card_modal = (
        By.XPATH,
        "//div[@class='head' and contains(text(), 'Agregar tarjeta')]",
    )
    card_number_field = (By.ID, "number")
    cvv_field = (By.XPATH, "//input[@id='code' and @class='card-input']")
    add_data_card_button = (
        By.XPATH,
        "//div[@class='pp-buttons']//button[contains(text(), 'Agregar')]",
    )
    last_added_card_row = (
        By.XPATH,
        "//div[contains(@class, 'pp-title') and text()='Tarjeta']",
    )
    payment_method_modal_close_button = (
        By.XPATH,
        "//div[contains(@class, 'payment-picker')]//div[contains(@class, 'section active')]//button[contains(@class, 'close-button')]",
    )
    comment_field = (By.ID, "comment")
    comment_field_container = (By.XPATH, "//input[@id='comment']/..")
    blanket_and_tissues_checkbox = (
        By.XPATH,
        "//div[contains(text(), 'Manta y pañuelos')]/following-sibling::div[@class='r-sw']//input",
    )
    blanket_and_tissues_checkbox_container = (
        By.XPATH,
        "//div[contains(text(), 'Manta y pañuelos')]/following-sibling::div[@class='r-sw']//input/..",
    )
    ice_cream_current_counter_value = (
        By.XPATH,
        "//div[contains(text(), 'Helado')]/following-sibling::div[@class='r-counter']//div[@class='counter-value']",
    )
    ice_cream_increase_counter_button = (
        By.XPATH,
        "//div[contains(text(), 'Helado')]/following-sibling::div[@class='r-counter']//div[@class='counter-plus']",
    )
    reservation_button = (By.XPATH, "//button[@class='smart-button']")
    searching_car_header = (
        By.XPATH,
        "//div[@class='order-header-title' and contains(text(), 'Buscar automóvil')]",
    )
    searching_car_timer = (By.CLASS_NAME, "order-header-time")
    driver_arrive_header = (
        By.XPATH,
        "//div[@class='order-header-title' and contains(text(), 'El conductor llegará en')]",
    )
    order_details_button = (
        By.XPATH,
        "//div[@class='order shown']//div[text()='Detalles']/parent::div/button",
    )
    order_details_shown_div = (By.CSS_SELECTOR, ".order-details.shown")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate_to_urban_routes(self):
        self.driver.get(data.urban_routes_url)

    def _find_element_presence(self, by, value, timeout=None):
        if timeout:
            wait = WebDriverWait(self.driver, timeout)
        else:
            wait = self.wait
        return wait.until(EC.presence_of_element_located((by, value)))

    def _find_element_clickable(self, by, value):
        return self.wait.until(
            EC.element_to_be_clickable((by, value)),
            f"❌ Error Element to be clickable: {value}",
        )

    def _find_element_visibility(self, locator, timeout=None):
        if timeout:
            wait = WebDriverWait(self.driver, timeout)
        else:
            wait = self.wait
        return wait.until(EC.visibility_of_element_located(locator))

    def is_element_present(self, by, value):
        return len(self.driver.find_elements(by, value)) > 0

    def is_button_disabled(self, locator):
        button = self._find_element_presence(*locator)
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
        return self._find_element_presence(*self.from_field).get_property("value")

    def get_to(self):
        return self._find_element_presence(*self.to_field).get_property("value")

    def click_request_taxi(self):
        self._find_element_clickable(*self.personal_mode_button).click()
        self._find_element_clickable(*self.taxi_type_button).click()
        self._find_element_clickable(*self.request_taxi_button).click()

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    def is_type_picker_shown(self):
        try:
            self._find_element_presence(*self.type_picker_shown_div, timeout=1)
            return True
        except Exception:
            return False

    def is_tariff_container_visible(self):
        try:
            self._find_element_visibility(self.tariff_picker_container)
            return True
        except Exception:
            return False

    def click_comfort_tariff_button(self):
        self._find_element_clickable(*self.comfort_tariff_button).click()

    def click_phone_number_button(self):
        self._find_element_clickable(*self.phone_number_button).click()

    def is_phone_number_modal_visible(self):
        try:
            self._find_element_visibility(self.phone_number_modal, 1)
            return True
        except Exception:
            return False

    def set_phone_number(self, phone_number):
        field = self._find_element_clickable(*self.phone_number_field)
        field.clear()
        field.send_keys(phone_number)

    def get_phone_number(self):
        return self._find_element_presence(*self.phone_number_field).get_property("value")

    def click_next_button_phone_modal(self):
        self._find_element_clickable(*self.next_button_phone_number).click()

    def is_sms_code_header_modal_visible(self):
        try:
            self._find_element_visibility(self.sms_code_modal_header, 1)
            return True
        except Exception:
            return False

    def fill_sms_code_field(self, code):
        field = self._find_element_clickable(*self.code_field)
        field.clear()
        field.send_keys(code)

    def click_confirm_button_verification_code(self):
        self._find_element_clickable(*self.confirm_button_sms_code).click()

    def add_phone_number(self, phone_number):
        self.click_phone_number_button()
        self.set_phone_number(phone_number)
        self.click_next_button_phone_modal()
        self.fill_sms_code_field(retrieve_phone_code(self.driver))
        self.click_confirm_button_verification_code()

    def click_payment_method_button(self):
        self._find_element_clickable(*self.payment_method_button).click()

    def is_payment_method_modal_visible(self):
        try:
            self._find_element_visibility(self.payment_method_modal)
            return True
        except Exception:
            return False

    def click_add_card_button(self):
        self._find_element_clickable(*self.add_card_button).click()

    def is_add_card_modal_visible(self):
        try:
            self._find_element_visibility(self.header_add_card_modal, 1)
            return True
        except Exception:
            return False

    def fill_card_number_field(self, card_number):
        field = self._find_element_clickable(*self.card_number_field)
        field.clear()
        field.send_keys(card_number)

    def fill_cvv_field(self, cvv):
        field = self._find_element_clickable(*self.cvv_field)
        field.clear()
        field.send_keys(cvv)

    def press_tab(self):
        ActionChains(self.driver).send_keys(Keys.TAB).perform()

    def click_add_card_filled_fields_button(self):
        self.press_tab()
        self._find_element_clickable(*self.add_data_card_button).click()

    def is_new_card_added(self):
        try:
            self._find_element_presence(*self.last_added_card_row)
            return True
        except Exception:
            return False

    def close_payment_method_modal(self):
        self._find_element_clickable(*self.payment_method_modal_close_button).click()

    def add_new_card(self, card_number, cvv):
        self.click_payment_method_button()
        self.click_add_card_button()
        self.fill_card_number_field(card_number)
        self.fill_cvv_field(cvv)
        self.click_add_card_filled_fields_button()

    def fill_driver_message_field(self, message):
        field = self._find_element_clickable(*self.comment_field)
        field.clear()
        field.send_keys(message)

    def get_driver_message(self):
        return self._find_element_presence(*self.comment_field).get_property("value")

    def is_driver_message_field_invalid(self):
        container = self._find_element_presence(*self.comment_field_container)
        return "error" in (container.get_attribute("class") or "")

    def is_blanket_and_tissues_selected(self):
        checkbox = self._find_element_presence(*self.blanket_and_tissues_checkbox)
        return checkbox.is_selected()

    def click_blanket_and_tissues(self):
        self._find_element_presence(*self.blanket_and_tissues_checkbox_container).click()

    def get_ice_cream_current_counter_value(self):
        return int(self._find_element_presence(*self.ice_cream_current_counter_value).text)

    def click_plus_one_ice_cream_button(self, quantity):
        for _ in range(quantity):
            self._find_element_clickable(*self.ice_cream_increase_counter_button).click()

    def click_reservation_button(self):
        self._find_element_clickable(*self.reservation_button).click()

    def reserve_taxi(self):
        self.set_route(data.address_from, data.address_to)
        self.click_request_taxi()
        self.add_phone_number(data.phone_number)
        self.click_reservation_button()

    def is_searching_for_a_car_modal_visible(self):
        try:
            self._find_element_visibility(self.searching_car_header)
            return True
        except Exception:
            return False

    def get_searching_for_a_car_timer(self):
        time.sleep(1)
        seconds = self._convert_timer_str_to_seconds(
            self._find_element_visibility(self.searching_car_timer).text
        )
        print(f"⌛ Tiempo de espera para buscar un automóvil: {seconds} segundos.")
        return seconds

    @staticmethod
    def _convert_timer_str_to_seconds(time_str):
        minutes, seconds = time_str.split(":")
        return int(minutes) * 60 + int(seconds)

    def is_driver_arriving_header_visible(self):
        timer = self.get_searching_for_a_car_timer()
        wait = WebDriverWait(self.driver, timer)
        try:
            wait.until(EC.visibility_of_element_located(self.driver_arrive_header))
            return True
        except Exception:
            return False

    def click_order_details_button(self):
        self._find_element_clickable(*self.order_details_button).click()

    def are_order_details_shown(self):
        try:
            self._find_element_visibility(self.order_details_shown_div)
            return True
        except Exception:
            return False
