# Copyright (c) 2004 Nanorex, Inc.  All rights reserved.
from qt import *
from MoleculePropDialog import *

nocolor = QColor(230,231,230) # needed by colortile and colorchooser

class MoleculeProp(MoleculePropDialog):
    def __init__(self, mol):
        MoleculePropDialog.__init__(self)
        self.mol = mol
        
        self.nameLineEdit.setText(mol.name)
        self.applyPushButton.setEnabled(False)
        
        self.mol.originalColor = self.mol.color # Save original molecule color in case of cancel

        if self.mol.color: # Set colortile to mol color (without border)
            self.colorPixmapLabel.setPaletteBackgroundColor(
                QColor(int(mol.color[0]*255), 
                             int(mol.color[1]*255), 
                             int(mol.color[2]*255)))
            self.colorPixmapLabel.setFrameShape(QFrame.NoFrame)
        else: # Set the colortile to gray (no color), with a box (border)
            self.colorPixmapLabel.setPaletteBackgroundColor(nocolor)
            self.colorPixmapLabel.setFrameShape(QFrame.Box)
        
        # Create header of the molecule info.
        self.atomsTextBrowser.setReadOnly(True)
        totalAtomsStr = "Total Atoms: " + str(len(mol.atoms)) + "\n\n"
        ele2Num = {}
        
        # Calculating the number of element types in this molecule.
        for a in self.mol.atoms.itervalues():
             if not ele2Num.has_key(a.element.symbol): ele2Num[a.element.symbol] = 1 # New element found
             else: ele2Num[a.element.symbol] += 1 # Increment element
        
        # String construction for each element to be displayed.        
        for item in ele2Num.iteritems():
            eleStr = item[0] + ": " + str(item[1]) + "\n"
            totalAtomsStr += eleStr
        
        # Display molecule info in a textbrowser in the dialog window.      
        self.atomsTextBrowser.setText(totalAtomsStr)

    #########################
    # Change molecule color
    #########################
    def changeMolColor(self):
        defcolor = (230.0/255.0, 231.0/255.0, 230.0/255.0)
        if self.mol.color: defcolor = self.mol.color
        color = QColorDialog.getColor(
            QColor(int(defcolor[0]*255), 
                         int(defcolor[1]*255), 
                         int(defcolor[2]*255)),
                         self, "ColorDialog")

        if color.isValid():
            self.colorPixmapLabel.setPaletteBackgroundColor(color)
            self.colorPixmapLabel.setFrameShape(QFrame.NoFrame)
            self.mol.color = color.red()/255.0, color.green()/255.0, color.blue()/255.0
            self.mol.setcolor(self.mol.color)
            self.mol.glpane.paintGL()

    def setMol2ElementColors(self):
        if not self.mol.color: return
        self.colorPixmapLabel.setPaletteBackgroundColor(nocolor)
        self.colorPixmapLabel.setFrameShape(QFrame.Box)
        self.mol.color = None
        self.mol.setcolor(self.mol.color)
        self.mol.glpane.paintGL()
        
    def nameChanged(self):
        self.applyPushButton.setEnabled(True)
                
    def applyButtonClicked(self):    
        self.mol.name = str(self.nameLineEdit.text())
        self.applyPushButton.setEnabled(False)            

    def accept(self):
        self.applyButtonClicked()    
        QDialog.accept(self)

    def reject(self):
        QDialog.reject(self)
        self.mol.color = self.mol.originalColor
        self.mol.setcolor(self.mol.color)
        self.mol.glpane.paintGL()