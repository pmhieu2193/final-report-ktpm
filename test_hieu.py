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

#Hàm thêm sách vào giỏ
#pre condition: tài khoản được mượn sách này, giỏ sách còn slot.
def add_to_cart(driver, string_url):
    #Truyển url của sách muốn thêm vào giỏ
    driver.get(string_url)
    # Lấy href của book (bỏ qua tên miền)
    href_book = string_url.split('/', 4)[-1]  # Tách thành 4 phần, lấy phần cuối cùng (id book)
    print("href_book: " + href_book)
    time.sleep(2)
    # Nhấn thêm vào giỏ
    button = driver.find_element(By.NAME, "addToCart")
    button.click()
    time.sleep(1)
    #trả về Href của book để xử lý sau này
    return href_book

#############add to cart#########3
#TC_AD_01 : Kiểm tra thêm sách vào giỏ hợp lệ.
#pre condition: tài khoản được mượn sách này, giỏ sách còn slot và ko chứa sách này.
#1 passed in 15.42s (Test Results 5 sec 718ms)
#=>giỏ sách xử lý trong ứng dụng là session
def test_add_to_cart_normal(driver):
    login_admin_user(driver)
    #Biến kiểm tra
    check = True
    #Truyền sách muốn thêm vào giỏ
    href_book = add_to_cart(driver,"http://localhost/mongodb/book.php?_id=656c8825ccdb9f789ba4ad8a")
    current_url = driver.current_url
    # Kiểm tra xem hệ thống có trả về trang cart sau khi add to cart không?
    if not current_url == "http://localhost/mongodb/cart.php":
        check = False
        assert check, "Hệ thống không trả về trang cart.php"
    link_elements = driver.find_elements(By.CSS_SELECTOR, '.link-text')
    # Danh sách để lưu các href (chứa id) sách trong giỏ
    links = []
    # Lặp qua từng phần tử và lấy văn bản trong onclick
    for link in link_elements:
        onclick_value = link.get_attribute('onclick')
        match = re.search(r"location\.href='(.*?)'", onclick_value)
        if match:
            links.append(match.group(1))
    # In ra danh sách các liên kết
    print(links)
    if not href_book in links:
        check = False
    assert check, "Giỏ không chứa sách vừa thêm"

#Nhiều cái test tay ko ra lỗi nhưng automated test lại ra (Test case hay)
#TC_AD_02: Kiểm tra thêm sách đã có trong giỏ vào giỏ.
#pre: giỏ sách còn slot
#fails 8 sec 911 ms
#AssertionError: Giỏ sách chứa sách bị trùng
def test_add_to_cart_with_cart_had_this_book(driver):
    login_admin_user(driver)
    check = True
    #Lặp lại việc thêm sách đó 2 lần
    a = add_to_cart(driver, "http://localhost/mongodb/book.php?_id=656c8825ccdb9f789ba4ad8a")
    href_book = add_to_cart(driver, "http://localhost/mongodb/book.php?_id=656c8825ccdb9f789ba4ad8a")
    current_url = driver.current_url
    if not current_url == "http://localhost/mongodb/cart.php":
        check = False
        assert check, "Hệ thống không trả về trang cart.php"
    #Kiểm tra sách trong giỏ có bị lặp lại không.
    links = []
    link_elements = driver.find_elements(By.CSS_SELECTOR, '.link-text')
    # Lặp qua từng phần tử và lấy văn bản trong onclick
    for link in link_elements:
        onclick_value = link.get_attribute('onclick')
        match = re.search(r"location\.href='(.*?)'", onclick_value)
        if match:
            links.append(match.group(1))
    # In ra danh sách các liên kết
    print(links)
    #Đếm số lần sách xuất hiện trong giỏ
    count = links.count(href_book)
    if count > 1:
        check = False
        assert check, "Giỏ sách chứa sách bị trùng"
    text_element = driver.find_element(By.XPATH, '//a[@name="invalid_book"]')
    text = text_element.text
    if not text == "Bạn đã thêm sách này trước đó rồi":
        check = False
    assert check,"Hệ thống không hiển thị thông báo 'Bạn đã thêm sách này trước đó rồi'"

#TC_AD_03: Kiểm tra thêm sách có cấp bậc cao hơn vào giỏ.
#1 passed in 13.70s
def test_add_to_cart_with_book_has_rank_higher(driver):
    #Login với tài khoản rank sinh viên
    login_normal_user(driver)
    check = True
    #Sách với rank cao hơn tài khoản đăng nhập hiện tại
    driver.get("http://localhost/mongodb/book.php?_id=657faa89ad0bb52317042d77")
    time.sleep(2)
    try:
        # Thử xác định nút "thêm vào giỏ"
        button = driver.find_element(By.NAME, "addToCart")
        #xác định thành công
        check = False
        assert check, "Vẫn tìm thấy nút thêm vào giỏ của sách vừa thêm"
    except:
        assert check

