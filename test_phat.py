import unittest
import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  # Importing TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import random
@pytest.mark.usefixtures("driver")
@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # Change to your desired browser
    yield driver
    driver.quit()

#function thực hiện đăng ký với biến tự động
def register(driver, email, password, name, number, id, address, gender_value, date, role):
    driver.get("http://localhost/mongodb/sigup.php")
    time.sleep(3)
    # Fill in registration information
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "name").send_keys(name)
    driver.find_element(By.NAME, "number").send_keys(number)
    driver.find_element(By.NAME, "cccd").send_keys(id)
    driver.find_element(By.NAME, "address").send_keys(address)
    time.sleep(3)
    # Handle gender input
    try:
        # Wait for the gender checkbox to be present
        gender_checkbox = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"input[name='gender'][value='{gender_value}']"))
        )
        gender_checkbox.click()  # Click the checkbox for the selected gender
    except Exception as e:
        print(f"Error locating gender checkbox: {e}")

    # Fill in date
    driver.find_element(By.NAME, "date").send_keys(date)

    # Select role from dropdown
    select_element = driver.find_element(By.NAME, "rank")
    select = Select(select_element)
    select.select_by_visible_text(role)
    time.sleep(3)

    # Submit the form
    submit_button = driver.find_element(By.XPATH, "/html/body/div[2]/form/button")
    submit_button.click()
    time.sleep(3)

#Pass_edge_24.11s _chorme_22.07s
#TC05
def test_register_valid_data(driver):
    email = "letanphat110@gmail.com"
    password = "123456"
    name = "Jrtanphat"
    number = "0765978220"
    cccd = "999999999"
    address = "Q7"
    gender = "0"
    date = "05-10-2003"
    role = "Công chức"

    register(driver, email, password, name, number, cccd, address, gender, date, role)
    # Xác minh kết quả
    current_url = driver.current_url
    assert "login.php" in current_url, f"quay về trang đăng nhập khi đăng ký thành công. URL hiện tại: {current_url}"
    try:
        success_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Tạo tài khoản thành công, vui vòng đăng nhập')]"))
        )
        assert success_message is not None
    except TimeoutException:
        assert False, "Success message not found on the page after waiting."


#Fail_Edege_16.68s_Chorme_16.68s
#TC06
def test_register_boundary_password(driver):
    email = "tanphat0@gmail.com"
    password = "1"
    name = "Jrtanphat"
    number = "0765978220"
    cccd = "086203"
    address = "Q7"
    gender = "1"
    date = "05-10-2003"
    role = "Công chức"

    register(driver, email, password, name, number, cccd, address, gender, date, role)
    current_url = driver.current_url
    assert "sigup.php" in current_url, f"Không quay về trang đăng ký khi đăng ký thất bại. URL hiện tại: {current_url}"
    try:
        # Kiểm tra thông báo lỗi
        alert_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Password is too short')]")
            )
        )
        assert alert_message is not None, "Thông báo lỗi về mật khẩu không hiển thị."
        print("Kiểm tra thành công: Ở lại trang đăng ký và hiển thị thông báo lỗi.")
    except AssertionError as e:
        print(f"Lỗi kiểm tra: {str(e)}")


#Fail_Edge_16.64s_Chorme_16.61s
#TC07
def test_register_invalid_email(driver):
    email = "ttp#.com"
    password = "123456"
    name = "Jrtanphat"
    number = "0765978220"
    cccd = "086203666666"
    address = "Q7"
    gender = "1"
    date = "05-10-2003"
    role = "Công chức"

    register(driver, email, password, name, number, cccd, address, gender, date, role)

    current_url = driver.current_url
    assert "sigup.php" in current_url, f"Không quay về trang đăng ký khi đăng ký thất bại. URL hiện tại: {current_url}"
    # Wait for the success message to appear
    try:
        alert_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Email không đúng định dạng')]")
            )
        )
        assert alert_message is not None, "Alert message for invalid email format not displayed."
    except TimeoutException:
        assert False, "Expected alert message not found on the page after waiting."


#Fail_Edge_16.60s_Chorme_16.68s
#TC_08
def test_register_blankinfo(driver):
    email = "tanpg@gmail.com"
    password = "123456"
    name = ""
    number = ""
    cccd = "086203002222"
    address = ""
    gender = "1"
    date = "05-10-2003"
    role = "Công chức"

    register(driver, email, password, name, number, cccd, address, gender, date, role)


    current_url = driver.current_url
    assert "sigup.php" in current_url, f"Không quay về trang đăng ký khi đăng ký thất bại. URL hiện tại: {current_url}"

    # Wait for the success message to appear
    try:
        alert_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Vui lòng điền đầy đủ thông tin')]")
            )
        )
        assert alert_message is not None, "Alert message for blank information not displayed."
    except TimeoutException:
        assert False, "Expected alert message not found on the page after waiting."


