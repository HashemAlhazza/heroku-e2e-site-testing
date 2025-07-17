import time, pytest, re
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page, expect, Dialog, Error, Response

from pytest_bdd import scenarios, given, when, then, parsers

scenarios('Features_Ghenkins/herokuapp.feature')

# Context holders
browser_context = {}
location_result = {}

@given('the browser is launched with geolocation set to latitude 37.7749 and longitude -122.4194')
def launch_browser_with_geolocation():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        geolocation={"latitude": 37.7749, "longitude": -122.4194},
        permissions=["geolocation"]
    )
    page = context.new_page()
    browser_context['playwright'] = playwright
    browser_context['browser'] = browser
    browser_context['context'] = context
    browser_context['page'] = page

@when('the user navigates to "https://the-internet.herokuapp.com/geolocation"')
def navigate_to_page():
    page: Page = browser_context['page']
    page.goto("https://the-internet.herokuapp.com/geolocation")

@when('the user clicks the "Where am I?" button')
def click_location_button():
    page: Page = browser_context['page']
    page.get_by_role("button", name="Where am I?").click()

@then('the latitude displayed should be "37.7749"')
def check_latitude():
    page: Page = browser_context['page']
    latitude = page.locator("#lat-value").inner_text()
    location_result['lat'] = latitude
    assert latitude == "37.7749"

@then('the longitude displayed should be "-122.4194"')
def check_longitude():
    page: Page = browser_context['page']
    longitude = page.locator("#long-value").inner_text()
    location_result['lon'] = longitude
    assert longitude == "-122.4194"
    
    # Close browser at end
    browser_context['browser'].close()
    browser_context['playwright'].stop()

        
@given("I am on the Horizontal Slider page")
def open_slider_page(page: Page):
    page.goto("https://the-internet.herokuapp.com")
    page.get_by_role("link", name="Horizontal Slider").click()

@when("I set the slider to specific values")
def set_slider_directly(page: Page):
    slider = page.get_by_role("slider")
    testlist = ["0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    for value in testlist:
        slider.fill(value)
        assert value == page.locator("#range").inner_text()
    slider.fill("0")

@when("I press the right arrow 5 times")
def press_right_arrow(page: Page):
    slider = page.get_by_role("slider")
    for _ in range(5):
        slider.press("ArrowRight")

@when("I press the left arrow 2 times")
def press_left_arrow(page: Page):
    slider = page.get_by_role("slider")
    for _ in range(2):
        slider.press("ArrowLeft")

@then("I should see the correct slider value")
def check_slider_result(page: Page):
    value = page.locator("#range").inner_text()
    assert value == "1.5"
    
@given("I am on the Hovers page")    
def navigate_to_Hovers_Page(page: Page):
    page.goto("https://the-internet.herokuapp.com")
    page.get_by_role("link", name="Hovers").click()
    
@then("I should see user names")    
def verify_user_names(page: Page):
    figure = page.locator(".figure")
    for i in range(figure.count()):
      figure.nth(i).hover()
      assert figure.nth(i).get_by_role("heading").inner_text() == "name: user" + str(i+1)
      
@given("I am on the Infinite Scroll page")
def open_scroll(page: Page):
    page.goto("https://the-internet.herokuapp.com")
    page.get_by_role("link", name="Infinite Scroll").click()
    page.wait_for_timeout(1000)

@when("I scroll down multiple times")
def scroll_down(page: Page):
    for _ in range(3):
        page.mouse.wheel(0, 2000)
        page.wait_for_timeout(1000)

@then("I should see more paragraphs loaded")
def check_more_loaded(page: Page):
    paragraphs = page.locator(".jscroll-added")
    assert paragraphs.count() > 0

@when(parsers.parse('I enter "{value}", press "{key1}", then press "{key2}"'))
def combined_input_actions(page: Page, value: str, key1: str, key2: str):
    input_box = page.locator("input[type='number']")
    input_box.fill(value)
    input_box.press(key1)
    input_box.press(key2)

@then(parsers.parse('the final value should be "{expected}"'))
def check_final_value(page: Page, expected: str):
    input_box = page.locator("input[type='number']")
    assert input_box.input_value() == expected

    


def test_JQuery_UI_Menus(page: Page):
    page.goto("https://the-internet.herokuapp.com")
    page.get_by_role("link", name="JQuery UI Menus").click()
    
    page.get_by_text("Enabled").hover()
    page.wait_for_timeout(500)
    
    downloads_menue = page.get_by_role("link", name="Downloads")
    back_to_jQuery_menue = page.get_by_role("link", name="Back to JQuery UI")
    
    expect(downloads_menue).to_be_visible()
    expect(back_to_jQuery_menue).to_be_visible()
    
    ui_items = page.locator("ul.ui-menu li.ui-menu-item >> visible=true")
    
    for i in range(ui_items.count()):
        item = ui_items.nth(i)
        assert item.is_visible()
        


# Add to your step definitions file

@given("I am on the JavaScript Alerts page")
def open_js_alerts_page(page: Page):
    page.goto("https://the-internet.herokuapp.com")
    page.get_by_role("link", name="JavaScript Alerts").click()

@when("I accept the JS Alert")
def accept_js_alert(page: Page):
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Click for JS Alert").click()

@then('I should see "You successfully clicked an alert"')
def check_js_alert_result(page: Page):
    expect(page.locator("#result")).to_have_text("You successfully clicked an alert")

@when("I accept the JS Confirm dialog")
def accept_js_confirm(page: Page):
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Click for JS Confirm").click()

@then('I should see "You clicked: Ok"')
def check_js_confirm_result(page: Page):
    expect(page.locator("#result")).to_have_text("You clicked: Ok")

@when("I dismiss the JS Prompt dialog")
def dismiss_js_prompt(page: Page):
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_role("button", name="Click for JS Prompt").click()

@then('I should see "You entered: null"')
def check_js_prompt_dismissed(page: Page):
    expect(page.locator("#result")).to_have_text("You entered: null")

@when(parsers.parse('I enter "{text}" in the JS Prompt and accept'))
def enter_text_js_prompt(page: Page, text: str):
    page.once("dialog", lambda dialog: dialog.accept(text))
    page.get_by_role("button", name="Click for JS Prompt").click()

@then(parsers.parse('I should see "You entered: {text}"'))
def check_js_prompt_accepted(page: Page, text: str):
    expect(page.locator("#result")).to_have_text(f"You entered: {text}")