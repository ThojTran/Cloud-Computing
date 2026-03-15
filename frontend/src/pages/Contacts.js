import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import contactsService from '../services/contactsService';
import './Contacts.scss';

function ContactForm({ initial = {}, onSave, onCancel, isEditing = false }) {
  const [form, setForm] = useState({ fullName: '', address: '', phone: '', email: '', ...initial });
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (isEditing && initial.id) {
      setForm({ fullName: initial.fullName || '', address: initial.address || '', phone: initial.phone || '', email: initial.email || '' });
    } else {
      setForm({ fullName: '', address: '', phone: '', email: '' });
    }
  }, [isEditing, initial.id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
    if (errors[name]) setErrors(prev => ({ ...prev, [name]: '' }));
  };

  const validate = () => {
    const newErrors = {};
    if (!form.fullName.trim()) newErrors.fullName = 'Họ tên bắt buộc';
    if (!form.phone.trim()) newErrors.phone = 'Số điện thoại bắt buộc';
    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validate();
    if (Object.keys(newErrors).length > 0) { setErrors(newErrors); return; }
    setSubmitting(true);
    try {
      console.log('Form submitting with data:', form);
      if (onSave) {
        await onSave(form);
      }
      setForm({ fullName: '', address: '', phone: '', email: '' });
    } catch (err) {
      console.error('Form submission error:', err);
      setErrors({ submit: err.message || 'Lỗi lưu dữ liệu' });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form className="contact-form" onSubmit={handleSubmit}>
      <h3 style={{ marginTop: 0 }}>{isEditing ? 'Cập Nhật Khách Hàng' : 'Thêm Khách Hàng Mới'}</h3>
      {errors.submit && <div className="error-text" style={{ marginBottom: '12px', color: '#e74c3c' }}>{errors.submit}</div>}
      <div className="form-group">
        <label>Họ và Tên <span className="required">*</span></label>
        <input name="fullName" value={form.fullName} onChange={handleChange} placeholder="Nhập họ tên" />
        {errors.fullName && <span className="error-text">{errors.fullName}</span>}
      </div>
      <div className="form-group">
        <label>Số Điện Thoại <span className="required">*</span></label>
        <input name="phone" value={form.phone} onChange={handleChange} placeholder="Nhập số điện thoại" />
        {errors.phone && <span className="error-text">{errors.phone}</span>}
      </div>
      <div className="form-group">
        <label>Địa Chỉ</label>
        <input name="address" value={form.address} onChange={handleChange} placeholder="Nhập địa chỉ" />
      </div>
      <div className="form-group">
        <label>Email</label>
        <input name="email" value={form.email} onChange={handleChange} type="email" placeholder="Nhập email" />
      </div>
      <div className="form-actions">
        <button type="submit" className="btn btn-primary btn-full" disabled={submitting}>{submitting ? 'Đang lưu...' : isEditing ? 'Cập nhật' : 'Lưu'}</button>
        <button type="button" className="btn btn-secondary btn-full" onClick={onCancel}>Hủy</button>
      </div>
    </form>
  );
}