#TC_AD_04: Kiểm tra thêm sách đã hết vào giỏ.
#1 passed in 13.07s
def test_add_to_cart_with_book_zero_qty(driver):
    #Login với tài khoản rank sinh viên
    login_normal_user(driver)
    check = True
    #Sách với số lượng đã hết
    driver.get("http://localhost/mongodb/book.php?_id=657fad6dad0bb52317042d7d")
    time.sleep(2)
    try:
        # Thử xác định nút "thêm vào giỏ"
        button = driver.find_element(By.NAME, "addToCart")
        #xác định thành công
        check = False
        assert check, "Vẫn tìm thấy nút thêm vào giỏ"
    except:
        h3_element = driver.find_element(By.TAG_NAME, 'h3')
        h3_text = h3_element.text
        if not h3_text == "Trạng thái: Sách đã bị mượn hết":
            check = False
        assert check, "Không hiển thị thông báo 'Sách đã bị mượn hết'"

#TC_AD_05: Kiểm tra thêm sách vào giỏ khi giỏ đã đầy.
#passed in 26.82s
#Làm kiểu cồng kềnh là kiểm tra xem trong giỏ có chứa href của quyển sách quá slot không
#->áp dụng cho tất cả trường hơp (mình làm cách 1)
#Làm kiểu nhanh gọn là sau khi thêm quyển sách thứ 5, sẽ đếm số sách là 5 hay 4 (đếm thẻ <tr>)
def test_add_to_cart_with_full_cart(driver):
    #login bằng tài khoản normal user, tài khoản này được mượn tối đa 4 quyển.
    login_normal_user(driver)
    check = True
    #Thêm 4 quyển sách để đầy giỏ, tại vì web lưu sách trong session
    book1 = add_to_cart(driver, "http://localhost/mongodb/book.php?_id=656c8825ccdb9f789ba4ad8a")
    book2 = add_to_cart(driver, "http://localhost/mongodb/book.php?_id=656f5c6a0746e87e6492ff5f")
    book3 = add_to_cart(driver, "http://localhost/mongodb/book.php?_id=656f5c950746e87e6492ff61")
    book4 = add_to_cart(driver, "http://localhost/mongodb/book.php?_id=657eaed6a5d9fbccc908ed8b")
    #Thêm sách thứ 5 và kiểm tra cart
    book_full_url = add_to_cart(driver, "http://localhost/mongodb/book.php?_id=657eb417a5d9fbccc908ed8d")
    text = driver.execute_script("return document.querySelector('a.back[name=\"invalid_book\"]').textContent;")
    if not text == "Số sách trong giỏ của bạn đã đạt tối đa":
        check = False
        assert check, "Hệ thống không hiển thị thông báo 'Số sách trong giỏ của bạn đã đạt tối đa'"
    # Kiểm tra sách trong giỏ chứa sách vượt quá tối đa vừa thêm không.
    links = []
    link_elements = driver.find_elements(By.CSS_SELECTOR, '.link-text')
    # Lặp qua từng phần tử và lấy văn bản trong onclick (id sách)
    for link in link_elements:
        onclick_value = link.get_attribute('onclick')
        match = re.search(r"location\.href='(.*?)'", onclick_value)
        if match:
            links.append(match.group(1))
    # In ra danh sách các liên kết
    print(links)
    # Đếm số lần sách xuất hiện trong giỏ
    count = links.count(book_full_url)
    if count > 1:
        check = False
    assert check, "Giỏ sách chứa sách vượt quá tối đa"

#TC_AD_06 :Kiểm tra thêm sách vào giỏ khi đã hết lượt mượn.
#passed in 15.93s
def test_add_to_cart_with_no_slot(driver):
    #login bằng tài khoản đã hết lượt mượn
    login_custom_user(driver, "test365", "123")
    check = True
    #Thêm 1 quyển sách
    book = add_to_cart(driver, "http://localhost/mongodb/book.php?_id=656c8825ccdb9f789ba4ad8a")
    time.sleep(2)
    #Lấy thông báo thứ 2
    text = driver.execute_script("return document.querySelector('a.back[name=\"session_infor\"]').textContent;")
    if not text == "Số sách được mượn còn lại là:0 Bạn chỉ được thêm số lượng sách tương ứng vào giỏ":
        print(text)
        check = False
        assert check, "Hệ thống không hiển thị thông báo 'Số sách trong giỏ của bạn đã đạt tối đa'"
    #Đếm số sách trong giỏ
    rows = driver.find_elements(By.TAG_NAME, 'tr')
    # Đếm số lượng thẻ <tr> (mỗi sách nằm trong 1 thẻ tr trong bảng)
    number_of_book = len(rows) -1
    #Nếu trong giỏ có sách -> fails
    if number_of_book > 0:
        check = False
    assert check, "Giỏ sách vẫn chứa sách"

