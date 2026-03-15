import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import contactsService from '../services/contactsService';
import './Contacts.scss';

export default function MessagePage() {
  const navigate = useNavigate();
  const [selectedContacts, setSelectedContacts] = useState([]);
  const [contactsMap, setContactsMap] = useState({});
  const [smsMessage, setSmsMessage] = useState('');
  const [emailSubject, setEmailSubject] = useState('');
  const [emailMessage, setEmailMessage] = useState('');

  useEffect(() => {
    const raw = sessionStorage.getItem('selectedContacts');
    const ids = raw ? JSON.parse(raw) : [];
    setSelectedContacts(ids);

    // tải danh sách khách hàng để hiển thị tổng hợp
    contactsService.listContacts().then(list => {
      const map = {};
      list.forEach(c => { map[c.id] = c; });
      setContactsMap(map);
    });
  }, []);

  const handleSendSms = async () => {
    if (selectedContacts.length === 0) return alert('Vui lòng chọn ít nhất một khách hàng');
    if (!smsMessage.trim()) return alert('Vui lòng nhập nội dung SMS');
    const res = await contactsService.sendSms(selectedContacts, smsMessage);
    alert(`✓ SMS đã gửi thành công: ${res.sent} tin nhắn`);
    setSmsMessage('');
    sessionStorage.removeItem('selectedContacts');
    navigate('/contacts');
  };

  const handleSendEmail = async () => {
    if (selectedContacts.length === 0) return alert('Vui lòng chọn ít nhất một khách hàng');
    if (!emailSubject.trim() || !emailMessage.trim()) return alert('Vui lòng nhập tiêu đề và nội dung email');
    const res = await contactsService.sendEmail(selectedContacts, emailSubject, emailMessage);
    alert(`✓ Email đã gửi thành công: ${res.sent} email`);
    setEmailSubject('');
    setEmailMessage('');
    sessionStorage.removeItem('selectedContacts');
    navigate('/contacts');
  };

  return (
    <div className="contacts-page">
      <div className="contacts-header">
        <div className="header-content">
          <h1>Gửi Tin Nhắn</h1>
          <p>Gửi SMS hoặc Email đến khách hàng đã chọn</p>
        </div>
        <div className="header-actions">
          <button className="btn btn-secondary" onClick={() => navigate('/contacts')}>← Quay lại</button>
        </div>
      </div>

      <div className="contacts-container">
        <div className="contacts-list-section">
          <div className="panel">
            <div className="section-title">Đã chọn: {selectedContacts.length} khách hàng</div>
            <div style={{marginTop:12, marginBottom:12}}>
              {selectedContacts.map(id => (
                <div key={id} style={{padding:6, borderBottom:'1px solid #eee'}}>
                  <strong>{contactsMap[id]?.fullName || id}</strong> — {contactsMap[id]?.phone || ''}
                </div>
              ))}
            </div>

            <div className="message-box sms-box">
              <div className="message-info">
                <label>Gửi SMS</label>
                <small>{selectedContacts.length > 0 ? `Gửi đến ${selectedContacts.length} khách hàng` : 'Chọn khách hàng để gửi'}</small>
              </div>
              <textarea placeholder="Nhập nội dung tin nhắn..." value={smsMessage} onChange={e => setSmsMessage(e.target.value)} rows="4" />
              <button className="btn btn-primary btn-full" onClick={handleSendSms}>✉️ Gửi SMS</button>
            </div>

            <div className="message-box email-box">
              <div className="message-info">
                <label>Gửi Email</label>
                <small>{selectedContacts.length > 0 ? `Gửi đến ${selectedContacts.length} khách hàng` : 'Chọn khách hàng để gửi'}</small>
              </div>
              <input type="text" placeholder="Tiêu đề email" value={emailSubject} onChange={e => setEmailSubject(e.target.value)} className="email-subject" />
              <textarea placeholder="Nội dung email..." value={emailMessage} onChange={e => setEmailMessage(e.target.value)} rows="6" />
              <button className="btn btn-primary btn-full" onClick={handleSendEmail}>📧 Gửi Email</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
