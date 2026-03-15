import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import contactsService from '../services/contactsService';
import './Contacts.scss';

function ContactForm({ initial = {}, onSave, onCancel, isEditing = false, isSubmitting = false }) {
  const [form, setForm] = React.useState({ fullName: '', address: '', phone: '', email: '', ...initial });
  const [errors, setErrors] = React.useState({});

  React.useEffect(() => setForm({ fullName: '', address: '', phone: '', email: '', ...initial }), [initial]);

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
    await onSave(form);
  };

  return (
    <form className="contact-form" onSubmit={handleSubmit}>
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
        <button type="submit" className="btn btn-primary" disabled={isSubmitting}>{isSubmitting ? 'Đang lưu...' : isEditing ? 'Cập nhật' : 'Lưu'}</button>
        <button type="button" className="btn btn-secondary" onClick={onCancel}>Hủy</button>
      </div>
    </form>
  );
}

export default function AddContact() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [contact, setContact] = useState(null);
  const [loading, setLoading] = useState(!!id);
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const isEditing = !!id;

  useEffect(() => {
    if (id) {
      fetchContact();
    }
  }, [id]);

  const fetchContact = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await contactsService.getContact(id);
      setContact(data);
    } catch (err) {
      setError('Không thể tải thông tin khách hàng: ' + err.message);
      console.error('Error fetching contact:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (formData) => {
    setIsSubmitting(true);
    setError(null);
    try {
      if (isEditing) {
        await contactsService.updateContact(id, formData);
      } else {
        await contactsService.createContact(formData);
      }
      navigate('/contacts');
    } catch (err) {
      setError(err.message || 'Lỗi lưu thông tin khách hàng');
      console.error('Error saving contact:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="contacts-page">
      <div className="contacts-header">
        <div className="header-content">
          <h1>{isEditing ? 'Sửa Thông Tin Khách Hàng' : 'Thêm Khách Hàng Mới'}</h1>
          <p>{isEditing ? 'Cập nhật thông tin khách hàng' : 'Nhập thông tin khách hàng để lưu vào hệ thống'}</p>
        </div>
        <div className="header-actions">
          <button className="btn btn-secondary" onClick={() => navigate('/contacts')}>← Quay lại</button>
        </div>
      </div>
      <div className="contacts-container">
        <div className="contacts-list-section">
          <div className="panel">
            {loading ? (
              <div style={{ padding: '40px', textAlign: 'center' }}>Đang tải...</div>
            ) : error ? (
              <div style={{ padding: '20px', color: '#e74c3c', backgroundColor: '#fee', borderRadius: '8px' }}>
                {error}
                <button onClick={fetchContact} style={{ marginLeft: '12px', padding: '4px 12px', cursor: 'pointer' }}>Thử lại</button>
              </div>
            ) : (
              <ContactForm 
                initial={contact || {}} 
                onSave={handleSave} 
                onCancel={() => navigate('/contacts')}
                isEditing={isEditing}
                isSubmitting={isSubmitting}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
