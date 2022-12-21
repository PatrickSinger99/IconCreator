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

        self.title("Icon Converter")
        self.resizable(False, False)
        self.iconbitmap("icons/app_icon.ico")

        # Runtime variables
        self.loaded_images_compressed = {}  # dictionary of all loaded images, key = path, value = ImageTk object
        self.loaded_images_original = {}  # Currently not used
        self.current_selected_image_path = None  # Path of image that is currently selected in the edit frame
        self.current_selected_image_data = None  # Currently selected image as ImageTk object
        self.display_images = True  # Toggle variable for displaying images in left sidebar

        self.canvas_button_click = False
        self.canvas_click_x = None
        self.canvas_click_y = None
        self.crop_lines = []

        """COLORS"""

        # Sidebar loaded image element
        self.image_bg_color = "light grey"  # "#adc2eb"
        self.image_hover_color = "#6f94dc"
        self.image_active_color = "#3366cc"

        # Delete button of loaded image element in sidebar
        self.delete_button_hover_color = "#ff6666"
        self.delete_button_active_color = "#ff3333"

        # Open folder button of loaded image element in sidebar
        self.folder_button_hover_color = "#ffad33"
        self.folder_button_active_color = "#ff9900"

        # Ico convert button
        self.convert_button_bg_color = "#00b386"
        self.convert_button_hover_color = "#00cc99"
        self.convert_button_active_color = "white"  # "#00e6ac"

        # Edit button
        self.edit_button_bg_color = "#ff9933"
        self.edit_button_hover_color = "#ffb366"

        """IMAGES"""

        # Header
        self.app_logo = tk.PhotoImage(file="icons/app_icon_medium_1.png")
        self.settings_icon = tk.PhotoImage(file="icons/settings.png")
        self.settings_hover_icon = tk.PhotoImage(file="icons/settings_hover.png")

        # Sidebar
        self.delete_icon = tk.PhotoImage(file="icons/delete.png")
        self.folder_icon = tk.PhotoImage(file="icons/folder.png")
        self.placeholder_image = tk.PhotoImage(file="icons/placeholder.png")
        self.expanded_display_icon = tk.PhotoImage(file="icons/expanded_display.png")
        self.compact_display_icon = tk.PhotoImage(file="icons/compact_display.png")
        self.plus_icon = tk.PhotoImage(file="icons/plus.png")

        # Image Edit
        self.crop_image = tk.PhotoImage(file="icons/crop.png")
        self.crop_hover_image = tk.PhotoImage(file="icons/crop_hover.png")

        self.rotate_left_image = tk.PhotoImage(file="icons/rotate_left.png")
        self.rotate_left_hover_image = tk.PhotoImage(file="icons/rotate_left_hover.png")
        self.rotate_right_image = tk.PhotoImage(file="icons/rotate_right.png")
        self.rotate_right_hover_image = tk.PhotoImage(file="icons/rotate_right_hover.png")

        self.flip_vertical_image = tk.PhotoImage(file="icons/flip_vertical.png")
        self.flip_vertical_hover_image = tk.PhotoImage(file="icons/flip_vertical_hover.png")
        self.flip_horizontal_image = tk.PhotoImage(file="icons/flip_horizontal.png")
        self.flip_horizontal_hover_image = tk.PhotoImage(file="icons/flip_horizontal_hover.png")

        # Footer
        self.convert_one_icon = tk.PhotoImage(file="icons/convert_one.png")
        self.convert_all_icon = tk.PhotoImage(file="icons/convert_all.png")
        self.arrow_image = tk.PhotoImage(file="icons/arrow.png")

        # Icon Animation
        self.app_logo_a1 = tk.PhotoImage(file="icons/app_icon_medium_2.png")
        self.app_logo_a2 = tk.PhotoImage(file="icons/app_icon_medium_3.png")
        self.app_logo_a3 = tk.PhotoImage(file="icons/app_icon_medium_4.png")

        """APP LAYOUT FRAMES"""

        # Header (Title, settings)
        self.header_frame = tk.Frame(self, bg="grey", width=900, height=40)
        self.header_frame.grid(row=0, column=0, columnspan=2)
        self.header_frame.pack_propagate(False)

        # Sidebar (Loaded images display)
        self.sidebar_frame = tk.Frame(self, bg="black", width=198, height=600)
        self.sidebar_frame.grid(row=1, column=0)
        self.sidebar_frame.pack_propagate(False)

        # Selected Image display
        self.image_frame = tk.Frame(self, bg="light grey", width=702, height=600)
        self.image_frame.grid(row=1, column=1)
        self.image_frame.pack_propagate(False)

        # Footer (Convert buttons)
        self.footer_frame = tk.Frame(self, bg="grey", width=900, height=40)
        self.footer_frame.grid(row=2, column=0, columnspan=2)
        self.footer_frame.pack_propagate(False)

        """HEADER"""

        # App title & logo
        self.title_label = tk.Label(self.header_frame, text=" Icon Converter", font=Font(size=18), bd=0,
                                    image=self.app_logo, compound="left", bg="grey", cursor="hand2")
        self.title_label.pack(side="left", padx=(6, 0))

        self.title_label.bind("<Button-1>", lambda e: self.animation_easter_egg_start())

        # App version info
        self.info_label = tk.Label(self.header_frame, text="Version 0.2", font=Font(size=10), bg="grey",
                                   fg="light grey")

        self.info_label.pack(side="left", padx=(10, 0))

        # Settings button
        self.settings_button = tk.Button(self.header_frame, text="Settings ", bd=0, relief="flat", cursor="hand2",
                                         font=Font(size=11), image=self.settings_icon, compound="right",
                                         bg="grey", activebackground="white")
        self.settings_button.pack(side="right", fill="y", ipadx=6)

        self.settings_button.bind("<Enter>", lambda e: self.settings_button
                                  .configure(bg="light grey", image=self.settings_hover_icon))
        self.settings_button.bind("<Leave>", lambda e: self.settings_button
                                  .configure(bg="grey", image=self.settings_icon))

        """SIDEBAR"""

        # FRAME: Sidebar header
        self.sidebar_title_frame = tk.Frame(self.sidebar_frame, bg=self.image_active_color)
        self.sidebar_title_frame.pack(side="top", fill="x", ipady=1)

        # Title for sidebar
        self.sidebar_title = tk.Label(self.sidebar_title_frame, text="Loaded Images", bg=self.image_active_color,
                                      font=Font(size=10, weight="bold"), fg="white")
        self.sidebar_title.pack(side="left", anchor="w", ipadx=2)

        # Toggle display button
        self.view_toggle_button = tk.Button(self.sidebar_title_frame, text="Collapse", command=self.toggle_images,
                                            cursor="hand2", bd=0, relief="flat", compound="right", width=60, anchor="e",
                                            image=self.compact_display_icon, font=Font(size=8),
                                            bg=self.image_active_color)
        self.view_toggle_button.pack(side="right", anchor="e", fill="y")

        self.view_toggle_button.bind("<Enter>", lambda e: self.view_toggle_button.configure(bg=self.image_hover_color))
        self.view_toggle_button.bind("<Leave>", lambda e: self.view_toggle_button.configure(bg=self.image_active_color))

        """SIDEBAR SCROLL FUNCTIONALITY"""

        # Canvas for hosting scrollable window
        self.body_canvas = tk.Canvas(self.sidebar_frame, highlightthickness=0, relief='ridge', bd=0)

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

        """IMAGE DISPLAY"""

        # FRAME: Sidebar header
        self.edit_title_frame = tk.Frame(self.image_frame, bg=self.convert_button_bg_color)
        self.edit_title_frame.pack(side="top", fill="x", ipady=1)

        # Title for sidebar
        self.sidebar_title = tk.Label(self.edit_title_frame, text="Edit Image", bg=self.convert_button_bg_color,
                                      font=Font(size=10, weight="bold"), fg="white")
        self.sidebar_title.pack(side="left", anchor="w", ipadx=5)

        # FRAME: Edit canvas
        self.canvas_frame = tk.Frame(self.image_frame)
        self.canvas_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.edit_canvas = tk.Canvas(self.canvas_frame, bd=0, highlightthickness=0, relief='ridge', width=0, height=0)
        self.edit_canvas.pack(fill="both", expand=True)
        self.edit_canvas.bind("<Motion>", self.canvas_cursor_position)
        self.edit_canvas.bind("<Button-1>", self.canvas_on_click)

        # Edit button frame
        self.edit_button_frame = tk.Frame(self.image_frame)
        self.edit_button_frame.pack(side="bottom")

        # Crop Button
        self.crop_button = tk.Button(self.edit_button_frame, image=self.crop_image, relief="flat", cursor="hand2",
                                     bg=self.edit_button_bg_color, bd=0)
        self.crop_button.grid(row=0, column=0, ipadx=2, ipady=2)

        self.crop_button.bind("<Enter>", lambda e: self.crop_button
                              .configure(image=self.crop_hover_image, bg=self.edit_button_hover_color))
        self.crop_button.bind("<Leave>", lambda e: self.crop_button
                              .configure(image=self.crop_image, bg=self.edit_button_bg_color))

        # Rotate left Button
        self.rotate_left_button = tk.Button(self.edit_button_frame, image=self.rotate_left_image, relief="flat",
                                            cursor="hand2", bg=self.edit_button_bg_color, bd=0)
        self.rotate_left_button.grid(row=0, column=1, ipadx=2, ipady=2)

        self.rotate_left_button.bind("<Enter>", lambda e: self.rotate_left_button
                                     .configure(image=self.rotate_left_hover_image, bg=self.edit_button_hover_color))
        self.rotate_left_button.bind("<Leave>", lambda e: self.rotate_left_button
                                     .configure(image=self.rotate_left_image, bg=self.edit_button_bg_color))

        # Rotate right Button
        self.rotate_right_button = tk.Button(self.edit_button_frame, image=self.rotate_right_image, relief="flat",
                                             cursor="hand2", bg=self.edit_button_bg_color, bd=0)
        self.rotate_right_button.grid(row=0, column=2, ipadx=2, ipady=2)

        self.rotate_right_button.bind("<Enter>", lambda e: self.rotate_right_button
                                      .configure(image=self.rotate_right_hover_image, bg=self.edit_button_hover_color))
        self.rotate_right_button.bind("<Leave>", lambda e: self.rotate_right_button
                                      .configure(image=self.rotate_right_image, bg=self.edit_button_bg_color))

        # Flip vertical Button
        self.flip_vertical_button = tk.Button(self.edit_button_frame, image=self.flip_vertical_image, relief="flat",
                                              cursor="hand2", bg=self.edit_button_bg_color, bd=0)
        self.flip_vertical_button.grid(row=0, column=3, ipadx=2, ipady=2)

        self.flip_vertical_button.bind("<Enter>", lambda e: self.flip_vertical_button
                                       .configure(image=self.flip_vertical_hover_image,
                                                  bg=self.edit_button_hover_color))
        self.flip_vertical_button.bind("<Leave>", lambda e: self.flip_vertical_button
                                       .configure(image=self.flip_vertical_image, bg=self.edit_button_bg_color))

        # Flip horizontal Button
        self.flip_horizontal_button = tk.Button(self.edit_button_frame, image=self.flip_horizontal_image, relief="flat",
                                                cursor="hand2", bg=self.edit_button_bg_color, bd=0)
        self.flip_horizontal_button.grid(row=0, column=4, ipadx=2, ipady=2)

        self.flip_horizontal_button.bind("<Enter>", lambda e: self.flip_horizontal_button
                                         .configure(image=self.flip_horizontal_hover_image,
                                                    bg=self.edit_button_hover_color))
        self.flip_horizontal_button.bind("<Leave>", lambda e: self.flip_horizontal_button
                                         .configure(image=self.flip_horizontal_image, bg=self.edit_button_bg_color))

        """FOOTER"""

        # Add images button
        self.add_images_button = tk.Button(self.footer_frame, text="Add images ", cursor="hand2", bd=0, relief="flat",
                                           compound="right", bg=self.image_active_color, image=self.plus_icon,
                                           font=Font(size=11), command=self.select_files, width=180)
        self.add_images_button.pack(side="left", fill="y", pady=5, padx=(5, 5), ipadx=3)

        self.add_images_button.bind("<Enter>", lambda e: self.add_images_button.configure(bg=self.image_hover_color))
        self.add_images_button.bind("<Leave>", lambda e: self.add_images_button.configure(bg=self.image_active_color))

        # Arrow guide image
        tk.Label(self.footer_frame, image=self.arrow_image, bg="grey").pack(side="left", padx=20)

        # File destination entry
        self.save_location_entry = tk.Entry(self.footer_frame, relief="flat", bd=0, bg="light grey", width=33)
        self.save_location_entry.pack(side="left", fill="y", pady=5, padx=(5, 5))

        # Arrow guide image
        tk.Label(self.footer_frame, image=self.arrow_image, bg="grey").pack(side="left", padx=20)

        # Convert all loaded images button
        self.convert_all_button = tk.Button(self.footer_frame, text="Convert all images ", bd=0, relief="flat",
                                            cursor="hand2", font=Font(size=11), image=self.convert_all_icon,
                                            compound="right", bg=self.convert_button_bg_color,
                                            activebackground=self.convert_button_active_color)
        self.convert_all_button.pack(side="right", fill="y", pady=5, padx=(5, 5), ipadx=3)

        self.convert_all_button.bind("<Enter>", lambda e: self.convert_all_button
                                     .configure(bg=self.convert_button_hover_color))
        self.convert_all_button.bind("<Leave>", lambda e: self.convert_all_button
                                     .configure(bg=self.convert_button_bg_color))

        # Convert selected image button
        self.convert_selected_button = tk.Button(self.footer_frame, text="Convert selected image ", bd=0, relief="flat",
                                                 cursor="hand2", font=Font(size=11), image=self.convert_one_icon,
                                                 compound="right", bg=self.convert_button_bg_color,
                                                 activebackground=self.convert_button_active_color)
        self.convert_selected_button.pack(side="right", fill="y", pady=5, padx=(5, 0), ipadx=3)

        self.convert_selected_button.bind("<Enter>", lambda e: self.convert_selected_button
                                          .configure(bg=self.convert_button_hover_color))
        self.convert_selected_button.bind("<Leave>", lambda e: self.convert_selected_button
                                          .configure(bg=self.convert_button_bg_color))

        """INITIAL CALLS"""

        self.after(30, self.check_convert_button_state)

    # Scroll sidebar canvas on mousewheel
    def on_mousewheel(self, event):
        # Only enable scrolling if scrollbar active
        if self.body_canvas.yview() != (0.0, 1.0):
            self.body_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Bind mousewheel to sidebar canvas
    def bind_to_mousewheel(self):
        self.body_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    # Unbind mousewheel from sidebar canvas
    def unbind_from_mousewheel(self):
        self.body_canvas.unbind_all("<MouseWheel>")

    # Add image to to loaded images sidebar
    def add_image(self, path):
        self.loaded_images_compressed[path] = image_scale_down(path)

        """ELEMENT FRAME"""

        # Frame for new image element
        image_frame = tk.Frame(self.content_frame, bg=self.image_bg_color, cursor="hand2")
        image_frame.pack(pady=(1, 0), padx=(1, 0))

        # image element color changes on mouse actions
        image_frame.bind("<Enter>", lambda e: self.set_to_hover_color(image_frame))
        image_frame.bind("<Leave>", lambda e: self.set_to_bg_color(image_frame))
        image_frame.bind("<Button-1>", lambda e: self.set_selected_image(path, image_frame))

        """HEADER"""

        # Title of image
        image_title = tk.Label(image_frame, text=path.split("/")[-1], bg=self.image_bg_color, width=22, anchor="w",
                               font=Font(size=9, weight="bold"))
        image_title.grid(row=0, column=0, sticky="w")
        image_title.bind("<Button-1>", lambda e: self.set_selected_image(path, image_frame))

        # remove image from sidebar button
        image_delete_button = tk.Button(image_frame, image=self.delete_icon, relief="flat", bd=0,
                                        bg=self.image_bg_color, activebackground=self.delete_button_active_color,
                                        command=lambda: self.remove_image(image_frame))
        image_delete_button.grid(row=0, column=1, sticky="ens", ipadx=2)

        image_delete_button.bind("<Enter>", lambda e: image_delete_button.configure(bg=self.delete_button_hover_color))
        image_delete_button.bind("<Leave>", lambda e: image_delete_button.configure(bg=self.image_hover_color))

        """BODY"""

        # IF toggle to display image is active, display image
        if self.display_images:
            shown_img = self.loaded_images_compressed[path]
        # ELSE display placeholder image
        else:
            shown_img = self.placeholder_image

        # Image display
        image_display = tk.Label(image_frame, image=shown_img, bd=0, bg=self.image_bg_color)
        image_display.grid(row=1, column=0, columnspan=2)
        image_display.bind("<Button-1>", lambda e: self.set_selected_image(path, image_frame))

        """FOOTER"""

        # Image path label
        path_label = tk.Label(image_frame, text=path, bg=self.image_bg_color, width=26, anchor="w", font=Font(size=7))
        path_label.grid(row=2, column=0, sticky="w")
        path_label.bind("<Button-1>", lambda e: self.set_selected_image(path, image_frame))

        # Button to open path of image in explorer
        path_button = tk.Button(image_frame, image=self.folder_icon, relief="flat", bd=0, bg=self.image_bg_color,
                                activebackground=self.folder_button_active_color,
                                command=lambda: subprocess.Popen("explorer.exe /select, \"" + path_label["text"]
                                                                 .replace("/", "\\") + "\""))
        path_button.grid(row=2, column=1, sticky="ens", ipadx=2)

        path_button.bind("<Enter>", lambda e: path_button.configure(bg=self.folder_button_hover_color))
        path_button.bind("<Leave>", lambda e: path_button.configure(bg=self.image_hover_color))

    # Remove image from sidebar
    def remove_image(self, image_frame):

        # IF image is currently selected, remove selection
        if image_frame.children["!label3"]["text"] == self.current_selected_image_path:
            self.current_selected_image_path = None
            self.current_selected_image_data = None

            # Reset edit canvas
            self.edit_canvas.delete("all")
            self.edit_canvas.configure(width=0, height=0)

        # Remove image reference from loaded image dictionary
        self.loaded_images_compressed.pop(image_frame.children["!label3"]["text"])

        # Destroy image element frame
        image_frame.destroy()

        self.check_convert_button_state()

    # Set correct background color for image element in sidebar based on selection
    def set_to_bg_color(self, frame_widget, ignore_active=False):
        # IF ignore active flag, change color regardless of state
        if ignore_active:
            frame_widget["bg"] = self.image_bg_color
            for widget in frame_widget.winfo_children():
                widget["bg"] = self.image_bg_color

        # IF image is currently not selected, change to inactive color
        elif frame_widget.children["!label3"]["text"] != self.current_selected_image_path:
            frame_widget["bg"] = self.image_bg_color
            for widget in frame_widget.winfo_children():
                widget["bg"] = self.image_bg_color

        # IF image is currently selected, change to active color
        else:
            frame_widget["bg"] = self.image_active_color
            for widget in frame_widget.winfo_children():
                widget["bg"] = self.image_active_color

    # Set image element content to hover color
    def set_to_hover_color(self, frame_widget):
        frame_widget["bg"] = self.image_hover_color
        for widget in frame_widget.winfo_children():
            widget["bg"] = self.image_hover_color

    # Select image and change appearence in sidebar
    def set_selected_image(self, img_path, frame_widget):
        # Remove possible active selection colors from loaded image elements
        for frame in self.content_frame.winfo_children():
            self.set_to_bg_color(frame, ignore_active=True)

        self.current_selected_image_path = img_path
        frame_widget["bg"] = self.image_active_color
        for widget in frame_widget.winfo_children():
            widget["bg"] = self.image_active_color

        # Save curent selected image data
        self.current_selected_image_data = image_scale_down(self.current_selected_image_path,
                                                            max_width=500, max_height=500)
        # Reset edit canvas
        self.edit_canvas.delete("all")
        # Add image to canvas
        self.edit_canvas.create_image(0, 0, anchor="nw", image=self.current_selected_image_data)
        self.edit_canvas.configure(width=self.current_selected_image_data.width(),
                                   height=self.current_selected_image_data.height())

        self.check_convert_button_state()

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

        self.check_convert_button_state()

    def check_convert_button_state(self):
        if len(self.loaded_images_compressed) == 0:
            self.convert_all_button["state"] = "disabled"
            self.convert_all_button.unbind("<Enter>")

            self.convert_selected_button["state"] = "disabled"
            self.convert_selected_button.unbind("<Enter>")
        else:
            self.convert_all_button["state"] = "normal"
            self.convert_all_button.bind("<Enter>", lambda e: self.convert_all_button
                                         .configure(bg=self.convert_button_hover_color))

        if self.current_selected_image_path is None:
            self.convert_selected_button["state"] = "disabled"
            self.convert_selected_button.unbind("<Enter>")
        else:
            self.convert_selected_button["state"] = "normal"
            self.convert_selected_button.bind("<Enter>", lambda e: self.convert_selected_button
                                              .configure(bg=self.convert_button_hover_color))

    def canvas_cursor_position(self, event):
        if self.canvas_button_click:
            x, y = event.x, event.y
            for line in self.crop_lines:
                self.edit_canvas.delete(line)

            x1 = self.edit_canvas.create_line(self.canvas_click_x, self.canvas_click_y,
                                              self.canvas_click_x, y, fill=self.edit_button_bg_color, width=1)
            x2 = self.edit_canvas.create_line(x, self.canvas_click_y,
                                              x, y, fill=self.edit_button_bg_color, width=1)
            y1 = self.edit_canvas.create_line(self.canvas_click_x, self.canvas_click_y,
                                              x, self.canvas_click_y, fill=self.edit_button_bg_color, width=1)
            y2 = self.edit_canvas.create_line(self.canvas_click_x, y,
                                              x, y, fill=self.edit_button_bg_color, width=1)

            self.crop_lines = [x1, x2, y1, y2]
            print('{}, {}'.format(x, y))

    def canvas_on_click(self, event):
        if self.canvas_button_click:
            self.canvas_button_click = False

        else:
            self.canvas_click_x = event.x
            self.canvas_click_y = event.y
            self.canvas_button_click = True

    def animation_easter_egg_start(self):
        self.title_label.configure(image=self.app_logo_a1)

        # Color change
        if self.title_label["fg"] == "SystemButtonText":
            self.title_label.configure(fg=self.image_active_color)

        elif self.title_label["fg"] == self.image_active_color:
            self.title_label.configure(fg=self.convert_button_bg_color)

        else:
            self.title_label.configure(fg="SystemButtonText")

        self.after(150, self.animation_easter_egg_a1)

    def animation_easter_egg_a1(self):
        self.title_label.configure(image=self.app_logo_a2)
        self.after(150, self.animation_easter_egg_a2)

    def animation_easter_egg_a2(self):
        self.title_label.configure(image=self.app_logo_a3)
        self.after(150, self.animation_easter_egg_a3d)

    def animation_easter_egg_a3d(self):
        self.title_label.configure(image=self.app_logo)

"""MAIN"""

if __name__ == "__main__":
    app = App()
    app.eval('tk::PlaceWindow . center')  # Start app window in center of screen

    app.add_image(path="E:/GitHub Repositories/IconCreator/src/test_imgs/5d83625f89b0c1814982d588f632464c.jpg")
    app.add_image(path="./test_imgs/9otlbw0pcbi11.png")
    app.add_image(path="./test_imgs/91e9898R7QL._RI_.jpg")
    app.add_image(path="./test_imgs/852aafd708a8b51554779573d67c4026fb9769a8r1-333-301v2_00.jpg")
    app.add_image(path="./test_imgs/20150915_165931.jpg")
    app.add_image(path="./test_imgs/Andere png.png")
    app.add_image(path="./test_imgs/iEXZkt98RtEMT0Ab3WzJaQ1bq2ymRE7S4y8HYFZ6wjA.png")

    app.mainloop()
