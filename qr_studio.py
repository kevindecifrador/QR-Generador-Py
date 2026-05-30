import tkinter as tk
from tkinter import filedialog, colorchooser
import qrcode
import webbrowser
import ttkbootstrap as tb
from PIL import Image, ImageDraw, ImageTk, ImageColor
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, SquareModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

PANEL_COLOR = "#2b3e50"

class QRStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador QR")
        self.root.geometry("850x570")
        
        self.set_defaults()
        self.setup_styles()
        
        self.main_container = tb.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)
        self.show_main_screen()

    def set_defaults(self):
        """Define o reinicia los valores de configuración."""
        self.qr_color = "#000000"
        self.bg_color = "#ffffff"
        self.logo_path = None
        self.current_qr_img = None
        self.round_corners = tk.BooleanVar(value=False)

    def setup_styles(self):
        self.style = tb.Style()
        self.style.configure('TButton', font=('Helvetica', 11, 'bold'))
        self.style.configure('Back.Link.TButton', font=('Helvetica', 12, 'italic'))
        self.style.configure('MainAction.TButton', font=('Helvetica', 13, 'bold'))

    def clear_screen(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def reset_fields(self):
        """Limpia todos los campos y resetea la vista previa."""
        self.set_defaults()
        if hasattr(self, 'entry_data'):
            self.entry_data.delete(0, tk.END)
            self.check_round.configure(variable=self.round_corners)
            self.btn_logo.configure(text="Añadir Logo", bootstyle="info-outline")
        self.update_preview()

    # INTERFAZ

    def show_main_screen(self):
        self.clear_screen()
        frame = tb.Frame(self.main_container)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tb.Label(frame, text="GENERADOR DE QR", font=("Helvetica", 35, "bold"), bootstyle="light").pack(pady=10)
        tb.Label(frame, text="Diseño profesional con bordes redondeados y logos", font=("Helvetica", 11)).pack(pady=(0, 30))

        tb.Button(frame, text="Empezar a Crear", bootstyle="success-outline", 
                  style="MainAction.TButton", command=self.show_editor_screen).pack(ipadx=40, ipady=12)

        self.render_credits()

    def show_editor_screen(self):
        self.clear_screen()
        editor = tb.Frame(self.main_container, padding=20)
        editor.pack(fill="both", expand=True)

        # Panel Izquierdo
        left = tb.Frame(editor, width=350)
        left.pack(side="left", fill="y", padx=(0, 20))

        tb.Button(left, text="← Volver", bootstyle="link", style="Back.Link.TButton", 
                  command=self.show_main_screen).pack(anchor="w")
        
        tb.Label(left, text="Configuración", font=("Helvetica", 22, "bold")).pack(pady=10, anchor="w")

        self.entry_data = tb.Entry(left, bootstyle="primary", font=("Helvetica", 11))
        self.entry_data.pack(fill="x", pady=5)
        self.entry_data.bind("<KeyRelease>", lambda e: self.update_preview())

        self.check_round = tb.Checkbutton(left, text="Esquinas Redondeadas", variable=self.round_corners, 
                                          bootstyle="round-toggle", command=self.update_preview)
        self.check_round.pack(pady=10, anchor="w")

        c_frame = tb.Frame(left)
        c_frame.pack(fill="x", pady=5)
        tb.Button(c_frame, text="Cuadritos", bootstyle="secondary-outline", 
                  command=lambda: self.pick_color('qr')).pack(side="left", expand=True, fill="x", padx=2)
        tb.Button(c_frame, text="Fondo", bootstyle="secondary-outline", 
                  command=lambda: self.pick_color('bg')).pack(side="left", expand=True, fill="x", padx=2)

        self.btn_logo = tb.Button(left, text="Añadir Logo", bootstyle="info-outline", command=self.add_logo)
        self.btn_logo.pack(fill="x", pady=10)

        tb.Button(left, text="Limpiar Campos", bootstyle="danger-outline", 
                  command=self.reset_fields).pack(fill="x", pady=5)

        tb.Button(left, text="Guardar como PNG", bootstyle="success", style="MainAction.TButton", 
                  command=self.save_qr).pack(fill="x", side="bottom")

        self.preview_panel = tb.Frame(editor, bootstyle="secondary")
        self.preview_panel.pack(side="right", fill="both", expand=True)
        
        self.preview_label = tb.Label(self.preview_panel, background=PANEL_COLOR)
        self.preview_label.place(relx=0.5, rely=0.5, anchor="center")

        self.update_preview()

    def render_credits(self):
        cred = tk.Label(self.main_container, text="@Kevin Sánchez. 2026",
                        font=("Arial", 10, "underline"), fg="#3498db", bg=PANEL_COLOR, cursor="hand2")
        cred.place(relx=1.0, rely=1.0, anchor="se", x=-15, y=-15)
        cred.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.instagram.com/kevin.san.99/"))

    def pick_color(self, target):
        color = colorchooser.askcolor()[1]
        if color:
            if target == 'qr': self.qr_color = color
            else: self.bg_color = color
            self.update_preview()

    def add_logo(self):
        path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])
        if path:
            self.logo_path = path
            self.btn_logo.configure(text="✅ Logo Cargado", bootstyle="info")
            self.update_preview()

    def apply_rounded_mask(self, img, radius):
        """Aplica redondeo real usando canal Alfa para evitar esquinas sobrantes."""
        img = img.convert("RGBA")
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0) + img.size, radius=radius, fill=255)
        
        # Crear imagen transparente y pegar el QR usando la máscara en el Alpha
        output = Image.new('RGBA', img.size, (0, 0, 0, 0))
        output.paste(img, (0, 0), mask=mask)
        return output

    def update_preview(self, event=None):
        data = self.entry_data.get() if hasattr(self, 'entry_data') else " "
        if not data: data = " "
        
        try:
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
            qr.add_data(data)
            qr.make(fit=True)

            fg_rgb = ImageColor.getcolor(self.qr_color, "RGB")
            bg_rgb = ImageColor.getcolor(self.bg_color, "RGB")
            drawer = RoundedModuleDrawer() if self.round_corners.get() else SquareModuleDrawer()

            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=drawer,
                color_mask=SolidFillColorMask(front_color=fg_rgb, back_color=bg_rgb)
            ).convert('RGB')

            if self.logo_path:
                logo = Image.open(self.logo_path).convert("RGBA")
                size = img.size[0] // 4
                logo = logo.resize((size, size), Image.Resampling.LANCZOS)
                pos = ((img.size[0] - size) // 2, (img.size[1] - size) // 2)
                draw = ImageDraw.Draw(img)
                draw.rectangle([pos, (pos[0]+size, pos[1]+size)], fill=self.bg_color)
                img.paste(logo, pos, mask=logo)

            if self.round_corners.get():
                img = self.apply_rounded_mask(img, radius=50)

            self.current_qr_img = img

            self.root.update_idletasks()
            w, h = self.preview_panel.winfo_width(), self.preview_panel.winfo_height()
            side = int(min(w, h) * 0.85) if w > 1 else 350

            preview = img.resize((side, side), Image.Resampling.LANCZOS)
            self.tk_img = ImageTk.PhotoImage(preview)
            self.preview_label.configure(image=self.tk_img)

        except Exception as e:
            print(f"Error: {e}")

    def save_qr(self):
        if self.current_qr_img:
            path = filedialog.asksaveasfilename(defaultextension=".png", 
                                               filetypes=[("PNG con transparencia", "*.png")])
            if path:
                self.current_qr_img.save(path)

if __name__ == "__main__":
    app_root = tb.Window(themename="superhero")
    QRStudio(app_root)
    app_root.mainloop()
