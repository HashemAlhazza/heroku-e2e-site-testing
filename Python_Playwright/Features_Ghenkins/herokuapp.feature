Feature: Internet Herokuapp test suite

    Scenario: User allows geolocation and sees correct coordinates
        Given the browser is launched with geolocation set to latitude 37.7749 and longitude -122.4194
        When the user navigates to "https://the-internet.herokuapp.com/geolocation"
        And the user clicks the "Where am I?" button
        Then the latitude displayed should be "37.7749"
        And the longitude displayed should be "-122.4194"

    Scenario: User adjusts the slider and verifies values
        Given I am on the Horizontal Slider page
        When I set the slider to specific values
        And I press the right arrow 5 times
        And I press the left arrow 2 times
        Then I should see the correct slider value

    Scenario: User Hovers over images and check their details
        Given I am on the Hovers page
        Then  I should see user names

    Scenario: User Infinite Scrolling
        Given I am on the Infinite Scroll page
        When I scroll for a certain ammount
        Then I should see more paraphraphs loading

    Scenario: Enter and validate input behavior
        Given I am on the Inputs page
        When I enter "816", press "ArrowUp", then press "ArrowDown"
        Then the final value should be

    Scenario: User interacts with JavaScript alerts and verifies results
        Given I am on the JavaScript Alerts page
        When I accept the JS Alert
        Then I should see "You successfully clicked an alert"
        When I accept the JS Confirm dialog
        Then I should see "You clicked: Ok"
        When I dismiss the JS Prompt dialog
        Then I should see "You entered: null"
        When I enter "test123" in the JS Prompt and accept
        Then I should see "You entered: test123"