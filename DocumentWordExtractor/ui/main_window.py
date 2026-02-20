"""Main application window."""

import webbrowser
from pathlib import Path

import requests
from PySide6.QtCore import Qt, Slot, QThread, Signal, QSettings, QEvent, QObject
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QToolBar,
    QPushButton,
    QPlainTextEdit,
    QListWidget,
    QListWidgetItem,
    QStatusBar,
    QSplitter,
    QFrame,
    QLabel,
    QFileDialog,
    QMessageBox,
    QStackedWidget,
    QSizePolicy,
    QApplication,
    QProgressBar,
)

from readers.document_factory import DocumentFactory
from processors.word_extractor import WordExtractor
from exporters.excel_exporter import ExcelExporter
from utils.styles import DARK_THEME, LIGHT_THEME


class FileLoadWorker(QThread):
    """Background worker for loading documents without blocking the UI."""

    finished = Signal(object, str)  # (file_path, text)
    error = Signal(str)

    def __init__(self, file_path: Path, parent=None):
        super().__init__(parent)
        self._file_path = file_path

    def run(self):
        try:
            reader = DocumentFactory.get_reader(self._file_path)
            if not reader:
                self.error.emit(f"Unsupported format: {self._file_path.suffix}")
                return
            text = reader.read(self._file_path)
            self.finished.emit(self._file_path, text)
        except Exception as e:
            self.error.emit(str(e))


GITHUB_API = "https://api.github.com/repos/Abdusalom0v/PDF-Word-/releases/latest"


class UpdateCheckWorker(QThread):
    """Background worker for checking GitHub releases."""

    finished = Signal(str | None, str | None)  # (latest_version, download_url) or (None, error_msg)
    error = Signal(str)

    def run(self):
        try:
            response = requests.get(GITHUB_API, timeout=5)
            response.raise_for_status()
            release = response.json()
            version = release.get("tag_name", "").lstrip("v")
            assets = release.get("assets", [])
            url = assets[0]["browser_download_url"] if assets else ""
            self.finished.emit(version, url)
        except Exception as e:
            self.finished.emit(None, str(e))


class DropFilter(QObject):
    """Event filter that accepts file drops and forwards to a callback."""

    def __init__(self, on_file_dropped):
        super().__init__()
        self._on_file_dropped = on_file_dropped

    def eventFilter(self, obj, event):
        if event.type() == QEvent.DragEnter:
            if event.mimeData().hasUrls():
                urls = event.mimeData().urls()
                if urls and urls[0].isLocalFile():
                    path = Path(urls[0].toLocalFile())
                    if path.suffix.lower() in (".pdf", ".docx", ".txt"):
                        event.acceptProposedAction()
                        return True
        elif event.type() == QEvent.Drop:
            urls = event.mimeData().urls()
            if urls and urls[0].isLocalFile():
                path = Path(urls[0].toLocalFile())
                if path.is_file() and path.suffix.lower() in (".pdf", ".docx", ".txt"):
                    event.acceptProposedAction()
                    self._on_file_dropped(path)
                    return True
        return super().eventFilter(obj, event)


class DocumentViewer(QPlainTextEdit):
    """Custom text viewer that emits a signal when mouse selection is finished."""

    selectionFinished = Signal()

    def mouseReleaseEvent(self, event):
        """Emit selectionFinished only after the mouse button is released."""
        super().mouseReleaseEvent(event)
        self.selectionFinished.emit()


class PhraseListWidget(QListWidget):
    """List widget that supports deleting items with the Delete key."""

    deletePressed = Signal()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            self.deletePressed.emit()
        else:
            super().keyPressEvent(event)


