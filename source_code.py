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
