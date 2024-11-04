__Hello My Friend 👋🏻__ <br>
__I'm Misagh and I'm Glad You're Here 😉__

# Audio2Video-Python🐍
I Wrote a Program in __Python__ That Can Convert Audio Files to ***Video*** and ***Video*** Files to Audio.

# Does It Require Any Installation Steps or Prerequisites?
`` pip install ffmpeg-python `` <br>
`` sudo apt-get install python3-tk `` <br>
`` sudo apt-get install ffmpeg `` <br>

# Line by Line Code Analysis

### Imports
```python
import ffmpeg
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
```
- **`import ffmpeg`**: This imports the `ffmpeg` library, which is used for processing multimedia files. It's a powerful tool for converting audio and video formats.
- **`import tkinter as tk`**: Imports the `tkinter` library for creating the GUI, allowing the user to interact with the application.
- **`from tkinter import filedialog, messagebox, ttk`**: Imports specific modules from `tkinter`. `filedialog` is for file selection dialogs, `messagebox` for displaying messages, and `ttk` provides themed widgets, including a progress bar.
- **`import os`**: Imports the `os` module to handle file system operations, such as checking if files exist.
- **`import threading`**: Imports the `threading` module to enable concurrent execution, allowing the GUI to remain responsive during file conversion.

### Global Variables
```python
conversion_thread = None
cancel_flag = False
```
- **`conversion_thread`**: This variable holds a reference to the thread running the conversion process. It helps in managing the conversion state.
- **`cancel_flag`**: This flag indicates whether the conversion should be canceled. It is checked in the conversion process.

### Conversion Function
```python
def convert_file(input_path, output_path):
    global cancel_flag
    try:
        progress_label.config(text="Converting... Please wait.")
        cancel_button.config(state=tk.NORMAL)

        process = (
            ffmpeg
            .input(input_path)
            .output(output_path)
            .global_args('-progress', 'pipe:1', '-nostats')
        )
        process = process.run_async(pipe_stderr=True)
```
- **`def convert_file(input_path, output_path)`**: Defines the function responsible for converting the file.
- **`global cancel_flag`**: Indicates that this function will modify the `cancel_flag` variable.
- **`try...except`**: Used for error handling during the conversion process. If an error occurs, it can be caught and handled.
- **`progress_label.config(...)`**: Updates the UI to inform the user that the conversion is in progress.
- **`cancel_button.config(state=tk.NORMAL)`**: Enables the cancel button while the conversion is active.
- **`process = ffmpeg.input(...).output(...).global_args(...)`**: Sets up the ffmpeg conversion command with the specified input and output paths. The `global_args` method includes arguments for progress reporting.

### Polling for Process Completion
```python
        while process.poll() is None:
            if cancel_flag:
                process.terminate()  # Cancel the conversion process
                progress_label.config(text="Conversion cancelled.")
                cancel_button.config(state=tk.DISABLED)
                return
            root.update_idletasks()  # Update the UI
            progress_bar.step(5)  # Update the progress bar
```
- **`while process.poll() is None`**: Continuously checks if the conversion process is still running.
- **`if cancel_flag:`**: Checks if the user has requested cancellation. If so, it terminates the process and updates the UI accordingly.
- **`root.update_idletasks()`**: Updates the GUI elements, ensuring the interface remains responsive.
- **`progress_bar.step(5)`**: Updates the progress bar to give visual feedback on the conversion process.

### Finalizing the Conversion
```python
        process.wait()

        if process.returncode == 0:
            progress_label.config(text="Conversion completed successfully!")
            messagebox.showinfo("Conversion Successful", f"File has been converted to {os.path.splitext(output_path)[1][1:].upper()}!")
        else:
            raise Exception("Conversion failed.")
```
- **`process.wait()`**: Waits for the conversion process to complete.
- **`if process.returncode == 0:`**: Checks if the conversion was successful (return code 0 indicates success).
- **`messagebox.showinfo(...)`**: Displays a success message to the user with the output file format.
- **`else: raise Exception("Conversion failed.")`**: Raises an error if the conversion failed, triggering the exception handling.

### Exception Handling
```python
    except Exception as e:
        messagebox.showerror("Error", f"Error in file conversion: {str(e)}")
    finally:
        cancel_button.config(state=tk.DISABLED)  # Disable the cancel button
        progress_bar.stop()  # Stop the progress bar
        progress_label.config(text="")  # Clear the status message
```
- **`except Exception as e:`**: Catches any exceptions that occur during conversion and shows an error message.
- **`finally:`**: Executes cleanup actions, regardless of success or failure (disabling the cancel button, stopping the progress bar, and clearing status messages).