class MainWindow(QMainWindow):
    """Main application window with document viewer and word selection."""

    def __init__(self) -> None:
        super().__init__()
        self._current_file: Path | None = None
        self._all_words: list[str] = []
        self._selected_words: list[str] = []
        self._load_worker: FileLoadWorker | None = None
        self._update_worker: UpdateCheckWorker | None = None
        self._update_download_url: str = ""
        self._update_latest_version: str = ""
        self._settings = QSettings("DocumentWordExtractor", "DocumentWordExtractor")
        self._dark_theme = self._settings.value("darkTheme", True, type=bool)
        self._setup_ui()
        self._connect_signals()
        self._apply_theme()

    def _setup_ui(self) -> None:
        """Initialize the user interface."""
        self.setWindowTitle("Document Word Extractor")
        self.setMinimumSize(800, 500)
        self.resize(1200, 750)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(1)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)

        # Document viewer area
        viewer_container = QWidget()
        viewer_container.setMinimumWidth(300)
        viewer_layout = QVBoxLayout(viewer_container)
        viewer_layout.setContentsMargins(12, 12, 6, 12)

        # Stacked widget: document viewer + loading overlay
        self._viewer_stack = QStackedWidget()
        self._viewer_stack.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )

        self._document_viewer = DocumentViewer()
        self._document_viewer.setPlaceholderText(
            "Open a document or drag and drop a file here..."
        )
        self._document_viewer.setReadOnly(True)
        self._viewer_stack.addWidget(self._document_viewer)

        # Loading overlay
        loading_frame = QFrame()
        loading_frame.setObjectName("loadingOverlay")
        loading_layout = QVBoxLayout(loading_frame)
        loading_layout.setAlignment(Qt.AlignCenter)
        loading_layout.setSpacing(12)
        self._loading_label = QLabel("Loading document...")
        self._loading_label.setObjectName("loadingLabel")
        loading_layout.addWidget(self._loading_label)
        self._loading_bar = QProgressBar()
        self._loading_bar.setRange(0, 0)  # Indeterminate
        self._loading_bar.setFixedWidth(200)
        loading_layout.addWidget(self._loading_bar, 0, Qt.AlignHCenter)
        self._viewer_stack.addWidget(loading_frame)

        viewer_layout.addWidget(self._viewer_stack)
        splitter.addWidget(viewer_container)

        # Right panel - Selected words
        words_panel = QFrame()
        words_panel.setObjectName("wordsPanel")
        words_panel.setMinimumWidth(220)
        words_panel.setMaximumWidth(380)
        words_panel.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding,
        )
        words_layout = QVBoxLayout(words_panel)
        words_layout.setContentsMargins(12, 12, 12, 12)
        words_layout.setSpacing(8)

        panel_title = QLabel("Selected Words")
        panel_title.setObjectName("panelTitle")
        words_layout.addWidget(panel_title)

        self._words_list = PhraseListWidget()
        self._words_list.setSelectionMode(QListWidget.ExtendedSelection)
        self._words_list.setDragDropMode(QListWidget.NoDragDrop)
        self._words_list.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )
        words_layout.addWidget(self._words_list)

        remove_selected_btn = QPushButton("Remove Selected")
        remove_selected_btn.setObjectName("removeSelectedButton")
        remove_selected_btn.clicked.connect(self._on_remove_selected_words)
        words_layout.addWidget(remove_selected_btn)

        clear_all_btn = QPushButton("Clear All")
        clear_all_btn.setObjectName("clearAllButton")
        clear_all_btn.clicked.connect(self._on_clear_all_words)
        words_layout.addWidget(clear_all_btn)

        splitter.addWidget(words_panel)

        splitter.setSizes([700, 300])
        layout.addWidget(splitter)

        # Install drop filter on widgets that can receive drops
        drop_filter = DropFilter(self._load_file_sync)
        for w in (central, splitter, viewer_container, self._document_viewer, words_panel, self._words_list):
            w.setAcceptDrops(True)
            w.installEventFilter(drop_filter)
        self._drop_filter = drop_filter  # Keep reference

        self._create_toolbar()
        self._create_status_bar()

    def _create_toolbar(self) -> None:
        """Create the main toolbar."""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        open_btn = QPushButton("Open File")
        open_btn.setObjectName("openButton")
        open_btn.clicked.connect(self._on_open_file)
        toolbar.addWidget(open_btn)

        select_all_btn = QPushButton("Select All Words")
        select_all_btn.setObjectName("selectAllButton")
        select_all_btn.clicked.connect(self._on_select_all_words)
        toolbar.addWidget(select_all_btn)

        export_btn = QPushButton("Export to Excel")
        export_btn.setObjectName("exportButton")
        export_btn.clicked.connect(self._on_export_excel)
        toolbar.addWidget(export_btn)

        toolbar.addSeparator()

        # Theme toggle
        self._theme_btn = QPushButton("☀ Light")
        self._theme_btn.setObjectName("themeButton")
        self._theme_btn.setToolTip("Switch between dark and light theme")
        self._theme_btn.clicked.connect(self._toggle_theme)
        toolbar.addWidget(self._theme_btn)

        toolbar.addSeparator()

        # Update check / Install button
        self._update_btn = QPushButton("Check for Update")
        self._update_btn.setObjectName("updateButton")
        self._update_btn.setToolTip("Check for new version")
        self._update_btn.clicked.connect(self._on_update_button_clicked)
        toolbar.addWidget(self._update_btn)

        self._open_btn = open_btn
        self._select_all_btn = select_all_btn
        self._export_btn = export_btn
        self._export_btn.setEnabled(False)

    def _create_status_bar(self) -> None:
        """Create the status bar."""
        self._status_bar = QStatusBar()
        self.setStatusBar(self._status_bar)
        self._status_file = QLabel("No file loaded")
        self._status_counter = QLabel("Selected: 0")
        self._status_bar.addWidget(self._status_file, 1)
        self._status_bar.addPermanentWidget(self._status_counter)

    def _connect_signals(self) -> None:
        """Connect widget signals."""
        self._document_viewer.selectionFinished.connect(self._on_selection_finished)
        self._words_list.itemSelectionChanged.connect(
            self._on_word_list_selection_changed
        )
        self._words_list.itemDoubleClicked.connect(self._on_word_double_clicked)
        self._words_list.deletePressed.connect(self._on_remove_selected_words)

    def _apply_theme(self) -> None:
        """Apply the current theme."""
        stylesheet = DARK_THEME if self._dark_theme else LIGHT_THEME
        self.setStyleSheet(stylesheet)
        self._theme_btn.setText("☀ Light" if self._dark_theme else "☽ Dark")

    def _toggle_theme(self) -> None:
        """Toggle between dark and light theme."""
        self._dark_theme = not self._dark_theme
        self._settings.setValue("darkTheme", self._dark_theme)
        self._apply_theme()

    def _on_update_button_clicked(self) -> None:
        """Handle update button click: Check for update or Install."""
        if self._update_download_url:
            # Currently showing Install - open download URL
            webbrowser.open(self._update_download_url)
            self._update_download_url = ""
            self._update_latest_version = ""
            self._update_btn.setText("Check for Update")
            self._update_btn.setToolTip("Check for new version")
            return
        self._start_update_check()

    def _start_update_check(self) -> None:
        """Start background update check."""
        if self._update_worker and self._update_worker.isRunning():
            return
        self._update_btn.setText("Checking...")
        self._update_btn.setEnabled(False)
        self._update_worker = UpdateCheckWorker(self)
        self._update_worker.finished.connect(self._on_update_check_finished)
        self._update_worker.start()

    def _on_update_check_finished(self, latest_version: str | None, result: str | None) -> None:
        """Handle update check result."""
        self._update_worker = None
        self._update_btn.setEnabled(True)
        current = QApplication.applicationVersion()
        if latest_version is not None and result:
            # Success: new version available
            if latest_version != current:
                self._update_download_url = result
                self._update_latest_version = latest_version
                self._update_btn.setText(f"Install v{latest_version}")
                self._update_btn.setToolTip(f"Download version {latest_version}")
                QMessageBox.information(
                    self,
                    "Update Available",
                    f"New version v{latest_version} is available.\nClick 'Install' to download.",
                )
            else:
                self._update_btn.setText("Check for Update")
                QMessageBox.information(
                    self,
                    "Up to Date",
                    "You are using the latest version.",
                )
        else:
            # Error
            self._update_btn.setText("Check for Update")
            QMessageBox.warning(
                self,
                "Update Check Failed",
                f"Could not check for updates.\n{result or 'Unknown error'}",
            )

    def _show_loading(self, message: str = "Loading document...") -> None:
        """Show the loading overlay."""
        self._loading_label.setText(message)
        self._viewer_stack.setCurrentIndex(1)
        self._open_btn.setEnabled(False)
        QApplication.processEvents()

    def _hide_loading(self) -> None:
        """Hide the loading overlay."""
        self._viewer_stack.setCurrentIndex(0)
        self._open_btn.setEnabled(True)

    def _load_file_sync(self, file_path: Path) -> None:
        """Load a file in the main thread (used for drop/open)."""
        self._show_loading()
        worker = FileLoadWorker(file_path, self)
        worker.finished.connect(self._on_file_loaded)
        worker.error.connect(self._on_load_error)
        worker.finished.connect(worker.deleteLater)
        worker.error.connect(worker.deleteLater)
        worker.start()
        self._load_worker = worker

    def _on_file_loaded(self, file_path: Path, text: str) -> None:
        """Handle successful file load."""
        self._hide_loading()
        self._load_worker = None
        self._current_file = file_path
        self._document_viewer.setPlainText(text)
        self._all_words = WordExtractor.extract_unique_words(text)
        self._selected_words = []
        self._update_words_list()
        self._status_file.setText(file_path.name)
        self._export_btn.setEnabled(True)

    def _on_load_error(self, error_msg: str) -> None:
        """Handle file load error."""
        self._hide_loading()
        self._load_worker = None
        if "Unsupported format" in error_msg:
            QMessageBox.warning(
                self,
                "Unsupported Format",
                f"Cannot open file.\nSupported: .pdf, .docx, .txt",
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to read file. The file may be corrupted or invalid.\n\n{error_msg}",
            )

    def _update_words_list(self) -> None:
        """Refresh the selected phrases list from current selection."""
        self._words_list.clear()
        for phrase in self._selected_words:
            self._words_list.addItem(QListWidgetItem(phrase))
        self._status_counter.setText(f"Selected: {len(self._selected_words)}")

    def _extract_selected_phrase(self) -> None:
        """
        Extract the current text selection as a single normalized phrase
        and add it to the list if valid.

        Rules:
        - Use QTextCursor.selectedText()
        - Replace unicode line separators (\u2029) with space
        - Trim leading/trailing whitespace
        - Collapse multiple spaces into one
        - Ignore selections shorter than 2 characters
        - Prevent duplicates (case-insensitive)
        """
        cursor = self._document_viewer.textCursor()
        if not cursor.hasSelection():
            return

        raw_text = cursor.selectedText()
        if not raw_text:
            return

        # Normalize multi-line selections and whitespace
        normalized = raw_text.replace("\u2029", " ")
        normalized = " ".join(normalized.split())

        # Ignore very short selections
        if len(normalized) < 2:
            return

        # Prevent duplicates (case-insensitive)
        lower_existing = {p.lower() for p in self._selected_words}
        if normalized.lower() in lower_existing:
            return

        self._selected_words.append(normalized)
        self._update_words_list()

    @Slot()
    def _on_selection_finished(self) -> None:
        """Handle text selection completion in document viewer (on mouse release)."""
        self._extract_selected_phrase()

    def _on_word_list_selection_changed(self) -> None:
        """Handle selection change in words list - update counter if needed."""
        self._status_counter.setText(f"Selected: {len(self._selected_words)}")

    @Slot()
    def _on_remove_selected_words(self) -> None:
        """Remove currently selected item(s) from the words list."""
        selected = self._words_list.selectedItems()
        if not selected:
            return
        indices = sorted(
            (self._words_list.row(item) for item in selected),
            reverse=True,
        )
        for i in indices:
            if 0 <= i < len(self._selected_words):
                del self._selected_words[i]
        self._update_words_list()

    @Slot()
    def _on_clear_all_words(self) -> None:
        """Clear all stored phrases."""
        if not self._selected_words:
            return
        self._selected_words.clear()
        self._update_words_list()

    @Slot(QListWidgetItem)
    def _on_word_double_clicked(self, item: QListWidgetItem) -> None:
        """Remove the double-clicked word from the list."""
        row = self._words_list.row(item)
        if 0 <= row < len(self._selected_words):
            del self._selected_words[row]
            self._update_words_list()

    @Slot()
    def _on_open_file(self) -> None:
        """Open file dialog and load document."""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Document",
            "",
            "Documents (*.pdf *.docx *.txt);;PDF (*.pdf);;Word (*.docx);;Text (*.txt);;All (*.*)",
        )
        if not path:
            return
        file_path = Path(path)
        self._load_file_sync(file_path)

    @Slot()
    def _on_select_all_words(self) -> None:
        """Add all unique words from document to selected list."""
        if not self._all_words:
            QMessageBox.information(
                self,
                "No Content",
                "Open a document first, or the document has no extractable words.",
            )
            return
        self._selected_words = list(self._all_words)
        self._update_words_list()
        self._words_list.selectAll()

    @Slot()
    def _on_export_excel(self) -> None:
        """Export selected words to Excel file."""
        if not self._selected_words:
            QMessageBox.warning(
                self,
                "No Words",
                "No words selected. Select text in the document or use 'Select All Words'.",
            )
            return
        default_name = "words.xlsx"
        if self._current_file:
            default_name = self._current_file.stem + "_words.xlsx"
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export to Excel",
            default_name,
            "Excel (*.xlsx);;All (*.*)",
        )
        if not path:
            return
        if ExcelExporter.export(self._selected_words, Path(path)):
            QMessageBox.information(
                self,
                "Export Complete",
                f"Exported {len(self._selected_words)} words to:\n{path}",
            )
        else:
            QMessageBox.critical(
                self,
                "Export Failed",
                "Could not save the Excel file.",
            )