#########Quản lý yêu cầu trả##################
#TC_RR_01: Kiểm tra điều hướng trang yêu cầu trả.
#Phải có yêu cầu trả
#passed in 13.48s
def test_nav_trong_yeu_cau_tra(driver):
    #Biến chứa tên miền, chỉ kiểm tra các link trong tên miền này
    home_page = "http://localhost/mongodb/"
    login_admin_user(driver)
    # Vào trang danh sách yêu cầu trả
    driver.get("http://localhost/mongodb/yeu_cau_tra.php")
    time.sleep(2)
    # Tìm tất cả các thẻ <a> trong bảng
    links = driver.find_elements(By.XPATH, '//table//a')

    # Lấy danh sách tất cả các href
    hrefs = [link.get_attribute('href') for link in links]
    list_link = []
    # In ra danh sách hrefs
    for href in hrefs:
        if href is None or href =="":
            continue
        url = href
        print(f"Checking: {url}")
        # Kiểm tra nếu URL không bắt đầu bằng home_page
        if not url.startswith(home_page):
            print(f"URL belongs to another domain, skipping it: {url}")
            continue
        try:
            response = requests.head(url, allow_redirects=True)
            if response.status_code >= 400:
                print(f"code: {response.status_code}")
                print(f"{url} is a broken link")
                list_link.append(url)
            else:
                print(f"{url} is a valid link")
        except requests.exceptions.RequestException as e:
            print(f"Error checking {url}: {e}")
    assert not list_link, print(list_link)

#TC_RR_02: Kiểm tra xác nhận yêu cầu trả.
#1 passed in 13.33s
def test_xac_nhan_yeu_cau_tra(driver):
    check = False
    login_admin_user(driver)
    # Vào trang danh sách yêu cầu trả
    driver.get("http://localhost/mongodb/yeu_cau_tra.php")
    time.sleep(2)
    # Tìm tất cả các nút 'xác nận yêu cầu trả'
    buttons = driver.find_elements(By.NAME, 'action_return')
    # Đếm số lượng nút trước khi bấm
    count = len(buttons)
    #Nếu không có nút
    if count == 0:
        assert check, "Không có yêu cầu trả"
    #Nếu không tìm thấy nút
    if buttons is None:
        assert check, "Không tìm thấy nút yêu cầu trả"
    # Bấm vào nút đầu tiên
    buttons[0].click()
    #Đếm số lượng nút sau khi bấm
    buttons_after_click = driver.find_elements(By.NAME, 'action_return')
    new_count = len(buttons_after_click)
    #Nếu số lượng nút yêu cầu trả không thay đổi (tức số lượng sách yêu cầu trả không giảm sau khi bấm nút)
    if count == new_count:
        assert check, "Số sách trong yêu cầu trả không giảm sau khi xác nhận"
    check = True
    assert check, "Có lỗi xảy ra"

#TC_RR_03: Kiểm tra xác nhận phiếu phạt với sách có thể trả (phải kiểm tra số lượng sách ntn?)
#passed in 14.62s
def test_tao_phat(driver):
    check = False
    login_admin_user(driver)
    # Vào trang danh sách yêu cầu trả
    driver.get("http://localhost/mongodb/yeu_cau_tra.php")
    time.sleep(2)
    #Kiểm tra xem hệ thống có yêu cầu trả nào không bằng cách đếm số nút xác nhận
    buttons = driver.find_elements(By.NAME, 'send')
    # Đếm số lượng nút trước khi bấm
    count = len(buttons)
    if count == 0:
        assert check, "Không có yêu cầu trả nào"
    #Ghi lý do và bấm vào nút gửi đầu tiên
    inputs = driver.find_elements(By.NAME, 'lydo')
    inputs[0].send_keys('Lý do trả sách')
    buttons[0].click()
    #Đếm số lượng nút sau khi nhấn
    buttons_after_click = driver.find_elements(By.NAME, 'send')
    new_count = len(buttons_after_click)
    if count == new_count:
        assert check, "Số sách trong yêu cầu trả không giảm sau khi xác nhận"
    check = True
    assert check, "Có lỗi xảy ra"

#TC_RR_04: Kiểm tra  xác nhận phiếu phạt với sách không thể trả.
#passed in 13.22s
def test_tao_phat_khong_tra_dc_sach(driver):
    check = False
    login_admin_user(driver)
    # Vào trang danh sách yêu cầu trả
    driver.get("http://localhost/mongodb/yeu_cau_tra.php")
    time.sleep(2)
    # Kiểm tra xem hệ thống có yêu cầu trả nào không bằng cách đếm số nút xác nhận
    buttons = driver.find_elements(By.NAME, 'send')
    # Đếm số lượng nút trước khi bấm
    count = len(buttons)
    if count == 0:
        assert check, "Không có yêu cầu trả nào"
    # Ghi lý do và bấm vào nút gửi đầu tiên
    inputs = driver.find_elements(By.NAME, 'lydo')
    inputs[0].send_keys('Lý do trả sách')
    checkboxes = driver.find_elements(By.NAME, 'cannotreturn')
    checkboxes[0].click()
    buttons[0].click()
    # Đếm số lượng nút sau khi nhấn
    buttons_after_click = driver.find_elements(By.NAME, 'send')
    new_count = len(buttons_after_click)
    if count == new_count:
        assert check, "Số sách trong yêu cầu trả không giảm sau khi xác nhận"
    check = True
    assert check, "Có lỗi xảy ra"