#Pass_Edge_23.60s_Chorme_20.61s
#TC_09
def test_register_registered_email(driver):
    email = "tanphatrey510@gmail.com"
    password = "123456"
    name = "Jrtanphat"
    number = "0762978220"
    cccd = "086203000101"
    address = "1041 Tran Xuan Soan"
    gender = "1"
    date = "05-10-2003"
    role = "Công chức"

    register(driver, email, password, name, number, cccd, address, gender, date, role)


    current_url = driver.current_url
    assert "sigup.php" in current_url, f"Không quay về trang đăng ký khi đăng ký thất bại. URL hiện tại: {current_url}"

    # Xác minh kết quả mong đợi
    assert "Email này đã được sử dụng" in driver.page_source


#Fail_Edge_16.63s_Chorme_16.94s
#TC_10
def test_register_specialcharacter(driver):
    email = "!@#$%^&*()@gmail.com"
    password = "123456"
    name = "!@#$%^&*"
    number = "0762978220"
    cccd = "00909090"
    address = "1041 Tran Xuan Soan"
    gender = "1"
    date = "05-10-2003"
    role = "Công chức"

    register(driver, email, password, name, number, cccd, address, gender, date, role)
    current_url = driver.current_url
    assert "sigup.php" in current_url, f"Không quay về trang đăng ký khi đăng ký thất bại. URL hiện tại: {current_url}"

    # Xác minh kết quả mong đợi
    try:
        alert_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Vui lòng điền đúng định dạng')]")
            )
        )
        assert alert_message is not None, "Alert message for invalid email format with special characters not displayed."
    except TimeoutException:
        assert False, "Expected alert message not found on the page after waiting."


#Pass_Edge_24.13s_Chorme_20.68s
#TC_11
def test_register_same_id(driver):
    email = "Jrtanphat@gmail.com"
    password = "123456"
    name = "Jrtanphat"
    number = "0762978220"
    cccd = "086203000101"
    address = "1041 Tran Xuan Soan"
    gender = "1"
    date = "05-10-2003"
    role = "Công chức"

    register(driver, email, password, name, number, cccd, address, gender, date, role)



    current_url = driver.current_url
    assert "sigup.php" in current_url, f"Không quay về trang đăng ký khi đăng ký thất bại. URL hiện tại: {current_url}"

    # Chờ và kiểm tra thông báo "CCCD này đã được đăng ký trước đó"
    # Xác minh kết quả mong đợi
    assert "CCCD này đã được đăng ký trước đó" in driver.page_source

def login(driver):

    driver.get("http://localhost/mongodb/login.php")
    driver.find_element(By.NAME, "email").send_keys("tanphatrey510@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123456")
    submit_button = driver.find_element(By.XPATH, "/html/body/div[2]/form/button")
    time.sleep(3)
    submit_button.click()
    time.sleep(3)
def search_book(driver, search_query):
    login(driver)  # Hàm đăng nhập (giả sử bạn đã định nghĩa trước)
    time.sleep(3)
    driver.get("http://localhost/mongodb/admin.php")  # Đường dẫn đến trang quản trị
    time.sleep(3)  # Chờ trang tải (khuyến nghị dùng WebDriverWait thay vì sleep)

    # Tìm hộp tìm kiếm
    search_box = driver.find_element(By.NAME, "timkiem")
    search_box.send_keys(search_query + Keys.RETURN)
    time.sleep(3)  # Chờ kết quả tìm kiếm

    try:
        # Chờ danh sách sản phẩm hiển thị
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-listing"))
        )

        # Lấy danh sách các sách tìm được
        books = driver.find_elements(By.CLASS_NAME, "product-card2")  # Cập nhật bộ chọn
        print(f"Number of books found: {len(books)}")

        # Trả về danh sách tiêu đề sách
        result = [book.find_element(By.CLASS_NAME, "book-brand").text for book in books]
        return result
    except TimeoutException:
        print("Fail: Không tìm thấy sách.")
        return []

#Pass_Edge_27.76s_Chorme_24.85s
#TC_12
def test_search_book_valid(driver):
    word = "Học chơi free fire"
    result = search_book(driver, word)

    # Đảm bảo kết quả không rỗng và chứa sách mong muốn
    assert len(result) > 0, f"Test failed: Không tìm thấy sách với từ khóa '{word}'."
    assert any(word.lower() in title.lower() for title in result), \
        f"Test failed: Không tìm thấy sách phù hợp với từ khóa '{word}'."

