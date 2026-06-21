# Urban Routes Automated Testing

## Overview

End-to-end (E2E) QA automation suite for the Urban Routes taxi reservation flow.
The tests cover SMS verification, payment flows, extras selection, and the
reservation lifecycle to prevent regressions in critical user journeys.

## Goal

Provide reliable functional validation for Urban Routes by automating core
user scenarios from entering addresses to completing a taxi reservation.
This suite aims to reduce manual testing effort and increase confidence in
release-ready behavior.

## Motivation

Manual testing of the full reservation flow is slow and error-prone. The SMS
verification code is generated dynamically and must be extracted from browser
network logs at runtime. Multiple modals, dynamic states and form validations
require stable architecture and robust synchronization to keep tests reliable
and maintainable.

## Key Achievements

- Introduced a Page Object Model to separate selectors from test logic.
- Implemented extraction of SMS verification codes using Chrome performance
	logs for deterministic phone verification testing.
- Used explicit waits (`WebDriverWait`) for reliable synchronization with
	dynamic UI elements.
- Covered the complete E2E flow: addresses, vehicle type, tariff selection,
	phone verification, card payment, extras selection and order search modal.

## Skills Demonstrated

**Automation & QA**
- Test architecture using Page Object Model (POM)
- Robust synchronization with `WebDriverWait`
- Runtime inspection of network traffic to extract verification tokens
- End-to-end functional validation with Pytest

**Development & Analysis**
- Advanced Python for test automation
- Complex Selenium interactions (ActionChains, Keys)
- Chrome DevTools Protocol usage for network inspection
- Selector optimization (XPath/CSS)

## Tech Stack

Python 3.14+ | Selenium 4.x | Pytest | Chrome DevTools Protocol | XPath/CSS

## Project Layout

- `pages/urban_routes_page.py` — Page Object implementing UI selectors and
	actions for the Urban Routes app.
- `tests/test_urban_routes.py` — Test cases ported to Pytest using the POM.
- `data.py` — Test data (addresses, phone numbers, card numbers, etc.).

Covered scenarios include:
- Entering origin and destination addresses
- Mode and vehicle type selection
- Choosing `Comfort` tariff
- Phone number entry and SMS verification
- Adding and validating credit cards
- Driver message input and validation
- Selecting extras (blanket & tissues, ice cream)
- Reserving a taxi and validating the "searching for a car" modal
- Viewing trip details

The repo also includes a helper to retrieve the SMS code from browser network
logs, which allows automated verification without external SMS infrastructure.

## Test Execution

### Prerequisites

- Python 3.14+
- Activate a virtual environment (e.g. `.venv`)
- Install dependencies: `pip install -r requirements.txt`
- Chrome browser and a matching ChromeDriver binary
- Set `urban_routes_url` in `data.py` to point at the test instance of Urban Routes

### Run the full suite

```bash
pytest -q
```

### Run the Urban Routes tests only

```bash
pytest -q tests/test_urban_routes.py::TestUrbanRoutes
```

If you need me to run the tests here (requires ChromeDriver and local browser), tell me and I will execute them and report results.