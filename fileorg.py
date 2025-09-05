import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
from tkinter import ttk


FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".flv"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Music": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Software": [".exe", ".msi"],
    "Scripts": [".py", ".sh", ".js", ".bat",],
    "Others": []  
}

def get_file_hash(file_path):
    
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def delete_duplicates(directory):
    
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = get_file_hash(file_path)
            
            if file_hash in file_hashes:
                os.remove(file_path)  # Delete duplicate
            else:
                file_hashes[file_hash] = file_path
    messagebox.showinfo("Success", "Duplicate files deleted!")

def organize_files(directory):
    
    if not os.path.exists(directory):
        messagebox.showerror("Error", "Directory does not exist!")
        return

    for category in FILE_CATEGORIES.keys():
        category_path = os.path.join(directory, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)

    for root, _, files in os.walk(directory, topdown=False):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_ext = os.path.splitext(filename)[1].lower()
            moved = False

            for category, extensions in FILE_CATEGORIES.items():
                if file_ext in extensions:
                    shutil.move(file_path, os.path.join(directory, category, filename))
                    moved = True
                    break

            if not moved:
                shutil.move(file_path, os.path.join(directory, "Others", filename))
    
    messagebox.showinfo("Success", "Files organized successfully!")

def select_folder():
    folder_selected = filedialog.askdirectory()
    entry_folder.delete(0, tk.END)
    entry_folder.insert(0, folder_selected)

def start_organizing():
    folder = entry_folder.get()
    if folder:
        organize_files(folder)

def start_deleting_duplicates():
    folder = entry_folder.get()
    if folder:
        delete_duplicates(folder)

# GUI Setup
root = tk.Tk()
root.title("Junk File Organizer")
root.geometry("450x300")
root.configure(bg="#2E3440")

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=6)
style.configure("TLabel", font=("Arial", 12), background="#2E3440", foreground="white")
style.configure("TEntry", font=("Arial", 12), padding=5)

label = ttk.Label(root, text="Select Folder:")
label.pack(pady=10)

entry_folder = ttk.Entry(root, width=50)
entry_folder.pack(pady=5)

btn_browse = ttk.Button(root, text="Browse", command=select_folder)
btn_browse.pack(pady=5)

btn_organize = ttk.Button(root, text="Organize Files", command=start_organizing)
btn_organize.pack(pady=5)

btn_delete_dups = ttk.Button(root, text="Delete Duplicates", command=start_deleting_duplicates)
btn_delete_dups.pack(pady=5)

root.mainloop()
