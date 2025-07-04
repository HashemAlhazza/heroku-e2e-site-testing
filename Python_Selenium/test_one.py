import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from selenium.webdriver import ActionChains # used for drag-drop functionality
from selenium.webdriver.support.ui import Select # used for the select from droplist
# all of the below is for the webdriver explicit wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By




# This fixture starts the browser only once per test session
@pytest.fixture(scope="session")
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://the-internet.herokuapp.com/")
    yield driver
    driver.quit()


def reset_site(driver):
    driver.get("https://the-internet.herokuapp.com/")

# def test_Add_Remove_Element(driver):
    
#     MainPageButton = driver.find_element(By.CSS_SELECTOR, 'a[href = "/add_remove_elements/"]')
#     MainPageButton.click()

#     AddButton = driver.find_element(By.XPATH, '//button[text() = "Add Element"]')
#     AddButton.click()

#     DeleteButton = driver.find_element(By.XPATH, '//button[text() = "Delete"]')
#     assert DeleteButton.is_displayed()
#     DeleteButton.click()

# def test_Add_Remove_MultiElements(driver):
#     reset_site(driver) # to go to the Main Page
    
#     MainPageButton = driver.find_element(By.CSS_SELECTOR, 'a[href = "/add_remove_elements/"]')
#     MainPageButton.click()

#     AddButton = driver.find_element(By.XPATH, '//button[text() = "Add Element"]')
#     for _ in range(6):
#         AddButton.click()

#     DeleteButtons = driver.find_elements(By.XPATH, '//button[text() = "Delete"]')
#     for Dbutton in DeleteButtons:
#         assert Dbutton.is_displayed()
#         Dbutton.click()

# def test_Basic_Auth(driver):
#     reset_site(driver)
    
#     # bypass the popup by embedding the username and password into the URL itself:
#     driver.get("https://admin:admin@the-internet.herokuapp.com/basic_auth")
    
#     message = driver.find_element(By.CSS_SELECTOR, '.example h3') # .className tagName
    
#     assert "Basic Auth" in message.text

# def test_broken_images(driver):
#     reset_site(driver)  

#     MainPageButton = driver.find_element(By.CSS_SELECTOR, 'a[href = "/broken_images"]')
#     MainPageButton.click()

#     images = driver.find_elements(By.TAG_NAME, "img")
#     broken_images = []

#     for img in images:
#         is_loaded = driver.execute_script(
#             "return arguments[0].complete && arguments[0].naturalWidth > 0;", img)

#         if is_loaded == False:
#             print(f"Image is broken, src = {img.get_attribute('src')}")
#             broken_images.append(img.get_attribute("src"))  # log broken images
#         else:
#             print("Image is normally loaded.")

#     assert len(broken_images) == 0, f"{len(broken_images)} broken image(s) found."


# def test_Challenging_DOM_3Buttons(driver):
    
#     reset_site(driver)
#     MainPageButton = driver.find_element(By.CSS_SELECTOR, 'a[href = "/challenging_dom"]')
#     MainPageButton.click()
    
#     # BlueButton = driver.find_element(By.CSS_SELECTOR, ".button")
#     # RedButton = driver.find_element(By.CSS_SELECTOR, ".button.alert")
#     # GreenButton = driver.find_element(By.CSS_SELECTOR, ".button.success")
#     time.sleep(1)
#     RandomTableWord = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(8) > td:nth-child(5)')
#      # In CSS, a space ( ) means: any descendant at any level
#      # The > means: a direct/immediate child only
     
#     assert RandomTableWord.text.strip() != ""
        
# def test_Checkboxes(driver):
#     reset_site(driver)
    
#     MainPageButton = driver.find_element(By.CSS_SELECTOR, '.large-12.columns > ul > li:nth-child(6) > a')
#     MainPageButton.click()
    
#     notChecked = []
    
#     CheckBoxes = driver.find_elements(By.CSS_SELECTOR, 'form#checkboxes input[type="checkbox"]')
    
#     for i in CheckBoxes:
#         if not i.is_selected():
#             notChecked.append(i)

