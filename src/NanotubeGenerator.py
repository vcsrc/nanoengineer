# Copyright (c) 2004-2006 Nanorex, Inc.  All rights reserved.
"""
NanotubeGenerator.py

$Id$

See http://www.nanoengineer-1.net/mediawiki/index.php?title=Nanotube_generator_dialog
for notes about what's going on here.
"""

__author__ = "Will"

from NanotubeGeneratorDialog import nanotube_dialog
from math import atan2, sin, cos, pi
import assembly, chem, bonds, Utility
from chem import molecule, Atom, gensym
import env
from HistoryWidget import redmsg, greenmsg
from qt import Qt, QApplication, QCursor, QDialog, QDoubleValidator, QValidator
from VQT import dot
import string
from widgets import double_fixup
from debug import Stopwatch, objectBrowse
from Utility import Group
from GeneratorBaseClass import GeneratorBaseClass

sqrt3 = 3 ** 0.5

class Chirality:

    # Nanotube bond length according to Dresselhaus, M. S.,
    # Dresselhaus, G., Eklund, P. C. "Science of Fullerenes and Carbon
    # Nanotubes" Academic Press: San Diego, CA, 1995; pp. 760.
    BONDLENGTH = 1.421  # angstroms

    # It's handy to have slightly a bigger version, and its square.
    MAXLEN = 1.2 * BONDLENGTH
    MAXLENSQ = MAXLEN ** 2

    def __init__(self, n, m):
        self.n, self.m = n, m
        x = (n + 0.5 * m) * sqrt3
        y = 1.5 * m
        angle = atan2(y, x)
        twoPiRoverA = (x**2 + y**2) ** .5
        AoverR = (2 * pi) / twoPiRoverA
        self.__cos = cos(angle)
        self.__sin = sin(angle)
        # time to get the constants
        s, t = self.x1y1(0,0)
        u, v = self.x1y1(1./3, 1./3)
        w, x = self.x1y1(0,1)
        F = (t - v)**2
        G = 2 * (1 - cos(AoverR * (s - u)))
        H = (v - x)**2
        J = 2 * (1 - cos(AoverR * (u - w)))
        L = self.BONDLENGTH
        denom = F * J - G * H
        self.R = (L**2 * (F - H) / denom) ** .5
        self.B = (L**2 * (J - G) / denom) ** .5
        self.A = self.R * AoverR

    def x1y1(self, n, m):
        c, s = self.__cos, self.__sin
        x = (n + .5*m) * sqrt3
        y = 1.5 * m
        x1 = x * c + y * s
        y1 = -x * s + y * c
        return (x1, y1)

    def mlimits(self, y3min, y3max, n):
        if y3max < y3min:
            y3min, y3max = y3max, y3min
        B, c, s = self.B, self.__cos, self.__sin
        P = sqrt3 * B * s
        Q = 1.5 * B * (c - s / sqrt3)
        m1, m2 = (y3min + P * n) / Q, (y3max + P * n) / Q
        return int(m1-1.5), int(m2+1.5)

    def xyz(self, n, m):
        x1, y1 = self.x1y1(n, m)
        x2, y2 = self.A * x1, self.B * y1
        R = self.R
        x3 = R * sin(x2/R)
        z3 = R * cos(x2/R)
        return (x3, y2, z3)

    def populate(self, mol, length):

        def add(element, x, y, z):
            atm = Atom(element, chem.V(x, y, z), mol)
            atm.set_atomtype_but_dont_revise_singlets("sp2")
            return atm

        evenAtomDict = { }
        oddAtomDict = { }
        bondDict = { }
        mfirst = [ ]
        mlast = [ ]

        for n in range(self.n):
            mmin, mmax = self.mlimits(-.5 * length, .5 * length, n)
            mfirst.append(mmin)
            mlast.append(mmax)
            for m in range(mmin, mmax+1):
                x, y, z = self.xyz(n, m)
                atm = add("C", x, y, z)
                evenAtomDict[(n,m)] = atm
                bondDict[atm] = [(n,m)]
                x, y, z = self.xyz(n+1./3, m+1./3)
                atm = add("C", x, y, z)
                oddAtomDict[(n,m)] = atm
                bondDict[atm] = [(n+1, m), (n, m+1)]

        # m goes axially along the nanotube, n spirals around the tube
        # like a barber pole, with slope depending on chirality. If we
        # stopped making bonds now, there'd be a spiral strip of
        # missing bonds between the n=self.n-1 row and the n=0 row.
        # So we need to connect those. We don't know how the m values
        # will line up, so the first time, we need to just hunt for the
        # m offset. But then we can apply that constant m offset to the
        # remaining atoms along the strip.
        n = self.n - 1
        mmid = (mfirst[n] + mlast[n]) / 2
        atm = oddAtomDict[(n, mmid)]
        class FoundMOffset(Exception): pass
        try:
            for m2 in range(mfirst[0], mlast[0] + 1):
                atm2 = evenAtomDict[(0, m2)]
                diff = atm.posn() - atm2.posn()
                if dot(diff, diff) < self.MAXLENSQ:
                    moffset = m2 - mmid
                    # Given the offset, zipping up the rows is easy.
                    for m in range(mfirst[n], mlast[n]+1):
                        atm = oddAtomDict[(n, m)]
                        bondDict[atm].append((0, m + moffset))
                    raise FoundMOffset()
            # If we get to this point, we never found m offset.
            # If this ever happens, it indicates a bug.
            raise Exception, "can't find m offset"
        except FoundMOffset:
            pass

        # Use the bond information to bond the atoms
        for (dict1, dict2) in [(evenAtomDict, oddAtomDict),
                               (oddAtomDict, evenAtomDict)]:
            for n, m in dict1.keys():
                atm = dict1[(n, m)]
                for n2, m2 in bondDict[atm]:
                    try:
                        atm2 = dict2[(n2, m2)]
                        if not bonds.bonded(atm, atm2):
                            bonds.bond_atoms(atm, atm2, bonds.V_GRAPHITE)
                    except KeyError:
                        pass