#Pass_Edge_27.23s_Chorme_24.73s
#TC_13
def test_search_book_invalid(driver):
    word = "1234"
    result = search_book(driver, word)
    assert len(result) == 0, f"Test failed: Không tìm thấy sách với từ khóa '{word}', nhưng lại có kết quả."

#Pass_Edge_27.32s_Chorme_25.54s
#TC_14
def test_search_book_with_nonexistent_keyword(driver):
    word = "NonExistentProduct123"
    result = search_book(driver, word)
    assert len(result) == 0, f"Test failed: Không tìm thấy sách với từ khóa '{word}', nhưng lại có kết quả."

#Pass_Edge_26.16s_Chorme_24.77s
#TC_15
def test_search_with_uppercase_keyword(driver):
    word = "HỌC CHƠI FREE FIRE"
    result = search_book(driver, word)

    # Đảm bảo kết quả không rỗng và chứa sách mong muốn
    assert len(result) > 0, f"Test failed: Không tìm thấy sách với từ khóa '{word}'."
    assert any(word.upper() in title.upper() for title in result), \
        f"Test failed: Không tìm thấy sách phù hợp với từ khóa '{word}'."

#Pass_Edge_25.61s_Chorme_27.08s
#TC_16
def test_search_with_special_characters(driver):
    word = "H@c chơ! fr$$ fire"
    result = search_book(driver, word)
    assert len(result) == 0, f"Test failed: Không tìm thấy sách với từ khóa '{word}', nhưng lại có kết quả."

#Pass_Edge_25.66s_Chorme_24.71s
#TC_17
def test_search_with_keyword_surrounded_by_whitespace(driver):
    word = "    Học chơi free fire    "
    result = search_book(driver, word)
    assert len(result) == 0, f"Test failed: Không tìm thấy sách với từ khóa '{word}', nhưng lại có kết quả."

#Fail_Edge_23.31s_Chorme_22.28s
#TC_18
def test_search_empty_characters(driver):
    word = ""
    result = search_book(driver, word)
    assert len(result) == 0, f"Test failed: Không tìm thấy sách với từ khóa '{word}', nhưng lại có kết quả."

#Function thực hiện trước khi test
def search_book_by_filter(driver, filter_query):
    login(driver)  # Hàm đăng nhập (giả sử bạn đã định nghĩa trước)
    driver.get("http://localhost/mongodb/admin.php")  # Đường dẫn đến trang quản trị
    time.sleep(3)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "ma_the_loai")))  # Đợi cho đến khi <select> hiển thị

    # Lấy phần tử <select> và chọn giá trị cần lọc
    select_element = driver.find_element(By.NAME, "ma_the_loai")
    select = Select(select_element)
    select.select_by_value(filter_query)  # Lựa chọn theo giá trị của filter_query

    # Chờ danh sách sách cập nhật sau khi thay đổi bộ lọc
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-card2")))

    # Lấy danh sách các cuốn sách sau khi chọn filter
    books = driver.find_elements(By.CLASS_NAME, "product-card2")
    time.sleep(5)

#in ra danh sách thông tin sách
    book_list = []
    for book in books:
        title = book.find_element(By.CLASS_NAME, "book-brand").text
        author = book.find_element(By.CLASS_NAME, "product-short-des2").text  # Tác giả
        language = book.find_elements(By.CLASS_NAME, "product-short-des2")[1].text  # Ngôn ngữ
        publisher = book.find_elements(By.CLASS_NAME, "product-short-des2")[2].text  # Nhà xuất bản

        book_list.append({
            "title": title,
            "author": author,
            "language": language,
            "publisher": publisher
        })

    return book_list

# Kiểm tra lại trong hàm test của bạn

#Pass_Edge_25.25s_Chorme_24.36s
#TC_19
def test_search_book_filter_category(driver):
    filter_option = "1"  # Ví dụ: "1" là giá trị cần lọc (thể loại sách_Giáo dục)
    result = search_book_by_filter(driver, filter_option)
    for book in result:
        print(book)

#Function thực hiện trước khi test
def add_book(driver,name,amount,des,author,language,year,pos,rank,cate,publisher,date_value):
    login(driver)
    driver.get("http://localhost/mongodb/admin.php")
    time.sleep(5)
    add_button = driver.find_element(By.XPATH,"/html/body/div[4]/div[1]/div/a[1]/button")
    time.sleep(5)
    add_button.click()

