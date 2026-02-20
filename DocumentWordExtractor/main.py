"""Document Word Extractor - Main entry point."""

import sys
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from ui.main_window import MainWindow


def main() -> None:
    """Run the application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Document Word Extractor")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("DocumentWordExtractor")

    # High DPI scaling
    app.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
