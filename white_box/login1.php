<?php
if (session_status() == PHP_SESSION_NONE) {
    session_start();
}
include("connection.php");

function startSession() {
    session_start();
}

function endSession() {
    session_unset();
    session_destroy();
}

function validate($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

function redirectWithError($error) {
    return "login.php?error=" . urlencode($error); // Trả về URL thay vì redirect
}

function loginUser($email, $password, $database) {
    $collection = $database->selectCollection('user');
    return $collection->findOne(['email' => $email, 'mat_khau' => $password]);
}

function handleLogin($email, $password, $database) {
    if (empty($email)) {
        return redirectWithError("Không được để trống Email");
    }
    
    if (empty($password)) {
        return redirectWithError("Không được để trống mật khẩu!");
    }

    $login = loginUser($email, $password, $database);
    
    if ($login) {
        if ($login->trang_thai_tai_khoan == -1) {
            return redirectWithError("Tài khoản của bạn đã bị từ chối!");
        }
        
        if ($login->trang_thai_tai_khoan == 2) {
            return redirectWithError("Tài khoản của bạn đã bị khoá!");
        }

        if (session_status() == PHP_SESSION_NONE) {
            startSession();
        }
        $_SESSION['_id'] = $login->_id;
        $_SESSION['ten'] = $login->ten;
        $_SESSION['ma_rank'] = $login->ma_rank;
        $_SESSION['email'] = $login->email;
        $_SESSION['trang_thai_tai_khoan'] = $login->trang_thai_tai_khoan;

        return $login->ma_rank == 0 ? "checkin.php" : "index.php"; // Trả về URL
    } else {
        return redirectWithError("Incorrect!");
    }
}

// Kiểm tra xem có dữ liệu POST không
if (isset($_POST['email']) && isset($_POST['password'])) {
    endSession(); // Kết thúc session trước khi xử lý đăng nhập

    $email = validate($_POST['email']);
    $password = validate($_POST['password']);
    
    $redirectUrl = handleLogin($email, $password, $database);
    
    if (strpos($redirectUrl, 'login.php') !== false) {
        header("Location: $redirectUrl");
        exit();
    } else {
        header("Location: $redirectUrl");
        exit();
    }
}
?>