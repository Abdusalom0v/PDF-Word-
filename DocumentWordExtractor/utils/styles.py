"""Application styles and themes."""

DARK_THEME = """
/* Main application styling */
QMainWindow {
    background-color: #1e1e2e;
}

QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: "Segoe UI", "SF Pro Display", system-ui, sans-serif;
    font-size: 13px;
}

/* Toolbar */
QToolBar {
    background-color: #181825;
    border: none;
    padding: 6px;
    spacing: 4px;
}

QToolBar::separator {
    width: 1px;
    background-color: #313244;
    margin: 4px 8px;
}

QPushButton {
    background-color: #45475a;
    color: #cdd6f4;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    min-height: 24px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #585b70;
}

QPushButton:pressed {
    background-color: #313244;
}

QPushButton:disabled {
    background-color: #313244;
    color: #6c7086;
}

/* Primary action button */
QPushButton#openButton {
    background-color: #89b4fa;
    color: #1e1e2e;
}

QPushButton#openButton:hover {
    background-color: #b4befe;
}

QPushButton#exportButton {
    background-color: #a6e3a1;
    color: #1e1e2e;
}

QPushButton#exportButton:hover {
    background-color: #94e2d5;
}

/* Theme toggle */
QPushButton#themeButton {
    background-color: transparent;
    padding: 6px 10px;
}

QPushButton#themeButton:hover {
    background-color: #313244;
}

/* Remove selected words */
QPushButton#removeSelectedButton {
    background-color: #f38ba8;
    color: #1e1e2e;
}

QPushButton#removeSelectedButton:hover {
    background-color: #eba0ac;
}

/* Document viewer */
QPlainTextEdit, QTextEdit {
    background-color: #11111b;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 8px;
    padding: 12px;
    selection-background-color: #89b4fa;
    selection-color: #1e1e2e;
    font-family: "Cascadia Code", "Consolas", "Fira Code", monospace;
    font-size: 13px;
}

/* Drop zone overlay */
QFrame#dropZone {
    background-color: rgba(30, 30, 46, 0.95);
    border: 2px dashed #89b4fa;
    border-radius: 12px;
}

QLabel#dropZoneLabel {
    color: #a6adc8;
    font-size: 14px;
}

/* Loading overlay */
QFrame#loadingOverlay {
    background-color: rgba(17, 17, 27, 0.9);
    border-radius: 8px;
}

QLabel#loadingLabel {
    color: #cdd6f4;
}

QProgressBar {
    background-color: #313244;
    border: none;
    border-radius: 4px;
    height: 6px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #89b4fa;
    border-radius: 4px;
}

/* List widget for selected words */
QListWidget {
    background-color: #11111b;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 8px;
    padding: 8px;
    outline: none;
}

QListWidget::item {
    padding: 8px 12px;
    border-radius: 4px;
}

QListWidget::item:hover {
    background-color: #313244;
}

QListWidget::item:selected {
    background-color: #89b4fa;
    color: #1e1e2e;
}

QListWidget::item:selected:!active {
    background-color: #45475a;
}

/* Right panel frame */
QFrame#wordsPanel {
    background-color: #181825;
    border-left: 1px solid #313244;
    border-radius: 0;
}

/* Status bar */
QStatusBar {
    background-color: #181825;
    color: #a6adc8;
    border-top: 1px solid #313244;
    padding: 4px 8px;
    font-size: 12px;
}

/* Scroll bars */
QScrollBar:vertical {
    background-color: #11111b;
    width: 12px;
    border-radius: 6px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #45475a;
    border-radius: 6px;
    min-height: 24px;
}

QScrollBar::handle:vertical:hover {
    background-color: #585b70;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background-color: #11111b;
    height: 12px;
    border-radius: 6px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background-color: #45475a;
    border-radius: 6px;
    min-width: 24px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #585b70;
}

/* Labels */
QLabel {
    color: #cdd6f4;
}

QLabel#panelTitle {
    font-weight: 600;
    font-size: 14px;
    color: #89b4fa;
    padding: 4px 0;
}
"""

