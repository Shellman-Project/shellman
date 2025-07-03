🔐 **Encrypt or Decrypt Files Using AES-256**

This command allows you to securely encrypt or decrypt multiple files in a directory using AES-256 and a password.

---

### 🧠 How It Works

- AES-256 in CBC mode is used with a password-based key (PBKDF2)
- Each file is processed individually
- Encrypted files include salt + IV + ciphertext in a single `.enc` file
- Output files are stored in a separate directory

---

### 🔧 Options

- `--mode encrypt|decrypt`: whether to encrypt or decrypt
- `--password`: password used to derive the encryption key
- `--ext`: process only files with this extension
- `--path`: directory to scan recursively (default: current folder)
- `--out`: output directory (default: `encrypted` or `decrypted`)

---

### ⚠️ Notes

- Encryption is secure only if the password is strong
- Encrypted files can be decrypted only with the same password
- File names are preserved, `.enc` is appended during encryption

---

### 📦 Examples

Encrypt `.log` files in the `logs` folder and store them in `secure/`:
shellman encrypt_files --mode encrypt --password mypass --ext log --path ./logs --out ./secure

Decrypt `.enc` files and output to `plain/`:
shellman encrypt_files --mode decrypt --password mypass --ext enc --path ./secure --out ./plain
