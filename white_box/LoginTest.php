<?php

use PHPUnit\Framework\TestCase;

require 'login1.php'; // Đảm bảo file login1.php được bao gồm

// Tạo interface cho Collection
interface CollectionInterface {
    public function findOne($criteria);
}

// Tạo interface cho Database
interface DatabaseInterface {
    public function selectCollection($name);
}

class LoginTest extends TestCase {

    protected function setUp(): void {
        // Bắt đầu output buffering để kiểm soát header
        ob_start();
    }

    protected function tearDown(): void {
        // Xóa output buffer
        ob_end_clean();
    }

    #Test đầu vào input
    public function testValidate() {
        $data = " Hello ";
        $this->assertEquals("Hello", validate($data));
    }
    #Test hệ thống trả về thông báo
    public function testRedirectWithError() {
        $errorUrl = redirectWithError("Không được để trống Email");
        $this->assertEquals("login.php?error=Không được để trống Email", urldecode($errorUrl));
    }
    #Test đăng nhập với email bỏ trống
    public function testHandleLoginWithEmptyEmail() {
        $databaseMock = $this->createMock(DatabaseInterface::class); // Giả lập đối tượng database
        $result = handleLogin("", "password", $databaseMock);
        $this->assertEquals("login.php?error=Không được để trống Email", urldecode($result));
    }
    #Test đăng nhập với password bỏ trống
    public function testHandleLoginWithEmptyPassword() {
        $databaseMock = $this->createMock(DatabaseInterface::class); // Giả lập đối tượng database
        $result = handleLogin("test@example.com", "", $databaseMock);
        $this->assertEquals("login.php?error=Không được để trống mật khẩu!", urldecode($result));
    }
    #Test đăng nhập thành công
    public function testLoginUserSuccessful() {
        // Tạo một đối tượng người dùng giả lập
        $mockUser = (object) [
            '_id' => '123',
            'ten' => 'Test User',
            'ma_rank' => 0,
            'email' => 'test@example.com',
            'trang_thai_tai_khoan' => 1
        ];

        // Tạo mock cho collection
        $mockCollection = $this->createMock(CollectionInterface::class);
        $mockCollection->method('findOne')
            ->willReturn($mockUser); // Khi gọi findOne, sẽ trả về mockUser

        // Tạo mock cho database
        $mockDatabase = $this->createMock(DatabaseInterface::class);
        $mockDatabase->method('selectCollection')
            ->willReturn($mockCollection); // Khi gọi selectCollection, sẽ trả về mockCollection

        // Gọi hàm handleLogin
        $result = handleLogin("test@example.com", "password", $mockDatabase);

        // Kiểm tra redirect đến checkin.php cho người dùng có ma_rank = 0
        $this->assertEquals("checkin.php", $result);
    }

    #Test đăng nhập thất bại
    public function testLoginUserIncorrect() {
        // Giả lập database và collection cho trường hợp không tìm thấy người dùng
        $databaseMock = $this->createMock(DatabaseInterface::class);
        $databaseMock->method('selectCollection')
            ->willReturn($this->createMockCollection(null)); // Không tìm thấy người dùng

        $result = handleLogin("wrong@example.com", "wrongpassword", $databaseMock);
        $this->assertEquals("login.php?error=Incorrect!", urldecode($result));
    }

    private function createMockCollection($user) {
        $mockCollection = $this->createMock(CollectionInterface::class);
        $mockCollection->method('findOne')
            ->willReturn($user); // Trả về user nếu tìm thấy
        return $mockCollection;
    }
}
?>