__Hello My Friend 👋🏻__ <br>
__I'm Misagh and I'm Glad You're Here 😉__

# Audio2Video-Python🐍
I Wrote a Program in __Python__ That Can Convert Audio Files to ***Video*** and ***Video*** Files to Audio.

# Does It Require Any Installation Steps or Prerequisites?
`` pip install ffmpeg-python `` <br>
`` sudo apt-get install python3-tk `` <br>
`` sudo apt-get install ffmpeg `` <br>

# Line by Line Code Analysis

### Import Statements:

```python
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import ffmpeg
```

- **os**: Provides functions to interact with the operating system, like checking file existence or managing file paths.
- **threading**: Allows running tasks asynchronously in the background to prevent blocking the main UI thread (important for long-running tasks like file conversions).
- **tkinter**: A GUI (Graphical User Interface) library in Python for creating windows, buttons, labels, and other interactive elements.
- **filedialog, messagebox, ttk**: These are specific submodules from `tkinter`. 
  - `filedialog`: Used to open file dialogs for selecting files and folders.
  - `messagebox`: Used to show pop-up dialogs for information, warnings, or errors.
  - `ttk`: Provides themed widgets like progress bars.
- **ffmpeg**: A powerful library for multimedia processing (converting audio and video files).

---

### Global Variables:

```python
conversion_thread = None  # To hold the reference to the thread running the conversion
cancel_flag = False  # A flag to indicate if the conversion is cancelled
```

- `conversion_thread`: Holds the reference to the thread that handles the conversion, allowing you to manage it later (e.g., cancel the process).
- `cancel_flag`: A flag to indicate whether the conversion process should be stopped (set to `True` if cancellation is requested).

---

### Helper Function to Update UI:

```python
def update_ui(label_text, progress_step, cancel_state):
    progress_label.config(text=label_text)  # Update the progress label with new text
    progress_bar.step(progress_step)  # Update the progress bar by a certain step
    cancel_button.config(state=cancel_state)  # Update the cancel button state (enabled/disabled)
    root.update_idletasks()  # Update the UI without blocking the main loop
```

- **update_ui**: This function updates the UI elements with new information (like progress or messages). It allows non-blocking updates while the conversion is happening.
  - `label_text`: Changes the text of the progress label.
  - `progress_step`: Advances the progress bar by a specific step.
  - `cancel_state`: Updates the state of the cancel button (enabled or disabled).
  - `root.update_idletasks()`: Refreshes the GUI without blocking it.

---

### File Conversion Function:

```python
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
```

- **convert_file**: Handles the file conversion using the `ffmpeg` library. This function is executed in a separate thread.
  - `input_path`: Path of the input file to convert.
  - `output_path`: Path where the converted file will be saved.
  - The function updates the UI with the current state (converting, success, failure, or cancellation).
  - It runs `ffmpeg` asynchronously (non-blocking) and checks for cancellation by periodically checking the `cancel_flag`.
  - If the process finishes successfully, it shows a success message. If there’s an error or if conversion is cancelled, it displays an error or cancellation message.

---

### File Selection Functions:

```python
def select_file():
    file_path = filedialog.askopenfilename(title="Select File", filetypes=[("All Files", "*.*")])
    if file_path:
        input_entry.delete(0, tk.END)  # Clear any existing text in the input entry
        input_entry.insert(0, file_path)  # Insert the selected file path
```

- **select_file**: Opens a file dialog to select the input file for conversion. The selected file path is inserted into the `input_entry` field.

```python
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
```

- **select_save_path**: Opens a save file dialog to choose the location and file format for the output. The default extension is set based on the selected format (e.g., `.mp4`, `.mp3`).

---

### Start Conversion:

```python
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
```

- **start_conversion**: Starts the conversion process.
  - Checks if both input and output paths are specified.
  - Validates that the input file exists.
  - Resets the `cancel_flag` and starts the progress bar.
  - Runs the conversion in a new thread using the `convert_file` function to prevent blocking the UI.

---

### Cancel Conversion:

```python
def cancel_conversion():
    global cancel_flag
    cancel_flag = True  # Set the flag to true to cancel the process
```

- **cancel_conversion**: Sets the `cancel_flag` to `True`, signaling that the conversion process should stop.

---

### Exit Application:

```python
def exit_application():
    root.quit()  # Exit the Tkinter main loop
    root.destroy()  # Destroy the Tkinter window
```

- **exit_application**: Closes the Tkinter application by quitting the main loop and destroying the window.

---

### Get Supported Formats:

```python
def get_supported_formats():
    return [
        "MP4", "MP3", "GIF", "AVI", "MOV", "WAV", "FLV", "MKV", "WEBM", "AAC", "OGG"
    ]  # List of supported file formats for conversion
```

- **get_supported_formats**: Returns a list of file formats supported for conversion (e.g., MP4, MP3, etc.).

---

### GUI Setup:

```python
root = tk.Tk()  # Initialize the Tkinter window
root.title("Advanced File Converter")  # Set the title of the window
root.geometry("450x550")  # Set the dimensions of the window
```

- **GUI Setup**: Initializes the main Tkinter window with the title "Advanced File Converter" and sets the size of the window.

---

The following lines set up the rest of the graphical user interface (UI), including the file selection buttons, format selection dropdown, progress bar, labels, and buttons for starting the conversion, canceling, and exiting the application. Each widget is added to the window using `pack()` to position them.

### Tkinter Main Loop:

```python
root.mainloop()  # Start the Tkinter application loop
```

- **root.mainloop()**: Starts the Tkinter event loop, which keeps the window open and responsive to user interactions (like button clicks).

---
