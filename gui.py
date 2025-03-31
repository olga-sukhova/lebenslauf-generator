# gui.py
import sys
import webbrowser
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, \
    QDialog, QComboBox

from pdf_generator import create_pdf
from PyQt5.QtWidgets import QFileDialog  # Для выбора файлов

def run_app():
    # app erstellen
    app = QApplication(sys.argv)

    # Hauptfenster erstellen
    window = QMainWindow()
    window.setWindowTitle("Lebenslauf-Generator")
    window.setGeometry(200, 200, 800, 600)      # Fenstergroeße und Anfangsposition festlegen
    # Fenster-Icon festlegen

    window.setWindowIcon(QIcon('assets/icons/cv3.ico'))  # Используем прямые слэши

    # Zentral-Widget erstellen
    central_widget = QWidget(window)
    central_widget.setStyleSheet("background-color: #DFE9F2;")
    window.setCentralWidget(central_widget)   # Zentral-Widget, das in der Mitte des Fensters platziert wird

    # Layout erstellen
    # Wie die Interface-Elemente (Schaltflächen, Textfelder usw.) im Fenster oder Container platziert werden
    layout = QVBoxLayout()                    # Vertical Box Layout

    # Eingabefeld fuer den Namen
    name_input = QLineEdit()                  # Einzeiliges Textfeld
    name_input.setPlaceholderText("Geben Sie Ihren Namen ein")
    name_input.setStyleSheet("""
        background-color: #DFE9F2;
        border: 3px solid #9BC1F2;
        border-radius: 3px;
        font-size: 14px;
    """)
    layout.addWidget(name_input)              # Hinzufügen dieser Widgets zum Layout

    # Eingabefeld fuer Berufserfahrung
    experience_input = QTextEdit()
    experience_input.setPlaceholderText("Beschreiben Sie Ihre berufliche Erfahrung")
    experience_input.setStyleSheet("""
        background-color: #DFE9F2;
        border: 3px solid #9BC1F2;
        border-radius: 3px;
        font-size: 14px;
    """)
    layout.addWidget(experience_input)

    # Eingabefeld fuer Fähigkeiten
    skills_input = QTextEdit()
    skills_input.setPlaceholderText("Geben Sie Ihre Fähigkeiten ein (z.B. Python, SQL, Kommunikation)")
    skills_input.setStyleSheet("""
        background-color: #DFE9F2;
        border: 3px solid #9BC1F2;
        border-radius: 3px;
        font-size: 14px;
    """)
    layout.addWidget(skills_input)
    # Label über der Dropdown-Liste hinzufügen
    template_label = QLabel("Wählen Sie eine Vorlage aus:")
    template_label.setStyleSheet("""
        font-size: 12px;
        font-weight: bold;
        color: #333333;
    """)
    layout.addWidget(template_label)
    # Dropdown-Liste zur Auswahl der Vorlage
    template_selector = QComboBox()
    template_selector.addItems(["Vorlage 1", "Vorlage 2", "Vorlage 3"])
    template_selector.setStyleSheet("""
        background-color: #DFE9F2;
        border: 2px solid #9BC1F2;
        border-radius: 5px;
        font-size: 14px;
        font-weight: normal;
        padding: 5px;
    """)
    layout.addWidget(template_selector)
    # Schaltfläche zum Hochladen eines Fotos
    photo_button = QPushButton("Foto hochladen")  # Кнопка "Загрузить фото"
    photo_button.setStyleSheet("background-color: #F2D5CE; font-size: 14px; font-weight: bold;")
    layout.addWidget(photo_button)

    # Schaltfläche zum Erstellen des Lebenslaufs
    submit_button = QPushButton("Lebenslauf erstellen")
    submit_button.setStyleSheet("background-color: #B5B4D9; font-size: 14px; font-weight: bold;")  # Применяем стили
    layout.addWidget(submit_button)

    # Schaltfläche zum Speichern der Daten
    save_button = QPushButton("Speichern")
    save_button.setStyleSheet("background-color: #F2D5CE; font-size: 14px; font-weight: bold;")  # Применяем стили
    layout.addWidget(save_button)

    # Schaltfläche für die Vorschau
    preview_button = QPushButton("Vorschau anzeigen")
    preview_button.setStyleSheet("background-color: #E9F2A2; font-size: 14px; font-weight: bold;")  # Применяем стили
    layout.addWidget(preview_button)

    # Schaltfläche für die Vorschau
    message_label = QLabel("")
    layout.addWidget(message_label)

    # photo_path = None
    # Handler für die Schaltflaeche hinzufuegen -> oeffnet den Dateiauswahldialog und speichert den Pfad zum ausgewaehlten Bild
    def on_photo_upload():
        global photo_path  # Globale Variable
        options = QFileDialog.Options()
        photo_file_path, _ = QFileDialog.getOpenFileName(
            None,
            "Wählen Sie ein Foto",
            "",
            "Bilder (*.png *.jpg *.jpeg *.bmp);;Alle Dateien (*)",
            options=options
        )
        if photo_file_path:
            photo_path = photo_file_path
            message_label.setText(f"Foto erfolgreich ausgewählt: {photo_path}")
            print(f"Foto hochgeladen: {photo_path}")  # Debug-Ausgabe
        else:
            print("Foto nicht ausgewählt.")  # Debug-Ausgabe

    photo_button.clicked.connect(on_photo_upload)

    # Handler zum Erstellen des Lebenslaufs -> Beim Klicken auf die Schaltfläche wird eine PDF generiert
    def on_submit():
        print("Funktion on_submit aufgerufen")  # Debug-Ausgabe

        name = name_input.text()
        experience = experience_input.toPlainText()
        skills = skills_input.toPlainText()
        selected_template = template_selector.currentText()

        # Eingabedaten überprüfen
        print(f"Name: {name}")
        print(f"Experience: {experience}")
        print(f"Skills: {skills}")
        print(f"Template: {selected_template}")
        print(f"Photo path: {photo_path}")  # Отладочный вывод

        # Überprüfen, ob das Foto hochgeladen wurde
        if not photo_path:
            message_label.setText("Bitte laden Sie ein Foto hoch.")
            print("Fehler: Foto wurde nicht hochgeladen.")  # Debug-Ausgabe
            return
