import customtkinter as ctk
import json

class PasswordManagerApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Password Keeper")
        self.root.geometry("800x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.passwords = self.load_passwords()

        self.create_widgets()
        self.show_passwords()

    def create_widgets(self):
        title = ctk.CTkLabel(self.root, text="Password Keeper", font = ctk.CTkFont(size=24,weight="bold"))
        title.pack(pady=20)

        self.site_entry = ctk.CTkEntry(self.root, placeholder_text="App ou Site")
        self.site_entry.pack(pady=10,padx=50,fill="x")

        self.username_entry = ctk.CTkEntry(self.root, placeholder_text="Usuário/Email")
        self.username_entry.pack(pady=10,padx=50,fill="x")

        self.password_entry = ctk.CTkEntry(self.root, placeholder_text="Senha")
        self.password_entry.pack(pady=10,padx=50,fill="x")

        self.delete_combo = ctk.CTkComboBox(self.root, values=[], width=400)
        self.delete_combo.pack(pady=10)

        self.password_display = ctk.CTkTextbox(self.root, height=30)
        self.password_display.pack(pady = 20, padx = 50, fill="both", expand=True)

        delete_select_btn = ctk.CTkButton(self.root, text="Deletar senha", height=30, command=self.delete_selected_password)
        delete_select_btn.pack(pady=10)

        add_btn = ctk.CTkButton(self.root, text="Adicionar senha", height=30, command=self.add_password)
        add_btn.pack(pady=20)

    def add_password(self):
        site = self.site_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if site and username and password:
            text = f"Site: {site}   |   Usuário: {username}   |   senha: {password}\n"
            self.password_display.insert("end", text)

            self.site_entry.delete(0,"end")
            self.username_entry.delete(0,"end")
            self.password_entry.delete(0,"end")

            entry = {"site": site, "username": username, "password": password}
            self.passwords.append(entry)
            self.save_passwords()
            self.update_delete_combo()
        
        else:
            print("Preencha todos os campos")

    def delete_passwords(self):
        self.passwords = []
        self.password_display.delete("1.0", "end")
        with open("passwords.json", "w", encoding="utf-8") as f:
            json.dump(self.passwords, f, ensure_ascii=False, indent=4)

    def delete_selected_password(self):
        selected = self.delete_combo.get()
        if not selected:
            return

        for entry in self.passwords:
            text = f"Site: {entry['site']} | Usuário: {entry['username']} | senha: {entry['password']}"
            if text == selected:
                self.passwords.remove(entry)
                break

        self.save_passwords()
        self.show_passwords()
        self.update_delete_combo()  

    def update_delete_combo(self):
        values = [f"Site: {entry['site']} | Usuário: {entry['username']} | senha: {entry['password']}" for entry in self.passwords]
        self.delete_combo.configure(values=values)
        if values:
            self.delete_combo.set(values[0])
        else:
            self.delete_combo.set("")

    def save_passwords(self):
        with open("passwords.json", "w", encoding="utf-8") as f:
            json.dump(self.passwords, f, ensure_ascii=False, indent=4)
    
    def load_passwords(self):
        try:
            with open("passwords.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except(FileNotFoundError, json.JSONDecodeError):
            return []

    def show_passwords(self):
        self.password_display.delete("1.0", "end")
        for entry in self.passwords:
            text = f"Site: {entry['site']}   |   Usuário: {entry['username']}   |   senha: {entry['password']}\n"
            self.password_display.insert("end", text)
        self.update_delete_combo()

    def run(self):
        self.root.mainloop()
    
if __name__ == "__main__":
    app = PasswordManagerApp()
    app.run()
