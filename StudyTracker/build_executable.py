import PyInstaller.__main__

PyInstaller.__main__.run([
    '--onefile',
    '--name', 'StudyTracker',
    '--add-data', 'clock_bg.jpeg;StudyTracker',
    '--add-data', 'headset_icon.png;StudyTracker',
    '--add-data', 'fonts/Dune_Rise.otf;fonts',
    '--add-data', 'fonts/Dune_Rise.ttf;fonts',
    '--icon', 'STDune.ico',
    '--noconsole',
    'Main.py'
])
