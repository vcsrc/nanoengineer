# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\atom\cad\src\UserPrefsDialog.ui'
#
# Created: Fri Jul 1 01:36:28 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.12
#
# WARNING! All changes made in this file will be lost!


from qt import *


class UserPrefsDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("UserPrefsDialog")


        UserPrefsDialogLayout = QVBoxLayout(self,11,6,"UserPrefsDialogLayout")

        self.prefs_tab = QTabWidget(self,"prefs_tab")

        self.tab = QWidget(self.prefs_tab,"tab")
        tabLayout = QGridLayout(self.tab,1,1,11,6,"tabLayout")

        self.file_locations_grp = QGroupBox(self.tab,"file_locations_grp")
        self.file_locations_grp.setColumnLayout(0,Qt.Vertical)
        self.file_locations_grp.layout().setSpacing(6)
        self.file_locations_grp.layout().setMargin(11)
        file_locations_grpLayout = QGridLayout(self.file_locations_grp.layout())
        file_locations_grpLayout.setAlignment(Qt.AlignTop)

        self.gamess_choose_btn = QPushButton(self.file_locations_grp,"gamess_choose_btn")

        file_locations_grpLayout.addWidget(self.gamess_choose_btn,1,2)

        self.gamess_lbl = QLabel(self.file_locations_grp,"gamess_lbl")
        self.gamess_lbl.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        file_locations_grpLayout.addWidget(self.gamess_lbl,1,0)

        self.gamess_path_linedit = QLineEdit(self.file_locations_grp,"gamess_path_linedit")
        self.gamess_path_linedit.setFrameShape(QLineEdit.LineEditPanel)
        self.gamess_path_linedit.setFrameShadow(QLineEdit.Sunken)

        file_locations_grpLayout.addWidget(self.gamess_path_linedit,1,1)

        tabLayout.addMultiCellWidget(self.file_locations_grp,1,1,0,1)

        self.groupBox7_2 = QGroupBox(self.tab,"groupBox7_2")
        self.groupBox7_2.setColumnLayout(0,Qt.Vertical)
        self.groupBox7_2.layout().setSpacing(6)
        self.groupBox7_2.layout().setMargin(11)
        groupBox7_2Layout = QVBoxLayout(self.groupBox7_2.layout())
        groupBox7_2Layout.setAlignment(Qt.AlignTop)

        self.display_compass_checkbox = QCheckBox(self.groupBox7_2,"display_compass_checkbox")
        self.display_compass_checkbox.setChecked(1)
        groupBox7_2Layout.addWidget(self.display_compass_checkbox)

        self.display_origin_axis_checkbox = QCheckBox(self.groupBox7_2,"display_origin_axis_checkbox")
        self.display_origin_axis_checkbox.setChecked(1)
        groupBox7_2Layout.addWidget(self.display_origin_axis_checkbox)

        self.display_pov_axis_checkbox = QCheckBox(self.groupBox7_2,"display_pov_axis_checkbox")
        self.display_pov_axis_checkbox.setChecked(1)
        groupBox7_2Layout.addWidget(self.display_pov_axis_checkbox)

        tabLayout.addWidget(self.groupBox7_2,0,0)

        self.compass_position_btngrp = QButtonGroup(self.tab,"compass_position_btngrp")
        self.compass_position_btngrp.setExclusive(1)
        self.compass_position_btngrp.setColumnLayout(0,Qt.Vertical)
        self.compass_position_btngrp.layout().setSpacing(6)
        self.compass_position_btngrp.layout().setMargin(11)
        compass_position_btngrpLayout = QGridLayout(self.compass_position_btngrp.layout())
        compass_position_btngrpLayout.setAlignment(Qt.AlignTop)

        self.upper_right_btn = QRadioButton(self.compass_position_btngrp,"upper_right_btn")
        self.upper_right_btn.setChecked(1)

        compass_position_btngrpLayout.addWidget(self.upper_right_btn,0,1)

        self.upper_left_btn = QRadioButton(self.compass_position_btngrp,"upper_left_btn")

        compass_position_btngrpLayout.addWidget(self.upper_left_btn,0,0)

        self.lower_left_btn = QRadioButton(self.compass_position_btngrp,"lower_left_btn")

        compass_position_btngrpLayout.addWidget(self.lower_left_btn,2,0)

        self.lower_right_btn = QRadioButton(self.compass_position_btngrp,"lower_right_btn")

        compass_position_btngrpLayout.addWidget(self.lower_right_btn,2,1)
        spacer8 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        compass_position_btngrpLayout.addItem(spacer8,1,0)
        spacer8_2 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        compass_position_btngrpLayout.addItem(spacer8_2,1,1)

        tabLayout.addWidget(self.compass_position_btngrp,0,1)
        self.prefs_tab.insertTab(self.tab,QString(""))

        self.TabPage = QWidget(self.prefs_tab,"TabPage")
        TabPageLayout = QVBoxLayout(self.TabPage,11,6,"TabPageLayout")

        layout11 = QHBoxLayout(None,0,6,"layout11")

        layout9 = QGridLayout(None,1,1,0,6,"layout9")

        self.color2_lbl = QLabel(self.TabPage,"color2_lbl")
        self.color2_lbl.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout9.addWidget(self.color2_lbl,3,0)

        layout37 = QHBoxLayout(None,0,6,"layout37")

        self.color1_frame = QFrame(self.TabPage,"color1_frame")
        self.color1_frame.setPaletteBackgroundColor(QColor(170,255,255))
        self.color1_frame.setFrameShape(QFrame.Box)
        self.color1_frame.setFrameShadow(QFrame.Plain)
        layout37.addWidget(self.color1_frame)

        self.choose_color1_btn = QPushButton(self.TabPage,"choose_color1_btn")
        layout37.addWidget(self.choose_color1_btn)

        layout9.addLayout(layout37,2,1)

        self.fill_type_lbl = QLabel(self.TabPage,"fill_type_lbl")
        self.fill_type_lbl.setEnabled(0)
        self.fill_type_lbl.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout9.addWidget(self.fill_type_lbl,1,0)

        layout37_2 = QHBoxLayout(None,0,6,"layout37_2")

        self.color2_frame = QFrame(self.TabPage,"color2_frame")
        self.color2_frame.setPaletteBackgroundColor(QColor(0,0,127))
        self.color2_frame.setFrameShape(QFrame.Box)
        self.color2_frame.setFrameShadow(QFrame.Plain)
        layout37_2.addWidget(self.color2_frame)

        self.choose_color2_btn = QPushButton(self.TabPage,"choose_color2_btn")
        layout37_2.addWidget(self.choose_color2_btn)

        layout9.addLayout(layout37_2,3,1)

        self.color1_lbl = QLabel(self.TabPage,"color1_lbl")
        self.color1_lbl.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout9.addWidget(self.color1_lbl,2,0)

        self.mode_combox = QComboBox(0,self.TabPage,"mode_combox")

        layout9.addWidget(self.mode_combox,0,1)

        self.mode_lbl = QLabel(self.TabPage,"mode_lbl")
        self.mode_lbl.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout9.addWidget(self.mode_lbl,0,0)

        self.fill_type_combox = QComboBox(0,self.TabPage,"fill_type_combox")
        self.fill_type_combox.setEnabled(0)

        layout9.addWidget(self.fill_type_combox,1,1)
        layout11.addLayout(layout9)

        layout10 = QVBoxLayout(None,0,6,"layout10")
        spacer6 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout10.addItem(spacer6)

        self.gradient_orient_btngrp = QButtonGroup(self.TabPage,"gradient_orient_btngrp")
        self.gradient_orient_btngrp.setExclusive(1)
        self.gradient_orient_btngrp.setColumnLayout(0,Qt.Vertical)
        self.gradient_orient_btngrp.layout().setSpacing(6)
        self.gradient_orient_btngrp.layout().setMargin(11)
        gradient_orient_btngrpLayout = QVBoxLayout(self.gradient_orient_btngrp.layout())
        gradient_orient_btngrpLayout.setAlignment(Qt.AlignTop)

        self.vertical_rbtn = QRadioButton(self.gradient_orient_btngrp,"vertical_rbtn")
        self.vertical_rbtn.setChecked(1)
        gradient_orient_btngrpLayout.addWidget(self.vertical_rbtn)

        self.horizontal_rbtn = QRadioButton(self.gradient_orient_btngrp,"horizontal_rbtn")
        gradient_orient_btngrpLayout.addWidget(self.horizontal_rbtn)
        layout10.addWidget(self.gradient_orient_btngrp)
        layout11.addLayout(layout10)
        spacer7_2 = QSpacerItem(50,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout11.addItem(spacer7_2)
        TabPageLayout.addLayout(layout11)
        spacer8_3 = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        TabPageLayout.addItem(spacer8_3)

        layout7 = QHBoxLayout(None,0,6,"layout7")

        self.restore_bgcolor_btn = QPushButton(self.TabPage,"restore_bgcolor_btn")
        layout7.addWidget(self.restore_bgcolor_btn)
        spacer8_4 = QSpacerItem(40,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout7.addItem(spacer8_4)
        TabPageLayout.addLayout(layout7)
        self.prefs_tab.insertTab(self.TabPage,QString(""))
        UserPrefsDialogLayout.addWidget(self.prefs_tab)

        layout28 = QHBoxLayout(None,0,6,"layout28")
        spacer7 = QSpacerItem(240,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout28.addItem(spacer7)

        self.ok_btn = QPushButton(self,"ok_btn")
        layout28.addWidget(self.ok_btn)
        UserPrefsDialogLayout.addLayout(layout28)

        self.languageChange()

        self.resize(QSize(476,283).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.ok_btn,SIGNAL("clicked()"),self,SLOT("accept()"))
        self.connect(self.display_compass_checkbox,SIGNAL("stateChanged(int)"),self.display_compass)
        self.connect(self.display_origin_axis_checkbox,SIGNAL("stateChanged(int)"),self.display_origin_axis)
        self.connect(self.display_pov_axis_checkbox,SIGNAL("stateChanged(int)"),self.display_pov_axis)
        self.connect(self.compass_position_btngrp,SIGNAL("clicked(int)"),self.set_compass_position)
        self.connect(self.gamess_choose_btn,SIGNAL("clicked()"),self.set_gamess_path)
        self.connect(self.prefs_tab,SIGNAL("selected(const QString&)"),self.setup_current_page)
        self.connect(self.mode_combox,SIGNAL("activated(int)"),self.mode_changed)
        self.connect(self.choose_color1_btn,SIGNAL("clicked()"),self.change_bgcolor1)
        self.connect(self.fill_type_combox,SIGNAL("activated(const QString&)"),self.fill_type_changed)
        self.connect(self.restore_bgcolor_btn,SIGNAL("clicked()"),self.restore_default_bgcolor)


    def languageChange(self):
        self.setCaption(self.__tr("Preferences"))
        self.file_locations_grp.setTitle(self.__tr("File Locations"))
        self.gamess_choose_btn.setText(self.__tr("Choose..."))
        self.gamess_lbl.setText(self.__tr("GAMESS :"))
        self.groupBox7_2.setTitle(self.__tr("Compass and Axes"))
        self.display_compass_checkbox.setText(self.__tr("Display Compass"))
        self.display_origin_axis_checkbox.setText(self.__tr("Display Origin Axis"))
        self.display_pov_axis_checkbox.setText(self.__tr("Display Point of View Axis"))
        self.compass_position_btngrp.setTitle(self.__tr("Compass Position"))
        self.upper_right_btn.setText(self.__tr("Upper Right"))
        self.upper_left_btn.setText(self.__tr("Upper Left"))
        self.lower_left_btn.setText(self.__tr("Lower Left"))
        self.lower_right_btn.setText(self.__tr("Lower Right"))
        self.prefs_tab.changeTab(self.tab,self.__tr("General"))
        self.color2_lbl.setText(self.__tr("Color 2 :"))
        self.choose_color1_btn.setText(self.__tr("Choose..."))
        self.fill_type_lbl.setText(self.__tr("Fill Type :"))
        self.choose_color2_btn.setText(self.__tr("Choose..."))
        self.color1_lbl.setText(self.__tr("Color :"))
        self.mode_combox.clear()
        self.mode_combox.insertItem(self.__tr("Select Chunks"))
        self.mode_combox.insertItem(self.__tr("Select Atoms"))
        self.mode_combox.insertItem(self.__tr("Move Chunks"))
        self.mode_combox.insertItem(self.__tr("Build"))
        self.mode_combox.insertItem(self.__tr("Cookie Cutter"))
        self.mode_combox.insertItem(self.__tr("Extrude"))
        self.mode_combox.insertItem(self.__tr("Fuse Chunks"))
        self.mode_combox.insertItem(self.__tr("Movie Player"))
        self.mode_lbl.setText(self.__tr("Mode :"))
        self.fill_type_combox.clear()
        self.fill_type_combox.insertItem(self.__tr("Solid"))
        self.fill_type_combox.insertItem(self.__tr("Gradient"))
        self.gradient_orient_btngrp.setTitle(self.__tr("Gradient Orientation"))
        self.vertical_rbtn.setText(self.__tr("Vertical"))
        self.horizontal_rbtn.setText(self.__tr("Horizontal"))
        self.restore_bgcolor_btn.setText(self.__tr("Restore Default Color"))
        self.prefs_tab.changeTab(self.TabPage,self.__tr("Background"))
        self.ok_btn.setText(self.__tr("OK"))


    def display_compass(self):
        print "UserPrefsDialog.display_compass(): Not implemented yet"

    def display_origin_axis(self):
        print "UserPrefsDialog.display_origin_axis(): Not implemented yet"

    def display_pov_axis(self):
        print "UserPrefsDialog.display_pov_axis(): Not implemented yet"

    def set_compass_position(self):
        print "UserPrefsDialog.set_compass_position(): Not implemented yet"

    def set_gamess_path(self):
        print "UserPrefsDialog.set_gamess_path(): Not implemented yet"

    def setup_current_page(self):
        print "UserPrefsDialog.setup_current_page(): Not implemented yet"

    def mode_changed(self):
        print "UserPrefsDialog.mode_changed(): Not implemented yet"

    def change_bgcolor1(self):
        print "UserPrefsDialog.change_bgcolor1(): Not implemented yet"

    def fill_type_changed(self):
        print "UserPrefsDialog.fill_type_changed(): Not implemented yet"

    def restore_default_bgcolor(self):
        print "UserPrefsDialog.restore_default_bgcolor(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("UserPrefsDialog",s,c)