### File Selection Functions
```python
def select_file():
    file_path = filedialog.askopenfilename(
        title="Select File",
        filetypes=[("All Files", "*.*")]
    )
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)
```
- **`def select_file():`**: Opens a file dialog for the user to select an input file.
- **`filedialog.askopenfilename(...)`**: Prompts the user to select a file, with options for filtering by type.
- **`if file_path:`**: Checks if a file was selected. If so, it updates the input entry field.

The `select_save_path()` function is similar but is for specifying the output file path.

### Starting Conversion
```python
def start_conversion():
    global cancel_flag, conversion_thread
    input_path = input_entry.get()
    output_path = output_entry.get()

    if not input_path or not output_path:
        messagebox.showwarning("Warning", "Please specify both input and output paths.")
        return

    if not os.path.exists(input_path):
        messagebox.showerror("Error", "Input file not found.")
        return

    cancel_flag = False
    progress_bar.start()

    conversion_thread = threading.Thread(target=convert_file, args=(input_path, output_path))
    conversion_thread.start()
```
- **`def start_conversion():`**: Starts the file conversion process.
- **`input_path = input_entry.get()`**: Retrieves the user-specified input file path.
- **`if not input_path or not output_path:`**: Checks if both paths are provided and shows a warning if not.
- **`if not os.path.exists(input_path):`**: Validates that the input file exists.
- **`cancel_flag = False`**: Resets the cancel flag to allow for a new conversion.
- **`progress_bar.start()`**: Starts the progress bar animation.
- **`conversion_thread = threading.Thread(...)`**: Initializes a new thread to run the conversion function, allowing the GUI to remain responsive.
- **`conversion_thread.start()`**: Starts the thread.

### Canceling Conversion
```python
def cancel_conversion():
    global cancel_flag
    cancel_flag = True
```
- **`def cancel_conversion():`**: Sets the `cancel_flag` to true, which the conversion function checks to terminate the process.

### Exiting the Application
```python
def exit_application():
    root.quit()
    root.destroy()
```
- **`def exit_application():`**: Closes the application window and cleans up resources.

### Supported Formats
```python
def get_supported_formats():
    return [
        "MP4", "MP3", "GIF", "AVI", "MOV", "WAV", "FLV", "MKV", "WEBM", "AAC", "OGG"
    ]
```
- **`def get_supported_formats():`**: Returns a list of supported output formats. This list can be extended as needed.

### GUI Setup
```python
root = tk.Tk()
root.title("Advanced File Converter")
root.geometry("450x550")

tk.Label(root, text="Select Input File:").pack(pady=5)
input_entry = tk.Entry(root, width=50)
input_entry.pack(pady=5)
tk.Button(root, text="Choose File", command=select_file).pack(pady=5)

tk.Label(root, text="Select Output Format:").pack(pady=5)
format_var = tk.StringVar(value="MP4")
output_formats = get_supported_formats()
format_menu = tk.OptionMenu(root, format_var, *output_formats)
format_menu.pack(pady=5)

tk.Label(root, text="Save Path:").pack(pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.pack(pady=5)
tk.Button(root, text="Choose Save Path", command=select_save_path).pack(pady=5)

convert_button = tk.Button(root, text="Convert", command=start_conversion, bg="green", fg="white")
convert_button.pack(pady=20)

cancel_button = tk.Button(root, text="Cancel", command=cancel_conversion, bg="red", fg="white", state=tk.DISABLED)
cancel_button.pack(pady=5)

progress_bar = ttk.Progressbar(root, mode="indeterminate", length=300)
progress_bar.pack(pady=10)
progress_label = tk.Label(root, text="")
progress_label.pack(pady=5)

exit_button = tk.Button(root, text="Exit",

 command=exit_application, bg="gray", fg="white")
exit_button.pack(pady=20)

root.mainloop()
```
- **`root = tk.Tk()`**: Initializes the main application window.
- **`root.title(...)`**: Sets the window title.
- **`root.geometry(...)`**: Defines the size of the window.
- The various `tk.Label`, `tk.Entry`, and `tk.Button` calls set up the GUI components for user input, including labels, entry fields for file paths, and buttons for selecting files, converting, canceling, and exiting.
- **`progress_bar = ttk.Progressbar(...)`**: Initializes a progress bar to give feedback on the conversion status.
- **`root.mainloop()`**: Starts the Tkinter event loop, which waits for user interactions.

### Summary
This code provides a simple but effective GUI for converting multimedia files using ffmpeg. It includes file selection, format options, progress tracking, and cancellation features. The threading model is crucial for keeping the interface responsive during potentially long-running conversions, improving the overall user experience.
