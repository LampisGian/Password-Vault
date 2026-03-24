from password_vault import PasswordVault


def print_menu():
    print("\n=== Password Vault ===")
    print("1. Add credential")
    print("2. View all credentials")
    print("3. Edit credential")
    print("4. Delete credential")
    print("5. Exit")


def read_non_empty_input(label):
    value = input(label).strip()
    while not value:
        print("This field cannot be empty.")
        value = input(label).strip()
    return value


def read_optional_input(label):
    return input(label).strip()


def read_entry_id():
    while True:
        raw_value = input("Enter credential ID: ").strip()
        if raw_value.isdigit() and int(raw_value) > 0:
            return int(raw_value)
        print("Please enter a valid positive number.")


def add_credential_cli(vault: PasswordVault):
    print("\nAdd Credential")
    name = read_non_empty_input("Name: ")
    url = read_optional_input("URL: ")
    username = read_non_empty_input("Username: ")
    password = read_non_empty_input("Password: ")
    notes = read_optional_input("Notes: ")

    try:
        vault.add_entry(name, url, username, password, notes)
        print("Credential added successfully.")
    except ValueError as error:
        print(error)


def view_credentials_cli(vault: PasswordVault):
    print("\nStored Credentials")
    entries = vault.retrieve_entries()

    if not entries:
        print("No credentials found.")
        return

    for entry in entries:
        print("-" * 40)
        print(f"ID: {entry['id']}")
        print(f"Name: {entry['name']}")
        print(f"URL: {entry['url']}")
        print(f"Username: {entry['username']}")
        print(f"Password: {entry['password']}")
        print(f"Notes: {entry['notes']}")
        print(f"Updated At: {entry['updated_at']}")


def edit_credential_cli(vault: PasswordVault):
    print("\nEdit Credential")
    entry_id = read_entry_id()
    existing_entry = vault.get_entry_by_id(entry_id)

    if existing_entry is None:
        print("Credential not found.")
        return

    print("Leave a field empty to keep the current value.")

    name = input(f"Name [{existing_entry['name']}]: ").strip() or existing_entry["name"]
    url = input(f"URL [{existing_entry['url']}]: ").strip() or existing_entry["url"]
    username = input(f"Username [{existing_entry['username']}]: ").strip() or existing_entry["username"]
    password = input(f"Password [{existing_entry['password']}]: ").strip() or existing_entry["password"]
    notes = input(f"Notes [{existing_entry['notes']}]: ").strip() or existing_entry["notes"]

    try:
        updated = vault.update_entry(entry_id, name, url, username, password, notes)
        if updated:
            print("Credential updated successfully.")
        else:
            print("Credential not found.")
    except ValueError as error:
        print(error)


def delete_credential_cli(vault: PasswordVault):
    print("\nDelete Credential")
    entry_id = read_entry_id()
    existing_entry = vault.get_entry_by_id(entry_id)

    if existing_entry is None:
        print("Credential not found.")
        return

    confirm = input(f"Are you sure you want to delete '{existing_entry['name']}'? (y/n): ").strip().lower()

    if confirm != "y":
        print("Delete cancelled.")
        return

    try:
        deleted = vault.delete_entry(entry_id)
        if deleted:
            print("Credential deleted successfully.")
        else:
            print("Credential not found.")
    except ValueError as error:
        print(error)


def main():
    vault = PasswordVault()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_credential_cli(vault)
        elif choice == "2":
            view_credentials_cli(vault)
        elif choice == "3":
            edit_credential_cli(vault)
        elif choice == "4":
            delete_credential_cli(vault)
        elif choice == "5":
            print("Exiting Password Vault.")
            break
        else:
            print("Invalid option. Please choose 1-5.")


if __name__ == "__main__":
    main()