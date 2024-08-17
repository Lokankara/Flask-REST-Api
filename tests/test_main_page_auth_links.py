from selene import browser
import allure
from pages.main_page import open_page, click_on_sign_in_link, click_on_create_account_link
from pages.create_account import should_be_create_account_url, registration_form_should_be_present
from pages.sign_in import should_be_sign_in_url, sign_in_form_should_be_present



@allure.feature('Main Page > Main Page')
@allure.title('The “Sign In” and “Create an Account” links are visible and clickable on the main page')
@allure.link('https://trello.com/c/GEQHU5fa')
def test_check_visible_clickable_auth_links():
    open_page()
    click_on_create_account_link()
    should_be_create_account_url()
    registration_form_should_be_present()
    browser.driver.back()
    click_on_sign_in_link()
    should_be_sign_in_url()
    sign_in_form_should_be_present()