#thêm thông tin sách
    driver.find_element(By.ID, "name").send_keys(name) #ten sach
    driver.find_element(By.ID, "quantity").send_keys(amount)  # Số lượng
    driver.find_element(By.ID, "description").send_keys(des)  # Mô tả
    driver.find_element(By.ID, "author").send_keys(author)  # Tác giả
    driver.find_element(By.ID, "language").send_keys(language)  # Ngôn ngữ
    driver.find_element(By.ID, "year").send_keys(year)  # Năm xuất bản
    driver.find_element(By.ID, "location").send_keys(pos)  # Vị trí
    time.sleep(3)

    rank_dropdown = driver.find_element(By.ID, "rank")
    # Tạo một đối tượng Select
    select_rank = Select(rank_dropdown)
    #chon gia tri select
    select_rank.select_by_value(rank)

#chọn giá trị category
    category_value = driver.find_element(By.ID, "category")
    select_category = Select(category_value)
    select_category.select_by_value(cate)
    time.sleep(3)

#chọn giá trị publisher
    publisher_value = driver.find_element(By.ID, "publisher")
    select_publisher = Select(publisher_value)
    select_publisher.select_by_value(publisher)
    time.sleep(3)

#chọn giá trị date
    date_input = driver.find_element(By.ID, "date")
    date_input.clear()
    date_input.send_keys(date_value)

#up ảnh
    upload_element = driver.find_element(By.ID, "image")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, 'image', '1.jpeg')
    upload_element.send_keys(image_path)

    driver.find_element(By.CLASS_NAME, "submit-form").click()
    time.sleep(3)

    # Kiểm tra sản phẩm có được thêm vào hay không
    driver.get("http://localhost/mongodb/admin.php")
    time.sleep(3)

    # Kiểm tra xem sản phẩm có tồn tại trong danh sách hay không
    product_list = driver.find_elements(By.XPATH, "//div[@class='product-info']")
    product_found = False

    for product in product_list:
        product_name = product.find_element(By.CLASS_NAME, "book-brand").text  # Lấy tên sản phẩm
        if name == product_name:  # Kiểm tra tên sản phẩm
            product_found = True
            print(f"Sản phẩm '{name}' đã được thêm thành công!")
            break

    # Kiểm tra sản phẩm có tồn tại trong danh sách hay không
    assert product_found, "Sản phẩm không được thêm vào danh sách!"

#Pass_Edge_43.48s_Chorme_43.92s
#TC_20
def test_add_book_valid_value(driver):
    name = "hi"
    amount = "5"
    des = "sach moi"
    author = "LTP"
    language = "VietNam"
    year = "2024"
    pos = "dunno"
    rank = "0"
    cate = "2"
    publisher = "1"
    date_value = "01/01/2020"
    add_book(driver, name, amount, des, author, language, year, pos, rank, cate, publisher, date_value)

#Fail_Edge_39.80s_Chorme_40.46s
#TC_21
def test_add_book_blank_value(driver):
    name = ""
    amount = ""
    des = ""
    author = ""
    language = ""
    year = ""
    pos = ""
    rank = "1"
    cate = "3"
    publisher = "1"
    date_value = "01/01/2020"
    add_book(driver, name, amount, des, author, language, year, pos, rank, cate, publisher, date_value)
    page_source = driver.page_source

    # Kiểm tra xem thông báo lỗi có xuất hiện trong page source hay không
    assert "Vui lòng điền đầy đủ thông tin" in page_source, "Thông báo lỗi không hiển thị"

