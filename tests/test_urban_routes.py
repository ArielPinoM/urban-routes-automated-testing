import data
from pages.urban_routes_page import UrbanRoutesPage, retrieve_phone_code


class TestUrbanRoutes:
    def test_set_route(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing set_route")
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from, f"🐛 Se esperaba: {address_from}, se obtuvo {routes_page.get_from()}"
        print(f"✅ Dirección 'desde' establecida con éxito")
        assert routes_page.get_to() == address_to, f"🐛 Se esperaba: {address_to}, se obtuvo {routes_page.get_to()}"
        print(f"✅ Dirección 'hasta' establecida con éxito")

    def test_set_valid_route_displays_mode_selector(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing set_valid_route_displays_mode_selector")
        routes_page.set_route(data.address_from, data.address_to)
        assert routes_page.is_type_picker_shown(), f"🐛 No se despliega el contenedor de selector de 'Modo'"
        print(f"✅ Se despliega el contenedor de selector de 'Modo'")

    def test_set_valid_from_address_empty_to_address_dont_display_mode_selector(
        self, routes_page: UrbanRoutesPage
    ):
        print(f"\n🧪 Testing set_valid_from_address_empty_to_address_dont_display_mode_selector")
        routes_page.set_route(data.address_from, "")
        assert routes_page.is_type_picker_shown() == False, f"🐛 Se despliega el contenedor de selector de 'Modo'"
        print(f"✅ No se despliega el contenedor de selector de 'Modo'")

    def test_set_valid_to_address_empty_from_address_dont_display_mode_selector(
        self, routes_page: UrbanRoutesPage
    ):
        print(f"\n🧪 Testing set_valid_to_address_empty_from_address_dont_display_mode_selector")
        routes_page.set_route("", data.address_to)
        assert routes_page.is_type_picker_shown() == False, f"🐛 Se despliega el contenedor de selector de 'Modo'"
        print(f"✅ No se despliega el contenedor de selector de 'Modo'")

    def test_set_invalid_to_address_valid_from_address_dont_display_mode_selector(
        self, routes_page: UrbanRoutesPage
    ):
        print(f"\n🧪 Testing set_invalid_to_address_valid_from_address_dont_display_mode_selector")
        routes_page.set_route(data.address_from, "invalid address")
        assert routes_page.is_type_picker_shown() == False, f"🐛 Se despliega el contenedor de selector de 'Modo'"
        print(f"✅ No se despliega el contenedor de selector de 'Modo'")

    def test_set_invalid_from_address_valid_to_address_dont_display_mode_selector(
        self, routes_page: UrbanRoutesPage
    ):
        print(f"\n🧪 Testing set_invalid_from_address_valid_to_address_dont_display_mode_selector")
        routes_page.set_route("invalid address", data.address_to)
        assert routes_page.is_type_picker_shown() == False, f"🐛 Se despliega el contenedor de selector de 'Modo'"
        print(f"✅ No se despliega el contenedor de selector de 'Modo'")

    def test_personal_taxi_request_displays_tariff_picker(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing personal_taxi_request_displays_tariff_picker")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        assert routes_page.is_tariff_container_visible(), "🐛 El contenedor de tarifas no se esta mostrando"
        print(f"✅ El contenedor de tarifas se muestra")

    def test_click_phone_number_button_opens_modal(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing click_phone_number_button_opens_modal")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_tariff_button()
        routes_page.click_phone_number_button()
        assert routes_page.is_phone_number_modal_visible(), "🐛 El modal para introducir numero de teléfono no se esta mostrando"
        print(f"✅ El modal para introducir numero de teléfono se muestra")

    def test_set_phone_number(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing set_phone_number")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_tariff_button()
        routes_page.click_phone_number_button()

        phone_number = data.phone_number
        routes_page.set_phone_number(phone_number)

        assert routes_page.get_phone_number() == phone_number, f"🐛 Se esperaba: {phone_number}, se obtuvo {routes_page.get_phone_number()}"
        print(f"✅ Numero teléfono '{phone_number}' ingresado con éxito")

    def test_phone_number_next_shows_sms_code_modal(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing phone_number_next_shows_sms_code_modal")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_tariff_button()
        routes_page.click_phone_number_button()

        phone_number = data.phone_number
        routes_page.set_phone_number(phone_number)
        # Hacer clic en "Siguiente"
        routes_page.click_next_button_phone_modal()
        assert routes_page.is_sms_code_header_modal_visible(), f"🐛 El modal para introducir el código del SMS no se muestra en pantalla"
        print(f"✅ El modal para introducir el código del SMS se muestra en pantalla")

    def test_invalid_phone_number_next_does_not_open_sms_modal(self, routes_page: UrbanRoutesPage):
        print("\n🧪 Testing invalid_phone_number_next_does_not_open_sms_modal")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_phone_number_button()
        routes_page.set_phone_number("+1123")
        routes_page.click_next_button_phone_modal()
        assert routes_page.is_sms_code_header_modal_visible() == False, "🐛 Se abre el modal para introducir el código del SMS"
        print("✅ No se abre el modal para introducir el código del SMS")

    def test_empty_phone_number_next_does_not_open_sms_modal(self, routes_page: UrbanRoutesPage):
        print("\n🧪 Testing empty_phone_number_next_does_not_open_sms_modal")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_phone_number_button()
        routes_page.set_phone_number("")
        routes_page.click_next_button_phone_modal()
        assert routes_page.is_sms_code_header_modal_visible() == False, "🐛 Se abre el modal para introducir el código del SMS"
        print("✅ No se abre el modal para introducir el código del SMS")

    def test_sms_code_is_4_digit_string(self, routes_page: UrbanRoutesPage):
        print("\n🧪 Testing sms_code_is_4_digit_string")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_tariff_button()
        routes_page.click_phone_number_button()
        phone_number = data.phone_number
        routes_page.set_phone_number(phone_number)
        routes_page.click_next_button_phone_modal()
        code = retrieve_phone_code(routes_page.driver)
        assert isinstance(code, str), "🐛 El código no es un string"
        assert len(code) == 4, f"🐛 Se esperaban 4 dígitos, pero se obtuvo: {code}"
        assert code.isdigit(), "🐛 El código contiene caracteres no numéricos: {code}"
        print(f"✅ El código SMS es un string numérico de 4 dígitos: {code}")

    def test_confirm_sms_code_closes_modal_and_marks_phone_filled(
        self, routes_page: UrbanRoutesPage
    ):
        print(f"\n🧪 Testing confirm_sms_code_closes_modal_and_marks_phone_filled")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_tariff_button()
        routes_page.click_phone_number_button()
        phone_number = data.phone_number
        routes_page.set_phone_number(phone_number)
        routes_page.click_next_button_phone_modal()
        code = retrieve_phone_code(routes_page.driver)
        routes_page.fill_sms_code_field(code)
        routes_page.click_confirm_button_verification_code()
        assert routes_page.is_sms_code_header_modal_visible() == False, f"🐛 El modal para introducir el código del SMS es visible en pantalla"
        assert routes_page.is_element_present(*routes_page.filled_phone_number_button), f"🐛 El botón para ingresar un numero de teléfono no indica que se ha aceptado el numero de teléfono"
        print("✅ Se agrego exitosamente el numero de teléfono")

    def test_confirm_wrong_sms_code_doesnt_closes_modal(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing confirm_wrong_sms_code_doesnt_closes_modal")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_tariff_button()
        routes_page.click_phone_number_button()
        phone_number = data.phone_number
        routes_page.set_phone_number(phone_number)
        routes_page.click_next_button_phone_modal()
        code = retrieve_phone_code(routes_page.driver)
        wrong_code = str(int(code) + 1)
        routes_page.fill_sms_code_field(wrong_code)
        routes_page.click_confirm_button_verification_code()
        assert routes_page.is_sms_code_header_modal_visible(), f"🐛 Se cerro el modal para introducir el código del SMS"
        print("✅ Hacer clic en confirmar con un código incorrecto no cierra el modal para ingresar el código del SMS")

    def test_click_payment_method_button_opens_modal(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing click_payment_method_button_opens_modal")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_payment_method_button()
        assert routes_page.is_payment_method_modal_visible(), f"🐛 El modal método de pago no es visible en pantalla"
        print("✅ Se desplegó el modal método de pago")

    def test_click_add_card_button_opens_modal(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing click_payment_method_button_opens_modal")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_payment_method_button()
        routes_page.click_add_card_button()
        assert routes_page.is_add_card_modal_visible(), f"🐛 El modal 'Agregar tarjeta' no es visible en pantalla"
        print("✅ Se desplegó el modal 'Agregar tarjeta'")

    def test_add_valid_card_number_and_cvv(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing add_valid_card_number_and_cvv")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        card_number = data.valid_card_number
        cvv = data.valid_card_code
        routes_page.add_new_card(card_number, cvv)
        # Verificar que aparece una fila con el texto "Tarjeta"
        assert routes_page.is_new_card_added(), f"🐛 No se agrego la tarjeta"
        print(f"✅ Se agrego la tarjeta con numero: {card_number}, cvv: {cvv}")

    def test_add_valid_card_number_and_invalid_cvv_does_nothing(
        self, routes_page: UrbanRoutesPage
    ):
        print(f"\n🧪 Testing add_valid_card_number_and_invalid_cvv")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        card_number = data.valid_card_number
        cvv = data.invalid_card_code
        routes_page.add_new_card(card_number, cvv)
        # Verificar que el modal sigue abierto
        assert routes_page.is_add_card_modal_visible(), f"🐛 El modal para agregar la tarjeta se cerró"
        print("✅ No ocurrió nada. El modal para agregar la tarjeta sigue abierto")

    def test_add_invalid_card_number_and_valid_cvv_does_nothing(
        self, routes_page: UrbanRoutesPage
    ):
        print(f"\n🧪 Testing add_invalid_card_number_and_valid_cvv_does_nothing")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        card_number = data.invalid_card_number
        cvv = data.valid_card_code
        routes_page.add_new_card(card_number, cvv)
        # Verificar que el modal sigue abierto
        assert routes_page.is_add_card_modal_visible(), f"🐛 El modal para agregar la tarjeta se cerró"
        print("✅ No ocurrió nada. El modal para agregar la tarjeta sigue abierto")

    def test_add_button_disabled_when_empty_card_number_and_empty_cvv(
        self, routes_page: UrbanRoutesPage
    ):
        print(f"\n🧪 Testing add_button_disabled_when_empty_card_number_and_empty_cvv")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_payment_method_button()
        routes_page.click_add_card_button()
        routes_page.fill_card_number_field("")
        routes_page.fill_cvv_field("")
        # Hacer un tab
        routes_page.press_tab()
        # Verificar que el botón esté deshabilitado
        assert routes_page.is_button_disabled(routes_page.add_data_card_button), "🐛 El botón 'Agregar' esta habilitado."
        print("✅ El botón 'Agregar' esta deshabilitado")

    def test_driver_message_field_accepts_24_characters(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing driver_message_field_accepts_24_characters")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        message = data.message_for_driver_24_chars
        routes_page.fill_driver_message_field(message)
        assert routes_page.get_driver_message() == message, f"🐛 No se agrego el mensaje en el campo"
        print(f"✅ Se agrego el mensaje en el campo: {message}")

    def test_driver_message_field_doesnt_accept_more_than_24_chars(
        self, routes_page: UrbanRoutesPage
    ):
        print(f"\n🧪 Testing driver_message_field_shows_invalid_more_than_24_chars")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        message = data.message_for_driver_28_chars
        routes_page.fill_driver_message_field(message)
        assert routes_page.is_driver_message_field_invalid(), f"🐛 El campo debería marcarse como invalido con mas de 24 caracteres. len: {len(message)}"
        print(f"✅ El campo se marca como invalido con el mensaje: {message}")

    def test_blanket_and_tissues_checkbox_changes_state(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing blanket_and_tissues_checkbox_changes_state")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_tariff_button()
        # Estado inicial
        initial_state = routes_page.is_blanket_and_tissues_selected()
        # Hacer clic/seleccionar
        routes_page.click_blanket_and_tissues()
        # Verificar que cambio
        new_state = routes_page.is_blanket_and_tissues_selected()
        assert new_state != initial_state, f"🐛 El checkbox no cambio de estado"
        print("✅ El checkbox cambio de estado")

    def test_ice_cream_plus_button_increases_counter_by_one(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing ice_cream_plus_button_increases_counter_by_one")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_tariff_button()
        # Aumentar el contador en 1
        routes_page.click_plus_one_ice_cream_button(1)
        # Estado final del contador
        current_counter_value = routes_page.get_ice_cream_current_counter_value()
        # Verificar que el valor del contador actual es igual a 1
        assert current_counter_value == 1, f"🐛 El valor del contador actual no coincide con el esperado. Valor actual: {current_counter_value}, esperado: {1}"
        print(f"✅ Hacer clic en el botón '+' aumenta en 1 el contador de helados. Valor actual: {current_counter_value}, esperado: {1}")

    def test_two_clicks_adds_two_ice_creams(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing two_clicks_adds_two_ice_creams")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_tariff_button()
        # Aumentar el contador en 2
        routes_page.click_plus_one_ice_cream_button(2)
        # Estado del contador
        current_counter_value = routes_page.get_ice_cream_current_counter_value()
        # Verificar que el valor del contador actual es igual a 2
        assert current_counter_value == 2, f"🐛 Se esperaba que se agregaran 2 helados. Se agregaron {current_counter_value}"
        print(
            f"✅ Se agregaron 2 helados")

    def test_complete_comfort_order_shows_searching_car_modal(
        self, routes_page: UrbanRoutesPage
    ):
        print(f"\n🧪 Testing complete_comfort_order_shows_searching_car_modal")
        # Paso 1
        routes_page.set_route(data.address_from, data.address_to)
        # Paso 2 y 3
        routes_page.click_request_taxi()
        # Paso 4
        routes_page.click_comfort_tariff_button()
        # Paso 5
        routes_page.add_phone_number(data.phone_number)
        # Paso 6
        routes_page.add_new_card(data.valid_card_number, data.valid_card_code)
        # Paso 7
        routes_page.close_payment_method_modal()
        # Paso 8
        routes_page.fill_driver_message_field(data.message_for_driver_24_chars)
        # Paso 9
        routes_page.click_blanket_and_tissues()
        # Paso 10
        routes_page.click_plus_one_ice_cream_button(2)
        # Hacer clic en el botón de reserva "Pedir un Taxi"
        routes_page.click_reservation_button()
        assert routes_page.is_searching_for_a_car_modal_visible(), f"🐛 No se desplegó el modal 'Buscar automóvil'"
        print(f"✅ Se desplegó el modal 'Buscar automóvil'")

    def test_book_taxi_without_phone_opens_phone_modal(self, routes_page: UrbanRoutesPage):
        print("\n🧪 Testing book_taxi_without_phone_opens_phone_modal")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_reservation_button()
        assert routes_page.is_phone_number_modal_visible(), "🐛 El modal para ingresar numero de teléfono no está visible"
        print("✅ El modal para ingresar numero de teléfono está visible")

    def test_driver_info_appears_after_timer_ends(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing driver_info_appears_after_timer_ends")
        routes_page.reserve_taxi()
        assert routes_page.is_driver_arriving_header_visible(), f"🐛 No se mostró la información del conductor"
        print(f"✅ Se mostró la información del conductor")

    def test_click_details_shows_trip_details(self, routes_page: UrbanRoutesPage):
        print("\n🧪 Testing click_details_shows_trip_details")
        routes_page.reserve_taxi()
        routes_page.click_order_details_button()
        assert routes_page.are_order_details_shown(), "🐛 Los detalles del viaje no son visibles al hacer clic en el botón 'Detalles'"
        print("✅ Los detalles del viaje son visibles al hacer clic en 'Detalles'")
