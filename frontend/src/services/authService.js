import config from '../config';

/**
 * Auth Service
 * Xử lý đăng ký, đăng nhập, và quản lý JWT token.
 * Gọi đến Flask backend: /api/user/*
 */
class AuthService {

  // ─────────────────── LOGIN ───────────────────
  async login(email, password) {
    const response = await fetch(`${config.API_URL}/api/user/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Đăng nhập thất bại');
    }

    // Lưu JWT token + thông tin user vào localStorage
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('userEmail', data.user.email);
    localStorage.setItem('userName', data.user.username);

    return data;
  }

  // ─────────────────── REGISTER ───────────────────
  async register(userData) {
    const response = await fetch(`${config.API_URL}/api/user/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: userData.email,
        username: userData.username || userData.fullName,
        password: userData.password,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Đăng ký thất bại');
    }

    return data;
  }

  // ─────────────────── LOGOUT ───────────────────
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('userName');
    localStorage.removeItem('isLoggedIn');
  }

  // ─────────────────── HELPERS ───────────────────
  getToken() {
    return localStorage.getItem('access_token');
  }

  /**
   * Trả về header Authorization cho các API call cần xác thực.
   * Sử dụng: fetch(url, { headers: { ...authService.getAuthHeader() } })
   */
  getAuthHeader() {
    const token = this.getToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  isLoggedIn() {
    return !!this.getToken();
  }
}

export default new AuthService();
