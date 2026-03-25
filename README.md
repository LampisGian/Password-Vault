# Password Vault

# Description
PassVault is a secure password manager application that uses encryption and a local SQLite database to store user credentials safely through a graphical user interface. The system allows users to manage their passwords locally, while protecting sensitive information by encrypting stored passwords instead of saving them in plain text.

## Getting Started
### 1) macOS app (`.app`)
- Download **PassVault.zip**
- Unzip the file
- Open the generated **.app** to launch the application directly on macOS

> **Note:** On macOS, the application stores its working files in the **Application Support** directory.  
To load the prepared database, open the following path:

 `/Users/<your-username>/Library/Application Support/PassVault`

 Then copy the files:
 - `vault.db`
 - `master_config.json`

 into that folder.  
 After that, open the application and it will load the ready-made vault data correctly.

> **Default master password:** `1234`

> **Security note:** If the master password is entered incorrectly 5 times, the application provides the option to **format the database** and start again from the beginning with a new vault setup.

---

### 2) Run from source (Python)
- Download (or clone) the full project folder
- Open a terminal in the project directory
- Run the GUI script:

```bash
python main.py
# or
python3 main.py
```

> **Note:**: When running from source, make sure the files vault.db and master_config.json are placed inside the project folder so the application can load the prepared database correctly.

## Tasks
- Research cryptography or fernet and SQLite. Plan database schema: site, username, password, notes.
- Implement database and function to add credentials. Encrypt passwords before storing.
- Create function to retrieve credentials (decrypt passwords).- Document the code.
- Add edit and delete features. Validate inputs.
- Add master password that unlocks access to vault.
- Add password generator (random strong passwords).
- Build a CLI or tkinter GUI: list entries, search, and view decrypted passwords.
- Add export to encrypted .txt file for backup.
- Add error handling, fix bugs, and test with mock data.
- Final testing. Create README with instructions and screenshots. Submit as Git repo.

## Estimated time to work 2 weeks
