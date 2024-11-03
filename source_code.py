import ffmpeg
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading

# Global variable to manage cancellation of the conversion process
conversion_thread = None
cancel_flag = False