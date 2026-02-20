# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Document Word Extractor
# Build: pyinstaller DocumentWordExtractor.spec

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        # PySide6 Qt
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'PySide6.shiboken6',
        # PyMuPDF (PDF support)
        'fitz',
        'PyMuPDF',
        # python-docx (Word support)
        'docx',
        'docx.opc',
        'docx.oxml',
        'docx.shared',
        'docx.styles',
        'docx.text.paragraph',
        # openpyxl (Excel export)
        'openpyxl',
        'openpyxl.cell',
        'openpyxl.styles',
        # Project modules (ensure collected)
        'readers',
        'readers.base_reader',
        'readers.document_factory',
        'readers.docx_reader',
        'readers.pdf_reader',
        'readers.text_reader',
        'readers.file_type_detector',
        'processors',
        'processors.word_extractor',
        'processors.text_processor',
        'exporters',
        'exporters.excel_exporter',
        'ui',
        'ui.main_window',
        'utils',
        'utils.styles',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DocumentWordExtractor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Set to 'path/to/icon.ico' if you have one
)
