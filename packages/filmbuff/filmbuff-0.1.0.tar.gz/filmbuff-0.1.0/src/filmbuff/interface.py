"""Provide a graphic user interface.

Copyright (C) 2021 emerac

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
import csv
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, cast

from PyQt5.QtCore import (
    QCoreApplication,
    QModelIndex,
    QSettings,
    QStandardPaths,
    Qt,
)
from PyQt5.QtGui import (
    QCloseEvent,
    QCursor,
    QKeyEvent,
    QIcon,
    QKeySequence,
    QResizeEvent,
    QShowEvent,
)
from PyQt5.QtSql import (
    QSqlDatabase,
    QSqlQuery,
    QSqlRecord,
    QSqlTableModel,
)
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QCheckBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QStatusBar,
    QTableView,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from filmbuff import metadata
from filmbuff import tablequery


logger = logging.getLogger(__name__)


class FileDialog(QFileDialog):
    """A configurable QFileDialog for user-filesystem interaction.

    Intended use cases include: asking the user which file to open and
    asking the user under which name and location they would like to
    save a file.

    """

    def __init__(self, **kwargs: Any) -> None:
        """Construct a FileDialog instance.

        Parameters
        ----------
        **kwargs
            A dictionary of FileDialog options.
            Each key corresponds to a QFileDialog method with that key's
            value being directly forwarded to the corresponding method.
            The key's and their corresponding methods are listed below:
                parent - __init__
                path - setDirectory
                file_mode - setFileMode
                accept_mode - setAcceptMode
                name_filter - setNameFilter
                options - setOptions

        Returns
        -------
        None

        """
        super().__init__(kwargs.get("parent"))
        self.setWindowModality(Qt.WindowModal)
        if kwargs.get("path") is not None:
            self.setDirectory(kwargs["path"])
        if kwargs.get("file_mode") is not None:
            self.setFileMode(kwargs["file_mode"])
        if kwargs.get("accept_mode") is not None:
            self.setAcceptMode(kwargs["accept_mode"])
        if kwargs.get("name_filter") is not None:
            self.setNameFilter(kwargs["name_filter"])
        if kwargs.get("options") is not None:
            self.setOptions(kwargs["options"])


class Interface(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("filmbuff")
        self.setWindowIcon(QIcon.fromTheme("x-office-spreadsheet"))

        QCoreApplication.setOrganizationName("filmbuff")
        QCoreApplication.setApplicationName("filmbuff")
        self.settings = QSettings()
        self.data_path = self.make_data_path()

        recent_files = self.settings.value("recent_files")
        if recent_files is None or not recent_files[-1].exists():
            self.con_name = "virtual_1"
            open_db(self.con_name, ":memory:")
            create_empty_table(self.con_name)
            self.set_window_title()
        else:
            self.con_name = "physical_1"
            open_db(self.con_name, str(recent_files[-1]))
            self.set_window_title()

        self._configure_model()
        self._configure_view()
        self._configure_header()
        self._configure_actions()
        self._configure_menubar()
        self._configure_toolbar()
        self._configure_header_context()

        self.statusbar = StatusBar(5000, self)
        self.setStatusBar(self.statusbar)

        self.update_recent_files_menu()

        self.setCentralWidget(self.view)

        self.resize_and_center()

        self.model.select()

        self.metadata_window: Optional[metadata.MetadataWindow] = None

    def closeEvent(self, event: QCloseEvent) -> None:
        super().closeEvent(event)
        self.save_window_geometry()
        self.save_header_state()

        if not self.is_state_resolved():
            event.ignore()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        mod = cast(Qt.KeyboardModifier, event.modifiers())
        if mod == Qt.ControlModifier and event.key() == Qt.Key_F:
            self.searchbar.setFocus()

        if self.view.hasFocus() and event.key() == Qt.Key_Return:
            current_row = self.view.currentIndex().row()
            max_row = self.model.rowCount() - 1
            first_visible = 0
            for visual_index in range(self.header.count()):
                logical_index = self.header.logicalIndex(visual_index)
                if self.model.headerData(logical_index, Qt.Horizontal) == "ID":
                    continue
                if not self.header.isSectionHidden(logical_index):
                    first_visible = self.header.logicalIndex(visual_index)
                    break

            if current_row == max_row:
                new_index = self.model.createIndex(0, first_visible)
                self.view.setCurrentIndex(new_index)
            else:
                new_index = self.model.createIndex(
                    current_row + 1,
                    first_visible,
                )
                self.view.setCurrentIndex(new_index)
            current_row = self.view.currentIndex().row()
            assert 0 <= current_row <= max_row

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        if self.width() > 900:
            self.spacer.setSizePolicy(
                QSizePolicy.Expanding,
                QSizePolicy.Preferred,
            )
            self.searchbar.setMinimumWidth(570)
        else:
            self.spacer.setSizePolicy(
                QSizePolicy.Minimum,
                QSizePolicy.Preferred,
            )
            self.searchbar.setMinimumWidth(0)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self.save_default_window_geometry()
        self.save_default_header_state()
        self.load_settings()
        self.set_header_check_states()

        status = f"All records displayed ({self.model.rowCount()})."
        self.statusbar.showMessage(status, self.statusbar.timeout)

    def data_export(self) -> None:
        dialog = FileDialog(
            parent=self,
            path=str(self.data_path),
            file_mode=QFileDialog.AnyFile,
            accept_mode=QFileDialog.AcceptSave,
            options=QFileDialog.DontConfirmOverwrite,
        )
        if not dialog.exec() == QDialog.Accepted:
            return
        save_path = dialog.selectedFiles()[0]

        if not save_path.endswith(".tsv"):
            save_path += ".tsv"

        if Path(save_path).exists():
            overwrite_dialog = MessageDialog(
                parent=self,
                icon=QMessageBox.Icon.Question,
                title="file conflict",
                text=(
                    f"A file named '{Path(save_path).name}' already exists in "
                    f"'{Path(save_path).parent.name}'.\n"
                    f"Would you like to overwrite '{Path(save_path).name}'?"
                ),
                info="The overwritten file will not be recoverable.",
                details=f"Full path of conflicting file:\n{save_path}",
                buttons=(QMessageBox.No | QMessageBox.Yes),
                default=QMessageBox.No,
            )
            if not overwrite_dialog.exec() == QMessageBox.Yes:
                status = "Export cancelled."
                self.statusbar.showMessage(status, self.statusbar.timeout)
                return
            else:
                Path(save_path).unlink()

        with open(save_path, "w", newline='') as tsv_file:
            tsv_writer = csv.writer(
                tsv_file,
                delimiter="\t",
                quotechar="|",
                quoting=csv.QUOTE_MINIMAL,
            )
            for row_index in range(self.model.rowCount()):
                record_data = []
                record = self.model.record(row_index)
                for column_index in range(record.count()):
                    record_data.append(record.value(column_index))
                tsv_writer.writerow(record_data)

        status = f"Successfully exported current sheet to '{save_path}'."
        self.statusbar.showMessage(status, self.statusbar.timeout)

    def data_import(self) -> None:
        dialog = FileDialog(
            parent=self,
            path=str(self.data_path),
            file_mode=QFileDialog.ExistingFile,
            accept_mode=QFileDialog.AcceptOpen,
            name_filter="Tab-separated value (*.tsv)",
        )
        if not dialog.exec() == QDialog.Accepted:
            return
        open_path = dialog.selectedFiles()[0]

        with open(open_path, newline="") as tsv_file:
            tsv_reader = csv.reader(
                tsv_file,
                delimiter="\t",
                quotechar="|",
            )
            row_count = 0
            for row in tsv_reader:
                record = self.model.record(-1)
                for index, item in enumerate(row):
                    if record.fieldName(index) == "id":
                        continue
                    record.setValue(index, item)
                self.model.insertRecord(-1, record)
                row_count += 1

        status = f"Import successful. {row_count} rows inserted."
        self.statusbar.showMessage(status, self.statusbar.timeout)

    def filter_view(self) -> None:
        self.model.setFilter("")
        self.model.select()

        query = self.searchbar.text()
        try:
            sql_string = tablequery.main(query, self.headers)
        except ValueError:
            dialog = MessageDialog(
                parent=self,
                icon=QMessageBox.Icon.Warning,
                title="search error",
                text="Invalid search syntax.".ljust(85),
                info=(
                    "Please check for typos or missing quotes.\n"
                    "For search syntax help, view the 'Help - Help' menu."
                ),
                buttons=QMessageBox.Ok,
            )
            dialog.exec()
            self.model.setFilter("")
            self.model.select()

            status = f"All records displayed ({self.model.rowCount()})."
            self.statusbar.showMessage(status, self.statusbar.timeout)
        else:
            self.model.setFilter(sql_string)
            self.model.select()

            status = f"Search results found ({self.model.rowCount()})."
            self.statusbar.showMessage(status, self.statusbar.timeout)

    def handle_transition(self, old_con_name: str) -> None:
        self.set_window_title()

        old_con = QSqlDatabase.database(old_con_name)
        old_con.close()
        assert old_con.isOpen() is False

        self._configure_model()
        self.view.setModel(self.model)

        self.update_recent_files()
        self.update_recent_files_menu()

    def insert_rows(
        self,
        checked: bool,
        record: Optional[QSqlRecord] = None,
    ) -> None:
        del checked  # Provided with signal, but is not useful.
        # The primeInsert signal that is emitted by insertRecord does
        # not contain row ID information because the row has not been
        # fully initialized in the database yet.
        # To work around this, block signals until the record is fully
        # initialized, then manually emit the signal so the row ID can
        # be obtained (necessary for undo/redo).
        self.model.blockSignals(True)
        if record is None:
            self.model.insertRecord(-1, self.model.record(-1))
        else:
            self.model.insertRecord(-1, record)
        self.model.blockSignals(False)
        self.model.select()

        row_ids = {}
        for index in range(self.model.rowCount()):
            row_ids[self.model.record(index).value("id")] = index
        new_index = row_ids[max(row_ids.keys())]
        new_record = self.model.record(new_index)
        self.model.primeInsert.emit(new_index, new_record)  # type: ignore

        if self.settings.value("table/scroll_to_inserted") == "0":
            pass
        else:
            self.make_row_visible(new_index)
            self.view.selectRow(new_index)

        status = f"Row inserted at row {new_index + 1}."
        self.statusbar.showMessage(status, self.statusbar.timeout)

    def is_state_resolved(self) -> bool:
        db_name = QSqlDatabase.database(self.con_name).databaseName()

        if (
            (db_name == ":memory:" and self.model.rowCount() > 0)
            or self.model.isDirty() is True
        ):
            dialog = MessageDialog(
                parent=self,
                icon=QMessageBox.Icon.Question,
                title="save changes",
                text="Would you like to save changes before closing?",
                info="Unsaved changes will be lost after closing.",
                buttons=(
                    QMessageBox.Discard |
                    QMessageBox.Cancel |
                    QMessageBox.Save
                ),
                default=QMessageBox.Cancel,
            )
            choice = dialog.exec()
        else:
            return True

        if db_name == ":memory:" and choice == QMessageBox.Save:
            self.save_as()
            return True
        elif self.model.isDirty() is True and choice == QMessageBox.Save:
            self.save_model()
            return True
        elif choice == QMessageBox.Discard:
            return True
        else:
            return False

    def load_settings(self) -> None:
        window_geometry = self.settings.value("window/geometry")
        if window_geometry is not None:
            self.restoreGeometry(window_geometry)

        header_state = self.settings.value("header/state")
        if header_state is not None:
            self.header.restoreState(header_state)
            self.view.updateGeometries()

        statusbar_state = self.settings.value("statusbar/visible")
        if statusbar_state is None or statusbar_state == "1":
            self.statusbar.setVisible(True)
        else:
            self.statusbar.setVisible(False)

    def make_row_visible(self, row_index: int) -> None:
        for visual_index in range(self.model.columnCount()):
            logical_index = self.header.logicalIndex(visual_index)
            if not self.header.isSectionHidden(logical_index):
                first_visible = logical_index
                break
        self.view.scrollTo(self.model.createIndex(row_index, first_visible))

    def new_sheet(self) -> None:
        if not self.is_state_resolved():
            return

        old_con_name = self.con_name
        self.set_new_connection_name("virtual")
        open_db(self.con_name, ":memory:")
        create_empty_table(self.con_name)

        self.handle_transition(old_con_name)

        status = "Opened new sheet."
        self.statusbar.showMessage(status, self.statusbar.timeout)

    def open_recent_file(self, db_path: str) -> None:
        if not self.is_state_resolved():
            return

        if not Path(db_path).exists():
            MessageDialog(
                parent=self,
                icon=QMessageBox.Icon.Warning,
                title="open recent file error",
                text=(
                    "The file could not be opened because it has\n"
                    "either been moved or deleted."
                ),
                details=f"Full path of the original file:\n{db_path}",
                buttons=QMessageBox.Ok,
            ).exec()
            return

        old_con_name = self.con_name
        self.set_new_connection_name("physical")
        open_db(self.con_name, db_path)

        self.handle_transition(old_con_name)

        status = f"Opened '{db_path}'."
        self.statusbar.showMessage(status, self.statusbar.timeout)

    def open_sheet(self) -> None:
        if not self.is_state_resolved():
            return
        dialog = FileDialog(
            parent=self,
            path=str(self.data_path),
            file_mode=QFileDialog.ExistingFile,
            accept_mode=QFileDialog.AcceptOpen,
            name_filter="SQLite3 database (*.sqlite)",
        )
        if not dialog.exec() == QDialog.Accepted:
            return
        open_path = dialog.selectedFiles()[0]

        old_con_name = self.con_name
        self.set_new_connection_name("physical")
        open_db(self.con_name, open_path)

        self.handle_transition(old_con_name)

        status = f"Opened '{open_path}'."
        self.statusbar.showMessage(status, self.statusbar.timeout)

    def perform_redo(self) -> None:
        if not self.model.redo_stack:
            return

        redo_info = self.model.redo_stack.pop()
        if redo_info["command"] == "deletion":
            for row in range(self.model.rowCount()):
                if self.model.record(row).value("id") == redo_info["row_id"]:
                    old_record = cast(QSqlRecord, redo_info["record"])
                    updated_record = self.update_record(
                        old_record,
                        self.model.record(row),
                    )
                    redo_info["record"] = updated_record
                    self.model.undo_stack.append(redo_info)

                    self.model.blockSignals(True)
                    self.model.removeRows(row, 1)
                    self.model.blockSignals(False)

                    status = "Redid row deletion."
                    self.statusbar.showMessage(status, self.statusbar.timeout)
        if redo_info["command"] == "insertion":
            self.model.blockSignals(True)
            record = cast(QSqlRecord, redo_info["record"])
            self.model.insertRecord(-1, record)
            self.model.blockSignals(False)

            new_id = self.model.record(self.model.rowCount() - 1).value("id")
            redo_info["row_id"] = new_id
            self.model.undo_stack.append(redo_info)

            status = "Redid row insertion."
            self.statusbar.showMessage(status, self.statusbar.timeout)
        self.model.select()
        self.toggle_undo_enable()
        self.toggle_redo_enable()

    def perform_undo(self) -> None:
        if not self.model.undo_stack:
            return

        undo_info = self.model.undo_stack.pop()
        if undo_info["command"] == "deletion":
            self.model.blockSignals(True)
            record = cast(QSqlRecord, undo_info["record"])
            self.model.insertRecord(-1, record)
            self.model.blockSignals(False)

            new_id = self.model.record(self.model.rowCount() - 1).value("id")
            undo_info["row_id"] = new_id
            self.model.redo_stack.append(undo_info)

            status = "Undid row deletion."
            self.statusbar.showMessage(status, self.statusbar.timeout)
        if undo_info["command"] == "insertion":
            for row in range(self.model.rowCount()):
                if self.model.record(row).value("id") == undo_info["row_id"]:
                    old_record = cast(QSqlRecord, undo_info["record"])
                    updated_record = self.update_record(
                        old_record,
                        self.model.record(row),
                    )
                    undo_info["record"] = updated_record
                    self.model.redo_stack.append(undo_info)

                    self.model.blockSignals(True)
                    self.model.removeRows(row, 1)
                    self.model.blockSignals(False)

                    status = "Undid row insertion."
                    self.statusbar.showMessage(status, self.statusbar.timeout)
        self.model.select()
        self.toggle_undo_enable()
        self.toggle_redo_enable()

    def remove_rows(self) -> None:
        removed_indexes = []
        for qt_index in self.view.selectedIndexes():
            if qt_index.row() not in removed_indexes:
                self.model.removeRows(qt_index.row(), 1)
                removed_indexes.append(qt_index.row())
        self.model.select()

        removed_rows = [index + 1 for index in removed_indexes]
        if len(removed_rows) == 1:
            status = f"Row {removed_rows[0]} removed."
        elif len(removed_rows) > 1:
            removed_rows.sort()
            min_row = removed_rows[0]
            max_row = removed_rows[-1]
            if removed_rows == [i for i in range(min_row, max_row + 1)]:
                status = f"Rows {min_row}-{max_row} removed."
            else:
                formatted = ", ".join([str(i) for i in removed_rows])
                status = f"Rows {formatted} removed."
        else:
            status = "No rows removed. At least one row must be selected."
        self.statusbar.showMessage(status, self.statusbar.timeout)

    def reset_filter(self, current_text: str) -> None:
        if current_text == "":
            self.model.setFilter("")
            self.model.select()

            status = f"All records displayed ({self.model.rowCount()})."
            self.statusbar.showMessage(status, self.statusbar.timeout)

    def resize_and_center(self) -> None:
        app = QApplication.instance()
        if app is not None:
            screen = app.primaryScreen()
        else:
            return

        screen_width = screen.availableGeometry().width()
        screen_height = screen.availableGeometry().height()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.resize(window_width, window_height)

        screen_center = screen.geometry().center()
        frame_center = self.frameGeometry().center()
        self.move(screen_center - frame_center)

    def restore_default_header_state(self) -> None:
        header_default_state = self.settings.value("header/default_state")
        if header_default_state is not None:
            self.header.restoreState(header_default_state)
            self.view.updateGeometries()
            self.set_header_check_states()

            status = "Default column configuration restored."
            self.statusbar.showMessage(status, self.statusbar.timeout)

    def restore_default_window_geometry(self) -> None:
        window_geometry = self.settings.value("window/default_geometry")
        if window_geometry is not None:
            self.restoreGeometry(window_geometry)

            status = "Default window configuration restored."
            self.statusbar.showMessage(status, self.statusbar.timeout)

    def restore_header_state(self) -> None:
        header_state = self.settings.value("header/state")
        if header_state is not None:
            self.header.restoreState(header_state)
            self.view.updateGeometries()

    def retrieve_metadata(self) -> None:
        if self.metadata_window is None:
            self.metadata_window = metadata.MetadataWindow(self)
        else:
            self.metadata_window.activateWindow()
        self.metadata_window.show()

    def save_as(self) -> None:
        dialog = FileDialog(
            parent=self,
            path=str(self.data_path),
            file_mode=QFileDialog.AnyFile,
            accept_mode=QFileDialog.AcceptSave,
            options=QFileDialog.DontConfirmOverwrite,
        )
        if not dialog.exec() == QDialog.Accepted:
            return
        save_path = dialog.selectedFiles()[0]

        # setDefaultSuffix is used, but it is not functioning.
        # https://bugreports.qt.io/browse/QTBUG-20011
        if not save_path.endswith(".sqlite"):
            save_path += ".sqlite"

        if Path(save_path).exists():
            overwrite_dialog = MessageDialog(
                parent=self,
                icon=QMessageBox.Icon.Question,
                title="file conflict",
                text=(
                    f"A file named '{Path(save_path).name}' already exists in "
                    f"'{Path(save_path).parent.name}'.\n"
                    f"Would you like to overwrite '{Path(save_path).name}'?"
                ),
                info="The overwritten file will not be recoverable.",
                details=f"Full path of conflicting file:\n{save_path}",
                buttons=(QMessageBox.No | QMessageBox.Yes),
                default=QMessageBox.No,
            )
            if not overwrite_dialog.exec() == QMessageBox.Yes:
                status = "Save cancelled."
                self.statusbar.showMessage(status, self.statusbar.timeout)
                return
            else:
                Path(save_path).unlink()

        current_db_name = QSqlDatabase.database(self.con_name).databaseName()
        if save_path == current_db_name:
            MessageDialog(
                parent=self,
                icon=QMessageBox.Icon.Warning,
                title="save error",
                text="The file that is currently open cannot be overwritten.",
                info="Please save to a different file name.",
                buttons=QMessageBox.Ok,
            ).exec()
            status = "Save cancelled."
            self.statusbar.showMessage(status, self.statusbar.timeout)
            return

        old_con_name = self.con_name
        self.set_new_connection_name("physical")
        open_db(self.con_name, save_path)

        create_empty_table(self.con_name)
        copy_all_data(old_con_name, self.con_name)

        self.handle_transition(old_con_name)

        status = f"Saved file as '{save_path}'."
        self.statusbar.showMessage(status, self.statusbar.timeout)

    def save_default_header_state(self) -> None:
        header_state = self.header.saveState()
        self.settings.setValue("header/default_state", header_state)

    def save_default_window_geometry(self) -> None:
        window_geometry = self.saveGeometry()
        self.settings.setValue("window/default_geometry", window_geometry)

    def save_header_state(self) -> None:
        header_state = self.header.saveState()
        self.settings.setValue("header/state", header_state)

    def save_model(self) -> None:
        if QSqlDatabase.database(self.con_name).databaseName() == ":memory:":
            self.save_as()
        else:
            self.model.submitAll()
            self.model.select()

            db_path = QSqlDatabase.database(self.con_name).databaseName()
            status = f"Saved current file '{db_path}'."
            self.statusbar.showMessage(status, self.statusbar.timeout)

    def save_window_geometry(self) -> None:
        window_geometry = self.saveGeometry()
        self.settings.setValue("window/geometry", window_geometry)

    def set_header_check_states(self) -> None:
        for index, context_action in enumerate(self.header_context_actions):
            if not self.header.isSectionHidden(index):
                context_action.setChecked(True)
            else:
                context_action.setChecked(False)

    def set_new_connection_name(self, con_type: str) -> None:
        con_names = QSqlDatabase.database().connectionNames()
        sep_con_names = list(
            filter(
                lambda s: s.startswith("{}_".format(con_type)),
                con_names,
            ),
        )
        if sep_con_names:
            con_numbers = [int(s[s.index("_") + 1:]) for s in sep_con_names]
            self.con_name = "{}_{}".format(con_type, max(con_numbers) + 1)
        else:
            self.con_name = "{}_1".format(con_type)

    def set_optimal_widths(self) -> None:
        self.header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.view.updateGeometries()
        self.header.setSectionResizeMode(QHeaderView.Interactive)

        status = "Columns resized to optimal widths."
        self.statusbar.showMessage(status, self.statusbar.timeout)

    def set_preferences(self) -> None:
        dialog = PreferencesDialog(self)
        if dialog.exec():
            scroll = dialog.scroll_checkbox.isChecked()
            if scroll:
                self.settings.setValue("table/scroll_to_inserted", "1")
            else:
                self.settings.setValue("table/scroll_to_inserted", "0")

            duration = dialog.duration_spinbox.value() * 1000
            self.statusbar.timeout = duration
            self.settings.setValue("statusbar/duration", duration)

            visible = dialog.visible_checkbox.isChecked()
            self.statusbar.setVisible(visible)
            if visible is True:
                self.settings.setValue("statusbar/visible", "1")
            else:
                self.settings.setValue("statusbar/visible", "0")
            status = "Preferences saved."
        else:
            status = "Preferences not saved."
        self.statusbar.showMessage(status, self.statusbar.timeout)

    def set_window_title(self) -> None:
        con = QSqlDatabase.database(self.con_name)
        db_name = con.databaseName()
        if db_name == ":memory:":
            self.setWindowTitle("New - filmbuff")
        else:
            self.setWindowTitle("{} - filmbuff".format(Path(db_name).stem))

    def toggle_header_visibility(self, logical_index: int) -> None:
        header_name = self.model.headerData(logical_index, Qt.Horizontal)
        if self.header.isSectionHidden(logical_index):
            self.header.showSection(logical_index)
            status = f"Column '{header_name}' is now shown."
            self.statusbar.showMessage(status, self.statusbar.timeout)
        else:
            self.header.hideSection(logical_index)
            status = f"Column '{header_name}' is now hidden."
            self.statusbar.showMessage(status, self.statusbar.timeout)

    def update_recent_files(self) -> None:
        db_path = Path(QSqlDatabase.database(self.con_name).databaseName())

        recent_files = self.settings.value("recent_files")
        if recent_files is None:
            recent_files = []

        if str(db_path) == ":memory:":
            return
        elif db_path in recent_files:
            del recent_files[recent_files.index(db_path)]
            recent_files.append(db_path)
        else:
            recent_files.append(db_path)

        if len(recent_files) > 6:
            recent_files.pop(0)

        self.settings.setValue("recent_files", recent_files)

    def update_recent_files_menu(self) -> None:
        recent_files = self.settings.value("recent_files")
        if recent_files is None:
            return

        self.recent_files_actions = []
        # The last file in the list is the current file (not displayed).
        for index in range(len(recent_files) - 2, -1, -1):
            self.recent_file_action = QAction()
            self.recent_file_action.setText(str(recent_files[index].name))
            self.recent_file_action.triggered.connect(
                lambda _, i=index: self.open_recent_file(str(recent_files[i])),
            )
            self.recent_files_menu.addAction(self.recent_file_action)
            self.recent_files_actions.append(self.recent_file_action)

    def update_undo_stack(self, description: str, index: int) -> None:
        if description == "deletion":
            undo_info = {
                "command": "deletion",
                "record": self.model.record(index),
                "row_id": self.model.record(index).value("id"),
            }
            self.model.undo_stack.append(undo_info)
        if description == "insertion":
            undo_info = {
                "command": "insertion",
                "record": self.model.record(index),
                "row_id": self.model.record(index).value("id"),
            }
            self.model.undo_stack.append(undo_info)

        self.toggle_undo_enable()
        self.toggle_redo_enable()

    def toggle_redo_enable(self) -> None:
        if self.model.redo_stack:
            self.redo_action.setEnabled(True)
        else:
            self.redo_action.setEnabled(False)

    def toggle_undo_enable(self) -> None:
        if self.model.undo_stack:
            self.undo_action.setEnabled(True)
        else:
            self.undo_action.setEnabled(False)

    @staticmethod
    def make_data_path() -> Path:
        """Ensure a standard location to store data exists.

        Parameters
        ----------
        None

        Returns
        -------
        :obj:`pathlib.Path`
            The standard location for storing persistent data.

        """
        path_enum = QStandardPaths.GenericDataLocation
        parent_path = Path(QStandardPaths.writableLocation(path_enum))
        data_path = parent_path / QCoreApplication.applicationName()
        data_path.mkdir(exist_ok=True)
        return data_path

    @staticmethod
    def update_record(outdated: QSqlRecord, updated: QSqlRecord) -> QSqlRecord:
        """Update a record's fields to match another record's field.

        Parameters
        ----------
        outdated
            The record to update.
        updated
            The record containing the desired values.

        Returns
        -------
        :obj:`PyQt5.QtQSql.QSqlRecord`
            The outdated record with all fields (except 'ID') updated.

        Notes
        -----
        The 'ID' field is not updated because it is automatically
        generated by the database.

        """
        # Overwriting the old record with the new record makes it not
        # able to be inserted. Instead, make the old record contain the
        # same information as the new record.
        for column_index in range(updated.count()):
            if updated.fieldName(column_index) == "ID":
                continue
            outdated.setValue(column_index, updated.value(column_index))
        return outdated

    def _configure_actions(self) -> None:
        self.restore_window_action = QAction()
        self.restore_window_action.setText("Window configuration")
        self.restore_window_action.triggered.connect(
            self.restore_default_window_geometry,
        )

        self.restore_header_action = QAction()
        self.restore_header_action.setText("Column configuration")
        self.restore_header_action.triggered.connect(
            self.restore_default_header_state,
        )

        self.header_context_actions = []
        for index, header in enumerate(self.headers.keys()):
            self.header_context_action = QAction()
            self.header_context_action.setCheckable(True)
            self.header_context_action.setText(header)
            self.header_context_action.triggered.connect(
                lambda check_state, i=index: self.toggle_header_visibility(i),
            )
            self.header_context_actions.append(self.header_context_action)

        self.optimal_widths_action = QAction()
        self.optimal_widths_action.setText("Optimal widths")
        self.optimal_widths_action.triggered.connect(self.set_optimal_widths)

        self.new_action = QAction()
        self.new_action.setText("New")
        self.new_action.setIcon(QIcon.fromTheme("document-new"))
        self.new_action.setShortcut(QKeySequence("Ctrl+n"))
        self.new_action.triggered.connect(self.new_sheet)

        self.open_action = QAction()
        self.open_action.setText("Open...")
        self.open_action.setIcon(QIcon.fromTheme("document-open"))
        self.open_action.setShortcut(QKeySequence("Ctrl+o"))
        self.open_action.triggered.connect(self.open_sheet)

        self.save_action = QAction()
        self.save_action.setText("Save")
        self.save_action.setIcon(QIcon.fromTheme("document-save"))
        self.save_action.setShortcut(QKeySequence("Ctrl+s"))
        self.save_action.triggered.connect(self.save_model)

        self.save_as_action = QAction()
        self.save_as_action.setText("Save as...")
        self.save_as_action.setIcon(QIcon.fromTheme("document-save-as"))
        self.save_as_action.setShortcut(QKeySequence("Shift+Ctrl+s"))
        self.save_as_action.triggered.connect(self.save_as)

        self.import_action = QAction()
        self.import_action.setText("Import tsv...")
        self.import_action.triggered.connect(self.data_import)

        self.export_action = QAction()
        self.export_action.setText("Export tsv...")
        self.export_action.triggered.connect(self.data_export)

        self.exit_action = QAction()
        self.exit_action.setText("Exit")
        self.exit_action.setShortcut(QKeySequence("Ctrl+q"))
        self.exit_action.triggered.connect(self.close)

        self.undo_action: QAction = QAction()
        self.undo_action.setText("Undo")
        self.undo_action.setIcon(QIcon.fromTheme("edit-undo"))
        self.undo_action.setShortcut(QKeySequence("Ctrl+z"))
        self.undo_action.triggered.connect(self.perform_undo)
        self.toggle_undo_enable()

        self.redo_action: QAction = QAction()
        self.redo_action.setText("Redo")
        self.redo_action.setIcon(QIcon.fromTheme("edit-redo"))
        self.redo_action.setShortcut(QKeySequence("Ctrl+y"))
        self.redo_action.triggered.connect(self.perform_redo)
        self.toggle_redo_enable()

        self.add_action = QAction()
        self.add_action.setText("Add row")
        self.add_action.setIcon(QIcon.fromTheme("list-add"))
        self.add_action.setShortcut(QKeySequence("Ctrl++"))
        self.add_action.triggered.connect(self.insert_rows)

        self.remove_action = QAction()
        self.remove_action.setText("Remove selected row(s)")
        self.remove_action.setIcon(QIcon.fromTheme("list-remove"))
        self.remove_action.setShortcut(QKeySequence("Ctrl+-"))
        self.remove_action.triggered.connect(self.remove_rows)

        self.preferences_action = QAction()
        self.preferences_action.setText("Preferences...")
        self.preferences_action.triggered.connect(self.set_preferences)

        self.help_action = QAction()
        self.help_action.setText("Help")
        self.help_action.setShortcut(QKeySequence("F1"))

        self.about_action = QAction()
        self.about_action.setText("About")

        self.search_action = QAction()
        self.search_action.setText("Search")
        self.search_action.setIcon(QIcon.fromTheme("system-search"))
        self.search_action.triggered.connect(self.filter_view)

        self.metadata_action = QAction()
        self.metadata_action.setText("Retrieve metadata")
        self.metadata_action.setIcon(QIcon.fromTheme("applications-internet"))
        self.metadata_action.setShortcut(QKeySequence("Ctrl+m"))
        self.metadata_action.triggered.connect(self.retrieve_metadata)

    def _configure_header(self) -> None:
        self.header: QHeaderView = self.view.horizontalHeader()
        self.header.setContextMenuPolicy(Qt.CustomContextMenu)
        self.header.setSortIndicatorShown(True)
        self.header.setSectionsMovable(True)

        self.header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.header.setStretchLastSection(True)

        self.header.setSectionResizeMode(QHeaderView.Interactive)

    def _configure_header_context(self) -> None:
        self.header_context = QMenu(self)
        self.header_context.addAction(self.optimal_widths_action)
        self.header_context.addSeparator()
        self.header.customContextMenuRequested.connect(
            lambda: self.header_context.exec(QCursor.pos()),
        )
        for context_action in self.header_context_actions:
            self.header_context.addAction(context_action)

    def _configure_menubar(self) -> None:
        self.menubar = self.menuBar()
        self.menubar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setMenuBar(self.menubar)

        self.file_menu = self.menubar.addMenu("&File")
        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.open_action)
        self.recent_files_menu: QMenu = self.file_menu.addMenu("Recent files")
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.save_as_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.import_action)
        self.file_menu.addAction(self.export_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)

        self.edit_menu = self.menubar.addMenu("&Edit")
        self.edit_menu.addAction(self.undo_action)
        self.edit_menu.addAction(self.redo_action)

        self.sheet_menu = self.menubar.addMenu("&Sheet")
        self.sheet_menu.addAction(self.add_action)
        self.sheet_menu.addAction(self.remove_action)

        self.view_menu = self.menubar.addMenu("&View")
        self.view_resize_menu = self.view_menu.addMenu("Resize columns")
        self.view_resize_menu.addAction(self.optimal_widths_action)
        self.view_menu.addSeparator()
        self.view_columns_menu = self.view_menu.addMenu("Show/hide columns")
        for action in self.header_context_actions:
            self.view_columns_menu.addAction(action)
        self.view_menu.addSeparator()
        self.view_defaults_menu = self.view_menu.addMenu("Restore defaults")
        self.view_defaults_menu.addAction(self.restore_header_action)
        self.view_defaults_menu.addAction(self.restore_window_action)

        self.tools_menu = self.menubar.addMenu("&Tools")
        self.tools_menu.addAction(self.preferences_action)

        self.help_menu = self.menubar.addMenu("&Help")
        self.help_menu.addAction(self.help_action)
        self.help_menu.addSeparator()
        self.help_menu.addAction(self.about_action)

    def _configure_model(self) -> None:
        self.model = Model(QSqlDatabase.database(self.con_name), self)
        self.headers = {}
        for index in range(self.model.columnCount()):
            model_header = self.model.headerData(index, Qt.Horizontal)

            display_header = model_header.replace("_", " ")
            if "id" in display_header.lower():
                display_header = display_header.upper()
            else:
                display_header = display_header.capitalize()

            self.headers[display_header] = model_header
            self.model.setHeaderData(index, Qt.Horizontal, display_header)
        self.model.select()

    def _configure_toolbar(self) -> None:
        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.searchbar = QLineEdit()
        self.searchbar.setClearButtonEnabled(True)
        self.searchbar.setPlaceholderText(
            "Type here and press enter to search...",
        )
        self.searchbar.returnPressed.connect(self.filter_view)
        self.searchbar.textChanged.connect(self.reset_filter)

        self.toolbar = QToolBar()
        self.toolbar.setFloatable(False)
        self.addToolBar(self.toolbar)
        self.toolbar.setMovable(False)
        self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)

        self.toolbar.addAction(self.new_action)
        self.toolbar.addAction(self.open_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.save_action)
        self.toolbar.addAction(self.save_as_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.undo_action)
        self.toolbar.addAction(self.redo_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.add_action)
        self.toolbar.addAction(self.remove_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.metadata_action)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.spacer)
        self.toolbar.addWidget(self.searchbar)
        self.toolbar.addAction(self.search_action)

    def _configure_view(self) -> None:
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.setAlternatingRowColors(True)
        self.view.setSortingEnabled(True)


class MessageDialog(QMessageBox):
    """A configurable QMessageBox for user interaction.

    Intended use cases include: notifying the user of an error, asking
    the user for a decision, etc.

    """

    def __init__(self, **kwargs: Any) -> None:
        """Construct a MessageDialog instance.

        Parameters
        ----------
        **kwargs
            A dictionary of QMessageBox options.
            Each key corresponds to a QMessageBox method with that key's
            value being directly forwarded to the corresponding method.
            The key's and their corresponding methods are listed below:
                parent - __init__
                icon - setIcon
                title - setWindowTitle
                text - setText
                info - setInformativeText
                details - setDetailedText
                buttons - setStandardButtons
                default - setDefaultButton


        Returns
        -------
        None

        """
        super().__init__(kwargs.get("parent"))
        if kwargs.get("icon") is not None:
            self.setIcon(kwargs["icon"])
        if kwargs.get("title") is not None:
            self.setWindowTitle(f"filmbuff - {kwargs['title']}")
        if kwargs.get("text") is not None:
            self.setText(kwargs["text"])
        if kwargs.get("info") is not None:
            self.setInformativeText(kwargs["info"])
        if kwargs.get("details") is not None:
            self.setDetailedText(kwargs["details"])
        if kwargs.get("buttons") is not None:
            self.setStandardButtons(kwargs["buttons"])
        if kwargs.get("default") is not None:
            self.setDefaultButton(kwargs["default"])


class Model(QSqlTableModel):
    def __init__(self, db: QSqlDatabase, parent: QMainWindow) -> None:
        super().__init__(parent, db)
        self.setTable("films")
        self.setEditStrategy(self.OnRowChange)
        self.undo_stack: List[Dict[str, Union[str, QSqlRecord, int]]] = []
        self.redo_stack: List[Dict[str, Union[str, QSqlRecord, int]]] = []

        self.beforeDelete.connect(  # type: ignore
            lambda row: parent.update_undo_stack("deletion", row),
        )
        self.primeInsert.connect(  # type: ignore
            lambda row, record: parent.update_undo_stack("insertion", row),
        )

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        flags: int = 0
        if index.column() == 10:
            flags = Qt.ItemIsSelectable
        else:
            flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        return cast(Qt.ItemFlags, flags)


class PreferencesDialog(QDialog):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)
        self.setWindowTitle("Preferences")

        table_label = QLabel("Table")
        table_label.setStyleSheet(
            "font-weight: bold; text-decoration: underline;",
        )
        self.scroll_checkbox = QCheckBox()
        scroll = parent.settings.value("table/scroll_to_inserted")
        if scroll == "0":
            self.scroll_checkbox.setChecked(False)
        else:
            self.scroll_checkbox.setChecked(True)

        statusbar_label = QLabel("Statusbar")
        statusbar_label.setStyleSheet(
            "font-weight: bold; text-decoration: underline;",
        )

        self.visible_checkbox = QCheckBox()
        visible = parent.settings.value("statusbar/visible")
        if visible == "0":
            self.visible_checkbox.setChecked(False)
        else:
            self.visible_checkbox.setChecked(True)

        self.duration_spinbox = QSpinBox()
        duration = parent.settings.value("statusbar/duration")
        if duration is not None:
            formatted_duration = int(int(duration) / 1000)
            self.duration_spinbox.setValue(formatted_duration)
        else:
            formatted_duration = int(parent.statusbar.timeout / 1000)
            self.duration_spinbox.setValue(formatted_duration)
        self.duration_spinbox.setSuffix(" s")

        form_layout = QFormLayout()
        form_layout.addRow(table_label)
        form_layout.addRow("Scroll to inserted rows:", self.scroll_checkbox)
        form_layout.addRow(statusbar_label)
        form_layout.addRow("Statusbar is visible:", self.visible_checkbox)
        form_layout.addRow("Message duration:", self.duration_spinbox)

        apply_button = QPushButton("Apply")
        apply_button.pressed.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.pressed.connect(self.reject)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(apply_button)
        buttons_layout.addWidget(cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)


class StatusBar(QStatusBar):
    def __init__(self, timeout: int, parent: QMainWindow) -> None:
        super().__init__(parent)
        self.setSizeGripEnabled(False)
        duration = parent.settings.value("statusbar/duration")
        if duration is not None:
            self.timeout = int(duration)
        else:
            self.timeout = timeout

    def showMessage(self, message: str, timeout: int = 0) -> None:
        super().showMessage(message, self.timeout)


def copy_all_data(con1_name: str, con2_name: str) -> None:
    """Copy all data from one QSQLite database to another.

    Parameters
    ----------
    con1_name
        The name of the source QSQLite database connection.
    con2_name
        The name of the destination QSQLite database connection.

    Returns
    -------
    None

    """
    con2 = QSqlDatabase.database(con2_name)
    db2_insertion = QSqlQuery(con2)
    db2_insertion.prepare(
        """
        INSERT INTO films (
            budget,
            cast_one,
            cast_two,
            cast_three,
            color,
            content,
            director,
            genre_one,
            genre_two,
            genre_three,
            imdb_id,
            notes,
            original_language,
            original_title,
            overview,
            popularity,
            production_country,
            release_date,
            revenue,
            runtime,
            spoken_language,
            status,
            tagline,
            title,
            tmdb_id,
            vote_average,
            vote_count
        )
        VALUES (
            :budget,
            :cast_one,
            :cast_two,
            :cast_three,
            :color,
            :content,
            :director,
            :genre_one,
            :genre_two,
            :genre_three,
            :imdb_id,
            :notes,
            :original_language,
            :original_title,
            :overview,
            :popularity,
            :production_country,
            :release_date,
            :revenue,
            :runtime,
            :spoken_language,
            :status,
            :tagline,
            :title,
            :tmdb_id,
            :vote_average,
            :vote_count
        )
        """
    )
    db1_selection = select_all_data(con1_name)
    while db1_selection.next():
        for column_index in range(db1_selection.record().count()):
            if not db1_selection.record().fieldName(column_index) == "id":
                db2_insertion.addBindValue(db1_selection.value(column_index))
        db2_insertion.exec()
    db1_selection.finish()
    db2_insertion.finish()


def create_empty_table(con_name: str) -> None:
    """Create a table in a QSQLite database for storing film info.

    Parameters
    ----------
    con_name
        The name of a QSQLite database connection.

    Returns
    -------
    None

    """
    con = QSqlDatabase.database(con_name)
    query = QSqlQuery(con)
    query.exec(
        """
        CREATE TABLE films (
            budget INTEGER,
            cast_one TEXT,
            cast_two TEXT,
            cast_three TEXT,
            color TEXT,
            content TEXT,
            director TEXT,
            genre_one TEXT,
            genre_two TEXT,
            genre_three TEXT,
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            imdb_id TEXT,
            notes TEXT,
            original_language TEXT,
            original_title TEXT,
            overview TEXT,
            popularity REAL,
            production_country TEXT,
            release_date TEXT,
            revenue INTEGER,
            runtime INTEGER,
            spoken_language TEXT,
            status TEXT,
            tagline TEXT,
            title TEXT,
            tmdb_id INTEGER,
            vote_average REAL,
            vote_count INTEGER
        )
        """
    )
    query.finish()


def open_db(con_name: str, db_name: str) -> bool:
    """Create a QSQLite database connection.

    Parameters
    ----------
    con_name
        The name of the QSQLite database connection to create.
    db_name
        The name (path) of the database to open.
        If ':memory:' is received, the database will be opened in-
        memory. If the name (path) provided does not exist, a disk-based
        database will be created in that location.

    Returns
    -------
    bool
        True if the connection is successfully opened, False if not.

    """
    con = QSqlDatabase.addDatabase("QSQLITE", con_name)
    con.setDatabaseName(db_name)
    if not con.open():
        MessageDialog(
            icon=QMessageBox.Icon.Warning,
            title="database error",
            text="An error occurred while opening the database.",
            info="The application will launch without an open database.",
            details=f"Error report:\n{con.lastError().databaseText()}",
            buttons=QMessageBox.Ok,
        ).exec()
        return False
    return True


def select_all_data(con_name: str) -> QSqlQuery:
    """Select all of the film information stored in a QSQLite database.

    Parameters
    ----------
    con_name
        The name of a QSQLite database connection.

    Returns
    -------
    :obj:`QSqlQuery`
        A query containing all of the information in the database.

    """
    con = QSqlDatabase.database(con_name)
    query = QSqlQuery(con)
    query.exec(
        """
        SELECT
            budget,
            cast_one,
            cast_two,
            cast_three,
            color,
            content,
            director,
            genre_one,
            genre_two,
            genre_three,
            id,
            imdb_id,
            notes,
            original_language,
            original_title,
            overview,
            popularity,
            production_country,
            release_date,
            revenue,
            runtime,
            spoken_language,
            status,
            tagline,
            title,
            tmdb_id,
            vote_average,
            vote_count
        FROM films
        ORDER BY id ASC
        """
    )
    return query


def main(argv: Optional[List[str]] = None) -> None:
    """Run the application's main graphic user interface.

    Parameters
    ----------
    argv
        An optional list of arguments to pass to QApplication.

    Returns
    -------
    None

    """
    app = QApplication([] if argv is None else argv)
    window = Interface()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
