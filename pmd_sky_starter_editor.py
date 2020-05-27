import os
import shutil
import subprocess
import sys
import threading

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from gui.starter import Ui_MainWindow

import mmap
import ctypes

app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)


playerMaleComboBoxes = [ui.PlayerMaleCombo1, ui.PlayerMaleCombo2, ui.PlayerMaleCombo3, ui.PlayerMaleCombo4,
                        ui.PlayerMaleCombo5, ui.PlayerMaleCombo6, ui.PlayerMaleCombo7, ui.PlayerMaleCombo8,
                        ui.PlayerMaleCombo9, ui.PlayerMaleCombo10, ui.PlayerMaleCombo11, ui.PlayerMaleCombo12,
                        ui.PlayerMaleCombo13, ui.PlayerMaleCombo14, ui.PlayerMaleCombo15, ui.PlayerMaleCombo16]

playerMaleCheckBoxes = [ui.PlayerMaleCheck1, ui.PlayerMaleCheck2, ui.PlayerMaleCheck3, ui.PlayerMaleCheck4,
                        ui.PlayerMaleCheck5, ui.PlayerMaleCheck6, ui.PlayerMaleCheck7, ui.PlayerMaleCheck8,
                        ui.PlayerMaleCheck9, ui.PlayerMaleCheck10, ui.PlayerMaleCheck11, ui.PlayerMaleCheck12,
                        ui.PlayerMaleCheck13, ui.PlayerMaleCheck14, ui.PlayerMaleCheck15, ui.PlayerMaleCheck16]

playerFemaleComboBoxes = [ui.PlayerFemaleCombo1, ui.PlayerFemaleCombo2, ui.PlayerFemaleCombo3, ui.PlayerFemaleCombo4,
                        ui.PlayerFemaleCombo5, ui.PlayerFemaleCombo6, ui.PlayerFemaleCombo7, ui.PlayerFemaleCombo8,
                        ui.PlayerFemaleCombo9, ui.PlayerFemaleCombo10, ui.PlayerFemaleCombo11, ui.PlayerFemaleCombo12,
                        ui.PlayerFemaleCombo13, ui.PlayerFemaleCombo14, ui.PlayerFemaleCombo15, ui.PlayerFemaleCombo16]

playerFemaleCheckBoxes = [ui.PlayerFemaleCheck1, ui.PlayerFemaleCheck2, ui.PlayerFemaleCheck3, ui.PlayerFemaleCheck4,
                        ui.PlayerFemaleCheck5, ui.PlayerFemaleCheck6, ui.PlayerFemaleCheck7, ui.PlayerFemaleCheck8,
                        ui.PlayerFemaleCheck9, ui.PlayerFemaleCheck10, ui.PlayerFemaleCheck11, ui.PlayerFemaleCheck12,
                        ui.PlayerFemaleCheck13, ui.PlayerFemaleCheck14, ui.PlayerFemaleCheck15, ui.PlayerFemaleCheck16]

partnerComboBoxes = [ui.PartnerCombo1, ui.PartnerCombo2, ui.PartnerCombo3, ui.PartnerCombo4, ui.PartnerCombo5,
                    ui.PartnerCombo6, ui.PartnerCombo7, ui.PartnerCombo8, ui.PartnerCombo9, ui.PartnerCombo10,
                    ui.PartnerCombo11, ui.PartnerCombo12, ui.PartnerCombo13, ui.PartnerCombo14, ui.PartnerCombo15,
                    ui.PartnerCombo16, ui.PartnerCombo17, ui.PartnerCombo18, ui.PartnerCombo19, ui.PartnerCombo20,
                    ui.PartnerCombo21]

partnerCheckBoxes = [ui.PartnerCheck1, ui.PartnerCheck2, ui.PartnerCheck3, ui.PartnerCheck4, ui.PartnerCheck5,
                    ui.PartnerCheck6, ui.PartnerCheck7, ui.PartnerCheck8, ui.PartnerCheck9, ui.PartnerCheck10,
                    ui.PartnerCheck11, ui.PartnerCheck12, ui.PartnerCheck13, ui.PartnerCheck14, ui.PartnerCheck15,
                    ui.PartnerCheck16, ui.PartnerCheck17, ui.PartnerCheck18, ui.PartnerCheck19, ui.PartnerCheck20,
                    ui.PartnerCheck21]


