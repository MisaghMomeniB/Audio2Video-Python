import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import ffmpeg

# Global flag for cancellation
conversion_thread = None  # To hold the reference to the thread running the conversion
cancel_flag = False  # A flag to indicate if the conversion is cancelled

# Helper function to update UI elements
def update_ui(label_text, progress_step, cancel_state):
    progress_label.config(text=label_text)  # Update the progress label with new text
    progress_bar.step(progress_step)  # Update the progress bar by a certain step
    cancel_button.config(state=cancel_state)  # Update the cancel button state (enabled/disabled)
    root.update_idletasks()  # Update the UI without blocking the main loop

# Function to convert the input file to the selected output format
def convert_file(input_path, output_path):
    global cancel_flag
    try:
        update_ui("Converting... Please wait.", 5, tk.NORMAL)  # Update UI to show conversion in progress

        process = ffmpeg.input(input_path).output(output_path).global_args('-progress', 'pipe:1', '-nostats')
        process = process.run_async(pipe_stderr=True)  # Run the ffmpeg conversion process asynchronously

        while process.poll() is None:  # Check if the process is still running
            if cancel_flag:
                process.terminate()  # Terminate the process if cancellation is requested
                update_ui("Conversion cancelled.", 0, tk.DISABLED)  # Update UI to show cancellation
                return
            update_ui("Converting... Please wait.", 5, tk.NORMAL)  # Update UI during conversion

        process.wait()  # Wait for the process to complete

        if process.returncode == 0:  # If conversion was successful
            update_ui("Conversion completed successfully!", 0, tk.DISABLED)  # Show success message
            messagebox.showinfo("Success", f"File converted to {os.path.splitext(output_path)[1][1:].upper()}!")
        else:
            raise Exception("Conversion failed.")  # Raise an error if conversion failed
    except Exception as e:
        messagebox.showerror("Error", f"Error during conversion: {str(e)}")  # Show an error message in case of failure
    finally:
        cancel_button.config(state=tk.DISABLED)  # Disable the cancel button once the process ends
        progress_bar.stop()  # Stop the progress bar after conversion

# Function to select an input file
def select_file():
    file_path = filedialog.askopenfilename(title="Select File", filetypes=[("All Files", "*.*")])
    if file_path:
        input_entry.delete(0, tk.END)  # Clear any existing text in the input entry
        input_entry.insert(0, file_path)  # Insert the selected file path

# Function to select output file path
def select_save_path():
    output_format = format_var.get().lower()  # Get the selected output format (lowercased)
    save_path = filedialog.asksaveasfilename(
        title="Select Save Path", 
        defaultextension=f".{output_format}",  # Set the default file extension based on the selected format
        filetypes=[(f"{output_format.upper()} files", f"*.{output_format}")]
    )
    if save_path:
        output_entry.delete(0, tk.END)  # Clear any existing text in the output entry
        output_entry.insert(0, save_path)  # Insert the selected save path

# Start conversion in a new thread to avoid UI freezing
def start_conversion():
    global cancel_flag, conversion_thread
    input_path = input_entry.get()  # Get the input file path from the entry field
    output_path = output_entry.get()  # Get the output file path from the entry field

    if not input_path or not output_path:  # If either input or output path is missing
        messagebox.showwarning("Input Missing", "Please specify both input and output paths.")
        return

    if not os.path.exists(input_path):  # If input file does not exist
        messagebox.showerror("File Not Found", "Input file not found.")
        return

    cancel_flag = False  # Reset the cancel flag to false before starting
    progress_bar.start()  # Start the progress bar

    conversion_thread = threading.Thread(target=convert_file, args=(input_path, output_path))  # Create a new thread for conversion
    conversion_thread.start()  # Start the conversion thread

# Cancel the ongoing conversion process
def cancel_conversion():
    global cancel_flag
    cancel_flag = True  # Set the flag to true to cancel the process

# Function to exit the application
def exit_application():
    root.quit()  # Exit the Tkinter main loop
    root.destroy()  # Destroy the Tkinter window

# Helper function to get supported formats
def get_supported_formats():
    return [
        "MP4", "MP3", "GIF", "AVI", "MOV", "WAV", "FLV", "MKV", "WEBM", "AAC", "OGG"
    ]  # List of supported file formats for conversion

# Setting up the GUI
root = tk.Tk()  # Initialize the Tkinter window
root.title("Advanced File Converter")  # Set the title of the window
root.geometry("450x550")  # Set the dimensions of the window

# Input file selection
tk.Label(root, text="Select Input File:").pack(pady=5)  # Create a label for input file selection
input_entry = tk.Entry(root, width=50)  # Create an entry field for the input file path
input_entry.pack(pady=5)  # Add the input entry field to the window
tk.Button(root, text="Choose File", command=select_file).pack(pady=5)  # Button to choose input file

# Output format selection
tk.Label(root, text="Select Output Format:").pack(pady=5)  # Label for output format selection
format_var = tk.StringVar(value="MP4")  # Default value for output format is MP4
output_formats = get_supported_formats()  # Get the list of supported formats
format_menu = tk.OptionMenu(root, format_var, *output_formats)  # Dropdown menu for format selection
format_menu.pack(pady=5)  # Add the dropdown menu to the window

# Output file path
tk.Label(root, text="Save Path:").pack(pady=5)  # Label for the save path
output_entry = tk.Entry(root, width=50)  # Entry field for the output file path
output_entry.pack(pady=5)  # Add the output entry field to the window
tk.Button(root, text="Choose Save Path", command=select_save_path).pack(pady=5)  # Button to choose save path

# Convert button
convert_button = tk.Button(root, text="Convert", command=start_conversion, bg="green", fg="white")  # Convert button
convert_button.pack(pady=20)  # Add the convert button to the window

# Cancel button
cancel_button = tk.Button(root, text="Cancel", command=cancel_conversion, bg="red", fg="white", state=tk.DISABLED)  # Cancel button
cancel_button.pack(pady=5)  # Add the cancel button to the window

# Progress bar
progress_bar = ttk.Progressbar(root, mode="indeterminate", length=300)  # Progress bar with indeterminate mode
progress_bar.pack(pady=10)  # Add the progress bar to the window

# Progress label
progress_label = tk.Label(root, text="")  # Label to display progress information
progress_label.pack(pady=5)  # Add the label to the window

# Exit button
exit_button = tk.Button(root, text="Exit", command=exit_application, bg="gray", fg="white")  # Exit button
exit_button.pack(pady=20)  # Add the exit button to the window

# Start the Tkinter main loop
root.mainloop()  # Start the Tkinter application loop