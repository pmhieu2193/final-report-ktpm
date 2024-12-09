# ====================== Đăng nhập =====================#
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    prefs = {
        'autofill.profile_enabled': False
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

def get_clickable_element(driver, by: By, arg, timeout = 10):
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, arg))
    )
    return element

# ============= Test các chức năng đăng nhập của user =============

#Test đăng nhập thành công
#passed in 11.79s
#TC_DN_01
def test_valid_login(driver):
    #Kết nối đến web
    driver.get("http://localhost/mongodb/")
    time.sleep(1)
    #Chọn nút đăng nhập
    user_icon = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a")
    user_icon.click()
    time.sleep(0.5)
    login_button = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a//div//button")
    login_button.click()
    time.sleep(1)
    #Điền thông tin và đăng nhập
    driver.find_element(By.NAME, "email").send_keys("lmt@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("lmt123")
    
    login_button = get_clickable_element(driver, By.XPATH, "//form//button")
    login_button.click()
    time.sleep(1)
    current_url = driver.current_url
    assert "http://localhost/mongodb/index.php" in current_url

# Test đăng nhập sai mật khẩu
#passed in 10.66s
#TC_DN_02
def test_login_with_wrong_password(driver):
        #Kết nối đến web
    driver.get("http://localhost/mongodb/")

    #Chọn nút đăng nhập
    user_icon = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a")
    user_icon.click()
    time.sleep(0.5)
    login_button = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a//div//button")
    login_button.click()
    time.sleep(1)
    #Điền thông tin và đăng nhập
    driver.find_element(By.NAME, "email").send_keys("lmt@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123lmt")
    login_button = get_clickable_element(driver, By.XPATH, "//form//button")
    #Nhấn đăng nhập
    login_button.click()
    time.sleep(1)
    message = driver.find_element(By.XPATH, "//div[@class='container']/form/a").text
    assert "Incorect!" in message

# Test đăng nhập khi để trống thông tin
# passed in 10.58s
#TC_DN_03
def test_login_with_blank_fields(driver):
        #Kết nối đến web
    driver.get("http://localhost/mongodb/")

    #Chọn nút đăng nhập
    user_icon = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a")
    user_icon.click()
    time.sleep(0.5)
    login_button = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a//div//button")
    login_button.click()
    time.sleep(1)
    #Điền thông tin và đăng nhập
    driver.find_element(By.NAME, "email").send_keys("")
    driver.find_element(By.NAME, "password").send_keys("")
    
    login_button = get_clickable_element(driver, By.XPATH, "//form//button")
    #Nhấn đăng nhập
    login_button.click()
    time.sleep(1)
    message = driver.find_element(By.XPATH, "//div[@class='container']/form/a").text
    assert "Không được để trống Email" in message

# Test đăng nhập khi để trống mật khẩu
# passed in 10.62s
#TC_DN_04
def test_login_with_blank_password_field(driver):
        #Kết nối đến web
    driver.get("http://localhost/mongodb/")

    #Chọn nút đăng nhập
    user_icon = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a")
    user_icon.click()
    time.sleep(0.5)
    login_button = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a//div//button")
    login_button.click()
    time.sleep(1)
    #Điền thông tin và đăng nhập
    driver.find_element(By.NAME, "email").send_keys("lmt@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("")
    login_button = get_clickable_element(driver, By.XPATH, "//form//button")
    #Nhấn đăng nhập
    login_button.click()
    time.sleep(1)
    message = driver.find_element(By.XPATH, "//div[@class='container']/form/a").text
    assert "Không được để trống tài khoản" in message

# Test đăng nhập khi điền email không đúng
# passed in 10.63s
#TC_DN_05
def test_login_with_wrong_email(driver):
    #Kết nối đến web
    driver.get("http://localhost/mongodb/")

    #Chọn nút đăng nhập
    user_icon = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a")
    user_icon.click()
    time.sleep(0.5)
    login_button = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a//div//button")
    login_button.click()
    time.sleep(1)
    #Điền thông tin và đăng nhập
    driver.find_element(By.NAME, "email").send_keys("lmt")
    driver.find_element(By.NAME, "password").send_keys("lmt123")
    login_button = get_clickable_element(driver, By.XPATH, "//form//button")
    #Nhấn đăng nhập
    login_button.click()
    time.sleep(1)
    message = driver.find_element(By.XPATH, "//div[@class='container']/form/a").text
    assert "Incorect!" in message

#Test đăng nhập bằng tài khoản đã bị khóa
#Test fail vì vẫn đăng nhập được
#TC_DN_06
def test_login_with_banned_account(driver):
    #Kết nối đến web
    driver.get("http://localhost/mongodb/")

    #Chọn nút đăng nhập
    user_icon = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a")
    user_icon.click()
    time.sleep(0.5)
    login_button = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a//div//button")
    login_button.click()
    time.sleep(1)
    #Điền thông tin và đăng nhập
    driver.find_element(By.NAME, "email").send_keys("lmtt@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("lmt123")
    login_button = get_clickable_element(driver, By.XPATH, "//form//button")
    #Nhấn đăng nhập
    login_button.click()
    time.sleep(1)
    message = driver.find_element(By.XPATH, "//div[@class='container']/form/a").text
    assert "Tài khoản của bạn đã bị khoá!" in message

# Test nosql injection
# passed in 10.74s
#TC_DN_07
def test_nosql_injection(driver):
        #Kết nối đến web
    driver.get("http://localhost/mongodb/")

    #Chọn nút đăng nhập
    user_icon = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a")
    user_icon.click()
    time.sleep(0.5)
    login_button = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a//div//button")
    login_button.click()
    time.sleep(1)
    #Điền thông tin và đăng nhập
    driver.find_element(By.NAME, "email").send_keys(f"admin'; return '' == '")
    driver.find_element(By.NAME, "password").send_keys("lmt123")
    login_button = get_clickable_element(driver, By.XPATH, "//form//button")
    #Nhấn đăng nhập
    login_button.click()
    time.sleep(1)
    message = driver.find_element(By.XPATH, "//div[@class='container']/form/a").text
    assert "Incorect!" in message

#Test chức năng đăng xuất
# passed in 13.74s
#TC_DN_08
def test_logout(driver):
    #Thực hiện đăng nhập thành công
    test_valid_login(driver)
    user_icon = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a")
    user_icon.click()
    time.sleep(0.5)
    #Ấn nút đăng xuất
    logout_button = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a//div//button")
    logout_button.click()
    time.sleep(1)
    #Sau khi đăng xuất thì trở lại trang chủ để kiểm tra
    return_to_homepage = get_clickable_element(driver, By.XPATH, "//a[text()='quay lại trang chủ']")
    return_to_homepage.click()
    user_icon = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a")
    user_icon.click()
    message = driver.find_element(By.XPATH, "//div[@class='login-logout-popup']//p").text
    assert "Chưa Đăng Nhập" in message


# ====================== tìm kiếm =====================#

#Test chức năng tìm kiếm khi để trống
# passed in 10.01s
#TC_TK_01
def test_find_product_with_blank_keyword(driver):
        #Kết nối đến web
    driver.get("http://localhost/mongodb/")
    time.sleep(1)
    #Nhập thông tin tìm kiếm
    driver.find_element(By.NAME, "timkiem").send_keys("")
    search_btn = get_clickable_element(driver, By.XPATH, "//button[text()='Tìm kiếm']")
    search_btn.click()
    time.sleep(1)
    
    #Tìm kiếm kết quả
    message = driver.find_element(By.XPATH, "//body").text
    assert "Vui lòng nhập từ khóa tìm kiếm." in message

#Test chức năng tìm kiếm sản phẩm không tồn tại
# passed in 11.16s
#TC_TK_02
def test_find_product_that_not_exist(driver):
    #Kết nối đến web
    driver.get("http://localhost/mongodb/")
    time.sleep(1)
    #Nhập thông tin tìm kiếm
    driver.find_element(By.NAME, "timkiem").send_keys("Album")
    search_btn = get_clickable_element(driver, By.XPATH, "//button[text()='Tìm kiếm']")
    search_btn.click()
    time.sleep(1)
    
    #Tìm kiếm kết quả
    message = driver.find_element(By.XPATH, "//h3").text
    time.sleep(1)
    assert "Không tìm thấy sách." in message

#Test chức năng tìm kiếm đúng sách
# passed in 13.09s
#TC_TK_03
def test_find_speciic_product(driver):
        #Kết nối đến web
    driver.get("http://localhost/mongodb/")
    time.sleep(1)
    #Nhập thông tin tìm kiếm
    driver.find_element(By.NAME, "timkiem").send_keys("Sách lập trình python")
    time.sleep(1)
    search_btn = get_clickable_element(driver, By.XPATH, "//button[text()='Tìm kiếm']")
    search_btn.click()
    time.sleep(2)
    
    #Tìm kiếm kết quả
    book_name = driver.find_element(By.XPATH, "//div[@class='product-card']").text
    time.sleep(1)
    assert "SÁCH LẬP TRÌNH PYTHON" in book_name

#Test chức năng tìm kiếm bằng 1 phần của tên sản phẩm đúng
# passed in 13.03s
#TC_TK_04
def test_find_product_with_keyword(driver):
    keyword = "sách"
    #Kết nối đến web
    driver.get("http://localhost/mongodb/")
    time.sleep(1)
    #Nhập thông tin tìm kiếm
    driver.find_element(By.NAME, "timkiem").send_keys(keyword)
    time.sleep(1)
    search_btn = get_clickable_element(driver, By.XPATH, "//button[text()='Tìm kiếm']")
    search_btn.click()
    time.sleep(2)
    
    #Tìm kiếm kết quả
    elements = driver.find_elements(By.XPATH, "//div[@class='product-card']")
    time.sleep(1)
    book_names = list(map(lambda element: element.text, elements))
    for book_name in book_names:
        assert keyword.upper() in book_name

#Test chức năng tìm kiếm sách bị ẩn
#Fail vì các sách ẩn vẫn hiển thị
#TC_TK_05
def test_find_hidden_product(driver):
    keyword = "TEST"
    #Kết nối đến web
    driver.get("http://localhost/mongodb/")
    time.sleep(1)
    #Nhập thông tin tìm kiếm
    driver.find_element(By.NAME, "timkiem").send_keys(keyword)
    time.sleep(1)
    search_btn = get_clickable_element(driver, By.XPATH, "//button[text()='Tìm kiếm']")
    search_btn.click()
    time.sleep(2)
    
    #Tìm kiếm kết quả
    books = driver.find_elements(By.XPATH, "//div[@class='product-card']")
    time.sleep(1)
    #Kiểm tra testcase
    if len(books) == 0:
        message = driver.find_element(By.XPATH, "//h3").text
        assert "Không tìm thấy sách." in message
    for book_name in books:
        assert keyword.upper() not in book_name.text

#Test chức năng lọc theo thể loại
# passed in 14.25s
#TC_TK_06
def test_product_type_filter(driver):
    #Kết nối đến web
    driver.get("http://localhost/mongodb/")
    time.sleep(1)

    categories = driver.find_elements(By.XPATH, "//select[@name='ma_the_loai']//option")
    for i in range(1, len(categories)):
        option = get_clickable_element(driver, By.XPATH, "//select[@name='ma_the_loai']")
        option.click()
        option.send_keys(Keys.DOWN)
        option.click()
        books = driver.find_elements(By.XPATH, "//div[@class='product-card']")
        assert len(books) > 0
        time.sleep(1)

# ====================== Quản lý người dung =====================#

#Test đăng nhập bằng tài khoản admin
# passed in 11.73s
#TC_UM_01
def test_login_with_admin_account(driver):
    #Kết nối đến web
    driver.get("http://localhost/mongodb/")
    time.sleep(1)
    #Chọn nút đăng nhập
    user_icon = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a")
    user_icon.click()
    time.sleep(0.5)
    login_button = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a//div//button")
    login_button.click()
    time.sleep(1)
    #Điền thông tin và đăng nhập
    driver.find_element(By.NAME, "email").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("123")
    
    login_button = get_clickable_element(driver, By.XPATH, "//form//button")
    login_button.click()
    time.sleep(1)
    current_url = driver.current_url
    assert "http://localhost/mongodb/checkin.php" in current_url

#Test đăng xuất khỏi trang admin
# passed in 11.78s
def test_logout_admin_acoount(driver):
    #Đăng nhập vào trang admin
    test_login_with_admin_account(driver)
    #Ấn nút đăng xuất
    logout_btn = get_clickable_element(driver, By.XPATH, "//form[@action='logout.php']/button")
    logout_btn.click()
    assert "http://localhost/mongodb/login.php" in driver.current_url

#Test điều hướng đến phần quản lý người dùng
# passed in 15.02s
#TC_UM_02
def test_navigate_to_user_management(driver):
    test_login_with_admin_account(driver)

    user_nav = get_clickable_element(driver, By.XPATH, "//div[@class='nav-space']/p[text()='Quản lý tài khoản']")
    user_nav.click()

    assert "http://localhost/mongodb/user.php" in driver.current_url


# =================== Quản lý người dùng ===================


#Test nếu input rỗng
# passed in 17.11s
#TC_UM_03
def test_find_user_with_empty_input(driver):
    test_navigate_to_user_management(driver)

    keyword = ""
    #Nhập keyword và ấn nút tìm kiếm
    driver.find_element(By.XPATH, "//input[@name='value_search']").send_keys(keyword)
    search_btn = get_clickable_element(driver, By.XPATH, "//button[text()='⚲ Tìm kiếm']")
    search_btn.click()
    #Đợi kết quả
    time.sleep(2)
    #Lấy kết quả
    results = driver.find_elements(By.XPATH, "//table/tbody//tr")
    #Vì keyword rỗng nên kq trả về toàn bộ user, len>1 vì element đầu tiên là header nên không tính
    assert len(results) > 1

#Test bằng 1 email cụ thể
# passed in 16.38s
#TC_UM_04
def test_find_user_with_valid_email_input(driver, keyword=None):
    test_navigate_to_user_management(driver)

    cur_keyword = keyword if keyword else "lmt2@gmail.com"
    #Nhập keyword và ấn nút tìm kiếm
    driver.find_element(By.XPATH, "//input[@name='value_search']").send_keys(cur_keyword)
    search_btn = get_clickable_element(driver, By.XPATH, "//button[text()='⚲ Tìm kiếm']")
    search_btn.click()
    #Đợi kết quả
    time.sleep(2)
    #Lấy kết quả
    results = driver.find_elements(By.XPATH, "//table/tbody//tr//td[1]")
    #dùng lower vì phần hiển thị email luôn viết hoa chữ cái đầu
    #Lấy phần tử thứ 1 vì 0 là header
    assert cur_keyword in str(results[0].text).lower()

#Test tìm kiếm user bằng keyword
# passed in 17.25s
#TC_UM_05
def test_find_user_by_keyword(driver):
    test_navigate_to_user_management(driver)

    keyword = "lmt"
    #Nhập keyword và ấn nút tìm kiếm
    driver.find_element(By.XPATH, "//input[@name='value_search']").send_keys(keyword)
    search_btn = get_clickable_element(driver, By.XPATH, "//button[text()='⚲ Tìm kiếm']")
    search_btn.click()
    #Đợi kết quả
    time.sleep(2)
    #Lấy kết quả
    results = driver.find_elements(By.XPATH, "//table/tbody//tr//td[1]")
    #dùng lower vì phần hiển thị email luôn viết hoa chữ cái đầu
    #Lấy phần tử thứ 1 vì 0 là header
    for i in range(1, len(results)):
        current_user = str(results[i].text).lower()
        assert keyword in current_user

#Test tìm kiếm 1 user chưa đăng ký
# passed in 16.69s
#TC_UM_06
def test_find_not_registed_user(driver, keyword=None):
    test_navigate_to_user_management(driver)

    #email chưa được đăng ký trong db
    cur_keyword = keyword if keyword else "asdlmt123987@gmail.com"
    #Nhập keyword và ấn nút tìm kiếm
    driver.find_element(By.XPATH, "//input[@name='value_search']").send_keys(cur_keyword)
    search_btn = get_clickable_element(driver, By.XPATH, "//button[text()='⚲ Tìm kiếm']")
    search_btn.click()
    #Đợi kết quả
    time.sleep(2)
    #Lấy kết quả
    results = driver.find_elements(By.XPATH, "//table/tbody//tr")
    
    #len == 1 vì driver lấy header
    assert len(results) == 1

#test bộ lọc số lượng
# passed in 30.06s
#TC_UM_07
def test_filter_by_num(driver):
    test_navigate_to_user_management(driver)

    #default là 10 nhưng lúc load thì sẽ hiển thị toàn bộ
    for i in range (1, 4):
        driver.find_element(By.XPATH, "//body").send_keys(Keys.HOME)

        num_filter = get_clickable_element(driver, By.XPATH, "//div//select[@name='num']")
        num_filter.click()
        num_filter.send_keys(Keys.DOWN)
        num_filter = get_clickable_element(driver, By.XPATH, "//div//select[@name='num']")
        num_filter.send_keys(Keys.ENTER)
        time.sleep(1)
        select_box = driver.find_element(By.NAME, "num")
        select = Select(select_box)
        # Lấy giá trị của option đang được chọn (value)
        selected_option = select.first_selected_option  # Lấy option đang được chọn
        selected_value = selected_option.get_attribute('value')  # Lấy giá trị 'value'
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Cuộn xuống dưới cùng của trang
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Đợi một chút để trang tải thêm phần tử (có thể điều chỉnh thời gian này)
            time.sleep(2)

            # Kiểm tra chiều cao của trang web sau khi cuộn
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            # Nếu không thay đổi chiều cao, có nghĩa là đã tải xong tất cả phần tử
            if new_height == last_height:
                break
            last_height = new_height
        
        results = driver.find_elements(By.XPATH, "//table/tbody//tr")
        #Vì khi chọn hiển thị thì option sẽ tự động cập nhật thành 10 user nên sẽ có điều kiện này
        #check len>31 vì set up db có nhiều hơn 31 user
        if int(selected_value) == 10:
            assert len(results) > 31
        else:
            assert len(results) == int(selected_value)+1

#test bộ lọc trạng thái
# passed in 35.55s
#TC_UM_08
def test_status_filter(driver):
    test_navigate_to_user_management(driver)
    status = {
        "0" : "Chưa được duyệt",
        "1" : "Đã được duyệt",
        "-1": "Đã từ chối",
        "2": "Tài khoản đã bị khoá"
    }
    #tính số lượng các option để loop
    options = driver.find_elements(By.XPATH, "//select[@name='status']//option")
    for i in range (0, len(options)-1):
        time.sleep(1)
        driver.find_element(By.XPATH, "//body").send_keys(Keys.HOME)
        time.sleep(0.5)
        #Chọn filter
        status_filter = get_clickable_element(driver, By.XPATH, "//div//select[@name='status']")
        status_filter.click()
        status_filter.send_keys(Keys.DOWN)
        status_filter = get_clickable_element(driver, By.XPATH, "//div//select[@name='status']")
        status_filter.send_keys(Keys.ENTER)
        time.sleep(1)
        #Lấy giá trị option
        select_box = driver.find_element(By.NAME, "status")
        select = Select(select_box)
        # Lấy giá trị của option đang được chọn (value)
        selected_option = select.first_selected_option  # Lấy option đang được chọn
        selected_value = selected_option.get_attribute('value')
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Cuộn xuống dưới cùng của trang
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Đợi một chút để trang tải thêm phần tử (có thể điều chỉnh thời gian này)
            time.sleep(2)

            # Kiểm tra chiều cao của trang web sau khi cuộn
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            # Nếu không thay đổi chiều cao, có nghĩa là đã tải xong tất cả phần tử
            if new_height == last_height:
                break
            last_height = new_height
        
        #Lấy thông tin user
        results = driver.find_elements(By.XPATH, "//table/tbody//tr//td[3]")
        #Kiểm tra từng user
        for i in range(1, len(results)):
            assert status[selected_value].lower() in str(results[i].text).lower()

#test bộ lọc phân loại người dùng
#Fail vì lọc không hoạt động
#TC_UM_09
def test_user_type_filter(driver):
    test_navigate_to_user_management(driver)
    #tính số lượng các option để loop
    options = driver.find_elements(By.XPATH, "//select[@name='role']//option")
    for i in range (0, len(options)):
        time.sleep(1)
        driver.find_element(By.XPATH, "//body").send_keys(Keys.HOME)

        #Chọn filter
        type_filter = get_clickable_element(driver, By.XPATH, "//div//select[@name='role']")
        type_filter.click()
        type_filter.send_keys(Keys.DOWN)
        type_filter = get_clickable_element(driver, By.XPATH, "//div//select[@name='role']")
        type_filter.send_keys(Keys.ENTER)
        time.sleep(1)
        #Lấy giá trị option
        select_box = driver.find_element(By.NAME, "role")
        select = Select(select_box)
        # Lấy giá trị của option đang được chọn (value)
        selected_option = select.first_selected_option  # Lấy option đang được chọn
        selected_value = selected_option.text
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Cuộn xuống dưới cùng của trang
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Đợi một chút để trang tải thêm phần tử (có thể điều chỉnh thời gian này)
            time.sleep(2)

            # Kiểm tra chiều cao của trang web sau khi cuộn
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            # Nếu không thay đổi chiều cao, có nghĩa là đã tải xong tất cả phần tử
            if new_height == last_height:
                break
            last_height = new_height
        
        #Lấy thông tin user
        
        results = driver.find_elements(By.XPATH, "//table/tbody//tr//td[4]")
        #Kiểm tra từng user
        for i in range(1, len(results)):
            assert selected_value.lower() in str(results[i].text).lower()

#Test áp dụng nhiều bộ lọc
# passed in 20.35s
#TC_UM_10
def test_multi_filter(driver):
    test_navigate_to_user_management(driver)
    #Chọn filter
    num_filter = get_clickable_element(driver, By.XPATH, "//div//select[@name='num']")
    num_filter.click()
    num_filter.send_keys(Keys.DOWN)
    num_filter.send_keys(Keys.ENTER)

    status_filter = get_clickable_element(driver, By.XPATH, "//div//select[@name='status']")
    status_filter.click()
    status_filter.send_keys(Keys.DOWN)
    status_filter.send_keys(Keys.ENTER)
    time.sleep(1)
    
    #vì chỉ check 1 lần nên không cần lấy value
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Cuộn xuống dưới cùng của trang
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Đợi một chút để trang tải thêm phần tử (có thể điều chỉnh thời gian này)
        time.sleep(2)

        # Kiểm tra chiều cao của trang web sau khi cuộn
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Nếu không thay đổi chiều cao, có nghĩa là đã tải xong tất cả phần tử
        if new_height == last_height:
            break
        last_height = new_height
    
    #Lấy thông tin user
    num_results = driver.find_elements(By.XPATH, "//table/tbody//tr")
    status_results = driver.find_elements(By.XPATH, "//table/tbody//tr//td[3]")
    #Kiểm tra từng user
    assert len(num_results) == 21
    for i in range(1, len(status_results)):
        assert "Chưa được duyệt".lower() in str(status_results[i].text).lower()  

#Test add nhiều tài khoản bằng admin
#Cái này để thêm nhiều tài khoản nhằm mục đích có dữ liệu để test nên không thêm vào đồ án
# passed in 21.72s khi tạo 1 tài khoản
#TC_UM_11
def test_add_multi_user(driver):
    #Kết nối đến web
    driver.get("http://localhost/mongodb/")
    time.sleep(1)
    #Chọn nút đăng nhập
    user_icon = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a")
    user_icon.click()
    time.sleep(0.5)
    login_button = get_clickable_element(driver, By.XPATH, "//div[@class='nav-items']//a//div//button")
    login_button.click()
    time.sleep(1)
    #Điền thông tin và đăng nhập

    for i in range(0, 1):
        #Đăng nhập admin
        driver.find_element(By.NAME, "email").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("123")
        login_button = get_clickable_element(driver, By.XPATH, "//form//button")
        login_button.click()    
        #Điều hướng sang quản lý user
        user_nav = get_clickable_element(driver, By.XPATH, "//div[@class='nav-space']/p[text()='Quản lý tài khoản']")
        user_nav.click()
        time.sleep(0.5)
        #Chọn nút thêm user
        add_new_user = get_clickable_element(driver, By.ID, "new-user")
        add_new_user.click()
        time.sleep(0.5)
        #Điền thông tin
        random_sdt = randint(111111, 999999)
        random_cccd = randint(100000, 999999)
        driver.find_element(By.NAME, "email").send_keys(f"nguoidung{i}@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("lmt123")
        driver.find_element(By.NAME, "name").send_keys(f"nguoidung {i}")
        driver.find_element(By.NAME, "number").send_keys(f"0{random_sdt+i}")
        driver.find_element(By.NAME, "cccd").send_keys(f"083{random_cccd+i}")
        driver.find_element(By.NAME, "address").send_keys("lVieejt Nam")

        sex_btn = get_clickable_element(driver, By.XPATH, "//input[@name='gender']")
        sex_btn.click()
        driver.find_element(By.XPATH, "//input[@type='date']").send_keys("06232003")
        driver.find_element(By.XPATH, "//body").send_keys(Keys.PAGE_DOWN)

        submit_btn = get_clickable_element(driver, By.XPATH, "//button[text()='Tạo Tài Khoản']")
        submit_btn.click()
        time.sleep(5)
        message = driver.find_element(By.XPATH, "//div[@class='container']/form/a").text
        assert "Tạo tài khoản thành công, vui vòng đăng nhập" in message


#Test chức năng xem chi tiết tài khoản user
# passed in 16.83s
#TC_UM_12
def test_user_detail(driver, keyword=None):
    #modify phần này để sử dụng lại việc check thông tin user sau khi thay đổi thông tin
    if keyword:
        test_find_user_with_valid_email_input(driver, keyword)
    else:
        test_navigate_to_user_management(driver)

    #Lấy thông tin của người dùng thứ index+1, vd: người dùng 1 thì index = 1+1
    index = 2
    user_info = driver.find_elements(By.XPATH, f"//table/tbody//tr[{index}]//td")
    #lưu thông tin vào 1 dict
    dict_user_info = {
        "Email": str(user_info[0].text).lower(),
        "name": str(user_info[1].text).lower(),
        "Status": str(user_info[2].text).lower(),
        "create_day": str(user_info[4].text).lower()
    }
    
    #Chọn nút chi tiết
    user_detail_btn = get_clickable_element(driver, By.XPATH, f"//table/tbody//tr[{index}]//td[6]//form//button")
    user_detail_btn.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//body").send_keys(Keys.END)
    time.sleep(1)
    user_email = driver.find_element(By.XPATH, "//div[@class='form']/div/h3").text
    user_name = driver.find_element(By.NAME, "ten").get_attribute('value')
    user_status = driver.find_element(By.XPATH, "//select[@name='status']").text
    
    #default role khi tải trang luôn là sinh viên nên không check nữa
    # user_role = driver.find_element(By.NAME, "rank")
    # select = Select(user_role)
    # # Lấy giá trị của option đang được chọn (value)
    # selected_option = select.first_selected_option  # Lấy option đang được chọn
    # selected_value = selected_option.text
    
    user_create_day = driver.find_element(By.XPATH, "//div[@class='form']/div/p").text

    assert dict_user_info['Email'] in user_email
    assert dict_user_info['name'] in user_name
    assert dict_user_info['Status'] in str(user_status).lower()
    assert dict_user_info['create_day'] in user_create_day

#Test chức năng thay đổi thông tin tài khoản
#Fail vì chức năng cập nhật sai
#TC_UM_13
def test_change_user_info(driver):
    #tìm kiếm user bằng email
    email = "lmt@gmail.com"
    test_find_user_with_valid_email_input(driver, email)

    #chọn nút xem chi tiết
    user_detail_btn = get_clickable_element(driver, By.XPATH, "//table/tbody//tr[2]//td[6]//form//button")
    user_detail_btn.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//body").send_keys(Keys.END)
    time.sleep(1)

    new_name = "RanDom Tri"
    new_role = "Công chức"

    #Đổi thành tên mới
    user_name = driver.find_element(By.NAME, "ten")
    user_name.clear()
    user_name.send_keys(new_name)
    
    #đổi role mới
    user_role = driver.find_element(By.NAME, "rank")
    select = Select(user_role)
    # Lấy giá trị của option đang được chọn (value)
    select.select_by_visible_text(new_role)
    
    tac = get_clickable_element(driver, By.NAME, "tac")
    tac.click()

    save_btn = get_clickable_element(driver, By.XPATH, "//div[@class='buttons']//button[1]")
    save_btn.click()

    test_find_user_with_valid_email_input(driver, email)

    user_info = driver.find_elements(By.XPATH, f"//table/tbody//tr[2]//td")

    assert new_name == user_info[1].text
    assert new_role.lower() == str(user_info[3].text).lower()

#Test chức năng từ chối tài khoản
# passed in 27.19s
#TC_UM_14
def test_deny_user_account(driver):
    test_navigate_to_user_management(driver)
    #Lấy element tùy chọn trạng thái
    status_options = driver.find_element(By.XPATH, "//select[@name='status']")
    select_options = Select(status_options)
    #Chọn các tài khoản chưa được duyệt
    select_options.select_by_visible_text("Chưa được duyệt")
    time.sleep(1)
    
    #Lấy email của tài khoản đầu tiên
    email = driver.find_element(By.XPATH, "//table/tbody//tr[2]//td[1]").text
    email = str(email).lower()
    #Chọn nút từ chối
    decline_btn = get_clickable_element(driver, By.XPATH, "//table/tbody//tr[2]//td[6]//form//button[2]")
    decline_btn.click()

    #Sau khi từ chối thì tìm lại tài khoản vừa từ chối để kiểm tra
    test_find_user_with_valid_email_input(driver, email)
    status = driver.find_element(By.XPATH, "//table/tbody//tr[2]//td[3]").text
    assert "Đã Từ Chối" in status

#Test chức năng từ duyệt tài khoản
# passed in 27.83s
#TC_UM_15
def test_accept_new_registration(driver):
    test_navigate_to_user_management(driver)
    #Lấy element tùy chọn trạng thái
    status_options = driver.find_element(By.XPATH, "//select[@name='status']")
    select_options = Select(status_options)
    #Chọn các tài khoản chưa được duyệt
    select_options.select_by_visible_text("Chưa được duyệt")
    time.sleep(1)
    
    #Lấy email của tài khoản đầu tiên
    email = driver.find_element(By.XPATH, "//table/tbody//tr[2]//td[1]").text
    email = str(email).lower()
    #Chọn nút duyệt
    decline_btn = get_clickable_element(driver, By.XPATH, "//table/tbody//tr[2]//td[6]//form//button[1]")
    decline_btn.click()

    #Sau khi từ chối thì tìm lại tài khoản vừa từ chối để kiểm tra
    test_find_user_with_valid_email_input(driver, email)
    status = driver.find_element(By.XPATH, "//table/tbody//tr[2]//td[3]").text
    assert "Đã Được Duyệt" in status

#Test chức năng bỏ trống trường thông tin tài khoản
#Fail vì có thể để trống mật khẩu
#TC_UM_16
def test_empty_user_detail(driver):
    #tìm kiếm user bằng email
    email = "user21@gmail.com"
    test_find_user_with_valid_email_input(driver, email)

    #chọn nút xem chi tiết
    user_detail_btn = get_clickable_element(driver, By.XPATH, "//table/tbody//tr[2]//td[6]//form//button[text()='Chi tiết']")
    user_detail_btn.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//body").send_keys(Keys.END)
    time.sleep(1)

    #Xóa các trường thông tin
    driver.find_element(By.NAME, "ten").clear()
    driver.find_element(By.NAME, "cccd").clear()
    driver.find_element(By.NAME, "number").clear()
    driver.find_element(By.NAME, "address").clear()
    driver.find_element(By.NAME, "pass").clear()
    #Lưu thông tin
    tac = get_clickable_element(driver, By.NAME, "tac")
    tac.click()

    save_btn = get_clickable_element(driver, By.XPATH, "//div[@class='buttons']//button[1]")
    save_btn.click()

    message = driver.find_element(By.XPATH, "/html/body/div[2]").text
    assert "Không được để trống mật khẩu!" in message

#Test chức năng xóa tài khoản
# passed in 31.16s
#TC_UM_17
def test_delete_user_account(driver):
    #tìm kiếm user bằng email có tồn tại
    email = "user24@gmail.com"
    test_find_user_with_valid_email_input(driver, email)

    #chọn nút xem chi tiết
    user_detail_btn = get_clickable_element(driver, By.XPATH, "//table/tbody//tr[2]//td[6]//form//button[text()='Chi tiết']")
    user_detail_btn.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//body").send_keys(Keys.END)
    time.sleep(1)

    delete_btn = get_clickable_element(driver, By.XPATH, "//div[@class='buttons']//button[text()='Xoá tài khoản']")
    delete_btn.click()
    time.sleep(1)

    #Tìm lại tài khoản đã xóa
    test_find_not_registed_user(driver, email)



# =================== wishlish  ======================


#Test thêm vào wishlist
# passed in 19.36s
#TC_WL_01
def test_add_to_wishlist(driver):
    test_valid_login(driver)

    #Bấm nút page down để kéo xuống
    driver.find_element(By.XPATH, "//body").send_keys(Keys.PAGE_DOWN)
    # driver.find_element(By.XPATH, "//body").send_keys(Keys.PAGE_DOWN)
    #đợi cho các element load
    time.sleep(0.4)
    #chọn 1 cuốn sách và bấm vào
    index = randint(1, 5)
    book = get_clickable_element(driver, By.XPATH, f"/html/body/section[2]/div/div[{index}]")
    book.click()
    time.sleep(1)
    book_name = driver.find_element(By.XPATH, "/html/body/section/div/h2").text
    #Thêm sách vào wishlist
    add_to_wishlist = get_clickable_element(driver, By.XPATH, "/html/body/section/div/div/form[2]/button")
    add_to_wishlist.click()
    time.sleep(1)
    #Kiểm tra là sách có được thêm vào wishlist chưa
    #Lấy danh sách sản phẩm trong wishlist
    books = driver.find_elements(By.XPATH, "//div[@class='cart-info']/div/h3")
    #Lấy tên
    book_names = list(map(lambda book: str(book.text).lower(), books))
    time.sleep(1)
    assert str(book_name).lower() in book_names

#Test thêm nhiều sách vào wishlist
# passed in 21.33s
#TC_WL_02
def test_add_multi_pd_to_wishlist(driver, no_products = 2):
    count = 0
    test_valid_login(driver)
    added_book_names = []
    index = randint(1, 4)
    while count < no_products:
        #Bấm nút page down để kéo xuống
        driver.find_element(By.XPATH, "//body").send_keys(Keys.PAGE_DOWN)
        # driver.find_element(By.XPATH, "//body").send_keys(Keys.PAGE_DOWN)
        #đợi cho các element load
        time.sleep(0.4)
        book = get_clickable_element(driver, By.XPATH, f"/html/body/section[2]/div/div[{index}]")
        book.click()
        time.sleep(1)
        book_name = driver.find_element(By.XPATH, "/html/body/section/div/h2").text
        added_book_names.append(str(book_name).lower())
        #Thêm sách vào wishlist
        add_to_wishlist = get_clickable_element(driver, By.XPATH, "/html/body/section/div/div/form[2]/button")
        add_to_wishlist.click()
        time.sleep(1)
        #Về trang chủ
        count += 1
        if count < no_products:
            homepage_btn = get_clickable_element(driver, By.XPATH, "/html/body/ul/li[1]/a")
            homepage_btn.click()
            index = index - 1 if index > 1 else 5

    #Kiểm tra là sách có được thêm vào wishlist chưa
    #Lấy danh sách sản phẩm trong wishlist
    driver.find_element(By.XPATH, "//body").send_keys(Keys.END)
    books = driver.find_elements(By.XPATH, "//div[@class='cart-info']/div/h3")
    #Lấy tên
    book_names = list(map(lambda book: str(book.text).lower(), books))
    time.sleep(1)
    result = [added_book_name in book_names for added_book_name in added_book_names]
    assert False not in result

#test Xem chi tiết sách trong wishlist
# passed in 17.50s
#TC_WL_03
def test_book_detail_in_wishlist(driver, add_new=True):
    if add_new:
        test_add_to_wishlist(driver)

    book_name = driver.find_element(By.XPATH, "//div[@class='cart-info']/div/h3").text
    detail_btn = get_clickable_element(driver, By.XPATH, "//a[@class='link-text']")
    detail_btn.click()
    time.sleep(0.5)
    book_name_detail = driver.find_element(By.XPATH, "/html/body/section/div/h2").text

    assert str(book_name).lower() in str(book_name_detail).lower()

#Test Thêm 1 sách đã có trong wishlist
# passed in 19.54s
#TC_WL_04
def test_add_existing_book_in_wishlist(driver):
    test_book_detail_in_wishlist(driver)

    add_to_wishlist = get_clickable_element(driver, By.XPATH, "/html/body/section/div/div/form[2]/button")
    add_to_wishlist.click()
    time.sleep(1)

    message = driver.find_element(By.XPATH, "/html/body/div[2]/h1[2]/a[3]/p").text
    assert "Bạn đã chọn sách này rồi" in message

#Test xóa 1 sản phẩm khỏi wishlist
# passed in 19.12s
#TC_WL_05
def test_delete_from_wishlist(driver):
    #Thêm 1 sản phẩm vào wishlist trong trường hợp wishlist trống
    test_add_to_wishlist(driver)

    #Lấy tên sản phẩm đầu tiên để check
    book_name = driver.find_element(By.XPATH, "//div[@class='cart-info']/div/h3").text

    #xóa sản phẩm
    delete_btn = get_clickable_element(driver, By.NAME, "btn_remove")
    delete_btn.click()
    time.sleep(1)

    #Kiểm tra xem sản phẩm đã bị xóa khỏi wishlist chưa
    books = driver.find_elements(By.XPATH, "//div[@class='cart-info']/div/h3")
    #Lấy tên
    book_names = list(map(lambda book: str(book.text).lower(), books))
    time.sleep(1)
    assert str(book_name).lower() not in book_names

#test xóa tất cả sản phẩm trong wishlist sau khi thêm sản phẩm
# passed in 22.51s
#TC_WL_06
def test_delete_all(driver):
    test_add_multi_pd_to_wishlist(driver)
    driver.find_element(By.XPATH, "//body").send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    no_books = driver.find_elements(By.NAME, "btn_remove")
    for i in range(0, len(no_books)):
        dlt_btn = get_clickable_element(driver, By.NAME, "btn_remove")
        dlt_btn.click()
        time.sleep(0.2)
    time.sleep(2)
    a = driver.find_elements(By.XPATH, "/html/body/div[2]/h1[2]/table/tbody/tr")
    assert len(a) == 1

#Test thêm vào cart từ wishlist
# passed in 18.68s
#TC_WL_07
def test_add_to_cart_form_wishlist(driver):
    test_add_to_wishlist(driver)

    #Lấy tên sản phẩm đầu tiên để check
    book_name = driver.find_element(By.XPATH, "//div[@class='cart-info']/div/h3").text

    add_to_cart_btn = get_clickable_element(driver, By.NAME, "addToCart")
    add_to_cart_btn.click()

    time.sleep(1)

    #Kiểm tra sản phẩm được thêm vào cart chưas
    books = driver.find_elements(By.XPATH, "//div[@class='cart-info']/div/h3")
    #Lấy tên
    book_names = list(map(lambda book: str(book.text).lower(), books))
    time.sleep(1)
    assert str(book_name).lower() in book_names