#     for chkbx in notChecked:
#         chkbx.click()
#         driver.save_screenshot("hhhhhh.png")
#         assert chkbx.is_selected()
        
# def test_Disappearing_Elements(driver):
#     reset_site(driver)
#     MainPageButton = driver.find_element(By.CSS_SELECTOR, 'a[href = "/disappearing_elements"]')
#     MainPageButton.click()
    
#     found = False
#     for _ in range(10):
#      AllElements = driver.find_elements(By.CSS_SELECTOR, 'ul li a')
#      for element in AllElements:
#          if element.text.strip().lower() == "gallery":
#              found = True
#              break

#      if found:
#         break
#      else:
#         driver.refresh() 
#     assert found == True, 'Element not found.'




"""
Can't Implement drag-drop using this method because selenium does not support
HTML-5 and Seleniums drag_and_drop() is known to fail silently on HTML5 implementations in Chrome.
""" 
# def test_Drag_and_Drop(driver):
#     reset_site(driver)
    
#     MainPageButton = driver.find_element(By.CSS_SELECTOR, 'a[href = "/drag_and_drop"]')
#     MainPageButton.click()
    
#     source = driver.find_element(By.ID, "column-b")
#     target = driver.find_element(By.ID, "column-a")
    
#     actions = ActionChains(driver)
#     actions.drag_and_drop(source, target).perform()
    
#     targetChange = driver.find_element(By.CSS_SELECTOR, 'div#column-a > header')
#     assert targetChange.text != 'A'


# def test_Dropdown_List(driver):
#     reset_site(driver)
    
#     MainPageButton = driver.find_element(By.CSS_SELECTOR, 'a[href = "/dropdown"]')
#     MainPageButton.click()
    
#     select = Select(driver.find_element(By.TAG_NAME, "select")) #built in funciton
#     select.select_by_index(1) # zero-based index, selection option 1
    
#     option1 = driver.find_element(By.CSS_SELECTOR, 'select > option:nth-child(2)')
#     is_selected = option1.get_attribute("selected")

#     assert is_selected == "true" or is_selected == "selected"
    
# def test_Dynamic_Content_text(driver):
#     reset_site(driver)
    
#     MainPageButton = driver.find_element(By.CSS_SELECTOR, 'a[href = "/dynamic_content"]')
#     MainPageButton.click()
    
#     all_text_initial = []
#     all_text_changed = []
    
#     initial_text = driver.find_elements(By.CLASS_NAME, 'large-10.columns')

#     for init in initial_text[1:]:
#         all_text_initial.append(init.text.strip())
            
#     # all_text_initial.pop(0)
    
#     driver.refresh()
    
#     changed_text = driver.find_elements(By.CLASS_NAME, 'large-10.columns')
    
#     for chngd in changed_text[1:]:
#         all_text_changed.append(chngd.text.strip())
        
#     # all_text_changed.pop(0)
    
#     found_difference = False
    
#     for before, after in zip(all_text_initial, all_text_changed):
#         if before != after:
#             found_difference = True
#             break

#     assert found_difference

# def test_Dynamic_Content_imgs(driver):
#     reset_site(driver)
    
#     MainPageButton = driver.find_element(By.CSS_SELECTOR, 'a[href = "/dynamic_content"]')
#     MainPageButton.click()
    
#     all_imgs_initial = []
#     all_imgs_changed = []
    
#     initial_imgs = driver.find_elements(By.CSS_SELECTOR, '.large-2.columns > img')
    
#     for img in initial_imgs:
#         all_imgs_initial.append(img.get_attribute('src'))
        
#     driver.refresh()
    
#     changed_imgs = driver.find_elements(By.CSS_SELECTOR, '.large-2.columns > img')
    
#     for img in changed_imgs:
#         all_imgs_changed.append(img.get_attribute('src'))  
          
#     found_difference = False
    
#     for before, after in zip(all_imgs_initial, all_imgs_changed):
#         if before != after:
#            found_difference = True
#            break
 
#     assert found_difference, "No image src changed after refresh — images may not be dynamic."
    
