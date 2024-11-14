### Import Statements
```python
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import ffmpeg
```
These lines import required modules:
- `os` for file and path operations.
- `threading` to run tasks in parallel, specifically the conversion in a separate thread.
- `tkinter` and specific components (`filedialog`, `messagebox`, `ttk`) for creating the GUI.
- `ffmpeg`, a library for managing the FFmpeg conversion process.

### Global Variables
```python
conversion_thread = None
cancel_flag = False
```
Defines global variables:
- `conversion_thread` will reference the thread handling file conversion.
- `cancel_flag` is a boolean that will be set to `True` when the user requests to cancel the conversion.

### Helper Function to Update the UI
```python
def update_ui(label_text, progress_step, cancel_state):
    progress_label.config(text=label_text)
    progress_bar.step(progress_step)
    cancel_button.config(state=cancel_state)
    root.update_idletasks()
```
The `update_ui` function updates the UI elements:
- Changes `progress_label` text.
- Advances the `progress_bar` by `progress_step`.
- Enables/disables the `cancel_button`.
- `root.update_idletasks()` refreshes the UI to reflect changes without freezing.

### File Conversion Function
```python
def convert_file(input_path, output_path):
    global cancel_flag
    try:
        update_ui("Converting... Please wait.", 5, tk.NORMAL)

        process = ffmpeg.input(input_path).output(output_path).global_args('-progress', 'pipe:1', '-nostats')
        process = process.run_async(pipe_stderr=True)

        while process.poll() is None:
            if cancel_flag:
                process.terminate()
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
```
The `convert_file` function performs the conversion:
1. Updates UI to indicate the conversion is starting.
2. Initiates the FFmpeg process using asynchronous execution with `run_async()`.
3. Checks if `cancel_flag` is `True`, terminating the process if requested.
4. If conversion completes successfully, it updates the UI and shows a success message.
5. If an error occurs, it shows an error message.
6. Finally, it disables the cancel button and stops the progress bar.

### Input File Selection
```python
def select_file():
    file_path = filedialog.askopenfilename(title="Select File", filetypes=[("All Files", "*.*")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)
```
The `select_file` function opens a file dialog for the user to select an input file. It then updates `input_entry` with the selected file path.

### Output File Path Selection
```python
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
```
The `select_save_path` function opens a dialog to specify where to save the converted file, using the selected format's extension. The `output_entry` is then updated with the save path.

### Starting the Conversion in a New Thread
```python
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

    cancel_flag = False
    progress_bar.start()

    conversion_thread = threading.Thread(target=convert_file, args=(input_path, output_path))
    conversion_thread.start()
```
`start_conversion` checks for missing input or output paths, verifies the input file exists, and resets `cancel_flag`. It starts the progress bar and runs `convert_file` in a new thread to keep the UI responsive.

### Cancelling the Conversion
```python
def cancel_conversion():
    global cancel_flag
    cancel_flag = True
```
This function sets `cancel_flag` to `True`, allowing `convert_file` to terminate the conversion process.

### Exiting the Application
```python
def exit_application():
    root.quit()
    root.destroy()
```
This function closes the Tkinter window and exits the application.

### Supported Formats
```python
def get_supported_formats():
    return ["MP4", "MP3", "GIF", "AVI", "MOV", "WAV", "FLV", "MKV", "WEBM", "AAC", "OGG"]
```
This function returns a list of supported output formats.

### Setting Up the GUI
```python
root = tk.Tk()
root.title("Advanced File Converter")
root.geometry("450x550")
```
Initializes the Tkinter window, sets the title, and dimensions.

### Input File Selection UI
```python
tk.Label(root, text="Select Input File:").pack(pady=5)
input_entry = tk.Entry(root, width=50)
input_entry.pack(pady=5)
tk.Button(root, text="Choose File", command=select_file).pack(pady=5)
```
Creates the UI components for selecting an input file, including a label, entry field, and a button.

### Output Format Selection UI
```python
tk.Label(root, text="Select Output Format:").pack(pady=5)
format_var = tk.StringVar(value="MP4")
output_formats = get_supported_formats()
format_menu = tk.OptionMenu(root, format_var, *output_formats)
format_menu.pack(pady=5)
```
Sets up a dropdown menu for output formats.

### Output File Path Selection UI
```python
tk.Label(root, text="Save Path:").pack(pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.pack(pady=5)
tk.Button(root, text="Choose Save Path", command=select_save_path).pack(pady=5)
```
Sets up the output file path selection UI with a label, entry field, and button.

### Convert and Cancel Buttons
```python
convert_button = tk.Button(root, text="Convert", command=start_conversion, bg="green", fg="white")
convert_button.pack(pady=20)

cancel_button = tk.Button(root, text="Cancel", command=cancel_conversion, bg="red", fg="white", state=tk.DISABLED)
cancel_button.pack(pady=5)
```
Creates `Convert` and `Cancel` buttons with color customization.

### Progress Bar and Label
```python
progress_bar = ttk.Progressbar(root, mode="indeterminate", length=300)
progress_bar.pack(pady=10)

progress_label = tk.Label(root, text="")
progress_label.pack(pady=5)
```
Adds a progress bar and a label for real-time conversion updates.

### Exit Button and Main Loop
```python
exit_button = tk.Button(root, text="Exit", command=exit_application, bg="gray", fg="white")
exit_button.pack(pady=20)

root.mainloop()
```
Creates an `Exit` button and starts the Tkinter main loop to run the application.