LIGHT_THEME = """
/* Main application styling */
QMainWindow {
    background-color: #eff1f5;
}

QWidget {
    background-color: #eff1f5;
    color: #4c4f69;
    font-family: "Segoe UI", "SF Pro Display", system-ui, sans-serif;
    font-size: 13px;
}

/* Toolbar */
QToolBar {
    background-color: #e6e9ef;
    border: none;
    padding: 6px;
    spacing: 4px;
}

QToolBar::separator {
    width: 1px;
    background-color: #ccd0da;
    margin: 4px 8px;
}

QPushButton {
    background-color: #acb0be;
    color: #4c4f69;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    min-height: 24px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #bcc0cc;
}

QPushButton:pressed {
    background-color: #9ca0b0;
}

QPushButton:disabled {
    background-color: #ccd0da;
    color: #a6adc8;
}

/* Primary action button */
QPushButton#openButton {
    background-color: #1e66f5;
    color: #ffffff;
}

QPushButton#openButton:hover {
    background-color: #4170d8;
}

QPushButton#exportButton {
    background-color: #40a02b;
    color: #ffffff;
}

QPushButton#exportButton:hover {
    background-color: #35a77c;
}

/* Theme toggle */
QPushButton#themeButton {
    background-color: transparent;
    padding: 6px 10px;
}

QPushButton#themeButton:hover {
    background-color: #ccd0da;
}

/* Remove selected words */
QPushButton#removeSelectedButton {
    background-color: #e64553;
    color: #ffffff;
}

QPushButton#removeSelectedButton:hover {
    background-color: #d20f39;
}

/* Document viewer */
QPlainTextEdit, QTextEdit {
    background-color: #ffffff;
    color: #4c4f69;
    border: 1px solid #ccd0da;
    border-radius: 8px;
    padding: 12px;
    selection-background-color: #1e66f5;
    selection-color: #ffffff;
    font-family: "Cascadia Code", "Consolas", "Fira Code", monospace;
    font-size: 13px;
}

/* Drop zone overlay */
QFrame#dropZone {
    background-color: rgba(230, 233, 239, 0.95);
    border: 2px dashed #1e66f5;
    border-radius: 12px;
}

QLabel#dropZoneLabel {
    color: #6c6f85;
    font-size: 14px;
}

/* Loading overlay */
QFrame#loadingOverlay {
    background-color: rgba(230, 233, 239, 0.95);
    border-radius: 8px;
}

QLabel#loadingLabel {
    color: #4c4f69;
}

QProgressBar {
    background-color: #ccd0da;
    border: none;
    border-radius: 4px;
    height: 6px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #1e66f5;
    border-radius: 4px;
}

/* List widget for selected words */
QListWidget {
    background-color: #ffffff;
    color: #4c4f69;
    border: 1px solid #ccd0da;
    border-radius: 8px;
    padding: 8px;
    outline: none;
}

QListWidget::item {
    padding: 8px 12px;
    border-radius: 4px;
}

QListWidget::item:hover {
    background-color: #e6e9ef;
}

QListWidget::item:selected {
    background-color: #1e66f5;
    color: #ffffff;
}

QListWidget::item:selected:!active {
    background-color: #acb0be;
}

/* Right panel frame */
QFrame#wordsPanel {
    background-color: #e6e9ef;
    border-left: 1px solid #ccd0da;
    border-radius: 0;
}

/* Status bar */
QStatusBar {
    background-color: #e6e9ef;
    color: #6c6f85;
    border-top: 1px solid #ccd0da;
    padding: 4px 8px;
    font-size: 12px;
}

/* Scroll bars */
QScrollBar:vertical {
    background-color: #e6e9ef;
    width: 12px;
    border-radius: 6px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #acb0be;
    border-radius: 6px;
    min-height: 24px;
}

QScrollBar::handle:vertical:hover {
    background-color: #bcc0cc;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background-color: #e6e9ef;
    height: 12px;
    border-radius: 6px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background-color: #acb0be;
    border-radius: 6px;
    min-width: 24px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #bcc0cc;
}

/* Labels */
QLabel {
    color: #4c4f69;
}

QLabel#panelTitle {
    font-weight: 600;
    font-size: 14px;
    color: #1e66f5;
    padding: 4px 0;
}
"""

# Backward compatibility
MODERN_STYLESHEET = DARK_THEME
