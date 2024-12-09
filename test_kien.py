from pickle import FALSE
from platform import system

import pytest
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import re
from datetime import datetime, timedelta


#Driver
@pytest.fixture
def driver():
    #Chrome driver
    driver = webdriver.Chrome()
    #Edge driver
    #driver = webdriver.Edge()
    driver.maximize_window()
    yield driver
    driver.quit()

#######################
#Hàm login bằng tài khoản admin
def login_admin_user(driver):
    driver.get("http://localhost/mongodb/login.php")
    driver.find_element(By.NAME, "email").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("123")
    button = driver.find_element(By.CLASS_NAME, "submit-btn")
    button.click()
    time.sleep(2)
    # Lấy đường dẫn hiện tai
    current_url = driver.current_url
    print(current_url)
    #return current_url

# Hàm login bằng tài khoản thông thường
def login_normal_user(driver):
    driver.get("http://localhost/mongodb/login.php")
    driver.find_element(By.NAME, "email").send_keys("normal_user")
    driver.find_element(By.NAME, "password").send_keys("123")
    button = driver.find_element(By.CLASS_NAME, "submit-btn")
    button.click()
    time.sleep(2)
    # Lấy đường dẫn hiện tai
    current_url = driver.current_url
    print(current_url)
    #return current_url

#Hàm login bằng tài khoản tuỳ chọn
def login_custom_user(driver, email, password):
    driver.get("http://localhost/mongodb/login.php")
    #test365
    #123
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    button = driver.find_element(By.CLASS_NAME, "submit-btn")
    button.click()
    time.sleep(2)
    # Lấy đường dẫn hiện tai
    current_url = driver.current_url
    print(current_url)

#####check in ###########
#TC_CI_01: Kiểm tra check-in với người dùng hợp lệ. (user không có sách trễ hạn trả)
#passed in 13.84s
def test_check_in_valid(driver):
    #Đăng nhập bằng tài khoản quyền admin
    check = False
    login_admin_user(driver)
    #Vào trang check-in
    driver.get("http://localhost/mongodb/checkin.php")
    time.sleep(2)
    user_id= "6733fea18d2e4709b8008084"
    #Nhập mã user vào ô tìm kiếm và nhấn nút tím kiếm
    driver.find_element(By.NAME, "userid").send_keys(user_id)
    driver.find_element(By.NAME, "search-checkin").click()
    check_in_btn = driver.find_element(By.NAME, "btn_checkin")
    #Nếu không tìm thấy nút check-in cho user sau khi tìm kiếm
    if check_in_btn is None:
        assert check, "Không thể tìm thấy nút check-in"
    check_in_btn.click()
    # Tìm thông báo check-in trong thẻ body
    body = driver.find_element(By.TAG_NAME, 'body')
    body_text = body.text
    # Kiểm tra xem thông báo cần tìm có trong body không
    search_text = user_id+" đã check in!"
    #Nếu thông báo có tồn tại, gán biến check= True
    if search_text in body_text:
        check = True
    assert check, "Không tìm thấy thông báo check-in thành công"

#TC_CI_02: Kiểm tra check-in với người dùng không hợp lệ.
#passed in 15.20s
def test_check_in_invalid(driver):
    # Đăng nhập bằng tài khoản quyền admin
    check = False
    login_admin_user(driver)
    # Vào trang check-in
    driver.get("http://localhost/mongodb/checkin.php")
    time.sleep(2)
    user_id = "invalid id"
    # Nhập mã user vào ô tìm kiếm và nhấn nút tím kiếm
    driver.find_element(By.NAME, "userid").send_keys(user_id)
    driver.find_element(By.NAME, "search-checkin").click()
    time.sleep(2)
    #Tìm thẻ chứa thông báo
    div_element = driver.find_element(By.CLASS_NAME, 'info-order')
    # Tìm thẻ thông báo nằm trong thẻ p trong thẻ div trên
    p_element = div_element.find_element(By.TAG_NAME, 'p')
    #Lấy thông báo
    message = p_element.text
    system_message = "Không Tìm Thấy User!"
    if message == system_message:
        check = True
    assert check, "Không tìm thấy thông báo"

#TC_CI_03: Kiểm tra check-in với người dùng hợp lệ đang trễ hạn trả.
#passed in 13.34s
def test_check_in_valid_with_user_borrowed_book(driver):
    check = False
    login_admin_user(driver)
    # Vào trang check-in
    driver.get("http://localhost/mongodb/checkin.php")
    time.sleep(2)
    user_id = "657fa789ad0bb52317042d6e"
    # Nhập mã user vào ô tìm kiếm và nhấn nút tím kiếm
    driver.find_element(By.NAME, "userid").send_keys(user_id)
    driver.find_element(By.NAME, "search-checkin").click()
    # Tìm thông báo trong thẻ <h1>
    h1_element = driver.find_element(By.TAG_NAME, 'h1')
    # Lấy văn bản từ thẻ <h1>
    message = h1_element.text
    system_message = "Danh sách sách trễ hạn trả"
    if message == system_message:
        print(message)
        check = True
    else:
        assert check, "Không tìm thấy danh sách sách trễ hạn trả"
    check_in_btn = driver.find_element(By.NAME, "btn_checkin")
    # Nếu không tìm thấy nút check-in cho user sau khi tìm kiếm
    if check_in_btn is None:
        check = False
        assert check, "Không thể tìm thấy nút check-in"
    check_in_btn.click()
    # Tìm thông báo check-in trong thẻ body
    body = driver.find_element(By.TAG_NAME, 'body')
    body_text = body.text
    # Kiểm tra xem thông báo cần tìm có trong body không
    search_text = user_id + " đã check in!"
    # Nếu thông báo có tồn tại, gán biến check= True
    if search_text in body_text:
        check = True
    else:
        check = False
    assert check, "Không tìm thấy thông báo check-in thành công"

#TC_CI_04: Kiểm tra check-in với người dùng bị cấm.
#Không tìm thấy nút check-in
#failed in 9.24s
#AssertionError: Vẫn hiển thị nút Check-in
def test_check_in_with_banned_user(driver):
    #Đăng nhập bằng tài khoản quyền admin
    check = False
    login_admin_user(driver)
    #Vào trang check-in
    driver.get("http://localhost/mongodb/checkin.php")
    time.sleep(2)
    user_id= "656ffd55c57de5739770ecb4"
    #Nhập mã user vào ô tìm kiếm và nhấn nút tím kiếm
    driver.find_element(By.NAME, "userid").send_keys(user_id)
    driver.find_element(By.NAME, "search-checkin").click()
    check_in_btn = driver.find_element(By.NAME, "btn_checkin")
    #Nếu không tìm thấy nút check-in cho user sau khi tìm kiếm
    if check_in_btn is None:
        check = True
    assert check, "Vẫn hiển thị nút Check-in"