#Fail_Edge_39.68s_Chorme_40.58s
#TC_22
def test_add_book_missing_img(driver):
    name = "Testing"
    amount = "5"
    des = "sach moi"
    author = "LTP"
    language = "VietNam"
    year = "2024"
    pos = "dunno"
    rank = "1"
    cate = "3"
    publisher = "1"
    date_value = "01/01/2020"

    login(driver)
    driver.get("http://localhost/mongodb/admin.php")
    time.sleep(5)
    add_button = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div/a[1]/button")
    time.sleep(5)
    add_button.click()

    driver.find_element(By.ID, "name").send_keys(name)  # ten sach
    driver.find_element(By.ID, "quantity").send_keys(amount)  # Số lượng
    driver.find_element(By.ID, "description").send_keys(des)  # Mô tả
    driver.find_element(By.ID, "author").send_keys(author)  # Tác giả
    driver.find_element(By.ID, "language").send_keys(language)  # Ngôn ngữ
    driver.find_element(By.ID, "year").send_keys(year)  # Năm xuất bản
    driver.find_element(By.ID, "location").send_keys(pos)  # Vị trí
    time.sleep(3)

    rank_dropdown = driver.find_element(By.ID, "rank")
    # Tạo một đối tượng Select
    select_rank = Select(rank_dropdown)
    # chon gia tri select
    select_rank.select_by_value(rank)

    category_value = driver.find_element(By.ID, "category")
    select_category = Select(category_value)
    select_category.select_by_value(cate)
    time.sleep(3)

    publisher_value = driver.find_element(By.ID, "publisher")
    select_publisher = Select(publisher_value)
    select_publisher.select_by_value(publisher)
    time.sleep(3)

    date_input = driver.find_element(By.ID, "date")
    date_input.clear()
    date_input.send_keys(date_value)

    driver.find_element(By.CLASS_NAME, "submit-form").click()
    time.sleep(3)
    page_source = driver.page_source

    driver.get("http://localhost/mongodb/admin.php")
    time.sleep(3)

    # Kiểm tra xem sản phẩm có tồn tại trong danh sách hay không
    product_list = driver.find_elements(By.XPATH, "//div[@class='product-info']")
    product_found = False

    for product in product_list:
        product_name = product.find_element(By.CLASS_NAME, "book-brand").text  # Lấy tên sản phẩm
        if name == product_name:  # Kiểm tra tên sản phẩm
            product_found = True
            print(f"Sản phẩm '{name}' đã được thêm thành công!")
            break

    # Kiểm tra sản phẩm có tồn tại trong danh sách hay không
    assert product_found, "Sản phẩm không được thêm vào danh sách!"


    # Kiểm tra xem thông báo lỗi có xuất hiện trong page source hay không
    assert "Vui lòng điền đầy đủ thông tin" in page_source, "Thông báo lỗi không hiển thị"
    product_list = driver.find_elements(By.XPATH, "//table[@id='product-list']//tr")
    assert not any(name in product.text for product in product_list), "Sản phẩm vẫn được thêm dù không có ảnh"

#Fail_Edge_40.05s_Chorme_40.50s
#TC_23
def test_add_book_minus_amount(driver):
    name = "Testing2"
    amount = "-10"
    des = "sach moi"
    author = "LTP"
    language = "VietNam"
    year = "2024"
    pos = "dunno"
    rank = "0"
    cate = "2"
    publisher = "1"
    date_value = "01/01/2020"
    add_book(driver, name, amount, des, author, language, year, pos, rank, cate, publisher, date_value)
    assert int(amount) >= 0, "Amount cannot be negative"

    add_book(driver, name, amount, des, author, language, year, pos, rank, cate, publisher, date_value)

def add_publisher(driver,name_pub,address,phone_num):
    login(driver)
    driver.get("http://localhost/mongodb/admin.php")
    time.sleep(2)
    add_pub_button = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div/a[2]/button")
    add_pub_button.click()
    time.sleep(2)
    add_pub2_button = driver.find_element(By.ID, "new-user")
    add_pub2_button.click()
    time.sleep(2)
    driver.find_element(By.NAME, "name").send_keys(name_pub)
    driver.find_element(By.NAME, "address").send_keys(address)
    driver.find_element(By.NAME, "phone").send_keys(phone_num)
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "submit-form").click()
    time.sleep(2)

    table = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/table")
    rows = table.find_elements(By.TAG_NAME, "tr")
    # Lặp qua các hàng để kiểm tra dữ liệu
    for row in rows:
        if name_pub in row.text:
            print(f"Nhà xuất bản '{name_pub}' có trong bảng.")
            return True

    print(f"Nhà xuất bản '{name_pub}' không có trong bảng.")
    return False

#Pass_Edge_26.91s_Chorme_26.46s
#TC_24
def test_add_publisher_valid_value(driver):
    name = "LTP"
    address = "1041"
    phone_num = "123456"
    add_publisher(driver, name, address, phone_num)

#Fail_Edge_25.52s_Chorme_26.05s
#TC_25
def test_add_publisher_blank_value(driver):
    name = ""
    address = "1041"
    phone_num = ""
    time.sleep(3)
    # Gọi hàm add_publisher và kiểm tra kết quả
    result = add_publisher(driver, name, address, phone_num)

    # Kiểm tra xem kết quả trả về có phải là False không (khi thêm không thành công)
    assert not result, "Test failed: Nhà xuất bản không được phép có giá trị trống!"
    time.sleep(3)

def update_publisher(driver, name, new_name, new_address, new_phone_num):
    login(driver)
    driver.get("http://localhost/mongodb/publisher.php")
    time.sleep(5)

    # Lấy bảng nhà xuất bản
    table = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/table")
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Kiểm tra nếu nhà xuất bản tồn tại trong bảng
    found_before_edit = False
    for row in rows:
        if name in row.text:
            found_before_edit = True
            edit_button = row.find_element(By.CLASS_NAME, "confirm-btn")  # Tìm nút sửa
            edit_button.click()  # Click vào nút sửa
            time.sleep(5)
            break

