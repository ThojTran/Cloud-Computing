import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import Login from './Auth/Login';
import Register from './Auth/Register';
import Contacts from './pages/Contacts';
import AddContact from './pages/AddContact';
import MessagePage from './pages/Message';
import authService from './services/authService';
import './App.css';

function App() {
  // Kiểm tra JWT token thay vì flag 'isLoggedIn'
  const [isLoggedIn, setIsLoggedIn] = useState(authService.isLoggedIn());

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  return (
    <Router>
      <InnerApp isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} onLogin={handleLogin} />
    </Router>
  );
}

function InnerApp({ isLoggedIn, setIsLoggedIn, onLogin }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    authService.logout();  // Xóa JWT token + user info
    setIsLoggedIn(false);
    navigate('/login');
  };

  return (
    <div className={`app-container ${isLoggedIn ? 'logged-in' : ''}`}>
      <div className="app-content">
        
        <header className="app-header">
        </header>

        <Routes>
          <Route
            path="/login"
            element={isLoggedIn ? <Navigate to="/contacts" /> : <Login onLogin={onLogin} />}
          />
          <Route
            path="/register"
            element={isLoggedIn ? <Navigate to="/contacts" /> : <Register />}
          />
          <Route
            path="/contacts"
            element={isLoggedIn ? <Contacts onLogout={handleLogout}/> : <Navigate to="/login" />}
          />
          <Route
            path="/contacts/new"
            element={isLoggedIn ? <AddContact /> : <Navigate to="/login" />}
          />
          <Route
            path="/contacts/:id"
            element={isLoggedIn ? <AddContact /> : <Navigate to="/login" />}
          />
          <Route
            path="/contacts/message"
            element={isLoggedIn ? <MessagePage /> : <Navigate to="/login" />}
          />
          <Route
            path="/"
            element={<Navigate to="/login" />}
          />
        </Routes>
      </div>
    </div>
  );
}

export default App;