# def test_Dynamic_Controls1(driver):
#     reset_site(driver)
    
#     MainPageButton = driver.find_element(By.CSS_SELECTOR, 'a[href = "/dynamic_controls"]')
#     MainPageButton.click()
    
#     RemoveButton = driver.find_element(By.CSS_SELECTOR, 'form#checkbox-example button')
#     RemoveButton.click()
    
#     # Wait up to 10 seconds until the element is visible
#     textMessage1 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'message')))
#     assert textMessage1.is_displayed()
    
#     AddButton = driver.find_element(By.CSS_SELECTOR, 'form#checkbox-example button')
#     AddButton.click()
    
#     textMessage2 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'message')))
#     assert textMessage2.is_displayed()
    
# def test_Dynamic_Controls2(driver):
    
#     EnableButton = driver.find_element(By.CSS_SELECTOR, 'form#input-example button')
#     EnableButton.click()
    
#     # Wait up to 10 seconds until the element is visible
#     textMessage1 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'form#input-example p')))
#     assert textMessage1.is_displayed()
    
#     DisableButton = driver.find_element(By.CSS_SELECTOR, 'form#input-example button')
#     DisableButton.click()
    
#     textMessage2 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'form#input-example p')))
#     assert textMessage2.is_displayed()
    
    
# def test_Dynamic_Loading1(driver):
#     reset_site(driver)
    
#     MainPageButton = driver.find_element(By.CSS_SELECTOR, 'a[href = "/dynamic_loading"]')
#     MainPageButton.click()
    
#     Example1_Button = driver.find_element(By.CSS_SELECTOR, 'a[href = "/dynamic_loading/1"]')
#     Example1_Button.click()
    
#     StartButton = driver.find_element(By.CSS_SELECTOR, 'div#start button')
#     StartButton.click()
    
#     ElementToWait = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#finish h4')))
#     assert ElementToWait.text.strip() == "Hello World!"


# def test_Dynamic_Loading2(driver):
#     reset_site(driver)
    
#     MainPageButton = driver.find_element(By.CSS_SELECTOR, 'a[href = "/dynamic_loading"]')
#     MainPageButton.click()
    
#     Example2_Button = driver.find_element(By.CSS_SELECTOR, 'a[href = "/dynamic_loading/2"]')
#     Example2_Button.click()
    
#     StartButton = driver.find_element(By.CSS_SELECTOR, 'div#start button')
#     StartButton.click()
    
#     ElementToWait = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#finish h4')))
#     assert ElementToWait.text.strip() == "Hello World!"
    
# def test_Entry_Ad(driver):
#     reset_site(driver)

#     MainPageButton = driver.find_element(By.CSS_SELECTOR, 'a[href = "/entry_ad"]')
#     MainPageButton.click()
#     time.sleep(3)
    
#     modal = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "modal"))
#     )

#     if modal.get_attribute('style') == 'display: none;':
#         driver.find_element(By.ID, 'restart-ad').click()
#         driver.get("https://the-internet.herokuapp.com/entry_ad")
#         modal = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, "modal"))
#         )

#     assert modal.get_attribute('style') == 'display: block;'

# This kind of test (Below) is not supported using Selenium

# def test_Exit_Intent(driver): 
#     reset_site(driver)
#     driver.maximize_window()
#     MainPageButton = driver.find_element(By.CSS_SELECTOR, 'a[href = "/exit_intent"]')
#     MainPageButton.click()
#     time.sleep(1)
#     # Move to the center of the page first
#     ActionChains(driver).move_by_offset(100, 100).perform()
#     # Move out of the viewport (simulate exit intent)
#     ActionChains(driver).move_by_offset(0, -50).perform()
#     time.sleep(1)
#     driver.save_screenshot('test1.png')

# def test_File_Download(driver):
#     reset_site(driver)
    
#     MainPageButton = driver.find_element(By.CSS_SELECTOR, 'a[href = "/download"]')
#     MainPageButton.click()    
    
#     FileNames = []
#     Download_Dir = r"C:/Users/Hashe/Downloads"
    