# GeneratorBaseClass must come BEFORE the dialog in the list of parents
class NanotubeGenerator(GeneratorBaseClass, nanotube_dialog):

    cmd = greenmsg("Insert Nanotube: ")
    sponsor_keyword = 'Nanotubes'

    # We now support multiple keywords in a list or tuple
    # sponsor_keyword = ('Nanotubes', 'Carbon')

    # pass window arg to constructor rather than use a global, wware 051103
    def __init__(self, win):
        nanotube_dialog.__init__(self, win) # win is parent.  Fixes bug 1089.  Mark 051119.
        GeneratorBaseClass.__init__(self, win)
        # Validator for the length linedit widget.
        self.validator = QDoubleValidator(self)
        # Range of nanotube length (0-1000, 2 decimal places)
        self.validator.setRange(0.0, 1000.0, 2)
        self.length_linedit.setValidator(self.validator)
        self.cursor_pos = 0
        self.lenstr = str(self.length_linedit.text())

    ###################################################
    # How to build this kind of structure, along with
    # any necessary helper functions

    def gather_parameters(self):
        n = self.chirality_n_spinbox.value()
        m = self.chirality_m_spinbox.value()
        assert n > 0, 'n cannot be zero'
        assert n >= m, 'n cannot be smaller than m'
        # Get length from length_linedit and make sure it is not zero.
        # length_linedit's validator makes sure this has a valid number (float).  
        # The only exception is when there is no text.  Mark 051103.
        if self.length_linedit.text():
            self.length = string.atof(str(self.length_linedit.text()))
        else:
            self.length = 0.0
            raise Exception("Please specify a valid length.")
        length = self.length
        return (n, m, length)

    def build_struct(self, params):
        n, m, length = params
        # This can take a few seconds. Inform the user.
        # 100 is a guess on my part. Mark 051103.
        if length > 100.0:
            env.history.message(self.cmd + "Creating nanotube. This may take a moment...")
        else: # Nanotubes under 100 Angstroms shouldn't take long.
            env.history.message(self.cmd + "Creating nanotube.")
        self.chirality = Chirality(n, m)
        PROFILE = False
        if PROFILE:
            sw = Stopwatch()
            sw.start()
        xyz = self.chirality.xyz
        mol = molecule(self.win.assy, gensym("Nanotube-"))
        atoms = mol.atoms
        mlimits = self.chirality.mlimits
        # populate the tube with some extra carbons on the ends
        # so that we can trim them later
        self.chirality.populate(mol, length + 4 * Chirality.MAXLEN)

        # Judgement call: because we're discarding carbons with funky
        # valences, we will necessarily get slightly more ragged edges
        # on nanotubes. This is a parameter we can fiddle with to
        # adjust the length. My thought is that users would prefer a
        # little extra length, because it's fairly easy to trim the
        # ends, but much harder to add new atoms on the end.
        #LENGTH_TWEAK = 0.5 * Chirality.BONDLENGTH
        LENGTH_TWEAK = Chirality.BONDLENGTH

        # trim all the carbons that fall outside our desired length
        # by doing this, we are introducing new singlets
        for atm in atoms.values():
            y = atm.posn()[1]
            if (y > .5 * (length + LENGTH_TWEAK) or
                y < -.5 * (length + LENGTH_TWEAK)):
                atm.kill()

        # trim all the carbons that only have one carbon neighbor
        for atm in atoms.values():
            if not atm.is_singlet() and len(atm.realNeighbors()) == 1:
                atm.kill()

        if PROFILE:
            t = sw.now()
            env.history.message(greenmsg("%g seconds to build %d atoms" %
                                         (t, len(atoms.values()))))
        return mol

    def length_fixup(self):
        '''Slot for the Length linedit widget.
        This gets called each time a user types anything into the widget.
        '''
        self.lenstr = double_fixup(self.validator, self.length_linedit.text(), self.lenstr)
        self.length_linedit.setText(self.lenstr)

    ###################################################
    # The done message

    def done_msg(self):
        return "Nanotube created."

    ###################################################
    # Special UI things that still must be implemented
    def toggle_nt_distortion_grpbox(self):
        print "nanotube_dialog.toggle_nt_distortion_grpbox(): Not implemented yet"

    def toggle_nt_parameters_grpbox(self):
        print "nanotube_dialog.toggle_nt_parameters_grpbox(): Not implemented yet"

    def toggle_mwcnt_grpbox(self):
        print "nanotube_dialog.toggle_mwcnt_grpbox(): Not implemented yet"

    def enter_WhatsThisMode(self):
        print "nanotube_dialog.enter_WhatsThisMode(): Not implemented yet"

    def changeLength(self):
        print "nanotube_dialog.changeLength(): Not implemented yet"

    def nChanged(self,a0):
        print "nanotube_dialog.nChanged(const QString&): Not implemented yet"

    def mChanged(self,a0):
        print "nanotube_dialog.mChanged(const QString&): Not implemented yet"

    def bondLengthChanged(self):
        print "nanotube_dialog.bondLengthChanged(): Not implemented yet"

    def previewClicked(self):
        print "nanotube_dialog.previewClicked(): Not implemented yet"

    def zDistortChanged(self):
        print "nanotube_dialog.zDistortChanged(): Not implemented yet"

    def xyDistortChanged(self):
        print "nanotube_dialog.xyDistortChanged(): Not implemented yet"
