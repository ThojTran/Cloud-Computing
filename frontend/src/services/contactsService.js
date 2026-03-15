import config from '../config';
import authService from './authService';

/**
 * Contacts Service (→ Flask /api/customers + /api/messages)
 *
 * Xử lý mapping:
 * - URL:    /api/contacts → /api/customers
 * - Fields: fullName ↔ full_name (camelCase ↔ snake_case)
 * - Auth:   Gắn JWT Bearer token vào mọi request
 */

const API_CUSTOMERS = `${config.API_URL}/api/customers`;
const API_MESSAGES  = `${config.API_URL}/api/messages`;

// ─────────────────── HELPERS ───────────────────

function getHeaders() {
  return {
    'Content-Type': 'application/json',
    ...authService.getAuthHeader(),
  };
}

async function handleResponse(res) {
  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    // Nếu token hết hạn → redirect về login
    if (res.status === 401) {
      authService.logout();
      window.location.href = '/login';
      throw new Error('Phiên đăng nhập hết hạn. Vui lòng đăng nhập lại.');
    }
    throw new Error(data.error || data.message || `API Error: ${res.status}`);
  }

  return data;
}

/**
 * Chuyển đổi customer data từ backend (snake_case) → frontend (camelCase)
 * Backend trả: { id, full_name, phone, email, address }
 * Frontend cần: { id, fullName, phone, email, address }
 */
function mapFromBackend(customer) {
  return {
    id: customer.id,
    fullName: customer.full_name,
    phone: customer.phone || '',
    email: customer.email || '',
    address: customer.address || '',
    created_at: customer.created_at,
  };
}

/**
 * Chuyển đổi customer data từ frontend (camelCase) → backend (snake_case)
 * Frontend gửi: { fullName, phone, email, address }
 * Backend cần: { full_name, phone, email, address }
 */
function mapToBackend(data) {
  const mapped = {};
  if (data.fullName !== undefined) mapped.full_name = data.fullName;
  if (data.phone !== undefined)    mapped.phone = data.phone;
  if (data.email !== undefined)    mapped.email = data.email;
  if (data.address !== undefined)  mapped.address = data.address;
  return mapped;
}

// ─────────────────── CRUD ───────────────────

async function listContacts() {
  const res = await fetch(API_CUSTOMERS, { headers: getHeaders() });
  const data = await handleResponse(res);
  // Backend trả { customers: [...] }, frontend cần array
  return (data.customers || []).map(mapFromBackend);
}

async function getContact(id) {
  const res = await fetch(`${API_CUSTOMERS}/${id}`, { headers: getHeaders() });
  const data = await handleResponse(res);
  return mapFromBackend(data.customer);
}

async function createContact(formData) {
  const res = await fetch(API_CUSTOMERS, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(mapToBackend(formData)),
  });
  const data = await handleResponse(res);
  return mapFromBackend(data.customer);
}

async function updateContact(id, formData) {
  const res = await fetch(`${API_CUSTOMERS}/${id}`, {
    method: 'PUT',
    headers: getHeaders(),
    body: JSON.stringify(mapToBackend(formData)),
  });
  const data = await handleResponse(res);
  return mapFromBackend(data.customer);
}

async function deleteContact(id) {
  const res = await fetch(`${API_CUSTOMERS}/${id}`, {
    method: 'DELETE',
    headers: getHeaders(),
  });
  return await handleResponse(res);
}

// ─────────────────── BULK DELETE ───────────────────

async function bulkDelete(ids) {
  const res = await fetch(`${API_CUSTOMERS}/bulk-delete`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ ids }),
  });
  return await handleResponse(res);
}

// ─────────────────── MESSAGING ───────────────────

/**
 * Gửi SMS cho danh sách customers
 * Frontend gọi: sendSms([1, 2, 3], "Hello")
 * Backend cần: POST /api/messages/send { type: "sms", content: "...", customer_ids: [...] }
 */
async function sendSms(ids, message) {
  const res = await fetch(`${API_MESSAGES}/send`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({
      type: 'sms',
      content: message,
      customer_ids: ids,
    }),
  });
  const data = await handleResponse(res);
  return {
    sent: data.data?.results?.filter(r => r.status === 'sent').length || 0,
    results: data.data?.results || [],
  };
}

/**
 * Gửi Email cho danh sách customers
 * Frontend gọi: sendEmail([1, 2, 3], "Subject", "Body")
 * Backend cần: POST /api/messages/send { type: "email", subject: "...", content: "...", customer_ids: [...] }
 */
async function sendEmail(ids, subject, message) {
  const res = await fetch(`${API_MESSAGES}/send`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({
      type: 'email',
      subject: subject,
      content: message,
      customer_ids: ids,
    }),
  });
  const data = await handleResponse(res);
  return {
    sent: data.data?.results?.filter(r => r.status === 'sent').length || 0,
    results: data.data?.results || [],
  };
}

export default {
  listContacts,
  getContact,
  createContact,
  updateContact,
  deleteContact,
  bulkDelete,
  sendSms,
  sendEmail,
};