#     FilesLink = driver.find_elements(By.CSS_SELECTOR, '.example a')
    
#     for file in FilesLink[6:10]:
#         file.click()
#         time.sleep(2)
#         FileNames.append(os.path.join(Download_Dir, file.text.strip()))
#         time.sleep(2)
            
#     for FullFilePath in FileNames:
#         assert os.path.exists(FullFilePath), "Boom, File not found bro."    

# def test_File_Upload(driver):
#     reset_site(driver)
    
#     MainPageButton = driver.find_element(By.CSS_SELECTOR, 'a[href = "/upload"]')
#     MainPageButton.click()
    
#     UploadInput = driver.find_element(By.CSS_SELECTOR, "input#file-upload")
#     UploadInput.send_keys(r"C:\Users\Hashe\Downloads\UploadTest.txt")
    
#     driver.find_element(By.ID, "file-submit").click()
#     time.sleep(0.5)
#     UploadMessage = driver.find_element(By.ID, "uploaded-files")
    
#     assert UploadMessage.text == "UploadTest.txt", 'Nope, not the same file buddy.'

# def test_Floating_Menue(driver):
#     reset_site(driver)
    
#     MainPageButton = driver.find_element(By.CSS_SELECTOR, 'a[href = "/floating_menu"]')
#     MainPageButton.click()
    
#     ContextMenu_before = driver.find_elements(By.CSS_SELECTOR, "div#menu > ul > li")
    
#     Action = ActionChains(driver)
#     Action.scroll_by_amount(0, 500).perform() #Scroll on the y-axis down by 500 pixels
#     time.sleep(1)
    
#     ContextMenu_after = driver.find_elements(By.CSS_SELECTOR, "div#menu > ul > li")
#     for before, after in zip(ContextMenu_before, ContextMenu_after):
#         assert before.text.strip() == after.text.strip()
#         assert after.is_displayed()

# def test_Forgot_Password(driver): # Failing - problem from website
#     reset_site(driver)
    
#     MainPageButton = driver.find_element(By.CSS_SELECTOR, 'a[href = "/forgot_password"]').click()   
    
#     EmailField = driver.find_element(By.CSS_SELECTOR, "input#email")
#     EmailField.send_keys("hashem.alhazza@gmail.com")
    
#     driver.find_element(By.CSS_SELECTOR, "button#form_submit").click()
#     message = driver.find_element(By.CSS_SELECTOR, "h1")
#     assert message.text == "Your e-mail's been sent!"

# def test_Form_Authentication(driver):
#     reset_site(driver)
#     MainPageButton = driver.find_element(By.CSS_SELECTOR, 'a[href = "/login"]').click()
    
#     UsernameField = driver.find_element(By.CSS_SELECTOR, 'input[name="username"]')
#     PasswordField = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
#     UsernameField.send_keys("tomsmith")
#     PasswordField.send_keys("SuperSecretPassword!")
#     Login = driver.find_element(By.CLASS_NAME, 'radius').click()
#     time.sleep(0.7)
    
#     Entry_Message = driver.find_element(By.CSS_SELECTOR, 'h2')
#     assert Entry_Message.text.strip() == "Secure Area"   
    
def test_Frames(driver):
    reset_site(driver)
    driver.find_element(By.CSS_SELECTOR, 'a[href="/frames"]').click()
    driver.find_element(By.CSS_SELECTOR, 'a[href="/nested_frames"]').click()

    def Check_Frame_Text(FramePath, ExpectedText, selector="body"):
        driver.switch_to.default_content()
        for frame in FramePath:
            driver.switch_to.frame(frame)
        element = driver.find_element(By.CSS_SELECTOR, selector)
        assert element.text.strip() == ExpectedText

    Check_Frame_Text(["frame-top", "frame-left"], "LEFT")
    Check_Frame_Text(["frame-top", "frame-middle"], "MIDDLE", selector="body div")
    Check_Frame_Text(["frame-top", "frame-right"], "RIGHT")
    Check_Frame_Text(["frame-bottom"], "BOTTOM")