overlay13Memory = []

sTextMemory = []
eTextMemory = []
iTextMemory = []
gTextMemory = []
fTextMemory = []
textMemory = [sTextMemory, eTextMemory, iTextMemory, gTextMemory, fTextMemory]

portraitMemory = []


def bytes2int(b):
    return int.from_bytes(b, "little")


def int2bytes(i, n):
    return i.to_bytes(n, 'little')


def signedint2bytes(i, n):
    return i.to_bytes(n, 'little', signed=True)


def increase_step():
    if ui.openButton.isEnabled():
        timer.stop()
        if ui.openButton.text() == "Save":
            ui.progressBar.setValue(100)
            init_values()
            ctypes.windll.user32.MessageBoxW(0, "Success: file opened!", "Info", 0x40)
        ui.progressBar.setValue(0)
    elif ui.progressBar.value() < 90:
        if os.path.exists("rom/data/"):
            if os.path.exists("rom/data/SCRIPT/"):
                if os.path.exists("rom/data/SCRIPT/D30P21A/"):
                    if os.path.exists("rom/data/SCRIPT/D70P41A/"):
                        if os.path.exists("rom/data/SCRIPT/S00P01A/"):
                            ui.progressBar.setValue(90)
                        else:
                            ui.progressBar.setValue(70)
                    else:
                        ui.progressBar.setValue(50)
                else:
                    ui.progressBar.setValue(30)
            else:
                ui.progressBar.setValue(10)


def finish():
    if ui.openButton.isEnabled():
        timer2.stop()
        ui.progressBar.setValue(100)
        ctypes.windll.user32.MessageBoxW(0, "Success: file created!", "Complete", 0x40)
        ui.progressBar.setValue(0)


def open_file():
    open_rom(choose_open_file())
    if not ui.openButton.isEnabled():
        ui.progressBar.setValue(0)
        timer.start(1000)


def choose_open_file():
    return QFileDialog.getOpenFileName(None, "Choose a ROM", "", "NDS Files (*.nds)")


def create_file():
    filename = choose_save_file()
    if filename[0]:
        ui.progressBar.setValue(0)

        save_values()
        fix_portraits()

        ui.progressBar.setValue(50)
        save_all_files()

        save_rom(filename)
        timer2.start(1000)


def choose_save_file():
    return QFileDialog.getSaveFileName(None, "Choose a Destination", "", "NDS Files (*.nds)")


def pmd_sky_eu(memory):
    code = b'POKEDUN SORAC2SP'
    for index in range(0, 16):
        if memory[index] != int2bytes(code[index], 1):
            return False
    return True


def unpack(my_args, dummy):
    subprocess.Popen(my_args, creationflags=subprocess.CREATE_NO_WINDOW).wait()  # Ejecutamos ndstool

    memory = []
    ret = True

    if not load_file("rom/header.bin", memory):
        ctypes.windll.user32.MessageBoxW(0, "ROM: Failed to open header.bin", "Fail!", 0x10)
        ret = False

    if not pmd_sky_eu(memory):
        ctypes.windll.user32.MessageBoxW(0, "ROM: ROM must be Pokemon Mystery Dungeon - Explorers of Sky (EU)",
                                         "Fail!", 0x10)
        ret = False

    load_all_files()

    if ret:
        ui.openButton.setText("Save")  # save
    ui.openButton.setEnabled(True)


def pack(my_args, dummy):
    subprocess.Popen(my_args, creationflags=subprocess.CREATE_NO_WINDOW).wait()  # Ejecutamos ndstool

    if os.path.exists("rom"):
        shutil.rmtree("rom", ignore_errors=True)

    ui.openButton.setText("Open")
    ui.openButton.setEnabled(True)