##############Quản ly ycm############
#Hàm lựa chọn của bộ lọc 1
def filter1(driver, value):
    # Tìm filter hiển thị số yêu cầu
    select_element = driver.find_element(By.NAME, 'num')
    # Tạo đối tượng Select
    select = Select(select_element)
    # Chọn option thứ 1 (hiển thị 10 yêu cầu)
    select.select_by_index(value)
    # Chờ cho hệ thống cập nhật lại danh sách
    time.sleep(2)

#Hàm lựa chọn của bộ lọc 2
def filter2(driver, value):
    # Tìm filter hiển thị yêu cầu chưa duyệt
    select_element = driver.find_element(By.NAME, 'status')
    # Tạo đối tượng Select
    select = Select(select_element)
    # Chọn option thứ 1 (hiển thị yêu cầu chưa duyệt)
    select.select_by_index(value)
    # Chờ cho hệ thống cập nhật lại danh sách
    time.sleep(2)

#TC_SR_01: Kiểm tra bộ lọc 1: Hiển thị 10 yêu cầu trả.
#passed in 15.15s
def test_filer1_select10(driver):
    check = False
    #Đăng nhập bằng tài khoản quyền admin
    login_admin_user(driver)
    driver.get("http://localhost/mongodb/yeu_cau_muon.php")
    time.sleep(2)
    filter1(driver, 1)
    #Đếm số yêu cầu trong danh sách sau khi cập nhật bằng cách
    # đếm tất cả các thẻ <tr> trong bảng
    rows = driver.find_elements(By.TAG_NAME, 'tr')
    # Đếm số thẻ <tr>
    number_of_rows = len(rows)
    print(number_of_rows)
    #Nếu số yêu cầu <=11 (bao gồm cả dòng chứa tiêu đề bảng)
    if number_of_rows <=11:
        check = True
    assert check, 'Số yêu cầu đã vượt quá 10: '+str(number_of_rows)

#TC_SR_02: Kiểm tra bộ lọc 1: Hiển thị 20 yêu cầu trả.
#passed in 15.38s
def test_filer1_select20(driver):
    check = False
    #Đăng nhập bằng tài khoản quyền admin
    login_admin_user(driver)
    driver.get("http://localhost/mongodb/yeu_cau_muon.php")
    time.sleep(2)
    filter1(driver, 2)
    #Đếm số yêu cầu trong danh sách sau khi cập nhật bằng cách
    # đếm tất cả các thẻ <tr> trong bảng
    rows = driver.find_elements(By.TAG_NAME, 'tr')
    # Đếm số thẻ <tr>
    number_of_rows = len(rows)
    print(number_of_rows)
    #Nếu số yêu cầu <=21 (bao gồm cả dòng chứa tiêu đề bảng)
    if number_of_rows <=21:
        check = True
    assert check, 'Số yêu cầu đã vượt quá 20: '+str(number_of_rows)

#TC_SR_03: Kiểm tra bộ lọc 1: Hiển thị 30 yêu cầu trả.
#passed in 15.19s
def test_filer1_select30(driver):
    check = False
    #Đăng nhập bằng tài khoản quyền admin
    login_admin_user(driver)
    driver.get("http://localhost/mongodb/yeu_cau_muon.php")
    time.sleep(2)
    filter1(driver, 3)
    # Đếm số yêu cầu trong danh sách sau khi cập nhật bằng cách
    # đếm tất cả các thẻ <tr> trong bảng
    rows = driver.find_elements(By.TAG_NAME, 'tr')
    # Đếm số thẻ <tr>
    number_of_rows = len(rows)
    print(number_of_rows)
    #Nếu số yêu cầu <=21 (bao gồm cả dòng chứa tiêu đề bảng)
    if number_of_rows <=31:
        check = True
    assert check, 'Số yêu cầu đã vượt quá 30: '+str(number_of_rows)


# TC_SR_04: Kiểm tra bộ lọc 2: Lọc theo yêu cầu chưa duyệt.
# passed in 15.06s
def test_filer2_select_chua_duyet(driver):
    check = False
    # Đăng nhập bằng tài khoản quyền admin
    login_admin_user(driver)
    driver.get("http://localhost/mongodb/yeu_cau_muon.php")
    time.sleep(2)
    filter2(driver, 1)
    rows = driver.find_elements(By.CSS_SELECTOR, 'div.small-container table tbody tr')
    # Danh sách để lưu các trạng thái không đúng
    texts = []
    i = 1
    #Lấy text chứa trạng thái yêu cầu nằm trong thẻ td thứ 7
    # Bỏ qua <tr> đầu tiên và lặp qua các <tr> còn lại (Thẻ <Tr> đầu tiên là tiêu đề)
    for row in rows[1:]:
        # Tìm tất cả các thẻ <td> trong <tr>
        cells = row.find_elements(By.TAG_NAME, 'td')
        # Kiểm tra xem có đủ <td> hay không
        if len(cells) >= 7:
            try:
                # Tìm thẻ <a> trong <td> thứ 7 (chỉ số 6)
                link = cells[6].find_element(By.TAG_NAME, 'a')
                string = "Đang Đợi Duyệt"
                if link.text != string:
                    # Lấy văn bản bên trong thẻ <a>
                    texts.append("Lỗi tại dòng "+str(i)+" có trạng thái: "+link.text)
            except:
                #Bỏ qua trạng thái None
                i = i + 1
                continue
        i = i +1
    # Nếu texts rỗng, tức không có yêu cầu nào có trạng thái không đúng
    if not texts:
        check = True
    assert check, texts

