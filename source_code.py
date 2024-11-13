import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import ffmpeg

# Global flag for cancellation
conversion_thread = None
cancel_flag = False

# Helper function to update UI elements
def update_ui(label_text, progress_step, cancel_state):
    progress_label.config(text=label_text)
    progress_bar.step(progress_step)
    cancel_button.config(state=cancel_state)
    root.update_idletasks()

# Function to convert the input file to the selected output format
def convert_file(input_path, output_path):
    global cancel_flag
    try:
        update_ui("Converting... Please wait.", 5, tk.NORMAL)

        process = ffmpeg.input(input_path).output(output_path).global_args('-progress', 'pipe:1', '-nostats')
        process = process.run_async(pipe_stderr=True)

        while process.poll() is None:
            if cancel_flag:
                process.terminate()  # Cancel the conversion
                update_ui("Conversion cancelled.", 0, tk.DISABLED)
                return
            update_ui("Converting... Please wait.", 5, tk.NORMAL)

        process.wait()

        if process.returncode == 0:
            update_ui("Conversion completed successfully!", 0, tk.DISABLED)
            messagebox.showinfo("Success", f"File converted to {os.path.splitext(output_path)[1][1:].upper()}!")
        else:
            raise Exception("Conversion failed.")
    except Exception as e:
        messagebox.showerror("Error", f"Error during conversion: {str(e)}")
    finally:
        cancel_button.config(state=tk.DISABLED)
        progress_bar.stop()

# Function to select an input file
def select_file():
    file_path = filedialog.askopenfilename(title="Select File", filetypes=[("All Files", "*.*")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

# Function to select output file path
def select_save_path():
    output_format = format_var.get().lower()
    save_path = filedialog.asksaveasfilename(
        title="Select Save Path",
        defaultextension=f".{output_format}",
        filetypes=[(f"{output_format.upper()} files", f"*.{output_format}")]
    )
    if save_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, save_path)

# Start conversion in a new thread to avoid UI freezing
def start_conversion():
    global cancel_flag, conversion_thread
    input_path = input_entry.get()
    output_path = output_entry.get()

    if not input_path or not output_path:
        messagebox.showwarning("Input Missing", "Please specify both input and output paths.")
        return

    if not os.path.exists(input_path):
        messagebox.showerror("File Not Found", "Input file not found.")
        return

    cancel_flag = False  # Reset the cancel flag
    progress_bar.start()

    conversion_thread = threading.Thread(target=convert_file, args=(input_path, output_path))
    conversion_thread.start()

# Cancel the ongoing conversion process
def cancel_conversion():
    global cancel_flag
    cancel_flag = True  # Set the flag to cancel the process

# Function to exit the application
def exit_application():
    root.quit()
    root.destroy()

# Helper function to get supported formats
def get_supported_formats():
    return [
        "MP4", "MP3", "GIF", "AVI", "MOV", "WAV", "FLV", "MKV", "WEBM", "AAC", "OGG"
    ]

# Setting up the GUI
root = tk.Tk()
root.title("Advanced File Converter")
root.geometry("450x550")

# Input file selection
tk.Label(root, text="Select Input File:").pack(pady=5)
input_entry = tk.Entry(root, width=50)
input_entry.pack(pady=5)
tk.Button(root, text="Choose File", command=select_file).pack(pady=5)

# Output format selection
tk.Label(root, text="Select Output Format:").pack(pady=5)
format_var = tk.StringVar(value="MP4")
output_formats = get_supported_formats()
format_menu = tk.OptionMenu(root, format_var, *output_formats)
format_menu.pack(pady=5)

# Output file path
tk.Label(root, text="Save Path:").pack(pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.pack(pady=5)
tk.Button(root, text="Choose Save Path", command=select_save_path).pack(pady=5)

# Convert button
convert_button = tk.Button(root, text="Convert", command=start_conversion, bg="green", fg="white")
convert_button.pack(pady=20)

# Cancel button
cancel_button = tk.Button(root, text="Cancel", command=cancel_conversion, bg="red", fg="white", state=tk.DISABLED)
cancel_button.pack(pady=5)

# Progress bar
progress_bar = ttk.Progressbar(root, mode="indeterminate", length=300)
progress_bar.pack(pady=10)

# Progress label
progress_label = tk.Label(root, text="")
progress_label.pack(pady=5)

# Exit button
exit_button = tk.Button(root, text="Exit", command=exit_application, bg="gray", fg="white")
exit_button.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()