#nếu không tìm thấy nxb thì out, còn nếu có thì điền lại thông tin nhà xuất bản mới
    if not found_before_edit:
        print("Không tìm thấy nhà xuất bản cần sửa.")
        return
    driver.find_element(By.NAME, "name").clear()
    driver.find_element(By.NAME, "name").send_keys(new_name)

    driver.find_element(By.NAME, "address").clear()
    driver.find_element(By.NAME, "address").send_keys(new_address)

    driver.find_element(By.NAME, "phone").clear()
    driver.find_element(By.NAME, "phone").send_keys(new_phone_num)

    time.sleep(3)

    # Lưu thay đổi
    driver.find_element(By.CLASS_NAME, "submit-form").click()
    time.sleep(3)

    table = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/table")
    rows_after_edit = table.find_elements(By.TAG_NAME, "tr")
    found_after_edit = False
#kiểm tra đã được update hay chưa
    for row in rows_after_edit:
        if new_name in row.text:
            found_after_edit = True
            break

    if found_after_edit:
        print("Sửa thành công!")
    else:
        print("Lỗi: Không thể sửa nhà xuất bản.")

#Pass_Edge_31.47s_Chorme_31.35s
#TC_26
def test_update_publisher(driver):
    name = "LTP"  # Tên nhà xuất bản cần sửa
    new_name = "LTP New"  # Tên mới
    new_address = "1234 New Address"  # Địa chỉ mới
    new_phone = "1234567890"  # Số điện thoại mới

    # Gọi hàm sửa nhà xuất bản và kiểm tra kết quả
    update_publisher(driver, name, new_name, new_address, new_phone)

    # Kiểm tra thông tin đã sửa trong bảng
    table = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/table")
    rows = table.find_elements(By.TAG_NAME, "tr")

    found_after_edit = False
    for row in rows:
        if new_name in row.text:  # Kiểm tra xem tên mới có trong bảng không
            found_after_edit = True
            break

    assert found_after_edit, "Test failed: Không tìm thấy nhà xuất bản sau khi sửa!"


def delete_publisher(driver, name):
    login(driver)
    time.sleep(5)
    driver.get("http://localhost/mongodb/publisher.php")
    time.sleep(5)

    # Lấy bảng nhà xuất bản
    table = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/table")
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Kiểm tra nếu nhà xuất bản tồn tại trong bảng
    found_before_delete = False
    for row in rows:
        if name in row.text:
            found_before_delete = True
            break

    if not found_before_delete:
        print("Không tìm thấy nhà xuất bản cần xóa.")
        return

    # Xóa nhà xuất bản
    for row in rows:
        if name in row.text:
            try:
                delete_button = row.find_element(By.CLASS_NAME, "cancel-btn")
                delete_button.click()
                time.sleep(5)

                # Chờ hộp thoại xác nhận
                WebDriverWait(driver, 5).until(EC.alert_is_present())

                # Xử lý hộp thoại xác nhận
                alert = driver.switch_to.alert
                alert.accept()  # Nhấn nút "OK"

                # Kiểm tra lại bảng sau khi xóa
                rows_after_delete = table.find_elements(By.TAG_NAME, "tr")
                found_after_delete = False
                for row in rows_after_delete:
                    if name in row.text:
                        found_after_delete = True
                        break

                if found_after_delete:
                    print("Lỗi: Nhà xuất bản vẫn còn sau khi xóa.")
                else:
                    print("Xóa thành công!")
                return

            except Exception as e:
                print(f"Có lỗi xảy ra khi xóa: {e}")
                return

#Pass_Edge_30.54s_Chorme_30.36s
#TC_27
def test_del_publisher(driver):
    name = "LTP New"
    delete_publisher(driver, name)

def add_category(driver, id_cat, name):
    login(driver)
    driver.get("http://localhost/mongodb/admin.php")
    cat_button = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div/a[3]/button")
    cat_button.click()
    time.sleep(3)
    cat_button_2 = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/a/button")
    cat_button_2.click()
    time.sleep(3)
    driver.find_element(By.XPATH, "/html/body/form/input[1]").send_keys(id_cat)
    driver.find_element(By.NAME, "name").send_keys(name)
    time.sleep(3)
    driver.find_element(By.CLASS_NAME, "submit-form").click()
    time.sleep(3)
    table = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/table")
    rows = table.find_elements(By.TAG_NAME, "tr")
    # Lặp qua các hàng để kiểm tra dữ liệu
    for row in rows:
        if name in row.text:
            print(f"Thể loại sách '{name}' có trong bảng.")
            return True

    print(f"Thể loại sách '{name}' không có trong bảng.")
    return False

#Pass_Edge_33.73s_Chorme_28.39s
#TC_28
def test_add_category(driver):
    id_cat = "5"
    name = "Testing"
    add_category(driver, id_cat, name)

