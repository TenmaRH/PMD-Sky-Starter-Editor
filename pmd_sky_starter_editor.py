import sys
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


fileName = ""


def bytes2int(b):
    return int.from_bytes(b, "little")


def int2bytes(i):
    return i.to_bytes(2, byteorder='little')


# n es el numero de caracteres
def string2bytes(s, n):
    if len(s) > n:
        s = s[0:n-1] + "."
    else:
        s = s.ljust(n)
    return s.encode('ansi')


def open_file():
    global fileName
    fileName = QFileDialog.getOpenFileName()
    if fileName[0]:
        with open(fileName[0], 'r') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as m:
                if m.read(16) == b'POKEDUN SORAC2SP':
                    init_values(m)
                    ui.actionSave.setEnabled(True)
                else:
                    ctypes.windll.user32.MessageBoxW(0, "El juego debe ser el Pokemon mundo misterioso exploradores "
                                                        "del cielo (EU version)!", "Error!", 0x10)
                m.close()


def init_values(m):
    global playerMaleComboBoxes
    global playerMaleCheckBoxes
    global playerFemaleComboBoxes
    global playerFemaleCheckBoxes
    global partnerComboBoxes
    global partnerCheckBoxes

    # Buscamos los Pokemon elegibles
    pokemon_list = []
    pokemon_string = ''
    number_bytes = 0
    length = 4790
    m.seek(int('0216AD2A', 16))
    while number_bytes < length:
        character = m.read(1)
        if character[0] != 0:
            pokemon_string += str(chr(character[0]))
        else:
            pokemon_list.append(pokemon_string)
            pokemon_string = ''
        number_bytes += 1

    # Ponemos los Pokemon elegibles
    for playerMaleComboBox in playerMaleComboBoxes:
        playerMaleComboBox.addItems(pokemon_list)
    for playerFemaleComboBox in playerFemaleComboBoxes:
        playerFemaleComboBox.addItems(pokemon_list)
    for partnerComboBox in partnerComboBoxes:
        partnerComboBox.addItems(pokemon_list)

    # Buscamos los pokemon player de la rom
    player_male_list = []
    player_female_list = []
    number_bytes = 0
    length = 32
    m.seek(int('001E0778', 16))
    while number_bytes < length:
        player_male_list.append(bytes2int(m.read(2)))
        player_female_list.append(bytes2int(m.read(2)))
        number_bytes += 2

    # Ponemos los pokemon player de la rom
    it = 0
    while it < 16:
        # Male
        player_male = player_male_list[it]
        if player_male < 600:
            playerMaleComboBoxes[it].setCurrentIndex(player_male)
            playerMaleCheckBoxes[it].setChecked(False)
        else:
            playerMaleComboBoxes[it].setCurrentIndex(player_male - 600)
            playerMaleCheckBoxes[it].setChecked(True)
        # Female
        player_female = player_female_list[it]
        if player_female < 600:
            playerFemaleComboBoxes[it].setCurrentIndex(player_female)
            playerFemaleCheckBoxes[it].setChecked(False)
        else:
            playerFemaleComboBoxes[it].setCurrentIndex(player_female - 600)
            playerFemaleCheckBoxes[it].setChecked(True)
        it += 1

    # Buscamos los pokemon partner de la rom
    partner_list = []
    number_bytes = 0
    length = 21
    m.seek(int('001E074C', 16))
    while number_bytes < length:
        partner_list.append(bytes2int(m.read(2)))
        number_bytes += 1

    # Ponemos los pokemon partner de la rom
    it = 0
    while it < 21:
        partner = partner_list[it]
        if partner < 600:
            partnerComboBoxes[it].setCurrentIndex(partner)
            partnerCheckBoxes[it].setChecked(False)
        else:
            partnerComboBoxes[it].setCurrentIndex(partner - 600)
            partnerCheckBoxes[it].setChecked(True)
        it += 1


def save_file():
    global playerMaleComboBoxes
    global playerMaleCheckBoxes
    global playerFemaleComboBoxes
    global playerFemaleCheckBoxes
    global partnerComboBoxes
    global partnerCheckBoxes

    # Datos que vamos a escribir en la rom
    player_list = []
    name_list = []
    it = 0
    while it < 16:
        # Male
        name_list.append(playerMaleComboBoxes[it].currentText())
        if not playerMaleCheckBoxes[it].isChecked():
            player_list.append(int2bytes(playerMaleComboBoxes[it].currentIndex()))
        else:
            player_list.append(int2bytes(playerMaleComboBoxes[it].currentIndex() + 600))
        # Female
        name_list.append(playerFemaleComboBoxes[it].currentText())
        if not playerFemaleCheckBoxes[it].isChecked():
            player_list.append(int2bytes(playerFemaleComboBoxes[it].currentIndex()))
        else:
            player_list.append(int2bytes(playerFemaleComboBoxes[it].currentIndex() + 600))
        it += 1

    partner_list = []
    it = 0
    while it < 21:
        if not partnerCheckBoxes[it].isChecked():
            partner_list.append(int2bytes(partnerComboBoxes[it].currentIndex()))
        else:
            partner_list.append(int2bytes(partnerComboBoxes[it].currentIndex() + 600))
        it += 1

    # Escribimos los datos en el juego
    global fileName
    with open(fileName[0], 'r+') as f:
        with mmap.mmap(f.fileno(), 0) as m:
            # Player
            m.seek(int('001DBF28', 16))
            for player in player_list:
                m.write(player)
            m.seek(int('001E0778', 16))
            for player in player_list:
                m.write(player)
            # Partner
            m.seek(int('001DBEE0', 16))
            for partner in partner_list:
                m.write(partner)
            m.seek(int('001E074C', 16))
            for partner in partner_list:
                m.write(partner)

            #Cambiamos los nombres del pokemon player
            fix_names(m, name_list)

            m.close()
            ctypes.windll.user32.MessageBoxW(0, "Los cambios se han guardado correctamente!", "Guardado completado!", 0x40)


def fix_names(m, name_list):
    # Arreglamos solo el texto en espaniol
    english_list = [7, 7, 10, 9, 7, 10, 8, 5, 6, 8, 8, 6, 9, 7, 5, 7, 5, 8, 9, 9, 6, 6, 9, 6, 8, 6, 7, 9, 6, 7, 7, 8]
    spanish_offsets = ['0264CCB3', '0264CCD4', '0264CEB5', '0264CED9', '0264D032', '0264D053', '0264D21C', '0264D23E',
                       '0264D402', '0264D422', '0264D614', '0264D636', '0264D7C0', '0264D7E3', '0264D968', '0264D987',
                       '0264DB43', '0264DB62', '0264DCC7', '0264DCEA', '0264DE5C', '0264DE7C', '0264E017', '0264E03A',
                       '0264E201', '0264E223', '0264E3DC', '0264E3FD', '0264E6A7', '0264E6C7', '0264E91A', '0264E93B']
    it = 0
    while it < 32:
        print(name_list[it])
        m.seek(int(spanish_offsets[it], 16))
        print(string2bytes(name_list[it], english_list[it]))
        m.write(string2bytes(name_list[it], english_list[it]))
        it += 1


ui.actionOpen.triggered.connect(open_file)
ui.actionSave.triggered.connect(save_file)


window.show()
sys.exit(app.exec_())