def open_rom(filename):
    if filename[0]:

        ui.openButton.setEnabled(False)

        if os.path.exists("rom"):
            shutil.rmtree("rom", ignore_errors=True)

        os.mkdir("rom")  # Creamos carpeta rom para poner los ficheros generados por el ndstool

        my_args = [
            "ndstool.exe",
            "-x",
            filename[0],
            "-9",
            "rom/arm9.bin",
            "-7",
            "rom/arm7.bin",
            "-y9",
            "rom/y9.bin",
            "-y7",
            "rom/y7.bin",
            "-d",
            "rom/data",
            "-y",
            "rom/overlay",
            "-t",
            "rom/banner.bin",
            "-h",
            "rom/header.bin"
        ]

        thread = threading.Thread(target=unpack, args=(my_args, 0))
        thread.start()


def save_rom(filename):
    if filename[0]:

        ui.openButton.setEnabled(False)

        my_args = [
            "ndstool.exe",
            "-c",
            filename[0],
            "-9",
            "rom/arm9.bin",
            "-7",
            "rom/arm7.bin",
            "-y9",
            "rom/y9.bin",
            "-y7",
            "rom/y7.bin",
            "-d",
            "rom/data",
            "-y",
            "rom/overlay",
            "-t",
            "rom/banner.bin",
            "-h",
            "rom/header.bin"
        ]

        thread = threading.Thread(target=pack, args=(my_args, 0))
        thread.start()


def load_file(filename, memory):
    if filename:
        with open(filename, 'r') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as m:
                memory.clear()
                for index in range(0, m.size()):
                    memory.append(m.read(1))
                m.close()
                return True
    return False


def save_file(filename, memory):
    if filename:
        with open(filename, 'r+') as f:
            with mmap.mmap(f.fileno(), 0) as m:
                m.seek(0)
                for byte in memory:
                    m.write(byte)
                m.close()
                return True
    return False


def load_all_files():
    if not load_file("rom/overlay/overlay_0013.bin", overlay13Memory):
        ctypes.windll.user32.MessageBoxW(0, "ROM: Failed to open overlay_0013.bin", "Fail!", 0x10)

    if not load_file("rom/data/MESSAGE/text_s.str", sTextMemory):
        ctypes.windll.user32.MessageBoxW(0, "ROM: Failed to open text_s.str", "Fail!", 0x10)

    if not load_file("rom/data/MESSAGE/text_e.str", eTextMemory):
        ctypes.windll.user32.MessageBoxW(0, "ROM: Failed to open text_e.str", "Fail!", 0x10)

    if not load_file("rom/data/MESSAGE/text_i.str", iTextMemory):
        ctypes.windll.user32.MessageBoxW(0, "ROM: Failed to open text_i.str", "Fail!", 0x10)

    if not load_file("rom/data/MESSAGE/text_g.str", gTextMemory):
        ctypes.windll.user32.MessageBoxW(0, "ROM: Failed to open text_g.str", "Fail!", 0x10)

    if not load_file("rom/data/MESSAGE/text_f.str", fTextMemory):
        ctypes.windll.user32.MessageBoxW(0, "ROM: Failed to open text_f.str", "Fail!", 0x10)

    if not load_file("rom/data/FONT/kaomado.kao", portraitMemory):
        ctypes.windll.user32.MessageBoxW(0, "ROM: Failed to open kaomado.kao", "Fail!", 0x10)


def save_all_files():
    save_file("rom/overlay/overlay_0013.bin", overlay13Memory)
    save_file("rom/data/MESSAGE/text_s.str", sTextMemory)
    save_file("rom/data/MESSAGE/text_e.str", eTextMemory)
    save_file("rom/data/MESSAGE/text_i.str", iTextMemory)
    save_file("rom/data/MESSAGE/text_g.str", gTextMemory)
    save_file("rom/data/MESSAGE/text_f.str", fTextMemory)
    save_file("rom/data/FONT/kaomado.kao", portraitMemory)


def open_save_file():
    if ui.openButton.text() == "Open":
        open_file()
    else:
        create_file()


def pokemon_name(value, language):
    entry = 0x00008880 + value * 4
    pointer = bytes2int(textMemory[language][entry] + textMemory[language][entry + 1] +
                        textMemory[language][entry + 2] + textMemory[language][entry + 3])

    pokemon_name = b''
    count = 0
    finish = False
    while not finish:
        byte = textMemory[language][pointer + count]
        if byte == int2bytes(0, 1):
            finish = True
        else:
            pokemon_name += byte
        count += 1

    return pokemon_name