#Fail_Edge_25.02s_Chorme_25.60s
#TC_29
def test_add_blank_category(driver):
    id_cat = ""
    name = "Testing2"
    result = add_category(driver, id_cat, name)

    # Kiểm tra xem kết quả trả về có phải là False không (khi thêm không thành công)
    assert not result, "Test failed: Thể loại không được phép có giá trị trống!"
    time.sleep(3)

def update_category(driver, id_cat, new_id_cat, new_name):
    login(driver)
    driver.get("http://localhost/mongodb/category.php")
    time.sleep(5)

    # Lấy bảng nhà xuất bản
    table = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/table")
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Kiểm tra nếu nhà xuất bản tồn tại trong bảng
    found_before_edit = False
    for row in rows:
        if id_cat in row.text:
            found_before_edit = True
            edit_button = row.find_element(By.CLASS_NAME, "confirm-btn")  # Tìm nút sửa
            edit_button.click()  # Click vào nút sửa
            time.sleep(5)
            break

    if not found_before_edit:
        print("Không tìm thấy thể loại cần sửa.")
        return
    driver.find_element(By.XPATH, "/html/body/form/input[1]").clear()
    driver.find_element(By.XPATH, "/html/body/form/input[1]").send_keys(new_id_cat)

    driver.find_element(By.NAME, "name").clear()
    driver.find_element(By.NAME, "name").send_keys(new_name)
    time.sleep(3)

    # Lưu thay đổi
    driver.find_element(By.CLASS_NAME, "submit-form").click()
    time.sleep(3)

    table = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/table")
    rows_after_edit = table.find_elements(By.TAG_NAME, "tr")
    found_after_edit = False
    for row in rows_after_edit:
        if new_name in row.text:
            found_after_edit = True
            break

    if found_after_edit:
        print("Sửa thành công!")
    else:
        print("Lỗi: Không thể sửa thể loại.")

#Pass_Edge_31.76s_chorme_31.30s
#TC_30
def test_update_category(driver):
    id_cat = "5"
    new_id_cat = "5 New"
    new_name = "Testing New"

    # Gọi hàm sửa nhà xuất bản và kiểm tra kết quả
    update_category(driver, id_cat, new_id_cat, new_name)

    # Kiểm tra thông tin đã sửa trong bảng
    table = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/table")
    rows = table.find_elements(By.TAG_NAME, "tr")

    found_after_edit = False
    for row in rows:
        if new_name in row.text:  # Kiểm tra xem tên mới có trong bảng không
            found_after_edit = True
            break

    assert found_after_edit, "Test failed: Không tìm thấy nhà xuất bản sau khi sửa!"

def delete_category(driver, name):
    login(driver)
    driver.get("http://localhost/mongodb/category.php")
    time.sleep(5)

    table = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/table")
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Kiểm tra nếu the loai sach tồn tại trong bảng
    found_before_delete = False
    for row in rows:
        if name in row.text:
            found_before_delete = True
            break

    if not found_before_delete:
        print("Không tìm thấy the loai cần xóa.")
        return

    # Xóa nhà xuất bản
    for row in rows:
        if name in row.text:
            try:
                delete_button = row.find_element(By.CLASS_NAME, "cancel-btn")
                delete_button.click()
                time.sleep(5)

                # Chờ hộp thoại xác nhận
                WebDriverWait(driver, 5).until(EC.alert_is_present())

                # Xử lý hộp thoại xác nhận
                alert = driver.switch_to.alert
                alert.accept()  # Nhấn nút "OK"

                # Kiểm tra lại bảng sau khi xóa
                rows_after_delete = table.find_elements(By.TAG_NAME, "tr")
                found_after_delete = False
                for row in rows_after_delete:
                    if name in row.text:
                        found_after_delete = True
                        break

                if found_after_delete:
                    print("Lỗi: The loai sach vẫn còn sau khi xóa.")
                else:
                    print("Xóa thành công!")
                return

            except Exception as e:
                print(f"Có lỗi xảy ra khi xóa: {e}")
                return

#Pass_Edge_24.97s_Chorme_24.86s
#TC_31
def test_del_category(driver):
    name = "Testing New"
    delete_category(driver, name)

