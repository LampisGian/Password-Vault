from password_vault import PasswordVault


def main():
    vault = PasswordVault()

    vault.add_entry(
        name="Gmail",
        url="https://mail.google.com",
        username="user@gmail.com",
        password="MyStrongPassword123!",
        notes="Personal account"
    )

    print("Credential added successfully.")


if __name__ == "__main__":
    main()