import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PIL import Image
import os
from pdf2image import convert_from_path

# Developer: Obaid Med Bouslahi

class ImageConverterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Converter")
        self.setGeometry(200, 200, 400, 250)  # Adjusted window size to accommodate developer's name
        self.setWindowIcon(QIcon("icon.ico"))  # Setting the window icon

        self.initUI()

    def initUI(self):
        # Setup layout
        layout = QVBoxLayout()

        # Add label for instructions
        self.label = QLabel("Select an image and conversion format:", self)
        layout.addWidget(self.label)

        # Input field to select image
        self.input_path_field = QLineEdit(self)
        self.input_path_field.setPlaceholderText("Choose an image")
        self.input_path_field.setReadOnly(True)
        layout.addWidget(self.input_path_field)

        # Add button to select image
        self.select_button = QPushButton("Select Image", self)
        self.select_button.clicked.connect(self.select_image)
        layout.addWidget(self.select_button)

        # Dropdown list to choose conversion format
        self.format_combobox = QComboBox(self)
        self.format_combobox.addItems(["JPEG", "PNG", "GIF", "TIFF", "PDF", "EPS", "AI"])
        layout.addWidget(self.format_combobox)

        # Input field to select save path
        self.output_path_field = QLineEdit(self)
        self.output_path_field.setPlaceholderText("Choose save path")
        self.output_path_field.setReadOnly(True)
        layout.addWidget(self.output_path_field)

        # Add button to choose save path
        self.select_output_button = QPushButton("Select Save Path", self)
        self.select_output_button.clicked.connect(self.select_output_path)
        layout.addWidget(self.select_output_button)

        # Add button to convert the image
        self.convert_button = QPushButton("Convert Image", self)
        self.convert_button.clicked.connect(self.convert_image)
        layout.addWidget(self.convert_button)

        # Add developer name at the bottom of the window
        self.developer_label = QLabel("Developer: Obaid Med Bouslahi", self)
        self.developer_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.developer_label)

        # Set layout for the window
        self.setLayout(layout)

    def select_image(self):
        # Open file dialog to select an image
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Choose Image", "", "Images (*.png *.jpg *.jpeg *.gif *.tiff *.pdf *.eps *.ai *.psd *.raw)", options=options)
        if file:
            self.input_path_field.setText(file)

    def select_output_path(self):
        # Open file dialog to select save path
        options = QFileDialog.Options()
        file, _ = QFileDialog.getSaveFileName(self, "Choose Save Path", "", "All Files (*);;Images (*.png *.jpg *.jpeg *.gif *.tiff *.pdf *.eps *.ai *.psd *.raw)", options=options)
        if file:
            self.output_path_field.setText(file)

    def convert_image(self):
        input_path = self.input_path_field.text()
        output_path = self.output_path_field.text()
        output_format = self.format_combobox.currentText()

        if not input_path or not output_path:
            self.label.setText("Please select an image and save path.")
            return

        # Add appropriate extension based on the selected format
        if not output_path.lower().endswith(f".{output_format.lower()}"):
            output_path = f"{output_path}.{output_format.lower()}"

        if input_path.lower().endswith('.pdf'):
            self.convert_pdf_to_images(input_path, output_path)
        else:
            self.convert_image_file(input_path, output_path, output_format)

    def convert_image_file(self, input_path, output_path, output_format):
        try:
            with Image.open(input_path) as img:
                img.convert('RGB').save(output_path, format=output_format)
            self.label.setText(f"Image successfully converted to {output_format}!")
        except Exception as e:
            self.label.setText(f"Error: {e}")

    def convert_pdf_to_images(self, input_path, output_folder):
        try:
            images = convert_from_path(input_path)
            for i, image in enumerate(images):
                output_path = os.path.join(output_folder, f"page_{i+1}.png")
                image.save(output_path, 'PNG')
            self.label.setText(f"PDF pages saved as PNG images in {output_folder}")
        except Exception as e:
            self.label.setText(f"Error converting PDF: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageConverterApp()
    window.show()
    sys.exit(app.exec_())
