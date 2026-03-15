require('dotenv').config({ path: '.env.server' });
const fs = require('fs').promises;
const path = require('path');

const dbPath = path.join(__dirname, 'data', 'contacts.json');
const dataDir = path.join(__dirname, 'data');

// db test backend đổi môi trường lại thành mysql2 dùng nodejs . cái này đang dùng chat gpt để test app
async function ensureDataDir() {
  try {
    await fs.mkdir(dataDir, { recursive: true });
  } catch (err) {
    console.error('Error creating data dir:', err);
  }
}

async function readContacts() {
  await ensureDataDir();
  try {
    const text = await fs.readFile(dbPath, 'utf8');
    return JSON.parse(text || '[]');
  } catch (err) {
    if (err.code === 'ENOENT') return [];
    console.error('Error reading contacts:', err);
    return [];
  }
}

async function writeContacts(contacts) {
  await ensureDataDir();
  try {
    await fs.writeFile(dbPath, JSON.stringify(contacts, null, 2), 'utf8');
  } catch (err) {
    console.error('Error writing contacts:', err);
    throw err;
  }
}

async function initDB() {
  await ensureDataDir();
  try {
    await fs.access(dbPath);
  } catch (err) {
    if (err.code === 'ENOENT') {
      await fs.writeFile(dbPath, '[]', 'utf8');
    }
  }
}

module.exports = { readContacts, writeContacts, initDB };