# TC_SR_05: Kiểm tra bộ lọc 2: Lọc theo yêu cầu đã duyệt.
# passed in 15.41s
def test_filer2_select_da_duyet(driver):
    check = False
    # Đăng nhập bằng tài khoản quyền admin
    login_admin_user(driver)
    driver.get("http://localhost/mongodb/yeu_cau_muon.php")
    time.sleep(2)
    filter2(driver, 2)
    # Kiểm tra trạng thái tất cả các yêu cầu đang hiển thị
    rows = driver.find_elements(By.CSS_SELECTOR, 'div.small-container table tbody tr')
    # Danh sách để lưu các trạng thái không đúng
    texts = []
    i = 1
    #Lấy text chứa trạng thái yêu cầu nằm trong thẻ td thứ 7
    # Bỏ qua <tr> đầu tiên và lặp qua các <tr> còn lại (Thẻ <Tr> đầu tiên là tiêu đề)
    for row in rows[1:]:
        # Tìm tất cả các thẻ <td> trong <tr>
        cells = row.find_elements(By.TAG_NAME, 'td')
        # Kiểm tra xem có đủ <td> hay không
        if len(cells) >= 7:
            try:
                # Tìm thẻ <a> trong <td> thứ 7 (chỉ số 6)
                link = cells[6].find_element(By.TAG_NAME, 'a')
                string = "Đã Duyệt"
                if link.text != string:
                    # Lấy văn bản bên trong thẻ <a>
                    texts.append("Lỗi tại dòng "+str(i)+" có trạng thái: "+link.text)
            except:
                #Bỏ qua trạng thái None
                i = i + 1
                continue
        i = i +1
    # Nếu texts rỗng, tức không có yêu cầu nào có trạng thái không đúng
    if not texts:
        check = True
    assert check, texts

# TC_SR_06: Kiểm tra bộ lọc 2: Lọc theo yêu cầu đã từ chối.
# passed in 15.26s
def test_filer2_select_da_tu_choi(driver):
    check = False
    # Đăng nhập bằng tài khoản quyền admin
    login_admin_user(driver)
    driver.get("http://localhost/mongodb/yeu_cau_muon.php")
    time.sleep(2)
    filter2(driver, 3)
    # Kiểm tra trạng thái tất cả các yêu cầu đang hiển thị
    rows = driver.find_elements(By.CSS_SELECTOR, 'div.small-container table tbody tr')
    # Danh sách để lưu các trạng thái không đúng
    texts = []
    i = 1
    #Lấy text chứa trạng thái yêu cầu nằm trong thẻ td thứ 7
    # Bỏ qua <tr> đầu tiên và lặp qua các <tr> còn lại (Thẻ <Tr> đầu tiên là tiêu đề)
    for row in rows[1:]:
        # Tìm tất cả các thẻ <td> trong <tr>
        cells = row.find_elements(By.TAG_NAME, 'td')
        # Kiểm tra xem có đủ <td> hay không
        if len(cells) >= 7:
            try:
                # Tìm thẻ <a> trong <td> thứ 7 (chỉ số 6)
                link = cells[6].find_element(By.TAG_NAME, 'a')
                string = "Đã Từ Chối"
                if link.text != string:
                    # Lấy văn bản bên trong thẻ <a>
                    texts.append("Lỗi tại dòng "+str(i)+" có trạng thái: "+link.text)
            except:
                #Bỏ qua trạng thái None
                i = i + 1
                continue
        i = i +1
    # Nếu texts rỗng, tức không có yêu cầu nào có trạng thái không đúng
    if not texts:
        check = True
    assert check, texts

