# 🔐 KeyCrypt

KeyCrypt is a simple yet secure credential storage system built using Python and MySQL.  
It encrypts and stores usernames and passwords in a database, ensuring only the right person can view and decrypt their own data.

---

## 📌 Features

- Store credentials securely in **encrypted format**
- **Common database password** is required to access any data
- Each user must enter their own **unique 8-character second password** to decrypt their data
- Prevents unauthorized access — no one can see another user's credentials
- Encrypted data remains protected even inside the database

---

## 🔐 Security Workflow

1. **Add Data**:
   - Enter username, password
   - Create a unique 8-character second password
   - Data is encrypted using `Fernet` and stored in MySQL

2. **View Data**:
   - Enter **database password** (common for all)
   - Then enter your **own second password**
   - If matched, you can see your decrypted username & password

3. **Hashing & Encryption**:
   - Passwords are encrypted using `Fernet` (AES-based)
   - Second password is hashed using SHA-256

---

## 💻 Technologies Used

- Python
- MySQL
- `cryptography` (Fernet encryption)
- `hashlib` (SHA-256 hashing)

---

## 🚀 Getting Started

### 📂 Project Structure

