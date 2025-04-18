import mysql.connector
from cryptography.fernet import Fernet
import hashlib
import base64

# 🔐 Generate encryption key from second password
def generate_key(second_password):
    hashed = hashlib.sha256(second_password.encode()).digest()
    return base64.urlsafe_b64encode(hashed)

# 🔐 Encrypt data
def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

# 🔐 Decrypt data
def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()

# 📦 Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Hackmebro1@#",  # Change to your DB password
    database="employee_db"
)
cursor = conn.cursor()

# 🔁 Menu Loop
while True:
    print("\n🔘 Choose an option:")
    print("1. ➕ Add New Employee")
    print("2. 📄 Show Encrypted Data")
    print("3. 🔓 Decrypt Your Data")
    print("4. ❌ Exit")

    choice = input("Enter your choice (1/2/3/4): ")

    match choice:
        case '1':
            print("\n🔹 Add New Employee")
            username = input("Enter username: ").strip()
            if not username:
                print("❌ Username cannot be empty!")
                continue

            password = input("Enter password: ")
            second_password = input("Enter second password (exactly 8 characters): ")

            if len(second_password) != 8:
                print("❌ Second password must be 8 characters long!\n")
                continue

            key = generate_key(second_password)
            encrypted_username = encrypt_data(username, key)
            encrypted_password = encrypt_data(password, key)
            hashed_second_password = hashlib.sha256(second_password.encode()).hexdigest()

            query = "INSERT INTO employees (username, hashed_password, second_password_hash) VALUES (%s, %s, %s)"
            values = (encrypted_username, encrypted_password, hashed_second_password)

            try:
                cursor.execute(query, values)
                conn.commit()
                print("✅ Employee added successfully.")
            except mysql.connector.IntegrityError:
                print("⚠️ Duplicate entry or error occurred.")

        case '2':
            cursor.execute("SELECT username, hashed_password, second_password_hash FROM employees")
            data = cursor.fetchall()
            if not data:
                print("📭 No data found in the database.")
            else:
                print("\n🔐 Encrypted Records:")
                for i, row in enumerate(data, start=1):
                    enc_user, enc_pass, hash_val = row
                    print(f"{i}. 🧾 Username (Encrypted): {enc_user}")
                    print(f"   🔑 Password (Encrypted): {enc_pass}")
                    print(f"   🧪 Second Password Hash: {hash_val}\n")

        case '3':
            cursor.execute("SELECT * FROM employees")
            data = cursor.fetchall()
            if not data:
                print("📭 No data to decrypt.")
            else:
                second_pass_input = input("\nEnter your second password to decrypt your data: ")
                key = generate_key(second_pass_input)
                hashed_input = hashlib.sha256(second_pass_input.encode()).hexdigest()

                cursor.execute("SELECT username, hashed_password FROM employees WHERE second_password_hash = %s", (hashed_input,))
                result = cursor.fetchall()

                if result:
                    print("\n🔓 Your Decrypted Credentials:")
                    for row in result:
                        try:
                            decrypted_username = decrypt_data(row[0], key)
                            decrypted_password = decrypt_data(row[1], key)
                            print(f"👤 Username: {decrypted_username} | 🔑 Password: {decrypted_password}")
                        except:
                            print("❌ Decryption failed for a record.")
                else:
                    print("⚠️ No records matched with that second password.")

        case '4':
            print("👋 Exiting... Bye!")
            break

        case _:
            print("❌ Invalid choice, try again.")

# 🧹 Cleanup
cursor.close()
conn.close()
