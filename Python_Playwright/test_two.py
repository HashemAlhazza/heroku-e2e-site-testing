import time, pytest, re
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page, expect, Dialog, Error, Response

def test_GeoLocation():
    with sync_playwright() as p:
        # Launch a Chromium browser instance (not headless for visibility)
        browser = p.chromium.launch(headless=False)
        
        # Create a new browser context with custom geolocation and permissions
        # This is necessary because geolocation and permissions are set per context,
        # not per page. The default (page) fixture does not allow setting these options.
        context = browser.new_context(
            geolocation={"latitude": 37.7749, "longitude": -122.4194},
            permissions=["geolocation"]
        )
        
        # Open a new page in the custom context
        page = context.new_page()
        # Navigate to the geolocation test page
        page.goto("https://the-internet.herokuapp.com/geolocation")
        # Click the "Where am I?" button to trigger geolocation
        page.get_by_role("button", name="Where am I?").click()
    
        # Retrieve and assert the latitude value displayed on the page
        latitude = page.locator("#lat-value").inner_text()
        assert latitude == "37.7749"
        # Retrieve and assert the longitude value displayed on the page
        longitude = page.locator("#long-value").inner_text()
        assert longitude == "-122.4194"
        
        # Close the browser
        browser.close()
        
def test_Horizontal_Slider(page: Page):
    page.goto("https://the-internet.herokuapp.com")
    page.get_by_role("link", name="Horizontal Slider").click()
    
    
    slider = page.get_by_role("slider")
    testlist = ["0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    # Directly set the slider value using fill
    for _ in testlist:
      slider.fill(_)
      value = page.locator("#range").inner_text()
      assert _ == value
      
    # Reset slider to 0 before keyboard interaction
    slider.fill("0")
    
    # Increase slider value by pressing the right arrow key 5 times      
    for _ in range(5):  # Press right arrow 5 times
        slider.press("ArrowRight")
    
    value = page.locator("#range").inner_text()
    assert value == "2.5"  # After 5 right presses from 0, value should be 2.5

    # Move slider to the left (decrease value)
    for _ in range(2):  # Press left arrow 2 times
        slider.press("ArrowLeft")
    
    value = page.locator("#range").inner_text()
    assert value == "1.5"
    
def test_hovers(page: Page):
    page.goto("https://the-internet.herokuapp.com")
    page.get_by_role("link", name="Hovers").click()
    
    figure = page.locator(".figure")
    for i in range(figure.count()):
      figure.nth(i).hover()
      assert figure.nth(i).get_by_role("heading").inner_text() == "name: user" + str(i+1)
    
def test_Infinite_Scroll(page: Page):
    page.goto("https://the-internet.herokuapp.com")
    page.get_by_role("link", name="Infinite Scroll").click()

    page.wait_for_timeout(1000) # this waiting is a MUST

    paragraphs = page.locator(".jscroll-added")
    count_before = paragraphs.count()
    
    for _ in range(3):
        page.mouse.wheel(0, 2000)
        page.wait_for_timeout(1000)
    
    count_after = paragraphs.count()

    # print(f"count before = {count_before}")
    # print(f"count after = {count_after}")

    assert count_after > count_before

def test_Inputs(page: Page):
    page.goto("https://the-internet.herokuapp.com")
    page.get_by_role("link", name="Inputs").click()
    
    input_box = page.locator("input[type='number']")
    
    input_box.fill("816")
    assert input_box.input_value() == "816"
    
    input_box.press("ArrowUp")
    assert input_box.input_value() == "817"
    
    input_box.press("ArrowDown")
    assert input_box.input_value() == "816"
    
    try:
        input_box.fill("abc")
    except Error as e:
        print("Input rejected as expected:", e)
    else:
        raise AssertionError("Input was accepted but should have failed")

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
        


def test_JavaScript_Alerts(page: Page):
    page.goto("https://the-internet.herokuapp.com")
    page.get_by_role("link", name="JavaScript Alerts").click()

    result_locator = page.locator("#result")
    jsprompt_test_text = "test123"

    # JS Alert
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Click for JS Alert").click()
    expect(result_locator).to_have_text("You successfully clicked an alert")

    # JS Confirm - accept
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Click for JS Confirm").click()
    expect(result_locator).to_have_text("You clicked: Ok")
    
    # JS Prompt - dismiss
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_role("button", name="Click for JS Prompt").click()
    expect(result_locator).to_have_text("You entered: null")

    # JS Prompt - enter text and accept
    page.once("dialog", lambda dialog: dialog.accept(jsprompt_test_text))
    page.get_by_role("button", name="Click for JS Prompt").click()
    expect(result_locator).to_have_text(f"You entered: {jsprompt_test_text}")

def test_javascript_onload_event_error(page: Page):
    error_messages = []

    # Listen for page-level JS exceptions - because the error happens when page is loading
    def handle_page_error(exc):
        print("Page error captured:", exc.message)
        error_messages.append(exc.message)

    page.on("pageerror", handle_page_error)

    page.goto("https://the-internet.herokuapp.com/javascript_error")
    
    page.wait_for_timeout(500)

    # This assertion checks if any of the error messages in the error_messages list contain the substring "reading 'xyz'".
    # The 'any' function returns True if at least one element in the iterable is True.
    # The iterable here is a generator expression: ("reading 'xyz'" in err for err in error_messages)
    # This generator goes through each 'err' in 'error_messages' and checks if "reading 'xyz'" is a substring of 'err'.
    # If at least one 'err' contains "reading 'xyz'", the assertion passes.
    # The for loop is written inside the generator expression, which is a compact way to loop and check a condition in one line.
    assert any("reading 'xyz'" in err for err in error_messages), \
            "Expected error not found bro."


def test_Key_Presses(page: Page):
    page.goto("https://the-internet.herokuapp.com")
    page.get_by_role("link", name="Key Presses").click()
    
    input_box = page.locator("#target")

    def assert_entered_Key(key: str):
        input_box.focus()
        input_box.press(key)
        expect(page.locator("#result")).to_have_text(f"You entered: {key.upper()}")

    for key in ["a", "z", "0", "1", "5", "F1", "F12"]:
        assert_entered_Key(key)

def test_Large_And_Deep_DOM(page: Page):
    page.goto("https://the-internet.herokuapp.com")
    page.get_by_role("link", name="Large & Deep DOM").click()
    
    last_div = page.locator("#sibling-50\\.3")
    expect(last_div).to_have_text("50.3")
    
    last_cell = page.locator("tr.row-50 > td.column-50")
    expect(last_cell).to_have_text("50.50")
    
    last_cell.scroll_into_view_if_needed()
    
    assert page.locator("tbody > tr").count() == 50 # No.Rows
    assert page.locator("tr.row-1 > td").count() == 50 # No.Columns   

def test_Multiple_Windows(page: Page):
    page.goto("https://the-internet.herokuapp.com")
    page.get_by_role("link", name="Multiple Windows").click()
    
    with page.expect_popup() as p:
        page.get_by_role("link", name="Click Here").click()

    newWindow = p.value

    heading = newWindow.get_by_role("heading").inner_text()
    assert heading == "New Window"

def test_nested_frames(page: Page):
    page.goto("https://the-internet.herokuapp.com/nested_frames")

    middle_frame = page.frame(name="frame-middle")
    assert middle_frame is not None
    middle_text = middle_frame.locator("#content").inner_text()
    assert middle_text.strip() == "MIDDLE"
    
    left_frame = page.frame(name="frame-left")
    assert left_frame is not None
    left_text = left_frame.locator("body").inner_text()
    assert left_text.strip() == "LEFT"
    
    right_frame = page.frame(name="frame-right")
    assert right_frame is not None
    right_text = right_frame.locator("body").inner_text()
    assert right_text.strip() == "RIGHT"
    
    bottom_frame = page.frame(name="frame-bottom")
    assert bottom_frame is not None
    bottom_text = bottom_frame.locator("body").inner_text()
    assert bottom_text.strip() == "BOTTOM"
    
def test_Notification_Messages(page: Page):    
    page.goto("https://the-internet.herokuapp.com")
    page.get_by_role("link", name="Notification Messages").click()
    
    click_button = page.get_by_role("link", name="Click here")
    notification_msg = page.locator("#flash").inner_text()
    
    assert (
        "Action successful" in notification_msg
        or "Action unsuccesful, please try again" in notification_msg
    )

def test_Redirect_Link_M1(page: Page):
    page.goto("https://the-internet.herokuapp.com")
    page.get_by_role("link", name="Redirect Link").click()
    page.get_by_role("link", name="here").click()
    page.wait_for_timeout(500)
    
    def check_status_code(page: Page, code: str):
        page.goto("https://the-internet.herokuapp.com/status_codes")
        status_code = page.get_by_role("link", name=code).click()
        msg = page.locator("p").inner_text()
        assert code in msg
        
    for code in ["200", "301", "404", "500"]:
        check_status_code(page, code)


def test_Redirect_Link_M2(page: Page):
    status_codes = ["200", "301", "404", "500"]

    def check_status_code(page: Page, code: str):
        responses = []
        def handle_response(response):
            if f"/status_codes/{code}" in response.url:
                responses.append(response)
        
        page.on("response", handle_response)
        page.goto("https://the-internet.herokuapp.com/status_codes")
        page.get_by_role("link", name=code).click()
        page.wait_for_timeout(500)
        
        assert responses[0].status == int(code)
        
    for code in status_codes:
        check_status_code(page, code)

def test_secure_file_download(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        http_credentials={"username": "admin", "password": "admin"}
    )
    
    page = context.new_page()
    page.goto("https://the-internet.herokuapp.com")
    page.get_by_role("link", name="Secure File Download").click()
    
    assert page.url == "https://the-internet.herokuapp.com/download_secure"
    # I already tested the downloading of the files properly on system

def test_Shadow_DOM(page: Page):
    page.goto("https://the-internet.herokuapp.com")
    page.get_by_role("link", name="Shadow DOM").click()
    
    # I located these elements using standard locators, which may not be fully reliable if the DOM structure changes.
    # However, the main goal of this test is to demonstrate accessing text inside a Shadow DOM.
    # Playwright makes this straightforward, as it can pierce shadow roots and locate elements inside Shadow DOM
    # just like regular DOM elements.
    
    shadow_text1 = page.locator("my-paragraph").locator("span").inner_text()
    shadow_text2 = page.locator("ul > li:nth-child(1)").inner_text()
    shadow_text3 = page.locator("ul > li:nth-child(2)").inner_text()
    
    assert shadow_text1 == "Let's have some different text!"
    assert shadow_text2 == "Let's have some different text!"
    assert shadow_text3 == "In a list!"

def test_Shifting_Content(page: Page):
    page.goto("https://the-internet.herokuapp.com")
    page.get_by_role("link", name="Shifting Content").click()
    
    page.get_by_role("link", name="Example 1: Menu Element").click()
    
    # Example 1 - Test if the number of items after shifting one of them:
    shift_links = page.get_by_role("link", name="click here")
    shift_links.nth(1).click()
    page.wait_for_timeout(500)
    menue_items = page.locator("ul li a")
    count = menue_items.count()
    assert 4 <= count <= 5
    
    # Example 2  - Test image shifting:
    page.goto("https://the-internet.herokuapp.com/shifting_content/image")
    img = page.locator(".shift")
    assert img.is_visible()
    
    # We use the bounding_box() method to capture the position and size of the image element.
    # The bounding box returns a dictionary with the image's x, y, width, and height (e.g., {'x': 100, 'y': 200, 'width': 100, 'height': 500}).
    # By comparing the width and height before and after reloading, we ensure the image's size remains consistent,
    # even if its position may shift due to the shifting content feature.

    original_box = img.bounding_box()
    
    for _ in range(5):
        page.reload()
        page.wait_for_timeout(250)
        new_box = img.bounding_box()
        assert (new_box is not None and original_box is not None)
        assert new_box["width"] == original_box["width"]
        assert new_box["height"] == original_box["height"]
        assert new_box["x"] == original_box["x"] or new_box["y"] == original_box["y"]
    
    # Go to Example 3: Shifting List of Sentences
    page.goto("https://the-internet.herokuapp.com")
    page.get_by_role("link", name="Shifting Content").click()
    page.get_by_role("link", name="Example 3: List").click()
    
    container = page.locator(".large-6.columns.large-centered")
    
    # This line creates a new list, text_before, that contains only the non-empty 
    # strings from the original text_before list.
    # The expression [t for t in text_before if t.strip()] is called a list comprehension.
    # It loops through each string t in text_before, and includes t in the new list only 
    # if t.strip() is not empty (i.e., the string is not just whitespace).
    text_before = container.inner_text().strip().split("\n")
    text_before = [t for t in text_before if t.strip()]
    
    page.reload()
    
    text_after = container.inner_text().strip().split("\n")
    text_after = [t for t in text_after if t.strip()]
    assert text_before != text_after 
    
# def test_slow_resource_detection(page: Page):
#     slow_request_found = False
#     slow_response_time = 0
    
#     def handle_response(response):
#         nonlocal slow_request_found, slow_response_time
#         if "/slow_external" in response.url:
#             slow_request_found = True
                
#     page.on("response", handle_response)
#     page.goto("https://the-internet.herokuapp.com/slow")
    
#     page.wait_for_timeout(35000)
    
#     assert slow_request_found

def test_Sortable_Data_Tables(page: Page):
    page.goto("https://the-internet.herokuapp.com")
    page.get_by_role("link", name="Sortable Data Tables").click()
    
    page.locator("#table1").get_by_text("Due").click()

    # Now we see if the prices are really sorted
    
    due_cells = page.locator("#table1 tbody tr td:nth-child(4)").all_inner_texts()
    
    due_values = []
    
    for value in due_cells:
        cleaned = value.replace("$", "") # removing the $ sign so we can comapre properly
        number = float(cleaned)
        due_values.append(number)
    
    # print("Due values before sorting:", due_values)
    sorted_due_values = sorted(due_values)
    # print("Due values after sorting:", sorted_due_values)
    
    assert due_values == sorted_due_values

def test_table1_sort_by_last_name(page: Page):
    page.goto("https://the-internet.herokuapp.com/tables")
    page.locator("#table1").get_by_text("Last Name").click()
    last_names = page.locator("#table1 tbody tr td:nth-child(1)").all_inner_texts()
    assert last_names == sorted(last_names)

def test_table1_sort_by_first_name(page: Page):
    page.goto("https://the-internet.herokuapp.com/tables")
    page.locator("#table1").get_by_text("First Name").click()
    first_names = page.locator("#table1 tbody tr td:nth-child(2)").all_inner_texts()
    assert first_names == sorted(first_names)

def test_table1_email_format(page: Page):
    page.goto("https://the-internet.herokuapp.com/tables")
    emails = page.locator("#table1 tbody tr td:nth-child(3)").all_inner_texts()
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    for email in emails:
        assert re.match(pattern, email), f"Invalid email format: {email}"
    
    
def test_table1_website_format(page: Page):
    page.goto("https://the-internet.herokuapp.com/tables")
    websites = page.locator("#table1 tbody tr td:nth-child(5)").all_inner_texts()
    pattern = r"^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)$"
    for website in websites:
        assert re.match(pattern, website), f"Invalid website format: {website}" 
    
def test_typos(page: Page):
    page.goto("https://the-internet.herokuapp.com/typos")
    paragraphs = page.locator("div.example > p").nth(1).inner_text().strip()
    orig = "Sometimes you'll see a typo, other times you won't."
    typo = "Sometimes you'll see a typo, other times you won,t."

    assert paragraphs in [orig, typo]