def pokemon_message(value, k):
    entry = 0x000019F0 + k * 4

    sPersonalityMessage = '¡[CS:K]'.encode('ansi') + pokemon_name(value, 0) + '[CR]!'.encode('ansi')
    ePersonalityMessage = 'Will be a [CS:K]'.encode('ansi') + pokemon_name(value, 1) + '[CR]!'.encode('ansi')
    iPersonalityMessage = 'Sarà il Pokémon [CS:K]'.encode('ansi') + pokemon_name(value, 2) + '[CR]!'.encode('ansi')
    gPersonalityMessage = 'wird ein [CS:K]'.encode('ansi') + pokemon_name(value, 3) + '[CR]!'.encode('ansi')
    fPersonalityMessage = '... un [CS:K]'.encode('ansi') + pokemon_name(value, 4) + '[CR]!'.encode('ansi')
    personalityMessages = [sPersonalityMessage, ePersonalityMessage, iPersonalityMessage,
                           gPersonalityMessage, fPersonalityMessage]

    for language in range(0, 5):
        pointer = bytes2int(textMemory[language][entry] + textMemory[language][entry + 1] +
                            textMemory[language][entry + 2] + textMemory[language][entry + 3])

        count = 0
        finish = False
        while not finish:
            byte = textMemory[language][pointer + count]
            if byte == int2bytes(0, 1):
                finish = True
            elif count < len(personalityMessages[language]):
                textMemory[language][pointer + count] = int2bytes(personalityMessages[language][count], 1)
            else:
                textMemory[language][pointer + count] = int2bytes(32, 1)
            count += 1


def fix_portraits():
    for index in range(0, 1154):
        entry = 0x000000A0 + index * 160
        first_pointer = (portraitMemory[entry] + portraitMemory[entry + 1] +
                         portraitMemory[entry + 2] + portraitMemory[entry + 3])

        byte = portraitMemory[entry + 7]
        if byte == int2bytes(255, 1):
            first_pointer += (portraitMemory[entry + 4] + portraitMemory[entry + 5] +
                              portraitMemory[entry + 6] + portraitMemory[entry + 7])
        else:
            first_pointer += signedint2bytes(-bytes2int(portraitMemory[entry + 4] + portraitMemory[entry + 5] +
                                                        portraitMemory[entry + 6] + portraitMemory[entry + 7]), 4)

        for it in range(2, 40, 2):
            offset = entry + it * 4
            byte = portraitMemory[offset + 3]
            if byte == int2bytes(255, 1):
                portraitMemory[offset] = int2bytes(first_pointer[0], 1)
                portraitMemory[offset + 1] = int2bytes(first_pointer[1], 1)
                portraitMemory[offset + 2] = int2bytes(first_pointer[2], 1)
                portraitMemory[offset + 3] = int2bytes(first_pointer[3], 1)
                portraitMemory[offset + 4] = int2bytes(first_pointer[4], 1)
                portraitMemory[offset + 5] = int2bytes(first_pointer[5], 1)
                portraitMemory[offset + 6] = int2bytes(first_pointer[6], 1)
                portraitMemory[offset + 7] = int2bytes(first_pointer[7], 1)