export default function Contacts({ onLogout }) {
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selected, setSelected] = useState(new Set());
  const [searchTerm, setSearchTerm] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);
  const [editingContact, setEditingContact] = useState(null);

  const fetchContacts = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await contactsService.listContacts();
      setContacts(data);
    } catch (err) {
      setError(err.message || 'Failed to load contacts. Make sure the backend server is running on port 4001.');
      console.error('Error fetching contacts:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchContacts(); }, []);

  const filteredContacts = contacts.filter(c => 
    c.fullName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    c.phone.includes(searchTerm) ||
    c.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const toggleSelect = (id) => {
    setSelected(prev => {
      const s = new Set(prev);
      if (s.has(id)) s.delete(id); else s.add(id);
      try { sessionStorage.setItem('selectedContacts', JSON.stringify(Array.from(s))); } catch(e) {}
      return s;
    });
  };
  
  const navigate = useNavigate();

  const handleDelete = async (id) => {
    if (!window.confirm('Bạn chắc chắn muốn xóa liên hệ này?')) return;
    try {
      await contactsService.deleteContact(id);
      fetchContacts();
    } catch (err) {
      alert('Lỗi xóa: ' + err.message);
    }
  };

  const handleEdit = (contact) => {
    setEditingContact(contact);
    setShowEditForm(true);
  };

  const handleBulkDelete = async () => {
    const ids = Array.from(selected);
    if (ids.length === 0) return alert('Vui lòng chọn ít nhất một khách hàng');
    if (!window.confirm(`Xóa ${ids.length} liên hệ?`)) return;
    try {
      await contactsService.bulkDelete(ids);
      setSelected(new Set());
      fetchContacts();
    } catch (err) {
      alert('Lỗi xóa: ' + err.message);
    }
  };

  const handleSendMessagePage = () => {
    try { sessionStorage.setItem('selectedContacts', JSON.stringify(Array.from(selected))); } catch(e) {}
    navigate('/contacts/message');
  };

  const handleFormSave = async (formData) => {
    try {
      console.log('Saving new contact:', formData);
      const result = await contactsService.createContact(formData);
      console.log('Contact created successfully:', result);
      setShowAddForm(false);
      fetchContacts();
    } catch (err) {
      console.error('Error in handleFormSave:', err);
      throw err;
    }
  };

  const handleEditFormSave = async (formData) => {
    try {
      console.log('Updating contact:', editingContact.id, formData);
      const result = await contactsService.updateContact(editingContact.id, formData);
      console.log('Contact updated successfully:', result);
      setShowEditForm(false);
      setEditingContact(null);
      fetchContacts();
    } catch (err) {
      console.error('Error in handleEditFormSave:', err);
      throw err;
    }
  };

  const selectedCount = selected.size;

  return (
    <div className="contacts-page">
      {/* MODAL FORM THÊM KHÁCH HÀNG */}
      {showAddForm && (
        <div className="modal-overlay" onClick={() => setShowAddForm(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <ContactForm onSave={handleFormSave} onCancel={() => setShowAddForm(false)} />
          </div>
        </div>
      )}

      {/* MODAL FORM SỬA KHÁCH HÀNG */}
      {showEditForm && editingContact && (
        <div className="modal-overlay" onClick={() => setShowEditForm(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <ContactForm 
              initial={editingContact} 
              onSave={handleEditFormSave} 
              onCancel={() => {
                setShowEditForm(false);
                setEditingContact(null);
              }}
              isEditing={true}
            />
          </div>
        </div>
      )}

      <div className="contacts-wrapper">
        {/* SIDEBAR BÊN TRÁI */}
        <aside className="contacts-sidebar">
          <div className="sidebar-container">
            <div className="sidebar-panel header-panel">
              <h2>Quản lý Khách Hàng</h2>
              <p>Quản lý thông tin khách hàng, gửi tin nhắn và email</p>
              <div className="header-actions">
                <button className="btn btn-secondary btn-full" onClick={() => navigate('/contacts')}>Danh sách</button>
                <button className="btn btn-danger btn-full" onClick={onLogout}>Đăng xuất</button>
              </div>
            </div>
            <div className="sidebar-panel">
              <h3>Công Cụ</h3>
              <button className="btn btn-primary btn-full" onClick={() => setShowAddForm(true)}>
                <span>+ Thêm Khách Hàng</span>
              </button>
              {selectedCount > 0 && (
                <button className="btn btn-danger btn-full" onClick={handleBulkDelete}>
                  <span> Xóa {selectedCount}</span>
                </button>
              )}
              <button className="btn btn-secondary btn-full" onClick={handleSendMessagePage}>
                <span> Gửi Tin</span>
              </button>
            </div>

            <div className="sidebar-panel stats">
              <h3>Thống Kê</h3>
              <div className="stat-item">
                <span className="stat-label">Tổng khách hàng</span>
                <span className="stat-value">{contacts.length}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Đã chọn</span>
                <span className="stat-value">{selectedCount}</span>
              </div>
            </div>
          </div>
        </aside>

        {/* NỘI DUNG CHÍNH BÊN PHẢI */}
        <div className="contacts-container">
          <div className="contacts-list-section">
            <div className="list-header">
              <input
                type="text"
                placeholder="Tìm kiếm theo tên, SĐT, email..."
                value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
                className="search-input"
              />
            </div>

            {error && (
              <div className="error-alert" style={{ backgroundColor: '#fee', color: '#c33', padding: '12px', borderRadius: '4px', marginBottom: '12px', border: '1px solid #fcc' }}>
                <strong>Lỗi:</strong> {error}
                <button onClick={() => fetchContacts()} style={{ marginLeft: '12px', padding: '4px 12px', cursor: 'pointer' }}>Thử lại</button>
              </div>
            )}

            <div className="contacts-list">
              {loading ? (
                <div className="loading">Đang tải dữ liệu...</div>
              ) : filteredContacts.length === 0 ? (
                <div className="empty-state">
                  <p>Không có khách hàng nào</p>
                  <small>Hãy thêm khách hàng mới để bắt đầu</small>
                </div>
              ) : (
                  <table className="contacts-table">
                    <thead>
                      <tr>
                        <th><input type="checkbox" onChange={(e) => {
                          if (e.target.checked) {
                            setSelected(new Set(contacts.map(c => c.id)));
                          } else {
                            setSelected(new Set());
                          }
                        }} /></th>
                        <th>STT</th>
                        <th>Tên</th>
                        <th>Email</th>
                        <th>Điện Thoại</th>
                        <th>Địa Chỉ</th>
                        <th>Hành Động</th>
                      </tr>
                    </thead>
                    <tbody>
                      {filteredContacts.map((c, index) => (
                        <tr key={c.id} className={selected.has(c.id) ? 'selected' : ''}>
                          <td className="checkbox-cell">
                            <input
                              type="checkbox"
                              checked={selected.has(c.id)}
                              onChange={() => toggleSelect(c.id)}
                            />
                          </td>
                          <td className="id-cell">{index + 1}</td>
                        <td className="name-cell">{c.fullName}</td>
                        <td className="email-cell">{c.email || 'N/A'}</td>
                        <td className="phone-cell">{c.phone}</td>
                        <td className="address-cell">{c.address || 'N/A'}</td>
                        <td className="action-cell">
                          <button className="btn btn-sm btn-secondary" onClick={() => handleEdit(c)}>Sửa</button>
                          <button className="btn btn-sm btn-danger" onClick={() => handleDelete(c.id)}>Xóa</button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
