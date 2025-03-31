# main.py
import sys
import webbrowser

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTextEdit, QComboBox, QPushButton, QLabel, QVBoxLayout, QLineEdit, \
    QApplication, QWidget, QDialog

from ResumeBuilder.pdf_generator import create_pdf


class LebenslaufGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.photo_path = None  # Klassenattribut zum Speichern des Foto-Pfads
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Lebenslauf-Generator")
        self.setGeometry(200, 200, 800, 600)

        # Zentrales Widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout
        self.layout = QVBoxLayout(self.central_widget)

        # Feld fuer den Namen
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Geben Sie Ihren Namen ein")
        self.layout.addWidget(self.name_input)

        # Feld fuer Berufserfahrung
        self.experience_input = QTextEdit()
        self.experience_input.setPlaceholderText("Beschreiben Sie Ihre berufliche Erfahrung")
        self.layout.addWidget(self.experience_input)

        # Feld fuer Fähigkeiten
        self.skills_input = QTextEdit()
        self.skills_input.setPlaceholderText("Geben Sie Ihre Fähigkeiten ein")
        self.layout.addWidget(self.skills_input)

        # Dropdown-Liste für Vorlagen
        self.template_selector = QComboBox()
        self.template_selector.setStyleSheet("background-color: #bfeaed; font-size: 14px; font-weight: bold;")
        self.template_selector.addItems(["Vorlage 1", "Vorlage 2", "Vorlage 3"])
        self.layout.addWidget(self.template_selector)

        # Schaltfläche zum Hochladen von Fotos
        self.photo_button = QPushButton("Foto hochladen")
        self.photo_button.setStyleSheet("background-color: #fdd9b5; font-size: 14px; font-weight: bold;")
        self.photo_button.clicked.connect(self.on_photo_upload)
        self.layout.addWidget(self.photo_button)

        # Schaltfläche zum Erstellen eines Lebenslaufs
        self.submit_button = QPushButton("Lebenslauf erstellen")
        self.submit_button.setStyleSheet("background-color: #D4E9A2; font-size: 14px; font-weight: bold;")
        self.submit_button.clicked.connect(self.on_submit)
        self.layout.addWidget(self.submit_button)

        # Schaltfläche fuer die Vorschau
        self.preview_button = QPushButton("Vorschau anzeigen")
        self.preview_button.setStyleSheet("background-color: #E9F2A2; font-size: 14px; font-weight: bold;")
        self.preview_button.clicked.connect(self.on_preview)  # Handler anschließen
        self.layout.addWidget(self.preview_button)

        # Label fuer die Anzeige von Nachrichten
        self.message_label = QLabel("")
        self.layout.addWidget(self.message_label)

    # Handler fuer die Vorschau
    def on_preview(self):
        try:
            name = self.name_input.text()
            experience = self.experience_input.toPlainText()
            skills = self.skills_input.toPlainText()

            if name and experience and skills and self.photo_path:
                # neues Fenster fuer die Vorschau
                preview_dialog = QDialog(self)
                preview_dialog.setWindowTitle("Vorschau")
                preview_dialog.setGeometry(150, 150, 600, 400)

                # QGridLayout
                dialog_layout = QGridLayout()

                # Feld zur Anzeige von Text erstellen
                preview_text = QTextEdit()
                preview_text.setReadOnly(True)
                preview_text.setText(
                    f"**Name:** {name}\n\n"
                    f"**Berufserfahrung:**\n{experience}\n\n"
                    f"**Fähigkeiten:**\n{skills}"
                )
                preview_text.setStyleSheet("font-size: 14px; padding: 10px;")
                dialog_layout.addWidget(preview_text, 0, 0, 2, 1)

                # Anzeige des Fotos
                photo_label = QLabel()
                pixmap = QPixmap(self.photo_path)
                photo_label.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio))
                photo_label.setStyleSheet("border: 2px solid gray;")
                dialog_layout.addWidget(photo_label, 0, 1, alignment=Qt.AlignRight | Qt.AlignTop)

                # Schaltfläche zum Schließen des Fensters erstellen
                close_button = QPushButton("Schließen")
                close_button.setStyleSheet("padding: 5px 15px; font-size: 12px;")
                close_button.clicked.connect(preview_dialog.close)
                dialog_layout.addWidget(close_button, 2, 1, alignment=Qt.AlignRight)

                preview_dialog.setLayout(dialog_layout)

                # Vorschau-Fenster öffnen
                preview_dialog.exec_()
            else:
                self.message_label.setStyleSheet("color: red;")
                self.message_label.setText("Bitte füllen Sie alle Felder aus und laden Sie ein Foto hoch.")
        except Exception as e:
            self.message_label.setText(f"Fehler: {str(e)}")

    def on_photo_upload(self):
        options = QFileDialog.Options()
        photo_file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Wählen Sie ein Foto",
            "",
            "Bilder (*.png *.jpg *.jpeg *.bmp);;Alle Dateien (*)",
            options=options
        )
        if photo_file_path:
            self.photo_path = photo_file_path  # Klassenattribut aktualisieren
            self.message_label.setText(f"Foto erfolgreich ausgewählt: {self.photo_path}")
            print(f"Foto wurde hochgeladen: {self.photo_path}")  # Debug-Ausgabe
        else:
            print("Foto wurde nicht ausgewählt.")  # Debug-Ausgabe

    def on_submit(self):
        print("Funktion on_submit wurde aufgerufen")  # Debug-Ausgabe

        name = self.name_input.text()
        experience = self.experience_input.toPlainText()
        skills = self.skills_input.toPlainText()
        selected_template = self.template_selector.currentText()

        # Eingabedaten überprüfen
        print(f"Name: {name}")
        print(f"Experience: {experience}")
        print(f"Skills: {skills}")
        print(f"Template: {selected_template}")
        print(f"Photo path: {self.photo_path}")  # Klassenattribut verwenden

        # Überprüfen, ob das Foto hochgeladen wurde
        if not self.photo_path:
            self.message_label.setText("Bitte laden Sie ein Foto hoch.")
            print("Fehler: Foto wurde nicht hochgeladen.")  # Debug-Ausgabe
            return

        # Rest der Funktion...
        try:
            file_name = create_pdf(name, experience, skills, selected_template, self.photo_path)
            print(f"PDF wurde erstellt: {file_name}")  # Debug-Ausgabe
            self.message_label.setText(f"Lebenslauf für {name} erfolgreich erstellt: {file_name}")
            webbrowser.open(file_name)
        except Exception as e:
            print(f"Fehler: {str(e)}")  # Debug-Ausgabe
            self.message_label.setText(f"Fehler bei der Erstellung: {str(e)}")


def run_app():
    app = QApplication(sys.argv)
    window = LebenslaufGenerator()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_app()
