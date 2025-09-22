import sys
import os
import math
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QFileDialog, QDoubleSpinBox, QSpinBox, QMessageBox, QScrollArea, QFrame
)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QSize

import fitz  # PyMuPDF
from reportlab.lib.units import mm

# --- Funções de Lógica de Imposição ---
def rotate_point(x, y, angle_degrees, center_x=0, center_y=0):
    angle_radians = math.radians(angle_degrees)
    translated_x = x - center_x
    translated_y = y - center_y
    rotated_x = translated_x * math.cos(angle_radians) - translated_y * math.sin(angle_radians)
    rotated_y = translated_x * math.sin(angle_radians) + translated_y * math.cos(angle_radians)
    return rotated_x + center_x, rotated_y + center_y

def get_rotated_bbox(width, height, angle_degrees):
    half_w, half_h = width / 2, height / 2
    corners = [
        (-half_w, -half_h),
        (half_w, -half_h),
        (half_w, half_h),
        (-half_w, half_h)
    ]
    rotated_corners = [rotate_point(cx, cy, angle_degrees) for cx, cy in corners]
    min_x = min(rc[0] for rc in rotated_corners)
    max_x = max(rc[0] for rc in rotated_corners)
    min_y = min(rc[1] for rc in rotated_corners)
    max_y = max(rc[1] for rc in rotated_corners)
    return max_x - min_x, max_y - min_y

class ImpositionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Protótipo de Imposição Irregular com GUI")
        self.setGeometry(100, 100, 1200, 800)

        self.input_pdf_path = ""
        self.output_pdf_path = "imposicao_final.pdf"
        self.sheet_width_mm = 210
        self.sheet_height_mm = 297
        self.shape_width_mm = 50
        self.shape_height_mm = 30
        self.rotations_degrees = [0, 90, 180, 270]
        self.padding_mm = 2.0
        self.num_shapes_to_impose = 20

        self.init_ui()
        self.load_config()

    def init_ui(self):
        main_layout = QHBoxLayout()

        # --- Painel de Controle (Esquerda) ---
        control_panel_layout = QVBoxLayout()
        control_panel_layout.setAlignment(Qt.AlignTop)
        
        # Input PDF
        input_pdf_layout = QHBoxLayout()
        self.input_pdf_label = QLabel("PDF de Entrada:")
        self.input_pdf_line = QLineEdit(self.input_pdf_path)
        self.input_pdf_line.setReadOnly(True)
        self.browse_pdf_button = QPushButton("Procurar...")
        self.browse_pdf_button.clicked.connect(self.browse_input_pdf)
        input_pdf_layout.addWidget(self.input_pdf_label)
        input_pdf_layout.addWidget(self.input_pdf_line)
        input_pdf_layout.addWidget(self.browse_pdf_button)
        control_panel_layout.addLayout(input_pdf_layout)

        # Output PDF
        output_pdf_layout = QHBoxLayout()
        self.output_pdf_label = QLabel("PDF de Saída:")
        self.output_pdf_line = QLineEdit(self.output_pdf_path)
        output_pdf_layout.addWidget(self.output_pdf_label)
        output_pdf_layout.addWidget(self.output_pdf_line)
        control_panel_layout.addLayout(output_pdf_layout)

        # Sheet Dimensions
        sheet_dim_layout = QHBoxLayout()
        sheet_dim_layout.addWidget(QLabel("Largura da Folha (mm):"))
        self.sheet_width_spin = QDoubleSpinBox()
        self.sheet_width_spin.setRange(1, 1000)
        self.sheet_width_spin.setValue(self.sheet_width_mm)
        self.sheet_width_spin.setSuffix(" mm")
        sheet_dim_layout.addWidget(self.sheet_width_spin)

        sheet_dim_layout.addWidget(QLabel("Altura da Folha (mm):"))
        self.sheet_height_spin = QDoubleSpinBox()
        self.sheet_height_spin.setRange(1, 1000)
        self.sheet_height_spin.setValue(self.sheet_height_mm)
        self.sheet_height_spin.setSuffix(" mm")
        sheet_dim_layout.addWidget(self.sheet_height_spin)
        control_panel_layout.addLayout(sheet_dim_layout)

        # Shape Dimensions
        shape_dim_layout = QHBoxLayout()
        shape_dim_layout.addWidget(QLabel("Largura da Forma (mm):"))
        self.shape_width_spin = QDoubleSpinBox()
        self.shape_width_spin.setRange(1, 500)
        self.shape_width_spin.setValue(self.shape_width_mm)
        self.shape_width_spin.setSuffix(" mm")
        shape_dim_layout.addWidget(self.shape_width_spin)

        shape_dim_layout.addWidget(QLabel("Altura da Forma (mm):"))
        self.shape_height_spin = QDoubleSpinBox()
        self.shape_height_spin.setRange(1, 500)
        self.shape_height_spin.setValue(self.shape_height_mm)
        self.shape_height_spin.setSuffix(" mm")
        shape_dim_layout.addWidget(self.shape_height_spin)
        control_panel_layout.addLayout(shape_dim_layout)

        # Rotations
        rotations_layout = QHBoxLayout()
        rotations_layout.addWidget(QLabel("Rotações (graus, separadas por vírgula):"))
        self.rotations_line = QLineEdit(", ".join(map(str, self.rotations_degrees)))
        rotations_layout.addWidget(self.rotations_line)
        control_panel_layout.addLayout(rotations_layout)

        # Padding
        padding_layout = QHBoxLayout()
        padding_layout.addWidget(QLabel("Preenchimento (mm):"))
        self.padding_spin = QDoubleSpinBox()
        self.padding_spin.setRange(0, 100)
        self.padding_spin.setValue(self.padding_mm)
        self.padding_spin.setSuffix(" mm")
        padding_layout.addWidget(self.padding_spin)
        control_panel_layout.addLayout(padding_layout)

        # Number of shapes to impose
        num_shapes_layout = QHBoxLayout()
        num_shapes_layout.addWidget(QLabel("Número de Formas a Impor:"))
        self.num_shapes_spin = QSpinBox()
        self.num_shapes_spin.setRange(1, 1000)
        self.num_shapes_spin.setValue(self.num_shapes_to_impose)
        num_shapes_layout.addWidget(self.num_shapes_spin)
        control_panel_layout.addLayout(num_shapes_layout)

        # Buttons
        self.preview_button = QPushButton("Gerar Pré-visualização")
        self.preview_button.clicked.connect(self.generate_preview)
        control_panel_layout.addWidget(self.preview_button)

        self.generate_pdf_button = QPushButton("Gerar PDF Final")
        self.generate_pdf_button.clicked.connect(self.generate_final_pdf)
        control_panel_layout.addWidget(self.generate_pdf_button)

        main_layout.addLayout(control_panel_layout, 1)

        # --- Painel de Pré-visualização (Direita) ---
        self.preview_scroll_area = QScrollArea()
        self.preview_scroll_area.setWidgetResizable(True)
        self.preview_widget = QLabel()
        self.preview_widget.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.preview_widget.setStyleSheet("background-color: lightgray; border: 1px solid gray;")
        self.preview_scroll_area.setWidget(self.preview_widget)
        main_layout.addWidget(self.preview_scroll_area, 3)

        self.setLayout(main_layout)

    def browse_input_pdf(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Selecionar PDF de Entrada", "", "PDF Files (*.pdf)")
        if fname:
            self.input_pdf_path = fname
            self.input_pdf_line.setText(fname)
            self.save_config()

    def get_parameters(self):
        try:
            self.output_pdf_path = self.output_pdf_line.text()
            self.sheet_width_mm = self.sheet_width_spin.value()
            self.sheet_height_mm = self.sheet_height_spin.value()
            self.shape_width_mm = self.shape_width_spin.value()
            self.shape_height_mm = self.shape_height_spin.value()
            self.rotations_degrees = list(map(int, self.rotations_line.text().replace(" ", "").split(",")))
            self.padding_mm = self.padding_spin.value()
            self.num_shapes_to_impose = self.num_shapes_spin.value()
            return True
        except ValueError:
            QMessageBox.critical(self, "Erro de Parâmetro", "Verifique os valores de rotação. Devem ser números inteiros separados por vírgula.")
            return False

    def save_config(self):
        config = {
            "input_pdf_path": self.input_pdf_path,
            "output_pdf_path": self.output_pdf_path,
            "sheet_width_mm": self.sheet_width_mm,
            "sheet_height_mm": self.sheet_height_mm,
            "shape_width_mm": self.shape_width_mm,
            "shape_height_mm": self.shape_height_mm,
            "rotations_degrees": self.rotations_degrees,
            "padding_mm": self.padding_mm,
            "num_shapes_to_impose": self.num_shapes_to_impose,
        }
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)

    def load_config(self):
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                config = json.load(f)
                self.input_pdf_path = config.get("input_pdf_path", "")
                self.output_pdf_path = config.get("output_pdf_path", "imposicao_final.pdf")
                self.sheet_width_mm = config.get("sheet_width_mm", 210)
                self.sheet_height_mm = config.get("sheet_height_mm", 297)
                self.shape_width_mm = config.get("shape_width_mm", 50)
                self.shape_height_mm = config.get("shape_height_mm", 30)
                self.rotations_degrees = config.get("rotations_degrees", [0, 90, 180, 270])
                self.padding_mm = config.get("padding_mm", 2.0)
                self.num_shapes_to_impose = config.get("num_shapes_to_impose", 20)

                self.input_pdf_line.setText(self.input_pdf_path)
                self.output_pdf_line.setText(self.output_pdf_path)
                self.sheet_width_spin.setValue(self.sheet_width_mm)
                self.sheet_height_spin.setValue(self.sheet_height_mm)
                self.shape_width_spin.setValue(self.shape_width_mm)
                self.shape_height_spin.setValue(self.shape_height_mm)
                self.rotations_line.setText(", ".join(map(str, self.rotations_degrees)))
                self.padding_spin.setValue(self.padding_mm)
                self.num_shapes_spin.setValue(self.num_shapes_to_impose)

    def generate_preview(self):
        if not self.get_parameters():
            return
        if not self.input_pdf_path or not os.path.exists(self.input_pdf_path):
            QMessageBox.warning(self, "Erro", "Selecione um PDF de entrada válido.")
            return

        self.save_config()
        self.preview_widget.clear()

        # Convert mm to points
        sheet_width_pt = self.sheet_width_mm * mm
        sheet_height_pt = self.sheet_height_mm * mm
        shape_width_pt = self.shape_width_mm * mm
        shape_height_pt = self.shape_height_mm * mm
        padding_pt = self.padding_mm * mm

        # --- Lógica de Imposição para Pré-visualização ---
        shapes_to_draw = [] # List of (x, y, rotated_w, rotated_h, angle, shape_index)

        current_x = padding_pt
        current_y = padding_pt
        max_row_height = 0
        shapes_placed = 0

        while shapes_placed < self.num_shapes_to_impose:
            best_fit_rotation = None
            best_fit_width = float("inf")
            best_fit_height = float("inf")
            
            for angle in self.rotations_degrees:
                rotated_w, rotated_h = get_rotated_bbox(shape_width_pt, shape_height_pt, angle)
                
                if current_x + rotated_w + padding_pt <= sheet_width_pt:
                    if current_y + rotated_h + padding_pt <= sheet_height_pt:
                        if rotated_w * rotated_h < best_fit_width * best_fit_height:
                            best_fit_rotation = angle
                            best_fit_width = rotated_w
                            best_fit_height = rotated_h
            
            if best_fit_rotation is not None:
                rotated_w, rotated_h = get_rotated_bbox(shape_width_pt, shape_height_pt, best_fit_rotation)
                shapes_to_draw.append((current_x, current_y, rotated_w, rotated_h, best_fit_rotation, shapes_placed + 1))

                current_x += rotated_w + padding_pt
                max_row_height = max(max_row_height, rotated_h + padding_pt)
                shapes_placed += 1
            else:
                current_x = padding_pt
                current_y += max_row_height + padding_pt
                max_row_height = 0
                
                if current_y + shape_height_pt + padding_pt > sheet_height_pt:
                    # No more space on the current page, start a new page for preview
                    # For preview, we'll just show the first page for now.
                    # A full multi-page preview would be more complex.
                    break 

        # --- Renderizar Pré-visualização --- 
        # Create a QImage for the preview
        # Scale down for display if needed, but keep aspect ratio
        display_scale = 0.8 # Adjust as needed
        preview_width = int(sheet_width_pt * display_scale)
        preview_height = int(sheet_height_pt * display_scale)
        preview_image = QImage(preview_width, preview_height, QImage.Format_ARGB32)
        preview_image.fill(Qt.white) # Fill with white background

        painter = QPainter(preview_image)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw sheet border
        painter.setPen(QColor(0, 0, 0)) # Black border
        painter.drawRect(0, 0, preview_width - 1, preview_height - 1)

        # Load input PDF page as image for drawing
        try:
            input_doc = fitz.open(self.input_pdf_path)
            input_page = input_doc[0] # Get the first page
            # Render at a higher DPI for better quality, then scale down for display
            pix = input_page.get_pixmap(matrix=fitz.Matrix(2, 2)) # Render at 2x scale
            input_qimage = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888) # Convert to QImage
            input_doc.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro de Pré-visualização", f"Não foi possível carregar o PDF para pré-visualização: {e}")
            painter.end()
            return

        for x, y, rotated_w, rotated_h, angle, shape_index in shapes_to_draw:
            # Scale coordinates for display
            display_x = x * display_scale
            display_y = y * display_scale
            display_rotated_w = rotated_w * display_scale
            display_rotated_h = rotated_h * display_scale

            # Draw bounding box
            painter.setPen(QColor(255, 0, 0)) # Red bounding box
            painter.drawRect(int(display_x), int(display_y), int(display_rotated_w), int(display_rotated_h))

            # Draw the input PDF content rotated
            painter.save()
            painter.translate(display_x + display_rotated_w / 2, display_y + display_rotated_h / 2)
            painter.rotate(angle)
            
            # Scale the input QImage to fit the rotated bounding box
            # Maintain aspect ratio
            
            # Calculate scale factor to fit input_qimage into display_rotated_w x display_rotated_h
            scale_factor_w = display_rotated_w / input_qimage.width()
            scale_factor_h = display_rotated_h / input_qimage.height()
            scale_factor = min(scale_factor_w, scale_factor_h)

            target_w = int(input_qimage.width() * scale_factor)
            target_h = int(input_qimage.height() * scale_factor)

            # Center the scaled image within the rotated bounding box
            draw_x = -target_w / 2
            draw_y = -target_h / 2

            painter.drawImage(int(draw_x), int(draw_y), input_qimage.scaled(target_w, target_h, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            painter.setPen(QColor(0, 0, 255)) # Blue text
            font = QFont("Arial", 8) # Explicitly create a QFont object
            painter.setFont(font)

            # Adjust text position for approximate centering within the rotated context
            text_label = f"#{shape_index} ({angle}°)"
            text_rect = painter.fontMetrics().boundingRect(text_label)
            text_draw_x = -text_rect.width() / 2
            text_draw_y = -text_rect.height() / 2 # Center vertically

            painter.drawText(int(text_draw_x), int(text_draw_y), text_label)
            painter.restore()

        painter.end()
        self.preview_widget.setPixmap(QPixmap.fromImage(preview_image))
        self.preview_widget.setFixedSize(preview_width, preview_height)

    def generate_final_pdf(self):
        if not self.get_parameters():
            return
        if not self.input_pdf_path or not os.path.exists(self.input_pdf_path):
            QMessageBox.warning(self, "Erro", "Selecione um PDF de entrada válido.")
            return

        self.save_config()

        # Convert mm to points
        sheet_width_pt = self.sheet_width_mm * mm
        sheet_height_pt = self.sheet_height_mm * mm
        shape_width_pt = self.shape_width_mm * mm
        shape_height_pt = self.shape_height_mm * mm
        padding_pt = self.padding_mm * mm

        output_doc = fitz.open()  # Create a new empty PDF

        try:
            input_doc = fitz.open(self.input_pdf_path)
        except Exception as e:
            QMessageBox.critical(self, "Erro ao Abrir PDF", f"Não foi possível abrir o PDF de entrada: {e}")
            return

        # Get the first page of the input PDF as a template
        input_page_template = input_doc[0]

        current_x = padding_pt
        current_y = padding_pt
        max_row_height = 0
        shapes_placed = 0
        
        # Start with a blank page for the output PDF
        output_page = output_doc.new_page(width=sheet_width_pt, height=sheet_height_pt)

        while shapes_placed < self.num_shapes_to_impose:
            best_fit_rotation = None
            best_fit_width = float("inf")
            best_fit_height = float("inf")

            for angle in self.rotations_degrees:
                rotated_w, rotated_h = get_rotated_bbox(shape_width_pt, shape_height_pt, angle)
                if current_x + rotated_w + padding_pt <= sheet_width_pt and current_y + rotated_h + padding_pt <= sheet_height_pt:
                    if rotated_w * rotated_h < best_fit_width * best_fit_height:
                        best_fit_rotation = angle
                        best_fit_width = rotated_w
                        best_fit_height = rotated_h

            if best_fit_rotation is not None:
                rotated_w, rotated_h = get_rotated_bbox(shape_width_pt, shape_height_pt, best_fit_rotation)
                target_rect = fitz.Rect(current_x, current_y, current_x + rotated_w, current_y + rotated_h)

                # Correctly insert the content of the input PDF page
                # PyMuPDF's show_pdf_page is the correct method for this, ensuring source document and page number are passed.
                output_page.show_pdf_page(
                    target_rect,
                    input_doc,  # The source document (not a page object)
                    0,          # The page number in the source document (0 for the first page)
                    rotate=best_fit_rotation
                )

                # Add a text label (without the 'align' argument)
                text_label = f"#{shapes_placed + 1} ({best_fit_rotation}°)"
                # Calculate text position for approximate centering. PyMuPDF's insert_text does not have an 'align' argument.
                # We need to manually calculate the text width to center it properly.
                # For simplicity in this prototype, we'll place it at a fixed offset from the top-left of the shape.
                text_x = current_x + 5 # Small offset from left
                text_y = current_y + 15 # Small offset from top
                output_page.insert_text(fitz.Point(text_x, text_y), text_label, fontsize=6, color=(1, 0, 0))

                current_x += rotated_w + padding_pt
                max_row_height = max(max_row_height, rotated_h + padding_pt)
                shapes_placed += 1
            else:
                current_x = padding_pt
                current_y += max_row_height
                max_row_height = 0

                # Check if a new row would fit
                min_h_for_next_row = min(get_rotated_bbox(shape_width_pt, shape_height_pt, r)[1] for r in self.rotations_degrees)
                if current_y + min_h_for_next_row + padding_pt > sheet_height_pt:
                    # Not enough space for another row, create a new page
                    output_page = output_doc.new_page(width=sheet_width_pt, height=sheet_height_pt)
                    current_x = padding_pt
                    current_y = padding_pt
                    max_row_height = 0

        try:
            output_doc.save(self.output_pdf_path, garbage=4, deflate=True)
            QMessageBox.information(self, "Sucesso", f"PDF final gerado em: {self.output_pdf_path}")
        except Exception as e:
            QMessageBox.critical(self, "Erro ao Salvar PDF", f"Não foi possível salvar o PDF: {e}")
        finally:
            output_doc.close()
            input_doc.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImpositionApp()
    ex.show()
    sys.exit(app.exec_())
