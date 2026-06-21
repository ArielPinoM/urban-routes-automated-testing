import data
from pages.urban_routes_page import UrbanRoutesPage, retrieve_phone_code


class TestUrbanRoutes:
    def test_set_route(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing set_route")
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from, f"🐛 Expected: {address_from}, got {routes_page.get_from()}"
        print(f"✅ 'From' address set successfully")
        assert routes_page.get_to() == address_to, f"🐛 Expected: {address_to}, got {routes_page.get_to()}"
        print(f"✅ 'To' address set successfully")

    def test_set_valid_route_displays_mode_selector(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing set_valid_route_displays_mode_selector")
        routes_page.set_route(data.address_from, data.address_to)
        assert routes_page.is_type_picker_shown(), f"🐛 Mode selector container did not appear"
        print(f"✅ Mode selector is displayed")

    def test_set_valid_from_address_empty_to_address_dont_display_mode_selector(
        self, routes_page: UrbanRoutesPage
    ):
        print(f"\n🧪 Testing set_valid_from_address_empty_to_address_dont_display_mode_selector")
        routes_page.set_route(data.address_from, "")
        assert routes_page.is_type_picker_shown() == False, f"🐛 Mode selector container appeared unexpectedly"
        print(f"✅ Mode selector is not displayed")

    def test_set_valid_to_address_empty_from_address_dont_display_mode_selector(
        self, routes_page: UrbanRoutesPage
    ):
        print(f"\n🧪 Testing set_valid_to_address_empty_from_address_dont_display_mode_selector")
        routes_page.set_route("", data.address_to)
        assert routes_page.is_type_picker_shown() == False, f"🐛 Mode selector container appeared unexpectedly"
        print(f"✅ Mode selector is not displayed")

    def test_set_invalid_to_address_valid_from_address_dont_display_mode_selector(
        self, routes_page: UrbanRoutesPage
    ):
        print(f"\n🧪 Testing set_invalid_to_address_valid_from_address_dont_display_mode_selector")
        routes_page.set_route(data.address_from, "invalid address")
        assert routes_page.is_type_picker_shown() == False, f"🐛 Mode selector container appeared unexpectedly"
        print(f"✅ Mode selector is not displayed")

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
        assert routes_page.is_tariff_container_visible(), "🐛 Tariff container is not displayed"
        print(f"✅ Tariff container is visible")

    def test_click_phone_number_button_opens_modal(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing click_phone_number_button_opens_modal")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_tariff_button()
        routes_page.click_phone_number_button()
        assert routes_page.is_phone_number_modal_visible(), "🐛 Phone number modal is not displayed"
        print(f"✅ Phone number modal is visible")

    def test_set_phone_number(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing set_phone_number")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_tariff_button()
        routes_page.click_phone_number_button()

        phone_number = data.phone_number
        routes_page.set_phone_number(phone_number)

        assert routes_page.get_phone_number() == phone_number, f"🐛 Expected: {phone_number}, got {routes_page.get_phone_number()}"
        print(f"✅ Phone number '{phone_number}' entered successfully")

    def test_phone_number_next_shows_sms_code_modal(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing phone_number_next_shows_sms_code_modal")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_tariff_button()
        routes_page.click_phone_number_button()

        phone_number = data.phone_number
        routes_page.set_phone_number(phone_number)
        # Click the 'Next' button to proceed with the phone verification flow
        routes_page.click_next_button_phone_modal()
        assert routes_page.is_sms_code_header_modal_visible(), f"🐛 SMS code modal is not displayed"
        print(f"✅ SMS code modal is displayed")

    def test_invalid_phone_number_next_does_not_open_sms_modal(self, routes_page: UrbanRoutesPage):
        print("\n🧪 Testing invalid_phone_number_next_does_not_open_sms_modal")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_phone_number_button()
        routes_page.set_phone_number("+1123")
        routes_page.click_next_button_phone_modal()
        assert routes_page.is_sms_code_header_modal_visible() == False, "🐛 SMS code modal opened unexpectedly"
        print("✅ SMS code modal did not open")

    def test_empty_phone_number_next_does_not_open_sms_modal(self, routes_page: UrbanRoutesPage):
        print("\n🧪 Testing empty_phone_number_next_does_not_open_sms_modal")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_phone_number_button()
        routes_page.set_phone_number("")
        routes_page.click_next_button_phone_modal()
        assert routes_page.is_sms_code_header_modal_visible() == False, "🐛 SMS code modal opened unexpectedly"
        print("✅ SMS code modal did not open")

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
        assert isinstance(code, str), "🐛 Code is not a string"
        assert len(code) == 4, f"🐛 Expected 4 digits, got: {code}"
        assert code.isdigit(), "🐛 Code contains non-numeric characters: {code}"
        print(f"✅ SMS code is a 4-digit numeric string: {code}")

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
        assert routes_page.is_sms_code_header_modal_visible() == False, f"🐛 SMS code modal is still visible"
        assert routes_page.is_element_present(*routes_page.filled_phone_number_button), f"🐛 Phone number button does not indicate acceptance of the phone number"
        print("✅ Phone number added successfully")

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
        assert routes_page.is_sms_code_header_modal_visible(), f"🐛 SMS code modal closed unexpectedly"
        print("✅ Confirming with an incorrect code does not close the SMS code modal")

    def test_click_payment_method_button_opens_modal(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing click_payment_method_button_opens_modal")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_payment_method_button()
        assert routes_page.is_payment_method_modal_visible(), f"🐛 Payment method modal is not visible"
        print("✅ Payment method modal opened")

    def test_click_add_card_button_opens_modal(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing click_payment_method_button_opens_modal")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_payment_method_button()
        routes_page.click_add_card_button()
        assert routes_page.is_add_card_modal_visible(), f"🐛 'Add card' modal is not visible"
        print("✅ 'Add card' modal opened")

    def test_add_valid_card_number_and_cvv(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing add_valid_card_number_and_cvv")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        card_number = data.valid_card_number
        cvv = data.valid_card_code
        routes_page.add_new_card(card_number, cvv)
        # Assert that a row with the text 'Tarjeta' appears (new card added confirmation)
        assert routes_page.is_new_card_added(), f"🐛 Card was not added"
        print(f"✅ Card added: {card_number}, cvv: {cvv}")

    def test_add_valid_card_number_and_invalid_cvv_does_nothing(
        self, routes_page: UrbanRoutesPage
    ):
        print(f"\n🧪 Testing add_valid_card_number_and_invalid_cvv")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        card_number = data.valid_card_number
        cvv = data.invalid_card_code
        routes_page.add_new_card(card_number, cvv)
        # Assert the add-card modal remains open (invalid input should not close it)
        assert routes_page.is_add_card_modal_visible(), f"🐛 Add-card modal closed unexpectedly"
        print("✅ No action occurred; add-card modal remains open")

    def test_add_invalid_card_number_and_valid_cvv_does_nothing(
        self, routes_page: UrbanRoutesPage
    ):
        print(f"\n🧪 Testing add_invalid_card_number_and_valid_cvv_does_nothing")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        card_number = data.invalid_card_number
        cvv = data.valid_card_code
        routes_page.add_new_card(card_number, cvv)
        # Assert the add-card modal remains open (invalid input should not close it)
        assert routes_page.is_add_card_modal_visible(), f"🐛 Add-card modal closed unexpectedly"
        print("✅ No action occurred; add-card modal remains open")

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
        # Send a Tab key to trigger form validation
        routes_page.press_tab()
        # Verify the 'Add' button is disabled when inputs are empty
        assert routes_page.is_button_disabled(routes_page.add_data_card_button), "🐛 'Add' button is enabled."
        print("✅ 'Add' button is disabled")

    def test_driver_message_field_accepts_24_characters(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing driver_message_field_accepts_24_characters")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        message = data.message_for_driver_24_chars
        routes_page.fill_driver_message_field(message)
        assert routes_page.get_driver_message() == message, f"🐛 Driver message not added to the field"
        print(f"✅ Driver message entered: {message}")

    def test_driver_message_field_doesnt_accept_more_than_24_chars(
        self, routes_page: UrbanRoutesPage
    ):
        print(f"\n🧪 Testing driver_message_field_shows_invalid_more_than_24_chars")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        message = data.message_for_driver_28_chars
        routes_page.fill_driver_message_field(message)
        assert routes_page.is_driver_message_field_invalid(), f"🐛 Field should be marked invalid for >24 chars. len: {len(message)}"
        print(f"✅ Field is marked invalid with message: {message}")

    def test_blanket_and_tissues_checkbox_changes_state(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing blanket_and_tissues_checkbox_changes_state")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_tariff_button()
        # Initial checkbox state
        initial_state = routes_page.is_blanket_and_tissues_selected()
        # Click/select the checkbox
        routes_page.click_blanket_and_tissues()
        # Verify the state changed
        new_state = routes_page.is_blanket_and_tissues_selected()
        assert new_state != initial_state, f"🐛 Checkbox state did not change"
        print("✅ Checkbox state changed")

    def test_ice_cream_plus_button_increases_counter_by_one(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing ice_cream_plus_button_increases_counter_by_one")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_tariff_button()
        # Increase the ice-cream counter by 1
        routes_page.click_plus_one_ice_cream_button(1)
        # Final counter value
        current_counter_value = routes_page.get_ice_cream_current_counter_value()
        # Assert the counter equals 1
        assert current_counter_value == 1, f"🐛 Counter value does not match expected. Current: {current_counter_value}, expected: 1"
        print(f"✅ Clicking '+' increases ice-cream counter by 1. Current: {current_counter_value}, expected: 1")

    def test_two_clicks_adds_two_ice_creams(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing two_clicks_adds_two_ice_creams")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_tariff_button()
        # Increase the ice-cream counter by 2
        routes_page.click_plus_one_ice_cream_button(2)
        # Counter state after clicks
        current_counter_value = routes_page.get_ice_cream_current_counter_value()
        # Assert the counter equals 2
        assert current_counter_value == 2, f"🐛 Expected 2 ice creams to be added. Added: {current_counter_value}"
        print(f"✅ Two ice creams were added")

    def test_complete_comfort_order_shows_searching_car_modal(
        self, routes_page: UrbanRoutesPage
    ):
        print(f"\n🧪 Testing complete_comfort_order_shows_searching_car_modal")
        # Step 1: set route
        routes_page.set_route(data.address_from, data.address_to)
        # Steps 2-3: request taxi
        routes_page.click_request_taxi()
        # Step 4: select Comfort tariff
        routes_page.click_comfort_tariff_button()
        # Step 5: add and verify phone number
        routes_page.add_phone_number(data.phone_number)
        # Step 6: add payment card
        routes_page.add_new_card(data.valid_card_number, data.valid_card_code)
        # Step 7: close payment modal
        routes_page.close_payment_method_modal()
        # Step 8: add driver message
        routes_page.fill_driver_message_field(data.message_for_driver_24_chars)
        # Step 9: select extras
        routes_page.click_blanket_and_tissues()
        # Step 10: add ice cream extras
        routes_page.click_plus_one_ice_cream_button(2)
        # Click the reservation button 'Request a Taxi'
        routes_page.click_reservation_button()
        assert routes_page.is_searching_for_a_car_modal_visible(), f"🐛 'Searching for a car' modal did not appear"
        print(f"✅ 'Searching for a car' modal displayed")

    def test_book_taxi_without_phone_opens_phone_modal(self, routes_page: UrbanRoutesPage):
        print("\n🧪 Testing book_taxi_without_phone_opens_phone_modal")
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi()
        routes_page.click_reservation_button()
        assert routes_page.is_phone_number_modal_visible(), "🐛 Phone number input modal is not visible"
        print("✅ Phone number input modal is visible")

    def test_driver_info_appears_after_timer_ends(self, routes_page: UrbanRoutesPage):
        print(f"\n🧪 Testing driver_info_appears_after_timer_ends")
        routes_page.reserve_taxi()
        assert routes_page.is_driver_arriving_header_visible(), f"🐛 Driver information was not displayed"
        print(f"✅ Driver information is displayed")

    def test_click_details_shows_trip_details(self, routes_page: UrbanRoutesPage):
        print("\n🧪 Testing click_details_shows_trip_details")
        routes_page.reserve_taxi()
        routes_page.click_order_details_button()
        assert routes_page.are_order_details_shown(), "🐛 Trip details are not visible after clicking 'Details'"
        print("✅ Trip details are visible after clicking 'Details'")
