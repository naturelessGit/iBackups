import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import platform

# Create main window
root = tk.Tk()
root.title("iBackups")
root.configure(bg="#1e1e1e")  # Dark background
root.geometry("800x600")

# Set system font
default_font = ("Segoe UI", 10) if platform.system() == "Windows" else ("San Francisco", 12)
root.option_add("*Font", default_font)

# Scrollable frame setup
main_frame = tk.Frame(root, bg="#1e1e1e")
main_frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(main_frame, bg="#1e1e1e", highlightthickness=0)
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#1e1e1e")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Style scrollbar
style = ttk.Style()
style.theme_use('clam')
style.configure("Vertical.TScrollbar", background="#333", troughcolor="#1e1e1e", bordercolor="#1e1e1e", arrowcolor="#ccc")

# Option storage
option_vars = {}

# Easy function to add options
def add_option(name, flag, section="General"):
    var = tk.BooleanVar()
    chk = tk.Checkbutton(scrollable_frame, text=name, variable=var, bg="#1e1e1e", fg="white", activebackground="#1e1e1e", activeforeground="white", selectcolor="#333")
    chk.pack(anchor="w", padx=20, pady=2)
    option_vars[flag] = var

# Text inputs
entries = {}

def add_entry(label, key, is_directory=False, fetch_udid=False):
    frame = tk.Frame(scrollable_frame, bg="#1e1e1e")
    frame.pack(fill="x", padx=20, pady=2)
    tk.Label(frame, text=label, bg="#1e1e1e", fg="white").pack(side="left")

    ent = tk.Entry(frame, bg="#333", fg="white", insertbackground="white", relief="flat")
    ent.pack(side="left", fill="x", expand=True, padx=(10, 0))
    entries[key] = ent

    if is_directory:
        def select_directory():
            directory = filedialog.askdirectory(title="Select Backup Directory")
            if directory:
                ent.delete(0, tk.END)
                ent.insert(0, directory)

        button = tk.Button(frame, text="Select Directory", command=select_directory, bg="#0078D7", fg="white", relief="flat", font=("Segoe UI", 10))
        button.pack(side="right", padx=10)

    if fetch_udid:
        def fetch_udid():
            try:
                udid = subprocess.check_output(["idevice_id", "-l"], text=True).strip()
                if udid:
                    ent.delete(0, tk.END)
                    ent.insert(0, udid)
                else:
                    messagebox.showwarning("No Device Found", "No device UDID found. Please connect a device.")
            except subprocess.CalledProcessError:
                messagebox.showerror("Error", "Failed to fetch UDID. Ensure that idevice_id is installed and the device is connected.")

        button = tk.Button(frame, text="Fetch UDID", command=fetch_udid, bg="#0078D7", fg="white", relief="flat", font=("Segoe UI", 10))
        button.pack(side="right", padx=10)

# Section for Backup options
tk.Label(scrollable_frame, text="Backup Options", bg="#1e1e1e", fg="cyan", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
add_entry("Backup Directory:", "--backup-dir", is_directory=True)
add_option("Full Backup", "--full")

# Section for Restore options
tk.Label(scrollable_frame, text="Restore Options", bg="#1e1e1e", fg="cyan", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
add_option("Restore System Files", "--system")
add_option("Do Not Reboot", "--no-reboot")
add_option("Create Backup Copy", "--copy")
add_option("Restore Device Settings", "--settings")
add_option("Remove Unrestored Items", "--remove")
add_option("Skip App Reinstall", "--skip-apps")
add_entry("Backup Password:", "--password")

# Section for Info and List options
tk.Label(scrollable_frame, text="Info & List Options", bg="#1e1e1e", fg="cyan", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
add_option("Show Backup Info", "info")
add_option("List Backup Files", "list")
add_option("Unpack Backup", "unback")

# Section for Encryption & Change Password options
tk.Label(scrollable_frame, text="Encryption & Change Password", bg="#1e1e1e", fg="cyan", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
add_option("Enable Encryption", "--encryption on")
add_option("Disable Encryption", "--encryption off")
add_entry("Encryption Password:", "--password")

# Section for Cloud options
tk.Label(scrollable_frame, text="Cloud Options", bg="#1e1e1e", fg="cyan", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
add_option("Enable Cloud", "--cloud on")
add_option("Disable Cloud", "--cloud off")

# Section for Additional Options
tk.Label(scrollable_frame, text="Additional Options", bg="#1e1e1e", fg="cyan", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
add_entry("Device UDID:", "--udid", fetch_udid=True)
add_entry("Source UDID:", "--source")
add_option("Connect to Network Device", "--network")
add_option("Interactive Mode", "--interactive")
add_option("Enable Debugging", "--debug")
add_option("Show Help", "--help")
add_option("Show Version", "--version")

# Terminal output
output_terminal = tk.Text(root, height=10, bg="#111", fg="lime", insertbackground="lime", relief="flat")
output_terminal.pack(fill="x", side="bottom")

# Function to execute the command
def execute_command():
    command = ["idevicebackup2"]

    # Default command (backup, if no other command specified)
    if not any(option_vars[flag].get() for flag in option_vars):  # If no options are selected
        command.append("backup")  # Default to backup if no command is set

    # Add selected options
    for flag, var in option_vars.items():
        if var.get():
            command.append(flag)

    # Add text entries for flags with values (like --backup-dir and --password)
    for flag, entry in entries.items():
        value = entry.get().strip()
        if value:
            command.append(value)

    # Handle missing command (e.g., backup)
    if len(command) == 1:  # No command added (i.e., only options are selected)
        command.append("backup")  # Fallback to backup

    output_terminal.insert(tk.END, f"Running: {' '.join(command)}\n\n")

    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # Read and display output line by line
        for line in proc.stdout:
            output_terminal.insert(tk.END, line)
            output_terminal.see(tk.END)

        proc.wait()
    except Exception as e:
        output_terminal.insert(tk.END, f"Error: {e}\n")

# Command button
execute_button = tk.Button(root, text="Backup!", command=execute_command, bg="#0078D7", fg="white", relief="flat", font=("Segoe UI", 12))
execute_button.pack(pady=10)

root.mainloop()
