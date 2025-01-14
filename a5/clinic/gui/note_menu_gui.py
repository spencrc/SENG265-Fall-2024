from PyQt6.QtWidgets import QVBoxLayout, QGridLayout, QMenu, QAbstractItemView, QAbstractScrollArea, QPushButton, QTableView, QWidget, QDialog, QMessageBox, QPlainTextEdit
from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtCore import Qt

from clinic.note import Note

from clinic.gui.create_edit_gui import CreateEditGui
from clinic.gui.search_note_gui import SearchNoteGUI

class NoteMenuGUI(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Medical Clinic System - Notes")
        self.resize(400, 300)
        self.target_code = None

        #note text box
        self.text_box = QPlainTextEdit()
        self.text_box.setReadOnly(True)
        self.last_refresh_func = self.refresh
        self.last_refresh_arg = None

        # Add buttons for actions
        create_button = QPushButton("Create Note")
        create_button.clicked.connect(self.create_note) # add this method
        refresh_button = QPushButton("List All Notes")
        refresh_button.clicked.connect(self.refresh)
        search_button = QPushButton("Search for Note") # in a QPlainTextEdit widget
        search_button.clicked.connect(self.search_note)
        clear_button = QPushButton("Clear Notes")
        clear_button.clicked.connect(self.clear)
        update_button = QPushButton("Update Note")
        update_button.clicked.connect(self.update_note)
        delete_button = QPushButton("Delete Note")
        delete_button.clicked.connect(self.delete_note)

        layout = QVBoxLayout()     
        layout.addWidget(self.text_box)

        layout2 = QGridLayout()
        layout2.addWidget(create_button, 0, 0)
        layout2.addWidget(update_button, 1, 0)
        layout2.addWidget(refresh_button, 2, 0)
        layout2.addWidget(search_button, 0, 1)
        layout2.addWidget(delete_button, 1, 1)
        layout2.addWidget(clear_button, 2, 1)

        layout.addLayout(layout2)

        self.setLayout(layout)
        self.refresh()

    # def contextMenuEvent(self, event):
    #     # Context menu for right-click actions
    #     selected_indexes = self.note_table.selectionModel().selectedRows() #gets currently selected boxes
    #     if len(selected_indexes) > 0: #if no boxes selected, dont pop up with context menu
    #         self.menu = QMenu(self)

    #         editAction = QAction('Edit Note', self)
    #         editAction.triggered.connect(self.edit_selected_note)
    #         self.menu.addAction(editAction)

    #         deleteAction = QAction('Delete Note', self)
    #         deleteAction.triggered.connect(self.delete_selected_note) # add this to init
    #         self.menu.addAction(deleteAction)

    #         # add other required actions
    #         self.menu.popup(QCursor.pos()) #puts menu at cursor position

    def refresh(self):
        # Refreshes data in the note table
        # self.note_model.refresh_data()
        # self.note_table.setEnabled(True)
        self.clear()
        notes = self.controller.list_notes()
        for note in notes:
            self.text_box.insertPlainText(str(note)+"\n")
        self.last_refresh_func = self.refresh
        self.last_refresh_arg = None

    def create_note(self):
        # Opens the create_edit_gui to create a new note
        self.create_edit_gui = CreateEditGui(self, "Note")
        self.create_edit_gui.show()
    
    def search_note(self, action_after_search="none"):
        # Opens the search_note_gui to search for a note by either code or text
        self.search_note_gui = SearchNoteGUI(self, action_after_search)
        self.setEnabled(False)
        self.search_note_gui.show()

    def refresh_by_search(self, code):
        self.clear()
        note = self.controller.search_note(code)
        self.text_box.insertPlainText(str(note)+"\n")
        self.last_refresh_func = self.refresh_by_search
        self.last_refresh_arg = code

    def refresh_by_retrieve(self, keyword):
        self.clear()
        notes = self.controller.retrieve_notes(keyword)
        for note in notes:
            self.text_box.insertPlainText(str(note)+"\n")
        self.last_refresh_func = self.refresh_by_retrieve
        self.last_refresh_arg = keyword

    def update_note(self):
        # Opens create_edit_gui to edit the selected note
        self.search_note(action_after_search="update")

    def delete_note(self):
        # Opens the delete_gui to delete the selected note
        self.search_note(action_after_search="delete")

    def clear(self):
        self.text_box.clear()

    def redo_refresh(self):
        if self.last_refresh_arg:
            self.last_refresh_func(self.last_refresh_arg)
        else:
            self.last_refresh_func()

    def closeEvent(self, event):
        self.controller.unset_current_patient()
        self = None