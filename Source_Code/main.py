from password_vault import PasswordVault


def main():
    vault = PasswordVault()

    # Add sample entry
    vault.add_entry(
        name="Gmail",
        url="https://mail.google.com",
        username="user@gmail.com",
        password="MyStrongPassword123!",
        notes="Personal account"
    )

    # Retrieve and display all entries
    entries = vault.retrieve_entries()

    for entry in entries:
        print("----------------------------")
        print(f"ID: {entry['id']}")
        print(f"Name: {entry['name']}")
        print(f"URL: {entry['url']}")
        print(f"Username: {entry['username']}")
        print(f"Password: {entry['password']}")
        print(f"Notes: {entry['notes']}")
        print(f"Updated At: {entry['updated_at']}")


if __name__ == "__main__":
    main()