#Pass_Edge_31.70s_Chorme_35.69s
#TC_32
def test_watch_book_list(driver):
    login(driver)
    driver.get("http://localhost/mongodb/report.php")
    time.sleep(3)

    # Đợi cho bảng xuất hiện và lấy nó
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/table"))
    )

    # Lấy tất cả các hàng trong bảng
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Kiểm tra số lượng hàng
    assert len(rows) > 0, "Không có hàng nào trong bảng."

    # Lấy tổng số sách bằng cách lấy ID của cuốn sách cuối cùng
    total_books = len(rows) - 1  # Vì hàng đầu tiên là tiêu đề
    print(f"Tổng số sách: {total_books}")

    # Lặp qua các hàng và lấy thông tin (chỉ lấy 3 cuốn đầu tiên)
    for row in rows[1:4]:  # Chỉ lấy 3 cuốn sách đầu tiên
        # Lấy thông tin từ các ô
        cells = row.find_elements(By.TAG_NAME, "td")

        if len(cells) >= 4:  # Kiểm tra số lượng ô trong mỗi hàng
            book_id = cells[0].text  # Lấy ID
            book_name = cells[1].text  # Lấy tên sách

            # Lấy lượt mượn và lượt thêm vào wishlist
            borrow_stat = cells[2].text  # Giả sử là ô 3
            adding_stat = cells[3].text  # Giả sử là ô 4

            # In thông tin sách mà không có "Xem Chi Tiết Sách"
            print(f"ID: {book_id}, Tên Sách: {book_name}, Lượt mượn: {borrow_stat}, Lượt thêm vào wishlist: {adding_stat}")

def watch_list_penalize(driver,value):
    login(driver)
    driver.get("http://localhost/mongodb/report.php")
    time.sleep(3)
    # Chờ thẻ <select> xuất hiện trên trang
    select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='cate']"))
    )

    # Tạo đối tượng Select để tương tác với thẻ <select>
    select = Select(select_element)

    # Chọn <option> có giá trị value="1"
    select.select_by_value(value)  # Hoặc có thể dùng 'select_by_visible_text' nếu bạn biết văn bản hiển thị

    watch_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div[1]/button"))
    )
    watch_button.click()

    
#Pass_Edge_36.59s_Chorme_42.13s
#TC_33
def test_watch_list_penalize(driver):
    value = "1"
    watch_list_penalize(driver, value)
    
    
def watch_overall(driver, start_date, end_date):
    login(driver)
    driver.get("http://localhost/mongodb/report.php")
    time.sleep(3)

    # Chọn trường ngày bắt đầu
    start_date_el = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/form/div/div/input[1]"))
    )
    start_date_el.send_keys(start_date)
    time.sleep(3)

    # Chọn trường ngày kết thúc (sửa lỗi, dùng end_date_el thay vì start_date_el)
    end_date_el = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/form/div/div/input[2]"))
    )
    end_date_el.send_keys(end_date)  # Sửa lỗi ở đây
    time.sleep(3)

    confirm_button = driver.find_element(By.XPATH,"/html/body/div[3]/form/div/div/div/button")
    confirm_button.click()

    # Lấy thông tin ngày từ trang
    info_date_el = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "info-date"))
    )
    info_date = info_date_el.text
    print(f"Ngày thông tin: {info_date}")

    # Lấy thông tin tổng quát
    info_div_el = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div[1]"))
    )
    info_text = info_div_el.text
    print(f"Thông tin tổng quát: {info_text}")

#Pass_Edge_51.86s_Chorme_59.13s
#TC_34
def test_watch_overall_valid_date(driver):
    start_date = "01/01/2020"
    end_date = "11/01/2024"
    assert start_date == "01/01/2020", "Ngày bắt đầu không hợp lệ"
    assert end_date == "11/01/2024", "Ngày kết thúc không hợp lệ"

    watch_overall(driver, start_date, end_date)

#Fail_Edge_46.15s_Chorme_53.76s
#TC_35
def test_watch_overall_invalid_date_range(driver):
    start_date = "01/01/2030"
    end_date = "01/01/2020"  # Ngày kết thúc trước ngày bắt đầu

    # Thực thi hàm và kiểm tra thông báo lỗi
    try:
        watch_overall(driver, start_date, end_date)
        pytest.fail("Chưa có thông báo lỗi khi ngày kết thúc trước ngày bắt đầu")
    except Exception as e:
        assert "Ngày kết thúc phải lớn hơn hoặc bằng ngày bắt đầu" in str(e), f"Thông báo lỗi không khớp: {str(e)}"

#Fail_Edge_47.40s_Chorme_55.75s
#TC_36
def test_watch_overall_invalid_date_format(driver):
    start_date = "2020-01-01"  # Định dạng sai
    end_date = "2024-11-01"  # Định dạng sai

    # Thực thi hàm và kiểm tra thông báo lỗi
    try:
        watch_overall(driver, start_date, end_date)
        pytest.fail("Chưa có thông báo lỗi khi ngày có định dạng không hợp lệ")
    except Exception as e:
        assert "Định dạng ngày không hợp lệ" in str(e), f"Thông báo lỗi không khớp: {str(e)}"