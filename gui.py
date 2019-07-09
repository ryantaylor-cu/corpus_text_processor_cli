#!/usr/bin/env python3

# To build for MacOS:
# pyinstaller --onefile --windowed --osx-bundle-identifier=CROW
# -n "Corpus Text Processor" --icon=default_icon.icns gui.py
#
# cp Info.plist dist/Corpus\ Text\ Processor.app/Contents/
# codesign -s "CROW" dist/Corpus\ Text\ Processor.app/
#
# mkdir Mac/ && mv dist/Corpus\ Text\ Processor.app Mac/
# pkgbuild --root Mac --identifier CROW --version 0.alpha4 --install-location
# /Applications CorpusTextProcessor-unsigned.pkg --sign "John Fullmer"

# https://simplemdm.com/certificate-sign-macos-packages/
# productsign --sign "3rd Party Mac Developer Installer: John Fullmer (A57QZ4FF3C)" CorpusTextProcessor-unsigned.pkg CorpusTextProcessor.pkg

# To build for Windows:
# pyinstaller --onefile -wF gui.py --icon=default_icon.ico
import PySimpleGUIQt as sg
# Windows can use PySimpleGUI
import convert_to_plaintext
import convert_to_utf8
import normalization
import os
print = sg.EasyPrint

sg.ChangeLookAndFeel('TealMono')
layout = [
    [sg.Text('Corpus Text Processor', size=(30, 1), font=("Verdana", 20))],
    [sg.Text('Choose folder:', size=(20, 1)),
        sg.InputText(""), sg.FolderBrowse(size=(9, 1))],
    [sg.Text('Choose processor:', size=(20, 1))],
    [sg.Radio("Convert to plaintext (saved to 'plaintext' folder)",
              "Processors", default=False)],
    [sg.Radio("Standardize to UTF-8 encoding (saved to 'converted' folder)",
              "Processors", default=False)],
    [sg.Radio("Normalize characters (saved to 'normalized' folder)",
              "Processors", default=False)],
    [sg.Button("Process files", size=(12, 1)), sg.Exit(size=(6, 1))]
]
window = sg.Window('Corpus Text Processor', keep_on_top=False, font=(
    "Verdana", 14), default_element_size=(40, 1)).Layout(layout)


def process_recursive(values):
    # values[0] is the directory to be processed
    directory = values[0]
    # values[1] is Plaintext
    # values[2] is UTF-8 Conversion
    # values[3] is Normalization
    if values[1] is True:
        print("*** CONVERTING TO PLAINTEXT ***")
        for dirpath, dirnames, files in os.walk(directory):
            for name in files:
                if (len(os.path.splitext(name)[1])):
                    convert_to_plaintext.convert(os.path.join(
                        dirpath, name), directory, name)
    if values[2] is True:
        print("*** CONVERTING TO UTF-8 ***")
        for dirpath, dirnames, files in os.walk(directory):
            for name in files:
                convert_to_utf8.convert(os.path.join(dirpath, name), name)
    if values[3] is True:
        print("*** NORMALIZING CHARACTERS ***")
        for dirpath, dirnames, files in os.walk(directory):
            for name in files:
                if (os.path.splitext(name)[1]) == ".txt":
                    normalization.normalize(os.path.join(dirpath, name), directory, name)

while True:
    event, values = window.Read()
    if event is None or event == 'Exit':
        break
    elif event == "Process files" and values[0] is not None and os.path.isdir(values[0]):
        process_recursive(values)
    else:
        print("You need to provide a valid folder")

window.Close()