# TC_SR_07: Kiểm tra kết hợp nhiều bộ lọc.
# passed in 17.53s
def test_combo2filter(driver):
    check_for_filter1 = False
    check_for_filter2 = False
    # Đăng nhập bằng tài khoản quyền admin
    login_admin_user(driver)
    driver.get("http://localhost/mongodb/yeu_cau_muon.php")
    time.sleep(2)

    ######Chọn filter chỉ hiển chị 20 yêu cầu
    filter1(driver, 2)

    ######Đếm số lượng yêu cầu##########3
    # Tương tự TC 15
    rows1 = driver.find_elements(By.TAG_NAME, 'tr')
    number_of_rows1 = len(rows1)
    if number_of_rows1 <= 21:
        check_for_filter1 = True

    ######Chọn filter chỉ yêu cầu đã duyệt
    filter2(driver, 2)

    #######Kiểm tra trạng thái các yêu cầu##############
    # Tương tự TC18
    rows = driver.find_elements(By.CSS_SELECTOR, 'div.small-container table tbody tr')
    texts = []
    i = 1
    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, 'td')
        if len(cells) >= 7:
            try:
                link = cells[6].find_element(By.TAG_NAME, 'a')
                string = "Đã Duyệt"
                if link.text != string:
                    texts.append("Lỗi tại dòng "+str(i)+" có trạng thái: "+link.text)
            except:
                i = i + 1
                continue
        i = i +1

    if not texts:
        check_for_filter2 = True

    if check_for_filter1 and not check_for_filter2:
        assert check_for_filter2, 'Số yêu cầu đã vượt quá 20: '+str(number_of_rows1)
    if not check_for_filter1 and check_for_filter2:
        assert check_for_filter1, texts
    if not check_for_filter1 and not check_for_filter2:
        texts.append('Số yêu cầu đã vượt quá 20: '+str(number_of_rows1))
        assert check_for_filter1, texts
    if check_for_filter1 and check_for_filter2:
        assert check_for_filter1


#TC_SR_08: Kiểm tra xem chi tiết yêu cầu mượn
#passed in 16.14s
def test_view_order_detail(driver):
    #Biến kiểm tra
    check = False
    #Đăng nhập bằng tài khoản admin
    login_admin_user(driver)
    driver.get("http://localhost/mongodb/yeu_cau_muon.php")
    #Chọn filter để hệ thống chỉ hiển thị các yêu cầu đã duyệt hoặc đã từ chối
    select_element = driver.find_element(By.NAME, 'status')
    select = Select(select_element)
    select.select_by_index(2)
    #Chờ để hệ thống tải lại danh sách
    time.sleep(1)

    #Click vào nút "xem chi tiết" đầu tiên trong danh sách
    get_order_button = driver.find_element(By.NAME, 'getOrder')
    get_order_button.click()
    time.sleep(2)
    #Lấy url hiện tại
    url = driver.current_url
    #Sử dụng regex chỉ lấy phần url không chứa tham số truy vấn
    base_url = re.match(r'^[^?]*', url).group()
    #Kiểm tra xem url truy cập sau khi bấm nút có phải là trang chi tiết hay không
    if base_url == "http://localhost/mongodb/chi_tiet_ycm.php":
        check = True
    assert check, "Không thể truy cập trang chi tiết đơn hàng"

#TC_SR_09: Kiểm tra huỷ yêu cầu mượn
#passed in 18.04s
def test_cancel_order_detail(driver):
    #Biến kiểm tra
    check = False
    #Đăng nhập bằng tài khoản admin
    login_admin_user(driver)
    driver.get("http://localhost/mongodb/yeu_cau_muon.php")
    #Chọn filter để hệ thống chỉ hiển thị các yêu cầu chưa duyệt
    select_element = driver.find_element(By.NAME, 'status')
    select = Select(select_element)
    select.select_by_index(1)
    #Chờ để hệ thống tải lại danh sách
    time.sleep(1)

    #Click vào nút "Huỷ" đầu tiên trong danh sách
    get_order_button = driver.find_element(By.CLASS_NAME, 'cancel-btn')
    get_order_button.click()
    time.sleep(2)
    #đếm số yêu cầu chưa duyệt trước và sau khi từ chối
    #làm kĩ thì đếm cả của bên từ chối luôn
    #nhưng mã nguồn mình lại ko reload lại sau khi xử lý -> chỉ cần đọc trạng thái trực tiếp

    #kiểm tra trạng thái yêu cầu vừa từ chối, tương tự TC19
    rows = driver.find_elements(By.CSS_SELECTOR, 'div.small-container table tbody tr')
    status = ""
    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, 'td')
        if len(cells) >= 7:
                link = cells[6].find_element(By.TAG_NAME, 'a')
                string = "Đã Từ Chối"
                if link.text == string:
                    check = True
                else:
                    status = link.text
                break
    assert check, "Trạng thái yêu cầu vừa từ chối là "+status

#TC_SR_10: Kiểm tra xác nhận yêu cầu mượn
#passed in 16.39s
#pre: Đăng nhập bằng tài khoản admin
def test_accept_in_order_detail(driver):
    check = False
    login_admin_user(driver)
    driver.get("http://localhost/mongodb/yeu_cau_muon.php")
    # Chọn filter để hệ thống chỉ hiển thị các yêu cầu chưa duyệt
    select_element = driver.find_element(By.NAME, 'status')
    select = Select(select_element)
    select.select_by_index(1)
    # Chờ để hệ thống tải lại danh sách
    time.sleep(1)
    # Click vào nút "Hành dộng" đầu tiên trong danh sách
    get_order_button = driver.find_element(By.CLASS_NAME, 'confirm-btn')
    get_order_button.click()
    time.sleep(2)
    url = driver.current_url
    # Sử dụng regex chỉ lấy phần url không chứa tham số truy vấn
    base_url = re.match(r'^[^?]*', url).group()
    # Kiểm tra xem url truy cập sau khi bấm nút có phải là trang chi tiết hay không
    if not base_url == "http://localhost/mongodb/chi_tiet_ycm.php":
        assert check, "Không thể truy cập trang chi tiết đơn hàng"
    #Nhấn vào nút xác nhận trong trang chi tiết
    accept_button = driver.find_element(By.CLASS_NAME, 'confirm-btn')
    accept_button.click()
    time.sleep(2)
    confirmed_btn = driver.find_element(By.CLASS_NAME, 'confirmed-btn')
    if confirmed_btn is not None:
        check = True
    assert check, "Không thể tìm thấy nút đã xác nhận"