def init_values():
    global playerMaleComboBoxes
    global playerMaleCheckBoxes
    global playerFemaleComboBoxes
    global playerFemaleCheckBoxes
    global partnerComboBoxes
    global partnerCheckBoxes

    maxPokemonId = 0x218

    pokemon_list = []
    for index in range(0, maxPokemonId):
        pokemon_list.append(pokemon_name(index, 1).decode('ansi'))  # english list

    for playerMaleComboBox in playerMaleComboBoxes:
        playerMaleComboBox.addItems(pokemon_list)
    for playerFemaleComboBox in playerFemaleComboBoxes:
        playerFemaleComboBox.addItems(pokemon_list)
    for partnerComboBox in partnerComboBoxes:
        partnerComboBox.addItems(pokemon_list)

    for it in range(0, 16):
        entry = 0x00001F78 + it * 4
        # Male
        player_male = bytes2int(overlay13Memory[entry] + overlay13Memory[entry + 1])
        if player_male < 600:
            playerMaleComboBoxes[it].setCurrentIndex(player_male)
            playerMaleCheckBoxes[it].setChecked(False)
        else:
            playerMaleComboBoxes[it].setCurrentIndex(player_male - 600)
            playerMaleCheckBoxes[it].setChecked(True)
        # Female
        player_female = bytes2int(overlay13Memory[entry + 2] + overlay13Memory[entry + 3])
        if player_female < 600:
            playerFemaleComboBoxes[it].setCurrentIndex(player_female)
            playerFemaleCheckBoxes[it].setChecked(False)
        else:
            playerFemaleComboBoxes[it].setCurrentIndex(player_female - 600)
            playerFemaleCheckBoxes[it].setChecked(True)

    for it in range(0, 21):
        entry = 0x00001F4C + it * 2
        partner = bytes2int(overlay13Memory[entry] + overlay13Memory[entry + 1])
        if partner < 600:
            partnerComboBoxes[it].setCurrentIndex(partner)
            partnerCheckBoxes[it].setChecked(False)
        else:
            partnerComboBoxes[it].setCurrentIndex(partner - 600)
            partnerCheckBoxes[it].setChecked(True)


def save_values():
    global playerMaleComboBoxes
    global playerMaleCheckBoxes
    global playerFemaleComboBoxes
    global playerFemaleCheckBoxes
    global partnerComboBoxes
    global partnerCheckBoxes

    k = 0
    for it in range(0, 16):
        entry = 0x00001F78 + it * 4
        k += 1
        # Male
        pokemon_message(playerMaleComboBoxes[it].currentIndex(), k)
        if not playerMaleCheckBoxes[it].isChecked():
            overlay13Memory[entry] = int2bytes(int2bytes(playerMaleComboBoxes[it].currentIndex(), 2)[0], 1)
            overlay13Memory[entry + 1] = int2bytes(int2bytes(playerMaleComboBoxes[it].currentIndex(), 2)[1], 1)
        else:
            overlay13Memory[entry] = int2bytes(int2bytes(playerMaleComboBoxes[it].currentIndex() + 600, 2)[0], 1)
            overlay13Memory[entry + 1] = int2bytes(int2bytes(playerMaleComboBoxes[it].currentIndex() + 600, 2)[1], 1)
        k += 1
        # Female
        pokemon_message(playerFemaleComboBoxes[it].currentIndex(), k)
        if not playerFemaleCheckBoxes[it].isChecked():
            overlay13Memory[entry + 2] = int2bytes(int2bytes(playerFemaleComboBoxes[it].currentIndex(), 2)[0], 1)
            overlay13Memory[entry + 3] = int2bytes(int2bytes(playerFemaleComboBoxes[it].currentIndex(), 2)[1], 1)
        else:
            overlay13Memory[entry + 2] = int2bytes(int2bytes(playerFemaleComboBoxes[it].currentIndex() + 600, 2)[0], 1)
            overlay13Memory[entry + 3] = int2bytes(int2bytes(playerFemaleComboBoxes[it].currentIndex() + 600, 2)[1], 1)
        k += 1

    for it in range(0, 21):
        entry = 0x00001F4C + it * 2
        if not partnerCheckBoxes[it].isChecked():
            overlay13Memory[entry] = int2bytes(int2bytes(partnerComboBoxes[it].currentIndex(), 2)[0], 1)
            overlay13Memory[entry + 1] = int2bytes(int2bytes(partnerComboBoxes[it].currentIndex(), 2)[1], 1)

        else:
            overlay13Memory[entry] = int2bytes(int2bytes(partnerComboBoxes[it].currentIndex() + 600, 2)[0], 1)
            overlay13Memory[entry + 1] = int2bytes(int2bytes(partnerComboBoxes[it].currentIndex() + 600, 2)[1], 1)


ui.openButton.clicked.connect(open_save_file)

timer = QTimer()
timer.timeout.connect(increase_step)

timer2 = QTimer()
timer2.timeout.connect(finish)


window.show()
sys.exit(app.exec_())
