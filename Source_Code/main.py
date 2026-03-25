import tkinter as tk
from tkinter import ttk
from password_vault import PasswordVault


BG = "#0b1220"
SURFACE = "#111827"
CARD = "#182235"
CARD_2 = "#22304a"
TEXT = "#e5e7eb"
MUTED = "#94a3b8"
ACCENT = "#38bdf8"
ACCENT_HOVER = "#0ea5e9"
SUCCESS = "#22c55e"
WARNING = "#f59e0b"
DANGER = "#ef4444"
BORDER = "#334155"
INPUT_BG = "#0f172a"


class PasswordVaultApp:
    def __init__(self, root):
        self.root = root
        self.vault = PasswordVault()
        self.selected_entry_id = None

        self.root.title("Password Vault")
        self.root.geometry("1280x760")
        self.root.minsize(1120, 680)
        self.root.configure(bg=BG)

        self.search_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.url_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.notes_var = tk.StringVar()
        self.updated_at_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")

        self._configure_styles()
        self._build_overlay_system()

        if not self.setup_or_unlock_vault():
            self.root.destroy()
            return

        self._build_ui()
        self.refresh_entries()

    def _configure_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Treeview",
            background=SURFACE,
            foreground=TEXT,
            fieldbackground=SURFACE,
            rowheight=34,
            borderwidth=0,
            font=("Helvetica", 11)
        )
        style.map(
            "Treeview",
            background=[("selected", ACCENT_HOVER)],
            foreground=[("selected", "#ffffff")]
        )
        style.configure(
            "Treeview.Heading",
            background=CARD_2,
            foreground=TEXT,
            relief="flat",
            borderwidth=0,
            font=("Helvetica", 11, "bold")
        )
        style.map("Treeview.Heading", background=[("active", CARD_2)])

        style.configure(
            "Vertical.TScrollbar",
            troughcolor=SURFACE,
            background=CARD_2,
            bordercolor=SURFACE,
            arrowcolor=TEXT
        )

    def _build_overlay_system(self):
        self.overlay = tk.Frame(self.root, bg="#000000")
        self.overlay.place_forget()

        self.overlay_card = tk.Frame(
            self.overlay,
            bg=CARD,
            highlightthickness=1,
            highlightbackground=BORDER
        )

        self.modal_done = tk.StringVar(value="")
        self.modal_result = None
        self.modal_inputs = []

    def _show_overlay(self):
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)
        self.overlay.lift()

    def _hide_overlay(self):
        for widget in self.overlay.winfo_children():
            widget.destroy()
        self.overlay.place_forget()

    def _center_overlay_card(self, width=460):
        self.overlay_card = tk.Frame(
            self.overlay,
            bg=CARD,
            highlightthickness=1,
            highlightbackground=BORDER
        )
        self.overlay_card.place(relx=0.5, rely=0.5, anchor="center", width=width)

    def _complete_modal(self, result):
        self.modal_result = result
        self.modal_done.set("done")
        self._hide_overlay()

    def _build_overlay_header(self, title, color):
        top_bar = tk.Frame(self.overlay_card, bg=color, height=6)
        top_bar.pack(fill="x")

        body = tk.Frame(self.overlay_card, bg=CARD, padx=24, pady=22)
        body.pack(fill="both", expand=True)

        tk.Label(
            body,
            text=title,
            bg=CARD,
            fg=TEXT,
            font=("Helvetica", 16, "bold")
        ).pack(anchor="w", pady=(0, 10))

        return body

    def notify(self, title, message, kind="info"):
        color = ACCENT
        if kind == "success":
            color = SUCCESS
        elif kind == "warning":
            color = WARNING
        elif kind == "error":
            color = DANGER

        toast = tk.Frame(
            self.root,
            bg=CARD,
            highlightthickness=1,
            highlightbackground=BORDER
        )
        toast.place(relx=1.0, x=-18, y=18, anchor="ne")

        stripe = tk.Frame(toast, bg=color, width=6)
        stripe.pack(side="left", fill="y")

        body = tk.Frame(toast, bg=CARD, padx=14, pady=12)
        body.pack(side="left", fill="both", expand=True)

        tk.Label(
            body,
            text=title,
            bg=CARD,
            fg=TEXT,
            font=("Helvetica", 11, "bold")
        ).pack(anchor="w")

        tk.Label(
            body,
            text=message,
            bg=CARD,
            fg=MUTED,
            font=("Helvetica", 10),
            justify="left",
            wraplength=320
        ).pack(anchor="w", pady=(4, 0))

        self.root.after(2600, toast.destroy)

    def confirm(self, title, message, kind="warning"):
        color = WARNING if kind == "warning" else ACCENT

        self.modal_done.set("")
        self.modal_result = False
        self._show_overlay()
        self._center_overlay_card(470)

        body = self._build_overlay_header(title, color)

        tk.Label(
            body,
            text=message,
            bg=CARD,
            fg=MUTED,
            font=("Helvetica", 11),
            justify="left",
            wraplength=380
        ).pack(anchor="w")

        button_row = tk.Frame(body, bg=CARD)
        button_row.pack(fill="x", pady=(20, 0))

        tk.Button(
            button_row,
            text="Cancel",
            bg=CARD_2,
            fg=TEXT,
            activebackground="#334155",
            activeforeground=TEXT,
            relief="flat",
            padx=18,
            pady=10,
            bd=0,
            command=lambda: self._complete_modal(False)
        ).pack(side="right", padx=(8, 0))

        tk.Button(
            button_row,
            text="Confirm",
            bg=DANGER if kind == "warning" else ACCENT_HOVER,
            fg="white",
            activebackground="#dc2626" if kind == "warning" else ACCENT,
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=10,
            bd=0,
            command=lambda: self._complete_modal(True)
        ).pack(side="right")

        self.root.wait_variable(self.modal_done)
        return self.modal_result

    def ask_fields(self, title, fields, submit_text="Submit", stripe_color=ACCENT, width=520):
        self.modal_done.set("")
        self.modal_result = None
        self.modal_inputs = []
        self._show_overlay()
        self._center_overlay_card(width)

        body = self._build_overlay_header(title, stripe_color)

        form = tk.Frame(body, bg=CARD)
        form.pack(fill="both", expand=True)

        for field in fields:
            row = tk.Frame(form, bg=CARD)
            row.pack(fill="x", pady=7)

            tk.Label(
                row,
                text=field["label"],
                bg=CARD,
                fg=MUTED,
                font=("Helvetica", 11),
                width=16,
                anchor="w"
            ).pack(side="left", padx=(0, 10))

            var = tk.StringVar(value=field.get("value", ""))

            entry = tk.Entry(
                row,
                textvariable=var,
                bg=INPUT_BG,
                fg=TEXT,
                insertbackground=TEXT,
                relief="flat",
                highlightthickness=1,
                highlightbackground=BORDER,
                highlightcolor=ACCENT,
                font=("Helvetica", 11),
                show="*" if field.get("hidden", False) else ""
            )
            entry.pack(side="left", fill="x", expand=True, ipady=8)

            if field.get("readonly", False):
                entry.configure(state="readonly")

            if field.get("focus", False):
                entry.focus_set()

            self.modal_inputs.append(var)

        button_row = tk.Frame(body, bg=CARD)
        button_row.pack(fill="x", pady=(18, 0))

        tk.Button(
            button_row,
            text="Cancel",
            bg=CARD_2,
            fg=TEXT,
            activebackground="#334155",
            activeforeground=TEXT,
            relief="flat",
            padx=18,
            pady=10,
            bd=0,
            command=lambda: self._complete_modal(None)
        ).pack(side="right", padx=(8, 0))

        tk.Button(
            button_row,
            text=submit_text,
            bg=ACCENT_HOVER,
            fg="white",
            activebackground=ACCENT,
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=10,
            bd=0,
            command=lambda: self._complete_modal([v.get().strip() for v in self.modal_inputs])
        ).pack(side="right")

        self.root.wait_variable(self.modal_done)
        return self.modal_result

    def setup_or_unlock_vault(self):
        if not self.vault.is_master_password_set():
            while True:
                values = self.ask_fields(
                    "Create Master Password",
                    [
                        {"label": "New master password", "hidden": True, "focus": True},
                        {"label": "Confirm password", "hidden": True}
                    ],
                    submit_text="Create",
                    stripe_color=ACCENT
                )

                if values is None:
                    return False

                password, confirm_password = values

                if not password:
                    self.notify("Error", "Master password cannot be empty.", kind="error")
                    continue

                if password != confirm_password:
                    self.notify("Error", "Passwords do not match.", kind="error")
                    continue

                try:
                    self.vault.set_master_password(password)
                    self.notify("Success", "Master password created successfully.", kind="success")
                    return True
                except Exception as error:
                    self.notify("Error", str(error), kind="error")
                    return False

        attempts = 5

        while attempts > 0:
            values = self.ask_fields(
                "Unlock Vault",
                [{"label": "Master password", "hidden": True, "focus": True}],
                submit_text="Unlock",
                stripe_color=ACCENT
            )

            if values is None:
                return False

            password = values[0]

            if self.vault.unlock_vault(password):
                self.notify("Welcome", "Vault unlocked successfully.", kind="success")
                return True

            attempts -= 1
            if attempts > 0:
                self.notify("Access Denied", f"Wrong master password. Attempts left: {attempts}", kind="error")

        should_format = self.confirm(
            "Too Many Failed Attempts",
            "You entered the wrong master password 5 times.\nDo you want to format the vault and create a new one?",
            kind="warning"
        )

        if not should_format:
            return False

        confirm_values = self.ask_fields(
            "Confirm Format",
            [{"label": "Type FORMAT", "focus": True}],
            submit_text="Format",
            stripe_color=WARNING,
            width=460
        )

        if confirm_values is None or confirm_values[0] != "FORMAT":
            self.notify("Cancelled", "Format cancelled.", kind="warning")
            return False

        self.vault.reset_vault()

        while True:
            values = self.ask_fields(
                "New Master Password",
                [
                    {"label": "New master password", "hidden": True, "focus": True},
                    {"label": "Confirm password", "hidden": True}
                ],
                submit_text="Create",
                stripe_color=SUCCESS
            )

            if values is None:
                return False

            password, confirm_password = values

            if not password:
                self.notify("Error", "Master password cannot be empty.", kind="error")
                continue

            if password != confirm_password:
                self.notify("Error", "Passwords do not match.", kind="error")
                continue

            self.vault.set_master_password(password)
            self.notify("Success", "Vault formatted and new master password created.", kind="success")
            return True

    def _make_entry(self, parent, variable):
        return tk.Entry(
            parent,
            textvariable=variable,
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
            font=("Helvetica", 11)
        )

    def _build_detail_row(self, parent, row, label, variable, command):
        tk.Label(
            parent,
            text=label,
            bg=CARD,
            fg=MUTED,
            font=("Helvetica", 11)
        ).grid(row=row, column=0, sticky="w", pady=12, padx=(0, 12))

        self._make_entry(parent, variable).grid(row=row, column=1, sticky="ew", pady=12)

        tk.Button(
            parent,
            text="Update",
            bg=CARD_2,
            fg=TEXT,
            activebackground="#334155",
            activeforeground=TEXT,
            relief="flat",
            padx=14,
            pady=8,
            bd=0,
            command=command
        ).grid(row=row, column=2, padx=(12, 0), pady=12)

    def _build_ui(self):
        shell = tk.Frame(self.root, bg=BG)
        shell.pack(fill="both", expand=True, padx=18, pady=18)

        header = tk.Frame(shell, bg=BG)
        header.pack(fill="x", pady=(0, 14))

        tk.Label(
            header,
            text="Password Vault",
            bg=BG,
            fg=TEXT,
            font=("Helvetica", 24, "bold")
        ).pack(side="left")

        tk.Label(
            header,
            text="Secure credential manager",
            bg=BG,
            fg=MUTED,
            font=("Helvetica", 11)
        ).pack(side="left", padx=(14, 0), pady=(8, 0))

        toolbar_card = tk.Frame(shell, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        toolbar_card.pack(fill="x", pady=(0, 14))

        toolbar = tk.Frame(toolbar_card, bg=CARD, padx=16, pady=14)
        toolbar.pack(fill="x")

        search_container = tk.Frame(toolbar, bg=INPUT_BG, highlightthickness=1, highlightbackground=BORDER)
        search_container.pack(side="left", fill="x", expand=True, padx=(0, 10))

        search_entry = tk.Entry(
            search_container,
            textvariable=self.search_var,
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            font=("Helvetica", 11)
        )
        search_entry.pack(fill="x", padx=12, pady=10)

        tk.Button(
            toolbar,
            text="Search",
            bg=ACCENT_HOVER,
            fg="white",
            activebackground=ACCENT,
            activeforeground="white",
            relief="flat",
            padx=16,
            pady=9,
            bd=0,
            command=self.search_entries
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            toolbar,
            text="Show All",
            bg=CARD_2,
            fg=TEXT,
            activebackground="#334155",
            activeforeground=TEXT,
            relief="flat",
            padx=16,
            pady=9,
            bd=0,
            command=self.refresh_entries
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            toolbar,
            text="+ Add",
            bg=ACCENT_HOVER,
            fg="white",
            activebackground=ACCENT,
            activeforeground="white",
            relief="flat",
            padx=16,
            pady=9,
            bd=0,
            command=self.open_add_overlay
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            toolbar,
            text="Delete",
            bg=DANGER,
            fg="white",
            activebackground="#dc2626",
            activeforeground="white",
            relief="flat",
            padx=16,
            pady=9,
            bd=0,
            command=self.delete_selected_entry
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            toolbar,
            text="Change Master Password",
            bg=CARD_2,
            fg=TEXT,
            activebackground="#334155",
            activeforeground=TEXT,
            relief="flat",
            padx=16,
            pady=9,
            bd=0,
            command=self.change_master_password
        ).pack(side="right")

        content = tk.Frame(shell, bg=BG)
        content.pack(fill="both", expand=True)

        left_card = tk.Frame(content, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        left_card.pack(side="left", fill="both", expand=False, padx=(0, 10))
        left_card.configure(width=420)

        right_card = tk.Frame(content, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        right_card.pack(side="left", fill="both", expand=True)

        left_header = tk.Frame(left_card, bg=CARD, padx=16, pady=14)
        left_header.pack(fill="x")

        tk.Label(
            left_header,
            text="Stored Entries",
            bg=CARD,
            fg=TEXT,
            font=("Helvetica", 16, "bold")
        ).pack(anchor="w")

        tk.Label(
            left_header,
            text="Select an item to view or edit its details",
            bg=CARD,
            fg=MUTED,
            font=("Helvetica", 10)
        ).pack(anchor="w", pady=(4, 0))

        tree_frame = tk.Frame(left_card, bg=CARD, padx=12, pady=12)
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=("id", "name", "username"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Site / Name")
        self.tree.heading("username", text="Username")
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("name", width=180, anchor="w")
        self.tree.column("username", width=150, anchor="w")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        right_header = tk.Frame(right_card, bg=CARD, padx=20, pady=16)
        right_header.pack(fill="x")

        tk.Label(
            right_header,
            text="Credential Details",
            bg=CARD,
            fg=TEXT,
            font=("Helvetica", 18, "bold")
        ).pack(anchor="w")

        tk.Label(
            right_header,
            text="Edit any field and save changes instantly",
            bg=CARD,
            fg=MUTED,
            font=("Helvetica", 10)
        ).pack(anchor="w", pady=(4, 0))

        detail_body = tk.Frame(right_card, bg=CARD, padx=20, pady=8)
        detail_body.pack(fill="both", expand=True)

        self._build_detail_row(detail_body, 0, "Name", self.name_var, self.update_name)
        self._build_detail_row(detail_body, 1, "URL", self.url_var, self.update_url)
        self._build_detail_row(detail_body, 2, "Username", self.username_var, self.update_username)
        self._build_detail_row(detail_body, 3, "Password", self.password_var, self.update_password)
        self._build_detail_row(detail_body, 4, "Notes", self.notes_var, self.update_notes)

        tk.Label(
            detail_body,
            text="Updated At",
            bg=CARD,
            fg=MUTED,
            font=("Helvetica", 11)
        ).grid(row=5, column=0, sticky="w", pady=12, padx=(0, 12))

        updated_entry = tk.Entry(
            detail_body,
            textvariable=self.updated_at_var,
            state="readonly",
            readonlybackground=INPUT_BG,
            fg=TEXT,
            relief="flat",
            font=("Helvetica", 11),
            width=44
        )
        updated_entry.grid(row=5, column=1, sticky="ew", pady=12)

        action_row = tk.Frame(detail_body, bg=CARD)
        action_row.grid(row=6, column=1, sticky="w", pady=(10, 0))

        tk.Button(
            action_row,
            text="Generate New Password",
            bg=ACCENT_HOVER,
            fg="white",
            activebackground=ACCENT,
            activeforeground="white",
            relief="flat",
            padx=16,
            pady=9,
            bd=0,
            command=self.generate_password_for_selected
        ).pack(side="left", padx=(0, 10))

        detail_body.columnconfigure(1, weight=1)

        status_bar = tk.Frame(shell, bg=CARD, highlightthickness=1, highlightbackground=BORDER, padx=14, pady=10)
        status_bar.pack(fill="x", pady=(14, 0))

        tk.Label(
            status_bar,
            textvariable=self.status_var,
            bg=CARD,
            fg=MUTED,
            font=("Helvetica", 10)
        ).pack(anchor="w")

    def set_status(self, text):
        self.status_var.set(text)

    def refresh_entries(self):
        try:
            entries = self.vault.retrieve_entries()
            self.populate_tree(entries)
            self.set_status(f"Loaded {len(entries)} credential(s).")
        except Exception as error:
            self.notify("Error", str(error), kind="error")

    def search_entries(self):
        try:
            entries = self.vault.search_entries(self.search_var.get())
            self.populate_tree(entries)
            self.set_status(f"Found {len(entries)} matching credential(s).")
        except Exception as error:
            self.notify("Error", str(error), kind="error")

    def populate_tree(self, entries):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for entry in entries:
            self.tree.insert("", "end", values=(entry["id"], entry["name"], entry["username"]))

        self.clear_details()

    def clear_details(self):
        self.selected_entry_id = None
        self.name_var.set("")
        self.url_var.set("")
        self.username_var.set("")
        self.password_var.set("")
        self.notes_var.set("")
        self.updated_at_var.set("")

    def on_tree_select(self, event=None):
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        entry_id = int(item["values"][0])

        try:
            entry = self.vault.get_entry_by_id(entry_id)
            if entry is None:
                self.clear_details()
                return

            self.selected_entry_id = entry["id"]
            self.name_var.set(entry["name"])
            self.url_var.set(entry["url"])
            self.username_var.set(entry["username"])
            self.password_var.set(entry["password"])
            self.notes_var.set(entry["notes"])
            self.updated_at_var.set(entry["updated_at"])
            self.set_status(f"Selected entry #{entry['id']} - {entry['name']}")
        except Exception as error:
            self.notify("Error", str(error), kind="error")

    def update_selected_entry(self):
        if self.selected_entry_id is None:
            self.notify("No Selection", "Select an entry first.", kind="warning")
            return

        try:
            updated = self.vault.update_entry(
                self.selected_entry_id,
                self.name_var.get(),
                self.url_var.get(),
                self.username_var.get(),
                self.password_var.get(),
                self.notes_var.get()
            )

            if updated:
                self.refresh_after_update()
                self.notify("Success", "Entry updated successfully.", kind="success")
            else:
                self.notify("Error", "Entry not found.", kind="error")
        except Exception as error:
            self.notify("Error", str(error), kind="error")

    def refresh_after_update(self):
        current_id = self.selected_entry_id
        current_query = self.search_var.get().strip()

        if current_query:
            entries = self.vault.search_entries(current_query)
        else:
            entries = self.vault.retrieve_entries()

        self.populate_tree(entries)

        for child in self.tree.get_children():
            values = self.tree.item(child)["values"]
            if int(values[0]) == current_id:
                self.tree.selection_set(child)
                self.tree.focus(child)
                self.tree.see(child)
                self.on_tree_select()
                break

    def update_name(self):
        self.update_selected_entry()

    def update_url(self):
        self.update_selected_entry()

    def update_username(self):
        self.update_selected_entry()

    def update_password(self):
        self.update_selected_entry()

    def update_notes(self):
        self.update_selected_entry()

    def generate_password_for_selected(self):
        if self.selected_entry_id is None:
            self.notify("No Selection", "Select an entry first.", kind="warning")
            return

        values = self.ask_fields(
            "Generate Strong Password",
            [{"label": "Password length", "value": "12", "focus": True}],
            submit_text="Generate",
            stripe_color=ACCENT,
            width=460
        )

        if values is None:
            return

        try:
            length = int(values[0])
            generated = self.vault.generate_password(length)
            self.password_var.set(generated)
            self.set_status("Generated a new strong password for the selected entry.")
            self.notify("Generated", "A new strong password was generated.", kind="success")
        except Exception as error:
            self.notify("Error", str(error), kind="error")

    def open_add_overlay(self):
        values = self.ask_fields(
            "Add New Credential",
            [
                {"label": "Name", "focus": True},
                {"label": "URL"},
                {"label": "Username"},
                {"label": "Password"},
                {"label": "Notes"}
            ],
            submit_text="Save",
            stripe_color=ACCENT,
            width=560
        )

        if values is None:
            return

        name, url, username, password, notes = values

        try:
            self.vault.add_entry(name, url, username, password, notes)
            self.refresh_entries()
            self.notify("Success", "Credential added successfully.", kind="success")
        except Exception as error:
            self.notify("Error", str(error), kind="error")

    def delete_selected_entry(self):
        if self.selected_entry_id is None:
            self.notify("No Selection", "Select an entry first.", kind="warning")
            return

        confirmed = self.confirm(
            "Delete Credential",
            "Are you sure you want to delete the selected credential?\nThis action cannot be undone.",
            kind="warning"
        )

        if not confirmed:
            return

        try:
            deleted = self.vault.delete_entry(self.selected_entry_id)
            if deleted:
                self.refresh_entries()
                self.notify("Deleted", "Credential deleted successfully.", kind="success")
            else:
                self.notify("Error", "Entry not found.", kind="error")
        except Exception as error:
            self.notify("Error", str(error), kind="error")

    def change_master_password(self):
        old_values = self.ask_fields(
            "Change Master Password",
            [{"label": "Current password", "hidden": True, "focus": True}],
            submit_text="Next",
            stripe_color=ACCENT,
            width=500
        )

        if old_values is None:
            return

        old_password = old_values[0]

        new_values = self.ask_fields(
            "Change Master Password",
            [
                {"label": "New password", "hidden": True, "focus": True},
                {"label": "Confirm password", "hidden": True}
            ],
            submit_text="Change",
            stripe_color=SUCCESS,
            width=500
        )

        if new_values is None:
            return

        new_password, confirm_password = new_values

        if not new_password:
            self.notify("Error", "New master password cannot be empty.", kind="error")
            return

        if new_password != confirm_password:
            self.notify("Error", "Passwords do not match.", kind="error")
            return

        try:
            changed = self.vault.change_master_password(old_password, new_password)
            if changed:
                self.notify("Success", "Master password changed successfully.", kind="success")
                self.set_status("Master password updated.")
            else:
                self.notify("Error", "Current master password is incorrect.", kind="error")
        except Exception as error:
            self.notify("Error", str(error), kind="error")


def main():
    root = tk.Tk()
    PasswordVaultApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()