###################################
        name = name_input.text()  # name
        experience = experience_input.toPlainText()  # Berufserfahrung
        skills = skills_input.toPlainText()  # Fähigkeiten
        selected_template = template_selector.currentText()  # Получаем выбранный шаблон

        # Проверяем, загружено ли фото
        if not photo_path:
            message_label.setText("Bitte laden Sie ein Foto hoch.")
            return

        # Проверяем, заполнены ли все поля
        if name and experience and skills:
            try:
                # Создание PDF-файла
                file_name = create_pdf(name, experience, skills, selected_template, photo_path)
                message_label.setText(f"Lebenslauf für {name} erfolgreich erstellt: {file_name}")

                # Открытие созданного PDF-файла с помощью webbrowser
                webbrowser.open(file_name)

            except Exception as e:
                # Обработка ошибок
                message_label.setText(f"Fehler bei der Erstellung: {str(e)}")
                print(f"Error: {str(e)}")
        else:
            message_label.setText("Bitte füllen Sie alle Felder aus.")

    submit_button.clicked.connect(on_submit)

    # Обработчик для сохранения данных
    def on_save():
        name = name_input.text()
        experience = experience_input.toPlainText()
        skills = skills_input.toPlainText()

        if name and experience and skills:
            file_name = f"{name}_data.txt"
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(f"Name: {name}\n")
                file.write(f"Berufserfahrung:\n{experience}\n")
                file.write(f"Fähigkeiten:\n{skills}\n")
            message_label.setText(f"Daten wurden in die Datei gespeichert: {file_name}")
        else:
            message_label.setText("Bitte füllen Sie alle Felder aus.")

    save_button.clicked.connect(on_save)

    # Обработчик для предварительного просмотра
    def on_preview():
            try:
                name = name_input.text()
                experience = experience_input.toPlainText()
                skills = skills_input.toPlainText()

                if name and experience and skills:
                    # Создаём новое окно для предварительного просмотра
                    preview_dialog = QDialog()
                    preview_dialog.setWindowTitle("Vorschau")
                    preview_dialog.setGeometry(150, 150, 400, 300)

                    dialog_layout = QVBoxLayout()

                    # Поле для отображения данных
                    preview_text = QTextEdit()
                    preview_text.setReadOnly(True)  # Поле только для чтения
                    preview_text.setText(
                        f"Name: {name}\n\n"
                        f"Berufserfahrung:\n{experience}\n\n"
                        f"Fähigkeiten: \n{skills}"
                    )
                    dialog_layout.addWidget(preview_text)

                    # Кнопка закрытия окна
                    close_button = QPushButton("Schließen")
                    close_button.clicked.connect(preview_dialog.close)
                    dialog_layout.addWidget(close_button)

                    preview_dialog.setLayout(dialog_layout)

                    # Открываем окно предварительного просмотра
                    preview_dialog.exec_()

                else:
                    # Вывод сообщения об ошибке
                    message_label.setText("Bitte füllen Sie alle Felder aus.")

            except Exception as e:
                # Выводим сообщение о любой возникшей ошибке
                message_label.setText(f"Fehler: {str(e)}")

    preview_button.clicked.connect(on_preview)

    # Устанавливаем layout в центральный виджет
    central_widget.setLayout(layout)


    # Показываем главное окно
    window.show()

    # Запускаем цикл обработки событий
    sys.exit(app.exec_())