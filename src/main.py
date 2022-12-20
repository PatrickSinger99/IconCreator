import tkinter as tk
from tkinter.font import Font
from image_edits import *
import subprocess
from tkinter import filedialog
import threading


"""APP"""


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Icon Creator")
        self.resizable(False, False)
        self.iconbitmap("icons/app_icon.ico")

        self.loaded_images_compressed = {}
        self.loaded_images_original = {}
        self.current_selected_image_path = None
        self.current_selected_image_data = None
        self.display_images = True

        """COLORS"""

        self.image_bg_color = "light grey"  # "#adc2eb"
        self.image_hover_color = "#6f94dc"
        self.image_active_color = "#3366cc"

        self.delete_button_hover_color = "#ff6666"
        self.delete_button_active_color = "#ff3333"

        self.folder_button_hover_color = "#ffad33"
        self.folder_button_active_color = "#ff9900"

        self.convert_button_bg_color = "#00b386"
        self.convert_button_hover_color = "#00cc99"
        self.convert_button_active_color = "white"  # "#00e6ac"

        """IMAGES"""

        self.app_logo = tk.PhotoImage(file="icons/app_icon_medium.png")

        self.settings_icon = tk.PhotoImage(file="icons/settings.png")

        self.delete_icon = tk.PhotoImage(file="icons/delete.png")
        self.folder_icon = tk.PhotoImage(file="icons/folder.png")
        self.placeholder_image = tk.PhotoImage(file="icons/placeholder.png")

        self.expanded_display_icon = tk.PhotoImage(file="icons/expanded_display.png")
        self.compact_display_icon = tk.PhotoImage(file="icons/compact_display.png")

        self.plus_icon = tk.PhotoImage(file="icons/plus.png")

        self.convert_one_icon = tk.PhotoImage(file="icons/convert_one.png")
        self.convert_all_icon = tk.PhotoImage(file="icons/convert_all.png")

        """FRAMES"""

        self.header_frame = tk.Frame(self, bg="grey", width=900, height=50)
        self.header_frame.grid(row=0, column=0, columnspan=2)
        self.header_frame.pack_propagate(False)

        self.sidebar_frame = tk.Frame(self, bg="black", width=200, height=700)
        self.sidebar_frame.grid(row=1, column=0)
        self.sidebar_frame.pack_propagate(False)

        self.image_frame = tk.Frame(self, bg="light grey", width=700, height=700)
        self.image_frame.grid(row=1, column=1)
        self.image_frame.pack_propagate(False)

        self.footer_frame = tk.Frame(self, bg="grey", width=900, height=50)
        self.footer_frame.grid(row=2, column=0, columnspan=2)
        self.footer_frame.pack_propagate(False)

        """HEADER CONTENT"""

        self.title_label = tk.Label(self.header_frame, text=" Icon Creator", font=Font(size=20), bd=0,
                                    image=self.app_logo, compound="left", bg="grey")

        self.title_label.pack(side="left", padx=(6, 0))

        self.info_label = tk.Label(self.header_frame, text="Version 0.1", font=Font(size=11), bg="grey",
                                   fg="light grey")

        self.info_label.pack(side="left", padx=(10, 0))

        self.settings_button = tk.Button(self.header_frame, text="Settings ", bd=0, relief="flat", cursor="hand2",
                                         font=Font(size=11), image=self.settings_icon, compound="right",
                                         bg="grey", activebackground="white")
        self.settings_button.pack(side="right", fill="y", ipadx=8)

        self.settings_button.bind("<Enter>", lambda e: self.settings_button.configure(bg="light grey"))
        self.settings_button.bind("<Leave>", lambda e: self.settings_button.configure(bg="grey"))

        """SIDEBAR HEADER"""

        self.sidebar_title_frame = tk.Frame(self.sidebar_frame, bg=self.image_active_color)
        self.sidebar_title_frame.pack(side="top", fill="x", ipady=1)

        self.view_toggle_button = tk.Button(self.sidebar_title_frame, text="Collapse", command=self.toggle_images,
                                            cursor="hand2", bd=0, relief="flat", compound="right", width=60, anchor="e",
                                            image=self.compact_display_icon, font=Font(size=8),
                                            bg=self.image_active_color)
        self.view_toggle_button.pack(side="right", anchor="e", fill="y")

        self.view_toggle_button.bind("<Enter>", lambda e: self.view_toggle_button.configure(bg=self.image_hover_color))
        self.view_toggle_button.bind("<Leave>", lambda e: self.view_toggle_button.configure(bg=self.image_active_color))

        self.sidebar_title = tk.Label(self.sidebar_title_frame, text="Selected Images", bg=self.image_active_color,
                                      font=Font(size=10, weight="bold"), fg="white")
        self.sidebar_title.pack(side="left", anchor="w")

        """SIDEBAR ADD IMAGE"""

        self.add_images_button = tk.Button(self.sidebar_frame, text="Add Images ", cursor="hand2", bd=0, relief="flat",
                                           compound="right", bg=self.image_active_color, image=self.plus_icon,
                                           font=Font(size=11), command=self.select_files)
        self.add_images_button.pack(side="bottom", fill="x", ipady=2)

        self.add_images_button.bind("<Enter>", lambda e: self.add_images_button.configure(bg=self.image_hover_color))
        self.add_images_button.bind("<Leave>", lambda e: self.add_images_button.configure(bg=self.image_active_color))

        """SCROLLABLE SIDE FRAME"""

        # Canvas for hosting scrollable window
        self.body_canvas = tk.Canvas(self.sidebar_frame)

        # Frame for displaying content. Will be set to canvas window
        self.content_frame = tk.Frame(self.body_canvas)
        self.content_frame.bind("<Configure>", lambda e: self.body_canvas
                                .configure(scrollregion=self.body_canvas.bbox("all")))
        self.content_frame.pack()

        # Scrollbar for scrolling canvas
        self.content_scrollbar = tk.Scrollbar(self.sidebar_frame, orient="vertical", command=self.body_canvas.yview)
        self.content_scrollbar.pack(side="right", fill="y")

        # Set content frame inside a window in the canvas
        self.body_canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        self.body_canvas.configure(yscrollcommand=self.content_scrollbar.set)
        self.body_canvas.pack(side="left", fill="both")

        # Bind scrollwheel to scrollbar to enable scrolling with mouse
        self.content_frame.bind("<Enter>", lambda e: self.bind_to_mousewheel())
        self.content_frame.bind("<Leave>", lambda e: self.unbind_from_mousewheel())

        """IMAGE CANVAS"""

        self.selected_image_display = tk.Label(self.image_frame, bd=0, text="No image selected", bg="light grey")
        self.selected_image_display.place(relx=0.5, rely=0.5, anchor="center")

        """FOOTER CONTENT"""

        self.convert_all_button = tk.Button(self.footer_frame, text="Convert all images ", bd=0, relief="flat",
                                            cursor="hand2", font=Font(size=11), image=self.convert_all_icon,
                                            compound="right", bg=self.convert_button_bg_color,
                                            activebackground=self.convert_button_active_color)
        self.convert_all_button.pack(side="right", fill="y", pady=8, padx=(4, 8), ipadx=3)

        self.convert_all_button.bind("<Enter>", lambda e: self.convert_all_button
                                     .configure(bg=self.convert_button_hover_color))
        self.convert_all_button.bind("<Leave>", lambda e: self.convert_all_button
                                     .configure(bg=self.convert_button_bg_color))

        self.convert_selected_button = tk.Button(self.footer_frame, text="Convert selected image ", bd=0, relief="flat",
                                                 cursor="hand2", font=Font(size=11), image=self.convert_one_icon,
                                                 compound="right", bg=self.convert_button_bg_color,
                                                 activebackground=self.convert_button_active_color)
        self.convert_selected_button.pack(side="right", fill="y", pady=8, padx=(0, 4), ipadx=3)

        self.convert_selected_button.bind("<Enter>", lambda e: self.convert_selected_button
                                          .configure(bg=self.convert_button_hover_color))
        self.convert_selected_button.bind("<Leave>", lambda e: self.convert_selected_button
                                          .configure(bg=self.convert_button_bg_color))

    def on_mousewheel(self, event):
        if self.body_canvas.yview() != (0.0, 1.0):
            self.body_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def bind_to_mousewheel(self):
        self.body_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def unbind_from_mousewheel(self):
        self.body_canvas.unbind_all("<MouseWheel>")

    def add_image(self, path):

        # self.loaded_images_original[path] = ImageTk.PhotoImage(Image.open(path))
        self.loaded_images_compressed[path] = image_scale_down(path)

        image_frame = tk.Frame(self.content_frame, bg=self.image_bg_color, cursor="hand2")
        image_frame.pack(pady=1, padx=(1, 0))

        image_title = tk.Label(image_frame, text=path.split("/")[-1], bg=self.image_bg_color, width=22, anchor="w",
                               font=Font(size=9, weight="bold"))
        image_title.grid(row=0, column=0, sticky="w")

        image_delete_button = tk.Button(image_frame, image=self.delete_icon, relief="flat", bd=0,
                                        bg=self.image_bg_color, activebackground=self.delete_button_active_color,
                                        command=lambda: self.remove_image(image_frame))
        image_delete_button.grid(row=0, column=1, sticky="ens", ipadx=2)

        if self.display_images:
            shown_img = self.loaded_images_compressed[path]
        else:
            shown_img = self.placeholder_image

        image_display = tk.Label(image_frame, image=shown_img, bd=0, bg=self.image_bg_color)
        image_display.grid(row=1, column=0, columnspan=2)

        path_label = tk.Label(image_frame, text=path, bg=self.image_bg_color, width=25, anchor="w", font=Font(size=7))
        path_label.grid(row=2, column=0, sticky="w")

        path_button = tk.Button(image_frame, image=self.folder_icon, relief="flat", bd=0, bg=self.image_bg_color,
                                activebackground=self.folder_button_active_color,
                                command=lambda: subprocess.Popen("explorer.exe /select, \"" + path_label["text"]
                                                                 .replace("/", "\\") + "\""))
        path_button.grid(row=2, column=1, sticky="ens", ipadx=2)

        """BINDS"""

        image_frame.bind("<Enter>", lambda e: self.set_to_hover_color(image_frame))
        image_frame.bind("<Leave>", lambda e: self.set_to_bg_color(image_frame))
        image_frame.bind("<Button-1>", lambda e: self.set_selected_image(path, image_frame))

        image_delete_button.bind("<Enter>", lambda e: image_delete_button.configure(bg=self.delete_button_hover_color))
        image_delete_button.bind("<Leave>", lambda e: image_delete_button.configure(bg=self.image_hover_color))

        path_button.bind("<Enter>", lambda e: path_button.configure(bg=self.folder_button_hover_color))
        path_button.bind("<Leave>", lambda e: path_button.configure(bg=self.image_hover_color))

        image_title.bind("<Button-1>", lambda e: self.set_selected_image(path, image_frame))
        image_display.bind("<Button-1>", lambda e: self.set_selected_image(path, image_frame))
        path_label.bind("<Button-1>", lambda e: self.set_selected_image(path, image_frame))

    def remove_image(self, image_frame):

        if image_frame.children["!label3"]["text"] == self.current_selected_image_path:
            self.current_selected_image_path = None
            self.current_selected_image_data = None
            self.selected_image_display["image"] = ""

        self.loaded_images_compressed.pop(image_frame.children["!label3"]["text"])

        image_frame.destroy()

    def set_to_bg_color(self, frame_widget, ignore_active=False):
        if ignore_active:
            frame_widget["bg"] = self.image_bg_color
            for widget in frame_widget.winfo_children():
                widget["bg"] = self.image_bg_color

        elif frame_widget.children["!label3"]["text"] != self.current_selected_image_path:
            frame_widget["bg"] = self.image_bg_color
            for widget in frame_widget.winfo_children():
                widget["bg"] = self.image_bg_color
        else:
            frame_widget["bg"] = self.image_active_color
            for widget in frame_widget.winfo_children():
                widget["bg"] = self.image_active_color

    def set_to_hover_color(self, frame_widget):
        frame_widget["bg"] = self.image_hover_color
        for widget in frame_widget.winfo_children():
            widget["bg"] = self.image_hover_color

    def set_selected_image(self, img_path, frame_widget):
        for frame in self.content_frame.winfo_children():
            self.set_to_bg_color(frame, ignore_active=True)

        self.current_selected_image_path = img_path
        frame_widget["bg"] = self.image_active_color
        for widget in frame_widget.winfo_children():
            widget["bg"] = self.image_active_color

        self.current_selected_image_data = image_scale_down(self.current_selected_image_path,
                                                            max_width=600, max_height=600)
        self.selected_image_display.configure(image=self.current_selected_image_data)

    def toggle_images(self):
        self.content_scrollbar.set(0, 1)

        if self.display_images:
            self.display_images = False
            self.view_toggle_button["image"] = self.expanded_display_icon
            self.view_toggle_button["text"] = "Expand "

            for frame in self.content_frame.winfo_children():
                frame.children["!label2"]["image"] = self.placeholder_image

        else:
            self.display_images = True
            self.view_toggle_button["image"] = self.compact_display_icon
            self.view_toggle_button["text"] = "Collapse"

            for frame in self.content_frame.winfo_children():
                frame.children["!label2"]["image"] = self.loaded_images_compressed[frame.children["!label3"]["text"]]

        self.body_canvas.yview_moveto(0)

    def select_files(self):
        selected_files = filedialog.askopenfilenames()

        for file in selected_files:
            if file.split(".")[-1].lower() in ["jpg", "jpeg", "png", "gif", "webp"]:
                if file not in self.loaded_images_compressed.keys():
                    threading.Thread(target=lambda: self.add_image(file), daemon=True).start()


"""MAIN"""

if __name__ == "__main__":
    app = App()

    app.add_image(path="E:/GitHub Repositories/IconCreator/src/test_imgs/5d83625f89b0c1814982d588f632464c.jpg")
    app.add_image(path="./test_imgs/9otlbw0pcbi11.png")
    app.add_image(path="./test_imgs/91e9898R7QL._RI_.jpg")
    app.add_image(path="./test_imgs/852aafd708a8b51554779573d67c4026fb9769a8r1-333-301v2_00.jpg")
    app.add_image(path="./test_imgs/20150915_165931.jpg")
    app.add_image(path="./test_imgs/Andere png.png")
    app.add_image(path="./test_imgs/iEXZkt98RtEMT0Ab3WzJaQ1bq2ymRE7S4y8HYFZ6wjA.png")

    app.mainloop()
