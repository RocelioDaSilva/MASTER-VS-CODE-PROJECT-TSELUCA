# Build PyInstaller Spec File
# Run: pyinstaller GEESP-Angola.spec

# This file tells PyInstaller how to bundle the app

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('data/processed', 'data/processed'),
        ('app_minimal.py', '.'),
        ('geesp_unified_app.py', '.'),
        ('scripts', 'scripts'),
        ('utils', 'utils'),
    ],
    hiddenimports=[
        'encodings',
        'encodings.utf_8',
        'encodings.utf_16',
        'encodings.ascii',
        'encodings.cp1252',
        'streamlit',
        'streamlit.web',
        'streamlit.web.server',
        'numpy',
        'pandas',
        'geopandas',
        'rasterio',
        'plotly',
        'plotly.graph_objects',
        'plotly.express',
        'folium',
        'pyproj',
        'shapely',
        'scipy',
        'sklearn',
        'sklearn.preprocessing',
        'sklearn.cluster',
        'sklearn.metrics',
        'pkg_resources',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludedimports=['matplotlib.tests'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GEESP-Angola',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GEESP-Angola',
)
