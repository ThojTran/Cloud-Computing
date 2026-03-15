const express = require('express');
const path = require('path');
const { readContacts, writeContacts, initDB } = require('./db');

const app = express();

// Middleware cơ bản
app.use(express.json());

// CORS đơn giản cho phát triển / sử dụng API
app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    if (req.method === 'OPTIONS') return res.sendStatus(204);
    next();
});

const buildDir = path.join(__dirname, '../build');
console.log('Using files in ' + buildDir);

// Tạo ID duy nhất - tự động tăng dần
function generateId(contacts = []) {
    const nextNum = contacts.length + 1;
    return 'KH' + String(nextNum).padStart(4, '0');
}

// API: CRUD Khách Hàng
app.get('/api/contacts', async (req, res) => {
    try {
        const contacts = await readContacts();
        res.json(contacts);
    } catch (error) {
        console.error('Error fetching contacts:', error);
        res.status(500).json({ message: 'Error fetching contacts' });
    }
});

app.get('/api/contacts/:id', async (req, res) => {
    try {
        const contacts = await readContacts();
        const contact = contacts.find(c => c.id === req.params.id);
        if (!contact) return res.status(404).json({ message: 'Contact not found' });
        res.json(contact);
    } catch (error) {
        console.error('Error fetching contact:', error);
        res.status(500).json({ message: 'Error fetching contact' });
    }
});

app.post('/api/contacts', async (req, res) => {
    const { fullName, address, phone, email } = req.body || {};
    if (!fullName || !phone) {
        return res.status(400).json({ message: 'fullName and phone are required' });
    }
    try {
        const contacts = await readContacts();
        const id = generateId(contacts);
        const newContact = { id, fullName, address: address || '', phone, email: email || '', created_at: new Date().toISOString() };
        contacts.unshift(newContact);
        await writeContacts(contacts);
        res.status(201).json(newContact);
    } catch (error) {
        console.error('Error creating contact:', error);
        res.status(500).json({ message: 'Error creating contact' });
    }
});

app.put('/api/contacts/:id', async (req, res) => {
    const { fullName, address, phone, email } = req.body || {};
    try {
        const contacts = await readContacts();
        const idx = contacts.findIndex(c => c.id === req.params.id);
        if (idx === -1) return res.status(404).json({ message: 'Contact not found' });
        contacts[idx] = { ...contacts[idx], fullName: fullName || contacts[idx].fullName, address: address !== undefined ? address : contacts[idx].address, phone: phone || contacts[idx].phone, email: email !== undefined ? email : contacts[idx].email, updated_at: new Date().toISOString() };
        await writeContacts(contacts);
        res.json(contacts[idx]);
    } catch (error) {
        console.error('Error updating contact:', error);
        res.status(500).json({ message: 'Error updating contact' });
    }
});

app.delete('/api/contacts/:id', async (req, res) => {
    try {
        const contacts = await readContacts();
        const idx = contacts.findIndex(c => c.id === req.params.id);
        if (idx === -1) return res.status(404).json({ message: 'Contact not found' });
        const removed = contacts.splice(idx, 1)[0];
        await writeContacts(contacts);
        res.json({ deleted: removed });
    } catch (error) {
        console.error('Error deleting contact:', error);
        res.status(500).json({ message: 'Error deleting contact' });
    }
});

// Xóa hàng loạt
app.post('/api/contacts/bulk-delete', async (req, res) => {
    const { ids } = req.body || {};
    if (!Array.isArray(ids)) return res.status(400).json({ message: 'ids must be an array' });
    try {
        let contacts = await readContacts();
        const before = contacts.length;
        contacts = contacts.filter(c => !ids.includes(c.id));
        await writeContacts(contacts);
        res.json({ deleted: before - contacts.length });
    } catch (error) {
        console.error('Error bulk deleting:', error);
        res.status(500).json({ message: 'Error bulk deleting' });
    }
});

// Mô phỏng gửi SMS
app.post('/api/contacts/send-sms', async (req, res) => {
    const { ids, message } = req.body || {};
    if (!Array.isArray(ids) || !message) return res.status(400).json({ message: 'ids and message are required' });
    try {
        const contacts = await readContacts();
        const targets = contacts.filter(c => ids.includes(c.id));
        const results = targets.map(c => ({ id: c.id, phone: c.phone, status: 'sent', message }));
        console.log('SMS sent to', results);
        res.json({ sent: results.length, results });
    } catch (error) {
        console.error('Error sending SMS:', error);
        res.status(500).json({ message: 'Error sending SMS' });
    }
});

// Mô phỏng gửi Email
app.post('/api/contacts/send-email', async (req, res) => {
    const { ids, subject, message } = req.body || {};
    if (!Array.isArray(ids) || !subject || !message) return res.status(400).json({ message: 'ids, subject and message are required' });
    try {
        const contacts = await readContacts();
        const targets = contacts.filter(c => ids.includes(c.id));
        const results = targets.map(c => ({ id: c.id, email: c.email, status: 'sent', subject, message }));
        console.log('Email sent to', results);
        res.json({ sent: results.length, results });
    } catch (error) {
        console.error('Error sending email:', error);
        res.status(500).json({ message: 'Error sending email' });
    }
});

// dùng để buil nghe 
const subDir = '/';
const logRequests = false;

app.use(subDir, express.static(buildDir));
app.get('*', (req, res) => {
    if (logRequests) {
        console.log(req.method + ' ' + req.url);
    }
    res.sendFile(path.join(buildDir, 'index.html'));
});

const port = process.env.PORT || 4001;

(async () => {
    try {
        await initDB();
        app.listen(port, () => {
            console.log('✓ JSON File Database initialized');
            console.log('✓ Server running on port ' + port);
        });
    } catch (err) {
        console.error('Database initialization failed:', err);
        process.exit(1);
    }
})();