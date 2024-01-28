import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import threading, time, pyautogui, keyboard #os
#1.0.2
class AutoTyperApp(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("AutoTyper - Stopped")

        #icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'col_studio.ico')
        #if os.path.exists(icon_path):
        #    self.master.iconbitmap(default=icon_path)

        self.master.geometry("500x400")

        self.text_to_type = ""
        self.running = False
        self.type_each_character = tk.BooleanVar()
        self.type_each_character.set(True)
        self.interval_var = tk.StringVar()
        self.interval_var.set("0.01")
        self.loop_var = tk.IntVar()
        self.loop_var.set(1)

        self.master.attributes('-topmost', 1)

        self.text_entry = ScrolledText(master, width=45, height=10, wrap=tk.WORD)
        self.text_entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10,sticky="nsew")

        self.import_button = tk.Button(master, text="Import Text File", command=self.import_text_file)
        self.import_button.grid(row=1, column=0, padx=10, sticky=tk.W)

        self.type_each_char_checkbox = tk.Checkbutton(master, text="Type Each Character", variable=self.type_each_character)
        self.type_each_char_checkbox.grid(row=2, column=0, sticky=tk.W)

        self.interval_label = tk.Label(master, text="Interval (seconds):")
        self.interval_label.grid(row=1, column=1, sticky=tk.E)
        self.interval_entry = tk.Entry(master, textvariable=self.interval_var)
        self.interval_entry.grid(row=1, column=2, sticky=tk.W)

        self.loop_label = tk.Label(master, text="Loop:")
        self.loop_label.grid(row=2, column=1, sticky=tk.E)
        self.loop_entry = tk.Entry(master, textvariable=self.loop_var)
        self.loop_entry.grid(row=2, column=2, sticky=tk.W)

        self.start_stop_button = tk.Button(master, text="Start Typing (F8)", command=self.toggle_start_stop)
        self.start_stop_button.grid(row=3, column=0, columnspan=3)

        self.loop_count_label = tk.Label(master, text="Loop Count: 0")
        self.loop_count_label.grid(row=4, column=0, columnspan=3)
        for i in range(3):
            master.grid_rowconfigure(i, weight=1)
            master.grid_columnconfigure(i, weight=1)

        keyboard.add_hotkey('F8', self.toggle_start_stop)
        self.bind("<B1-Motion>", self.on_resize)
        self.bind("<ButtonRelease-1>", self.stop_resizing)

        # Set the resizing flag to False initially
        self.resizing = False

    def on_resize(self, event):
        if self.resizing:
            # Calculate the new size based on the mouse position
            new_width = self.winfo_pointerx() - self.winfo_rootx()
            new_height = self.winfo_pointery() - self.winfo_rooty()

            # Set the new size for the window
            self.geometry(f"{new_width}x{new_height}")

    def start_resizing(self, event):
        # Set the resizing flag to True
        self.resizing = True

    def stop_resizing(self, event):
        # Set the resizing flag to False
        self.resizing = False

    def import_text_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                self.text_entry.delete(1.0, tk.END)
                self.text_entry.insert(tk.END, file.read())

    def toggle_start_stop(self):
        if not self.running:
            self.text_to_type = self.text_entry.get(1.0, tk.END)
            self.text_entry.config(state=tk.DISABLED)
            self.type_each_char_checkbox.config(state=tk.DISABLED)
            self.interval_entry.config(state=tk.DISABLED)
            self.import_button.config(state=tk.DISABLED)
            self.loop_entry.config(state=tk.DISABLED)
            self.start_stop_button.config(text="Stop Typing (F8)")
            self.master.title("AutoTyper - Running")

            self.loop_count = self.loop_var.get()
            self.running = True

            autotyper_thread = threading.Thread(target=self.autotype)
            autotyper_thread.start()
        else:
            self.text_entry.config(state=tk.NORMAL)
            self.type_each_char_checkbox.config(state=tk.NORMAL)
            self.interval_entry.config(state=tk.NORMAL)
            self.import_button.config(state=tk.NORMAL)
            self.loop_entry.config(state=tk.NORMAL)
            self.start_stop_button.config(text="Start Typing (F8)")
            self.master.title("AutoTyper - Stopped")

            self.running = False

    def autotype(self):
        text = self.text_to_type[:-1]
        interval = float(self.interval_var.get())
        for loop in range(self.loop_count):
            if not self.type_each_character.get():
                pyautogui.typewrite(text)
                time.sleep(interval)
            else:
                for char in text:
                    if not self.running:
                        break

                    if self.type_each_character.get():
                        pyautogui.typewrite(char)


                    time.sleep(interval)

            self.loop_count_label.config(text=f"Loop Count: {loop + 1}")

        self.stop_program()

    def stop_program(self):
        self.text_entry.config(state=tk.NORMAL)
        self.type_each_char_checkbox.config(state=tk.NORMAL)
        self.interval_entry.config(state=tk.NORMAL)
        self.import_button.config(state=tk.NORMAL)
        self.loop_entry.config(state=tk.NORMAL)
        self.start_stop_button.config(text="Start Typing (F8)")
        self.master.title("AutoTyper - Stopped")

        self.running = False

if __name__ == "__main__":
    root = tk.Tk()  # Create an instance of Tk()
    app = AutoTyperApp(master=root)  # Pass Tk() instance as master
    app.mainloop()
