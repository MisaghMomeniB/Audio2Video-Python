import ffmpeg
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading

# Global variable to manage cancellation of the conversion process
conversion_thread = None
cancel_flag = False

# Function to convert the input file to the selected output format
def convert_file(input_path, output_path):
    global cancel_flag
    try:
        # Update UI to show conversion in progress
        progress_label.config(text="Converting... Please wait.")
        cancel_button.config(state=tk.NORMAL)

        # Create an ffmpeg process for conversion
        process = (
            ffmpeg
            .input(input_path)
            .output(output_path)
            .global_args('-progress', 'pipe:1', '-nostats')
        )
        process = process.run_async(pipe_stderr=True)

        # Poll the process for its completion
        while process.poll() is None:
            if cancel_flag:
                process.terminate()  # Cancel the conversion process
                progress_label.config(text="Conversion cancelled.")
                cancel_button.config(state=tk.DISABLED)
                return
            root.update_idletasks()  # Update the UI
            progress_bar.step(5)  # Update the progress bar

        # Wait for the process to finish
        process.wait()

        # Check the result of the conversion
        if process.returncode == 0:
            progress_label.config(text="Conversion completed successfully!")
            messagebox.showinfo("Conversion Successful", f"File has been converted to {os.path.splitext(output_path)[1][1:].upper()}!")
        else:
            raise Exception("Conversion failed.")
    except Exception as e:
        messagebox.showerror("Error", f"Error in file conversion: {str(e)}")
    finally:
        cancel_button.config(state=tk.DISABLED)  # Disable the cancel button
        progress_bar.stop()  # Stop the progress bar
        progress_label.config(text="")  # Clear the status message

# Function to select an input file
def select_file():
    file_path = filedialog.askopenfilename(
        title="Select File",
        filetypes=[("All Files", "*.*")]
    )
    if file_path:
        input_entry.delete(0, tk.END)  # Clear the entry field
        input_entry.insert(0, file_path)  # Insert the selected file path

# Function to select a save path for the output file
def select_save_path():
    output_format = format_var.get().lower()  # Get the selected format
    save_path = filedialog.asksaveasfilename(
        title="Select Save Path",
        defaultextension=f".{output_format}",
        filetypes=[(f"{output_format.upper()} files", f"*.{output_format}")]
    )
    if save_path:
        output_entry.delete(0, tk.END)  # Clear the entry field
        output_entry.insert(0, save_path)  # Insert the selected save path

# Function to start the conversion process in a new thread
def start_conversion():
    global cancel_flag, conversion_thread
    input_path = input_entry.get()  # Get input file path
    output_path = output_entry.get()  # Get output file path

    # Validate input and output paths
    if not input_path or not output_path:
        messagebox.showwarning("Warning", "Please specify both input and output paths.")
        return

    if not os.path.exists(input_path):
        messagebox.showerror("Error", "Input file not found.")
        return

    cancel_flag = False  # Reset the cancel flag
    progress_bar.start()  # Start the progress bar

    # Create a thread for file conversion
    conversion_thread = threading.Thread(target=convert_file, args=(input_path, output_path))
    conversion_thread.start()  # Start the conversion thread

# Function to cancel the ongoing conversion
def cancel_conversion():
    global cancel_flag
    cancel_flag = True  # Set the cancel flag to true

# Function to exit the application
def exit_application():
    root.quit()  # Quit the main loop
    root.destroy()  # Destroy the root window

# Function to retrieve supported formats from ffmpeg
def get_supported_formats():
    # List of supported formats (can be extended)
    return [
        "MP4", "MP3", "GIF", "AVI", "MOV", "WAV", "FLV", "MKV", "WEBM", "AAC", "OGG"
    ]

# Setting up the GUI
root = tk.Tk()
root.title("Advanced File Converter")  # Set window title
root.geometry("450x550")  # Set window size

# Input file selection
tk.Label(root, text="Select Input File:").pack(pady=5)
input_entry = tk.Entry(root, width=50)  # Entry for input file path
input_entry.pack(pady=5)
tk.Button(root, text="Choose File", command=select_file).pack(pady=5)  # Button to choose file

# Output format selection
tk.Label(root, text="Select Output Format:").pack(pady=5)
format_var = tk.StringVar(value="MP4")  # Default format
output_formats = get_supported_formats()  # Get supported formats
format_menu = tk.OptionMenu(root, format_var, *output_formats)  # Dropdown for output formats
format_menu.pack(pady=5)

# Output file save path
tk.Label(root, text="Save Path:").pack(pady=5)
output_entry = tk.Entry(root, width=50)  # Entry for output file path
output_entry.pack(pady=5)
tk.Button(root, text="Choose Save Path", command=select_save_path).pack(pady=5)  # Button to choose save path

# Convert button
convert_button = tk.Button(root, text="Convert", command=start_conversion, bg="green", fg="white")  # Convert button
convert_button.pack(pady=20)