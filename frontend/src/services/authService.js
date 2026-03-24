import config from '../config';

class AuthService {

  // ─────────────────── LOGIN ───────────────────
  async login(email, password) {
    const response = await fetch(`${config.API_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Đăng nhập thất bại');
    }

    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('userEmail', data.user.email);
    localStorage.setItem('userName', data.user.username);
    localStorage.setItem('orgId', data.user.org_id || '');
    localStorage.setItem('role', data.user.role || '');

    return data;
  }

  // ─────────────────── REGISTER USER ───────────────────
  async register(userData) {
    const response = await fetch(`${config.API_URL}/api/auth/register`, {
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

  // ─────────────────── REGISTER ORG ───────────────────
  async registerOrg(orgData) {
    const response = await fetch(`${config.API_URL}/api/auth/register-org`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        org_name: orgData.orgName,
        email: orgData.email,
        username: orgData.username,
        password: orgData.password,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Tạo tổ chức thất bại');
    }

    return data;
  }

  // ─────────────────── JOIN ORG ───────────────────
  async joinOrg(inviteCode) {
    const response = await fetch(`${config.API_URL}/api/auth/join-org`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...this.getAuthHeader(),
      },
      body: JSON.stringify({ invite_code: inviteCode }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Join org thất bại');
    }

    return data;
  }

  // ─────────────────── LOGOUT ───────────────────
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('userName');
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('orgId');
    localStorage.removeItem('role');
  }

  // ─────────────────── HELPERS ───────────────────
  getToken() {
    return localStorage.getItem('access_token');
  }

  getAuthHeader() {
    const token = this.getToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  isLoggedIn() {
    return !!this.getToken();
  }

  getRole() {
    return localStorage.getItem('role');
  }

  isAdmin() {
    return this.getRole() === 'admin';
  }
}

export default new AuthService();