#TC_SR_11: Kiểm tra từ chối yêu cầu mượn tại trang chi tiết
#passed in 16.43s
#pre: Đăng nhập bằng tài khoản admin
def test_cancel_in_order_detail(driver):
    check = False
    login_admin_user(driver)
    driver.get("http://localhost/mongodb/yeu_cau_muon.php")
    # Chọn filter để hệ thống chỉ hiển thị các yêu cầu chưa duyệt
    select_element = driver.find_element(By.NAME, 'status')
    select = Select(select_element)
    select.select_by_index(1)
    # Chờ để hệ thống tải lại danh sách
    time.sleep(1)
    # Click vào nút "Hành dộng" đầu tiên trong danh sách
    get_order_button = driver.find_element(By.CLASS_NAME, 'confirm-btn')
    get_order_button.click()
    time.sleep(2)
    url = driver.current_url
    # Sử dụng regex chỉ lấy phần url không chứa tham số truy vấn
    base_url = re.match(r'^[^?]*', url).group()
    # Kiểm tra xem url truy cập sau khi bấm nút có phải là trang chi tiết hay không
    if not base_url == "http://localhost/mongodb/chi_tiet_ycm.php":
        assert check, "Không thể truy cập trang chi tiết đơn hàng"
    #Nhấn vào nút xác nhận trong trang chi tiết
    accept_button = driver.find_element(By.CLASS_NAME, 'cancel-btn')
    accept_button.click()
    time.sleep(2)
    canceled_btn = driver.find_element(By.CLASS_NAME, 'canceled-btn')
    if canceled_btn is not None:
        check = True
    assert check, "Không thể tìm thấy nút đã từ chối yêu cầu"

#######################cart####################

#TC_cb_01: Kiểm tra xoá sách khỏi giỏ
#pre: Tài khoản còn lượt mượn, add to cart thành công
#passed in 14.36s
def test_remove_book_from_cart(driver):
    login_normal_user(driver)
    check = True
    #Thêm 1 quyển sách ngẫu nhiên
    book1 = add_to_cart(driver, "http://localhost/mongodb/book.php?_id=656c8825ccdb9f789ba4ad8a")
    #Đếm số sách trước khi xoá bằng cách đếm số thẻ <tr> trong bảng
    rows_before = driver.find_elements(By.TAG_NAME, 'tr')
    number_of_book_before = len(rows_before)
    #nhấn vào nút xoá sách khỏi giỏ đầu tiên
    btn_remove = driver.find_element(By.NAME, 'btn_remove')
    btn_remove.click()
    #Đếm số sách sau khi xoá 1 quyển sách khỏi giỏ
    rows_after = driver.find_elements(By.TAG_NAME, 'tr')
    number_of_book_after = len(rows_after)
    if number_of_book_before == (number_of_book_after -1):
        check = True
    assert check, "Số sách trước và sau xoá không thay đổi"

#TC_CB_02: Kiểm tra nút mượn thêm sách.
#passed in 15.17s
def test_borrow_more_book(driver):
    login_normal_user(driver)
    check = True
    cart_button = driver.find_element(By.NAME, 'gotoCart')
    cart_button.click()
    time.sleep(2)
    borrow_more_btn = driver.find_element(By.NAME, 'borrow_more')
    borrow_more_btn.click()
    time.sleep(2)
    url = driver.current_url
    if url=="http://localhost/mongodb/index.php":
        check = True
    assert check, "Không thể trở về trang chủ"


#Phương pháp chuyển đổi trạng thái, chỉ quan tâm đến trạng thái hệ thống
#tách thành các funcion ứng với các trạng thái hệ thống, để tái sử dụng


