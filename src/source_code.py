import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import ffmpeg

# Global variables
conversion_thread = None  # Reference to the conversion thread
cancel_flag = False  # Flag to indicate if the conversion should be cancelled


def update_ui(label_text, progress_step=0, cancel_state=tk.DISABLED):
    """
    Update the UI elements during the conversion process.
    """
    progress_label.config(text=label_text)  # Update the progress label
    if progress_step > 0:
        progress_bar.step(progress_step)  # Update the progress bar
    cancel_button.config(state=cancel_state)  # Enable/disable the cancel button
    root.update_idletasks()  # Refresh the UI without blocking the main loop


def convert_file(input_path, output_path):
    """
    Convert the input file to the specified output format using ffmpeg.
    Runs in a separate thread to avoid freezing the UI.
    """
    global cancel_flag
    try:
        update_ui("Converting... Please wait.", 5, tk.NORMAL)  # Indicate conversion in progress

        # Start the ffmpeg conversion process
        process = (
            ffmpeg.input(input_path)
            .output(output_path)
            .global_args('-progress', 'pipe:1', '-nostats')
            .run_async(pipe_stderr=True)
        )

        # Monitor the conversion process
        while process.poll() is None:
            if cancel_flag:
                process.terminate()  # Terminate the process if cancellation is requested
                update_ui("Conversion cancelled.", 0, tk.DISABLED)
                return

            # Update the UI periodically during conversion
            update_ui("Converting... Please wait.", 5, tk.NORMAL)

        # Wait for the process to complete
        process.wait()

        # Check if the conversion was successful
        if process.returncode == 0:
            update_ui("Conversion completed successfully!", 0, tk.DISABLED)
            messagebox.showinfo("Success", f"File converted to {os.path.splitext(output_path)[1][1:].upper()}!")
        else:
            raise Exception("Conversion failed.")

    except Exception as e:
        messagebox.showerror("Error", f"Error during conversion: {str(e)}")
    finally:
        # Clean up after conversion
        cancel_flag = False
        cancel_button.config(state=tk.DISABLED)
        progress_bar.stop()


def select_file():
    """
    Open a file dialog to select the input file.
    """
    file_path = filedialog.askopenfilename(title="Select Input File", filetypes=[("All Files", "*.*")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)


def select_save_path():
    """
    Open a file dialog to select the output file path.
    """
    output_format = format_var.get().lower()
    save_path = filedialog.asksaveasfilename(
        title="Select Save Path",
        defaultextension=f".{output_format}",
        filetypes=[(f"{output_format.upper()} files", f"*.{output_format}")]
    )
    if save_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, save_path)


def start_conversion():
    """
    Start the file conversion process in a new thread.
    """
    global conversion_thread, cancel_flag

    input_path = input_entry.get()
    output_path = output_entry.get()

    # Validate input and output paths
    if not input_path or not output_path:
        messagebox.showwarning("Input Missing", "Please specify both input and output paths.")
        return

    if not os.path.exists(input_path):
        messagebox.showerror("File Not Found", "Input file not found.")
        return

    # Reset the cancel flag and start the conversion thread
    cancel_flag = False
    progress_bar.start()
    conversion_thread = threading.Thread(target=convert_file, args=(input_path, output_path))
    conversion_thread.start()


def cancel_conversion():
    """
    Cancel the ongoing conversion process.
    """
    global cancel_flag
    cancel_flag = True


def exit_application():
    """
    Exit the application gracefully.
    """
    global conversion_thread

    if conversion_thread and conversion_thread.is_alive():
        cancel_conversion()  # Attempt to cancel the conversion before exiting
        conversion_thread.join()  # Wait for the thread to terminate

    root.quit()
    root.destroy()


def get_supported_formats():
    """
    Return a list of supported file formats for conversion.
    """
    return ["MP4", "MP3", "GIF", "AVI", "MOV", "WAV", "FLV", "MKV", "WEBM", "AAC", "OGG"]


# Set up the GUI
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