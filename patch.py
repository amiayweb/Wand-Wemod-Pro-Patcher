import os
import sys
import glob
import subprocess
import re
import shutil
import time
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

COLORS = {
    "bg_dark": "#020617",
    "bg_card": "#0f172a",
    "bg_header": "#1e293b",
    "accent": "#3b82f6",
    "accent_hover": "#2563eb",
    "text_main": "#f8fafc",
    "text_dim": "#94a3b8",
    "cyan": "#22d3ee",
    "green": "#4ade80",
    "yellow": "#fde047",
    "red": "#f87171",
    "border": "#334155"
}

class ModernButton(tk.Button):
    def __init__(self, master, **kwargs):
        self.normal_bg = kwargs.get("bg", COLORS["accent"])
        self.hover_bg = kwargs.get("hover_bg", COLORS["accent_hover"])
        kwargs.pop("hover_bg", None)
        super().__init__(master, 
            relief="flat", 
            bd=0, 
            cursor="hand2", 
            activebackground=self.hover_bg,
            activeforeground="white",
            **kwargs
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        if self['state'] != 'disabled':
            self['background'] = self.hover_bg

    def on_leave(self, e):
        if self['state'] != 'disabled':
            self['background'] = self.normal_bg

class WeModPatcherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoPro | WeMod (Wand) Patcher")
        self.root.geometry("850x650")
        self.root.minsize(850, 650)
        self.root.maxsize(850, 650)
        self.root.configure(bg=COLORS["bg_dark"])
        self.root.resizable(False, False)
        self.setup_ui()
        self.log("[*] System initialized. Ready to patch this shit.", "cyan")

    def setup_ui(self):
        header = tk.Frame(self.root, bg=COLORS["bg_header"], height=90)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        title_frame = tk.Frame(header, bg=COLORS["bg_header"])
        title_frame.pack(expand=True)

        tk.Label(
            title_frame, text="AUTOPRO", fg=COLORS["accent"], 
            bg=COLORS["bg_header"], font=("Impact", 32)
        ).pack(side="left")
        
        tk.Label(
            title_frame, text="PRO PATCHER", fg=COLORS["text_main"], 
            bg=COLORS["bg_header"], font=("Segoe UI Semibold", 24)
        ).pack(side="left", padx=15)

        workspace = tk.Frame(self.root, bg=COLORS["bg_dark"], padx=30, pady=25)
        workspace.pack(fill="both", expand=True)

        sidebar = tk.Frame(workspace, bg=COLORS["bg_card"], width=260, highlightthickness=1, highlightbackground=COLORS["border"])
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar, text="COMMAND CENTER", fg=COLORS["text_dim"], 
            bg=COLORS["bg_card"], font=("Segoe UI Bold", 10)
        ).pack(pady=(25, 20))

        self.btn_auto = ModernButton(
            sidebar, text="AUTO-DETECT PATCH", 
            command=self.start_auto_patch,
            bg=COLORS["accent"], fg="white", font=("Segoe UI Bold", 10),
            width=22, height=2
        )
        self.btn_auto.pack(pady=12)

        self.btn_manual = ModernButton(
            sidebar, text="MANUAL PATCH", 
            command=self.start_manual_patch,
            bg=COLORS["bg_header"], hover_bg="#475569", 
            fg="white", font=("Segoe UI Semibold", 10),
            width=22, height=2
        )
        self.btn_manual.pack(pady=12)

        tk.Frame(sidebar, bg=COLORS["border"], height=1).pack(fill="x", padx=25, pady=25)

        self.btn_restore = ModernButton(
            sidebar, text="RESTORE ORIGINAL", 
            command=self.start_restore,
            bg="#b91c1c", hover_bg="#dc2626", 
            fg="white", font=("Segoe UI Semibold", 10),
            width=22, height=2
        )
        self.btn_restore.pack(pady=12)

        console_panel = tk.Frame(workspace, bg=COLORS["bg_dark"])
        console_panel.pack(side="right", fill="both", expand=True, padx=(25, 0))

        tk.Label(
            console_panel, text="LOGS", fg=COLORS["text_dim"], 
            bg=COLORS["bg_dark"], font=("Segoe UI Bold", 10)
        ).pack(anchor="w", pady=(0, 12))

        self.log_area = scrolledtext.ScrolledText(
            console_panel, 
            bg="#020617", 
            fg=COLORS["text_main"], 
            font=("Consolas", 10),
            state="disabled",
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            padx=15, pady=15
        )
        self.log_area.pack(fill="both", expand=True)

        self.credits_bar = tk.Frame(self.root, bg=COLORS["bg_header"], height=35)
        self.credits_bar.pack(fill="x", side="bottom")
        
        self.credits_text = tk.Label(
            self.credits_bar, text="MADE BY AMIAY_SEG", 
            fg=COLORS["text_dim"], bg=COLORS["bg_header"], 
            font=("Segoe UI Bold", 9), padx=15
        )
        self.credits_text.pack(side="left")

        self.log_area.tag_config("cyan", foreground=COLORS["cyan"])
        self.log_area.tag_config("green", foreground=COLORS["green"])
        self.log_area.tag_config("yellow", foreground=COLORS["yellow"])
        self.log_area.tag_config("red", foreground=COLORS["red"])
        self.log_area.tag_config("white", foreground=COLORS["text_main"])

    def clear_logs(self):
        self.log_area.configure(state="normal")
        self.log_area.delete('1.0', tk.END)
        self.log_area.configure(state="disabled")

    def log(self, message, color="white"):
        self.log_area.configure(state="normal")
        self.log_area.insert(tk.END, f"{message}\n", color)
        self.log_area.configure(state="disabled")
        self.log_area.see(tk.END)
        self.root.update_idletasks()

    def kill_wemod(self):
        self.log("[*] Analyzing active processes...", "cyan")
        result = subprocess.run('tasklist /FI "IMAGENAME eq Wand.exe" /FO CSV /NH', shell=True, capture_output=True, text=True)
        if "Wand.exe" in result.stdout:
            self.log("[!] WeMod detected. Force closing...", "yellow")
            subprocess.run('taskkill /F /IM Wand.exe /T', shell=True, capture_output=True)
            time.sleep(1.5)
            self.log("[+] Process terminated successfully.", "green")

    def get_latest_wemod_dir(self):
        local_app_data = os.getenv('LOCALAPPDATA')
        if not local_app_data: return None
        wand_dir = os.path.join(local_app_data, 'Wand')
        if not os.path.exists(wand_dir): return None
        app_dirs = glob.glob(os.path.join(wand_dir, 'app-*'))
        if not app_dirs: return None
        app_dirs.sort(key=lambda x: os.path.basename(x), reverse=True)
        return app_dirs[0]

    def run_command(self, command):
        cmd_display = command.split(' ')[0] + " " + command.split(' ')[1] if len(command.split(' ')) > 1 else command
        self.log(f"[*] Executing module: {cmd_display}...", "white")
        if "npx " in command and "--yes" not in command:
            command = command.replace("npx ", "npx --yes ")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            self.log(f"[!] Critical Error: {result.stderr[:120]}", "red")
            return False
        return True

    def do_patch_logic(self, wemod_exe, asar_file):
        try:
            self.kill_wemod()
            extract_dir = "app_extracted"
            backup_dir = "backups"
            
            self.log("\n--- STAGE 1: ASAR DATA EXTRACTION ---", "cyan")
            if not os.path.exists(backup_dir): os.makedirs(backup_dir)
            bak_path = os.path.join(backup_dir, "app.asar.bak")
            if not os.path.exists(bak_path):
                shutil.copy2(asar_file, bak_path)
                self.log(f"[+] Security backup created: {bak_path}", "green")
                
            if os.path.exists(extract_dir): shutil.rmtree(extract_dir)
            if not self.run_command(f'npx asar extract "{asar_file}" {extract_dir}'): return

            self.log("\n--- STAGE 2: ELECTRON FUSE OVERRIDE ---", "cyan")
            self.run_command(f'npx --yes @electron/fuses write --app "{wemod_exe}" EnableEmbeddedAsarIntegrityValidation=off')

            self.log("\n--- STAGE 3: CORE LOGIC MODIFICATION ---", "cyan")
            patched_count = 0
            for root_dir, _, files in os.walk(extract_dir):
                for file in files:
                    if file.endswith(".js"):
                        path = os.path.join(root_dir, file)
                        try:
                            with open(path, 'r', encoding='utf-8') as f: content = f.read()
                        except: continue

                        orig = content
                        if re.search(r'const\s+a\s*=\s*await\s+this\.#R\.fetch\(i\)', content):
                            self.log(f"[+] Patching API Subsystem: {file}", "yellow")
                            content = re.sub(r'const\s+a\s*=\s*await\s+this\.#R\.fetch\(i\);?\s*return\s+await\s+this\.#M\(a\);?', 
                                'const a=await this.#R.fetch(i);let res=await this.#M(a);if(e.endpoint==="/v3/account"&&res&&typeof res==="object"){res.subscription={startedAt:"2020-01-01T00:00:00Z",state:"active",period:"yearly"};res.flags|=512;}return res', content)

                        if re.search(r'const\s+\w+\s*=\s*\(\w+\)\s*=>\s*!!\w+\?\.subscription', content):
                            self.log(f"[+] Patching Boolean Logic: {file}", "yellow")
                            content = re.sub(r'(const\s+\w+\s*=\s*)\(\w+\)\s*=>\s*!!\w+\?\.subscription', r'\1(e)=>true', content)

                        if content != orig:
                            with open(path, 'w', encoding='utf-8') as f: f.write(content)
                            patched_count += 1

            self.log(f"[*] Successfully modified {patched_count} source files.", "white")
            if patched_count == 0:
                self.log("[!] Modification failed. Structure mismatch.", "red")
                return

            self.log("\n--- STAGE 4: ASAR REPACKAGING ---", "cyan")
            if self.run_command(f'npx asar pack {extract_dir} "{asar_file}" --unpack "*.{{node,exe,dll,pdb}}"'):
                self.log("\n[SUCCESS] Operation completed with no errors.", "green")
                messagebox.showinfo("AutoPro", "WeMod Patched Successfully!")
            else:
                self.log("\n[FAILURE] Repack module failed.", "red")
                
        except Exception as e:
            self.log(f"\n[FATAL] System failure: {str(e)}", "red")
        finally:
            self.set_buttons_state("normal")

    def set_buttons_state(self, state):
        self.btn_auto.config(state=state)
        self.btn_manual.config(state=state)
        self.btn_restore.config(state=state)

    def start_auto_patch(self):
        self.clear_logs()
        latest_dir = self.get_latest_wemod_dir()
        if latest_dir:
            exe = os.path.join(latest_dir, 'Wand.exe')
            asar = os.path.join(latest_dir, 'resources', 'app.asar')
            if os.path.exists(exe) and os.path.exists(asar):
                self.log(f"[+] WeMod discovered at:\n    {latest_dir}", "green")
                self.set_buttons_state("disabled")
                threading.Thread(target=self.do_patch_logic, args=(exe, asar), daemon=True).start()
                return
        self.log("[!] Automated discovery failed.", "red")

    def start_manual_patch(self):
        exe_path = filedialog.askopenfilename(title="Select Wand.exe", filetypes=[("WeMod Executable", "Wand.exe"), ("All Files", "*.*")])
        if not exe_path: return
        self.clear_logs()
        asar_path = os.path.join(os.path.dirname(exe_path), 'resources', 'app.asar')
        if not os.path.exists(asar_path):
            self.log("[!] app.asar missing in target resource folder.", "red")
            return
        self.set_buttons_state("disabled")
        threading.Thread(target=self.do_patch_logic, args=(exe_path, asar_path), daemon=True).start()

    def start_restore(self):
        self.clear_logs()
        self.set_buttons_state("disabled")
        threading.Thread(target=self.restore_logic, daemon=True).start()

    def restore_logic(self):
        try:
            self.kill_wemod()
            bak_path = os.path.join("backups", "app.asar.bak")
            if not os.path.exists(bak_path):
                self.log("[!] Local backup repository empty.", "red")
                return
            latest_dir = self.get_latest_wemod_dir()
            if latest_dir:
                asar = os.path.join(latest_dir, 'resources', 'app.asar')
                shutil.copy2(bak_path, asar)
                self.run_command(f'npx --yes @electron/fuses write --app "{os.path.join(latest_dir, "Wand.exe")}" EnableEmbeddedAsarIntegrityValidation=on')
                self.log("[SUCCESS] System restored to factory settings.", "green")
                messagebox.showinfo("AutoPro", "Original state restored.")
        finally:
            self.set_buttons_state("normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeModPatcherGUI(root)
    root.mainloop()