#TC_CB_03: Kiểm tra gửi yêu cầu mượn.
# failed in 13.83s
# Thoả 2 yêu cầu là yêu cầu được gửi và cập nhật lại số yêu cầu mượn
#E AssertionError: Không làm mới lại nội dung giỏ hàng sau khi đã gửi yêu cầu
def test_cart(driver):
    check = False
    login_admin_user(driver)
    # Thêm khoảng 3 quyển sách
    book1 = add_to_cart(driver, "http://localhost/mongodb/book.php?_id=656c8825ccdb9f789ba4ad8a")
    #book2 = add_to_cart(driver, "http://localhost/mongodb/book.php?_id=656f5c6a0746e87e6492ff5f")
    #book3 = add_to_cart(driver, "http://localhost/mongodb/book.php?_id=656f5c950746e87e6492ff61")
    ########Lấy các thông tin######
    #Lấy thông tin về số lượt mượn trước khi mượn


    ####Cần lặp lại cái này để tính số sau khi cart
    #Sử dụng javaScript lấy văn bản thông báo
    text = driver.execute_script("return document.querySelector('a.back[name=\"session_infor\"]').textContent;")
    match = re.search(r'\d+', text)
    number_can_borrow = match.group()
    number_can_borrow = int(number_can_borrow)
    print(number_can_borrow)
    #Lấy thông tin số sách đang mượn
    table = driver.find_element(By.NAME, 'book')
    rows = table.find_elements(By.TAG_NAME, 'tr')
    #Trừ 1 cột <tr> chứa tiêu đề bảng
    number_current_books = len(rows) - 1
    print(number_current_books)

    table = driver.find_element(By.NAME, 'price')
    cells = table.find_elements(By.TAG_NAME, 'td')
    # Lấy các giá trị từ các thẻ <td> mong muốn
    number_of_books = cells[1].text  # <td>1</td>
    number_of_books = int(number_of_books)

    #nhấn thêm vào giỏ -> giỏ phải trống sách, không còn hiển thị bảng tạo ycm
    send_cart = driver.find_element(By.CLASS_NAME, 'btn-cart')
    send_cart.click()
    time.sleep(2)

    #Kiểm tra bảng tạo ycm là đc rồi
    send_cart_after_click = driver.find_element(By.CLASS_NAME, 'btn-cart')

    # số sách đc mượn sau khi mượn
    text_after = driver.execute_script("return document.querySelector('a.back[name=\"session_infor\"]').textContent;")
    match = re.search(r'\d+', text_after)
    number_can_borrow_after = match.group()
    number_can_borrow_after = int(number_can_borrow_after)

    if not number_can_borrow == (number_can_borrow_after + number_current_books):
        assert check, "Mượn sách không thành công, không cập nhật giá trị sách đc mượn"

    if not send_cart_after_click is None:
        assert check, "Không làm mới lại nội dung giỏ hàng sau khi đã gửi yêu cầu"

    check = True
    assert check

#TC_CB_04: Kiểm tra thông tin giỏ sách trước và sau khi gửi yêu cầu
#passed in 14.31s
def test_cart_information(driver):
    check = False
    login_admin_user(driver)
    # Thêm khoảng 3 quyển sách
    book1 = add_to_cart(driver, "http://localhost/mongodb/book.php?_id=656c8825ccdb9f789ba4ad8a")
    #book2 = add_to_cart(driver, "http://localhost/mongodb/book.php?_id=656f5c6a0746e87e6492ff5f")
    #book3 = add_to_cart(driver, "http://localhost/mongodb/book.php?_id=656f5c950746e87e6492ff61")
    ########Lấy các thông tin######
    #Lấy thông tin về số lượt mượn trước khi mượn
    #Sử dụng javaScript lấy văn bản thông báo
    text = driver.execute_script("return document.querySelector('a.back[name=\"session_infor\"]').textContent;")
    match = re.search(r'\d+', text)
    number_can_borrow = match.group()
    print(number_can_borrow)
    #Lấy thông tin số sách đang mượn
    table = driver.find_element(By.NAME, 'book')
    rows = table.find_elements(By.TAG_NAME, 'tr')
    #Trừ 1 cột <tr> chứa tiêu đề bảng
    number_current_books = len(rows) - 1
    print(number_current_books)

    table = driver.find_element(By.NAME, 'price')
    cells = table.find_elements(By.TAG_NAME, 'td')
    # Lấy các giá trị từ các thẻ <td> mong muốn
    number_of_books = cells[1].text  # <td>1</td>
    borrow_date = cells[3].text  # <td>01-12-2024</td>
    return_date = cells[5].text  # <td>08-12-2024</td>

    print(f'Số sách: {number_of_books}')
    print(f'Ngày mượn: {borrow_date}')
    print(f'Ngày phải trả chung: {return_date}')

    ####
    today = datetime.now().date()
    date_must_return = today + timedelta(days=7)

    date_object_borrow = datetime.strptime(borrow_date, "%d-%m-%Y").date()
    date_object_return = datetime.strptime(return_date, "%d-%m-%Y").date()
    print(today)
    print(date_object_borrow)
    if not today == date_object_borrow:
        assert check, "Ngày mượn hiện tại trên hệ thống sai"
    if not date_must_return == date_object_return:
        assert check, "Ngày phải trả không chính xác"
    if not int(number_of_books) == number_current_books:
        print("----")
        print(number_of_books)
        print("-----")
        print(number_current_books)
        assert check, "Số sách đang mượn và số sách hiển thị không chính xác"
    check = True
    assert check, "Có lỗi sảy ra"
