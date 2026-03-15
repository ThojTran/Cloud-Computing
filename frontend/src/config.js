// Cấu hình trung tâm cho frontend
// Tất cả services sẽ import từ đây thay vì hardcode URL

const config = {
  API_URL: process.env.REACT_APP_BACKEND_URL || 'http://34.237.215.20:5000/api',
};

export default config;
