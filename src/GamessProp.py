# Copyright (c) 2005 Nanorex, Inc.  All rights reserved.
'''
GamessProp.py

$Id$
'''
__author__ = "Mark"


# Ask Bruce where all this should ultimately live.

# This is the GAMESS UI widget default settings (for energy).

ui={'comment':'','runtyp':0,'scftyp':0, 'icharg':0, 'mult':0, 'gbasis':0, 'ecm':0, 'dfttyp':0, 'gridsize':1, 'ncore':0,
        'conv':1, 'rmsdconv':1, 'iterations':50, 'memory':70, 'extrap':1, 'dirscf':1, 'damp':0, 'shift':0, 'diis':0,'soscf':0,'rstrct':0,
        'gbasisname':'AM1'}

# These are the GAMESS parms set defaults (for energy).

# $CONTRL group section ####################################
#
# The general form for the $CONTRL group is (keyword order does not matter):
#
#   $CONTRL
#   runtyp=energy coord=unique scftyp=rhf icharg=1 mult=1 mplevl=0 
#   maxit=200 inttyp=pople icut=11 qmttol=1.0E-6
#   $END
#
# $CONTRL group keywords and their default values.
contrl={'runtyp':'energy', 'coord':'unique', 'scftyp':'RHF', 'icharg':0, 'mult':1, 'mplevl':'0', 
        'maxit':50, 'icut':11, 'inttyp':'hondo', 'qmttol':'1.0E-6', 'dfttyp':0, 'nprint':9}
# Note: The 'dfttyp' keyword in the $CONTRL group is only valid for PC GAMESS.

# $CONTRL keywords and their optional values 
runtyp=['energy', 'optimize'] # RUNTYP
scftyp=['RHF', 'UHF', 'ROHF'] # SCFTYP
mplevl=[ 0, 0, '2'] # MPLEVL: None=0, DFT=0, MP2='2'
inttyp=['pople', 'pople', 'hondo'] # Set by EMC, None=POPLE, DFT=POPLE, MP2=HONDO
nprint=-5,-2,7,8,9 # Not currently used. nprint is always 9 for now.

# $SCF group section ####################################
#
# The general form for the $SCF group is (keyword order does not matter):
#
#   $SCF
#   conv=10E-05 coord=unique extrap=.T. dirscf=.T. damp=.F shift=.F. diis=.T. soscf=.F. rstrct=.F.
#   $END
#
# $SCF group keywords and their default values.
scf={'conv':1, 'nconv':1, 'extrap':'.T.','dirscf':'.T.', 'damp':'.F.', 'shift':'.F.', 'diis':'.T.',
     'soscf':'.F.','rstrct':'.F.'}
# Note: Keyword 'conv' is used by GAMESS, 'nconv' is used by PC GAMESS.

# CONV keyword and its optional values
conv='10E-04','10E-05','10E-06','10E-07' # Density Convergence

# Useful true or false tuple.
tf='.F.', '.T.' # True/False for SCF parameters

# $SYSTEM group section ####################################
#
# The general form for the $SYSTEM group is:
#
#   $SYSTEM
#   timlim=1000 memory=70000000
#   $END
#
# $SYSTEM group keywords and their default values.
system={'timlim':1000, 'memory':70000000}

# $MP2 group section ####################################
#
# The general form for the $MP2 group is (keyword order does not matter):
#
#   $MP2
#   ncore=0
#   $END
#
# The $MP2 group is written only when the Electron Correlation Method = MP2.
# To include core electrons, we add the keyword NCORE=0.
# To exclude core electrons, we leave NCORE out of the $MP2 group altogether.
# So, with the checkbox not checked, ncore=0, and the NCORE keyword isn't written.
# With the checkbox checked, ncore='0' (string type), NCORE=0 is written.  Mark 050528.
mp2={'ncore':0} # Core electrons for MP2
ncore=[0, '0'] # Core electrons: Not included=0, Included='0'. 

# Useful Electron Correlation Method variables.
ecm=['None', 'DFT', 'MP2'] 
DFT=1
MP2=2

# $DFT group section (GAMESS only) ##############################
#
# The general form for the $DFT group is (keyword order does not matter):
#
#   $DFT
#    dfttyp=SLATER nrad=96 nthe=12 nphi=24 switch=3.0E-04
#   $END
#
# $DFT group keywords and their default values.
dft={'dfttyp':0, 'nrad':0}
# Note: In PC GAMESS, the $DFT group contains the grid size parameters 
# only, and the DFTTYP keyword is placed in the $CONTRL group.

# DFTTYP functions for GAMESS, specified by the DFTTYP keyword in the $DFT group.
# The PC GAMESS DFTTYP functions are different (see pcgms_dfttyp_items).
# The DFTTYP keyword values are the same without the '(x)' text.  The selected
# item is written to the $DFT group like this: dfttyp=SLATER
gms_dfttyp_items='SLATER (E)','BECKE (E)','GILL (E)','PBE (E)','VWN (C)', \
    'LYP (C)', 'OP (C)', 'SVWN (E+C)', 'SLYP (E+C)', 'SOP (E+C)', 'BVWN (E+C)', \
    'BLYP (E+C)', 'BOP (E+C)', 'GVWN (E+C)', 'GLYP (E+C)', 'GOP (E+C)', \
    'PBEVWN (E+C)', 'PBELYP (E+C)', 'PBEOP (E+C)', 'BHHLYP (H)', 'B3LYP (H)'

# DFTTYP functions for PC GAMESS. These are different for GAMESS.
# The DFTTYP keyword values are the same without the '(x)' text.                
pcgms_dfttyp_items = 'SLATER (E)','B88 (E)','GILL96 (E)','XPBE96 (E)','LYP (C)', \
    'VWN1RPA (C)','VWN5 (C)','PW91LDA (C)','CPBE96 (C)','CPW91 (C)', \
    'SLYP (E+C)','BLYP (E+C)','GLYP (E+C)','SVWN1RPA (E+C)', \
    'BVWN1RPA (E+C)','VWN5 (E+C)','BVWN5 (E+C)','PBE96 (E+C)', \
    'PBEPW91 (E+C)','B3LYP1 (H)','BELYP5 (H)','BHHLYP (H)','PBE0 (H)', \
    'PBE1PW91 (H)','B3PW91 (H)'

# The 5 DFT grid size parameters for:
#   - Course
#   - Default, 
#   - Fine
#   - Very Fine
#   - Army Grade.
# These are the $DFT grid size parameters for GAMESS.
gms_gridsize= '=48 nthe=12 nphi=24 switch=1.0E-03', \
                '96 nthe=12 nphi=24 switch=3.0E-04', \
                '96 nthe=24 nphi=48 switch=3.0E-04', \
                '96 nthe=36 nphi=72 switch=3.0E-04', \
                '96 nthe=36 nphi=72 switch=3.0E-04'
# Note: the first number is the 'nrad' parm. 'nrad=' is printed by the prin1 method.
# Also, Damian needs to supply parameters for "Very Fine" (Army Grade used twice).
                
# These are the $DFT grid size parameters for PC GAMESS.
pcgms_gridsize='48 lmax=19', \
                            '63 lmax=29', \
                            '63 lmax=53', \
                            '95 lmax=89', \
                            '128 lmax=131'
# Note: the first number is the 'nrad' parm. 'nrad=' is printed by the prin1 method.

# $GUESS group section ##############################
#
# The general form for the $GUESS group is:
#
#   $GUESS
#    guess=huckel
#   $END
#
# $GUESS group keywords and their default values.
guess={'guess':'huckel'}

# The GUESS keyword and its optional values
guess_keyword=['huckel', 'moread']
# Note: Writing the 'guess' keyword requires special case code in the prin1 method 
# since its group name is the same ('guess'). Mark 050529
    
# $STATPT group section ##############################
#
# The general form for the $STATPT group is:
#
#   $STATPT
#    hess=guess
#   $END
#
# $STATPT group keywords and their default values.
statpt={'hess':'guess', 'opttol':1}

# The HESS keyword and its optional values
hess=['guess', 'read']

# OPTTOL keyword and its optional values
opttol=[0.0001, 0.00001, 0.000001, 0.0000001] # RMSD Convergence

# $BASIS group section ##############################
#
# The general form for the $BASIS group is:
#
#   $BASIS
#   gbasis=AM1 NGAUSS=0 NDFUNC=0 NPFUNC=0 NFFUNC=0 DIFFSP=.F. DIFFS=.F.
#   $END
#
# $BASIS group keywords and their default values.
basis={'gbasis':'AM1'}

# The GBASIS keyword and its optional values
gbasis='AM1 NGAUSS=0 NDFUNC=0 NPFUNC=0 NFFUNC=0 DIFFSP=.F. DIFFS=.F.', \
    'PM3 NGAUSS=0 NDFUNC=0 NPFUNC=0 NFFUNC=0 DIFFSP=.F. DIFFS=.F.', \
    'STO NGAUSS=3 NDFUNC=0 NPFUNC=0 NFFUNC=0 DIFFSP=.F. DIFFS=.F.', \
    'STO NGAUSS=6 NDFUNC=0 NPFUNC=0 NFFUNC=0 DIFFSP=.F. DIFFS=.F.', \
    'N21 NGAUSS=3 NDFUNC=0 NPFUNC=0 NFFUNC=0 DIFFSP=.F. DIFFS=.F.', \
    'N21 NGAUSS=3 NDFUNC=1 NPFUNC=0 NFFUNC=0 DIFFSP=.F. DIFFS=.F.', \
    'N31 NGAUSS=6 NDFUNC=0 NPFUNC=0 NFFUNC=0 DIFFSP=.F. DIFFS=.F.', \
    'N31 NGAUSS=6 NDFUNC=1 NPFUNC=0 NFFUNC=0 DIFFSP=.F. DIFFS=.F.', \
    'N31 NGAUSS=6 NDFUNC=1 NPFUNC=1 NFFUNC=0 DIFFSP=.F. DIFFS=.F.', \
    'N31 NGAUSS=6 NDFUNC=1 NPFUNC=0 NFFUNC=0 DIFFSP=.T. DIFFS=.F.', \
    'N31 NGAUSS=6 NDFUNC=1 NPFUNC=1 NFFUNC=0 DIFFSP=.T. DIFFS=.F.', \
    'N31 NGAUSS=6 NDFUNC=1 NPFUNC=0 NFFUNC=0 DIFFSP=.T. DIFFS=.T.', \
    'N31 NGAUSS=6 NDFUNC=1 NPFUNC=1 NFFUNC=0 DIFFSP=.T. DIFFS=.T.', \
    'N311 NGAUSS=6 NDFUNC=0 NPFUNC=0 NFFUNC=0 DIFFSP=.F. DIFFS=.F.', \
    'N311 NGAUSS=6 NDFUNC=1 NPFUNC=0 NFFUNC=0 DIFFSP=.F. DIFFS=.F.', \
    'N311 NGAUSS=6 NDFUNC=1 NPFUNC=1 NFFUNC=0 DIFFSP=.F. DIFFS=.F.', \
    'N311 NGAUSS=6 NDFUNC=1 NPFUNC=0 NFFUNC=0 DIFFSP=.T. DIFFS=.F.', \
    'N311 NGAUSS=6 NDFUNC=1 NPFUNC=1 NFFUNC=0 DIFFSP=.T. DIFFS=.F.', \
    'N311 NGAUSS=6 NDFUNC=1 NPFUNC=0 NFFUNC=0 DIFFSP=.T. DIFFS=.T.', \
    'N311 NGAUSS=6 NDFUNC=1 NPFUNC=1 NFFUNC=0 DIFFSP=.T. DIFFS=.T.'

from qt import *
import sys, os, time
from GamessPropDialog import *
from ServerManager import ServerManager
from HistoryWidget import redmsg
from files_gms import insertgms
from debug import print_compact_traceback
        
class GamessProp(GamessPropDialog):
    '''The Gamess Jig Properties dialog used for:
    - running a GAMESS energy calculation on a structure (group of atoms).
    - running a GAMESS optimization on a structure.
    - setting and saving the GAMESS parameters used for an energy calculation or optimization.
    '''
       
    def __init__(self):
        GamessPropDialog.__init__(self, modal=True)
        self.sManager = ServerManager()
        self.servers = self.sManager.getServers()
        self.server = self.servers[0]
        
        
    def showDialog(self, job):
        '''Display the GAMESS Jig Properties dialog'''
        self.gamessJig =  job.gamessJig
        self.job = job
        self.pset = self.gamessJig.pset
        self.win = self.gamessJig.assy.w
        self.glpane = self.gamessJig.assy.o
        self.history = self.gamessJig.assy.w.history
        
        if self._setup(): return
        self.exec_loop()


    ######Private or helper methods###############################
    def _setup(self):
        ''' Setup widgets to initial (default or defined) values. Return True on error.
        '''
        gamess = self.gamessJig #  In case we cancel later (not implemented yet)
        
        self.originalColor = self.gamessJig.normcolor

        #To fix bug 684
        #if gamess.is_disabled():
        #    self.run_job_btn.setEnabled(False)
        #else:
        #    self.run_job_btn.setEnabled(True)
        
        # Init the top widgets (name, runtyp drop box, comment)
        self.name_linedit.setText(gamess.name)
        self.runtyp_combox.setCurrentItem(self.pset.ui.runtyp) # RUNTYP
        self.calculate_changed(self.pset.ui.runtyp)
        self.comment_linedit.setText(self.pset.ui.comment)
        
        # Color chooser.
        self.colorPixmapLabel.setPaletteBackgroundColor(
            QColor(int(gamess.normcolor[0]*255), 
                         int(gamess.normcolor[1]*255), 
                         int(gamess.normcolor[2]*255)))
        
        # Electronic Structure Properties section.
        self.scftyp_btngrp.setButton(self.pset.ui.scftyp) # RHF, UHF, or ROHF
        self.icharg_spinbox.setValue(self.pset.ui.icharg) # Charge
        self.multi_combox.setCurrentItem(self.pset.ui.mult) # Multiplicity
        # Disable RHF if multiplicity is not the first item.
        if self.pset.ui.mult == 0:
            self.rhf_radiobtn.setEnabled(1) # Enable RHF
        else:
            self.rhf_radiobtn.setEnabled(0) # Disable RHF
        
        # System Memory and Usage
        self.dirscf_checkbox.setChecked(self.pset.ui.dirscf) # DIRSCF
        self.memory_spinbox.setValue(self.pset.ui.memory) # Memory
        
        # Electron Correlation Method and Basis Set
        ecm = self.pset.ui.ecm
        self.ecm_btngrp.setButton(self.pset.ui.ecm) # None, DFT or MP2
        self.set_ecmethod(self.pset.ui.ecm) # None, DFT or MP2
        self.gbasis_combox.setCurrentItem(self.pset.ui.gbasis) # Basis set
        
        # Load the combo box with all the valid DFT functions.  
        self._load_dfttyp_combox()
        self.dfttyp_combox.setCurrentItem(self.pset.ui.dfttyp) # DFT Functional
        self.gridsize_combox.setCurrentItem(self.pset.ui.gridsize) # Grid Size
        self.core_electrons_checkbox.setChecked(self.pset.ui.ncore) # Include core electrons
            
        # Convergence Criteria
        self.density_conv_combox.setCurrentItem(self.pset.ui.conv) # Density Convergence
        self.rmsd_combox.setCurrentItem(self.pset.ui.rmsdconv) # RMSD Convergence
        self.iterations_spinbox.setValue(self.pset.ui.iterations) # Iterations

# These have been removed per discussions with Damian.
# Mark 050628
#        self.extrap_checkbox.setChecked(self.pset.ui.extrap) # EXTRAP
#        self.damp_checkbox.setChecked(self.pset.ui.damp) # DAMP
#        self.diis_checkbox.setChecked(self.pset.ui.diis) # DIIS
#        self.shift_checkbox.setChecked(self.pset.ui.shift) # SHIFT
#        self.soscf_checkbox.setChecked(self.pset.ui.soscf) # SOSCF
#        self.rstrct_checkbox.setChecked(self.pset.ui.rstrct) # RSTRCT
        
        # Load the server combo box
        #self._reloadServerList() # Not used in A6.  Mark.
        
        # If there is an error, return 1. NIY.
        return 0
 
 
    def _reloadServerList(self):
        """ Load the server combo box"""
        self.server_combox.clear()
        for s in self.servers:
            self.server_combox.insertItem(s.hostname + "-" + s.engine)
        if self.server not in self.servers:
            self.server = self.servers[0]
        indx = self.servers.index(self.server)
        self.server_combox.setCurrentItem(indx)    
               
        
    def _rename(self):
        '''Rename the jig.
        '''
        self.gamessJig.name = str(self.name_linedit.text())


    def _load_dfttyp_combox(self):
        '''Load list of DFT function in a combobox widget'''
        self.dfttyp_combox.clear() # Clear all combo box items
        if self.server.engine == 'GAMESS':
            for f in gms_dfttyp_items:
                self.dfttyp_combox.insertItem(f)
        elif self.server.engine == 'PC GAMESS':
            for f in pcgms_dfttyp_items:
                self.dfttyp_combox.insertItem(f)
        else:
            print "load_dfttyp_combox: Unknown GAMESS Version.  Loading GAMES DFT functionals."
            for f in gms_dfttyp_items:
                self.dfttyp_combox.insertItem(f)


    def _update_gbasis_list(self, val):
        '''Add/remove AM1 and PM3 to/from the gbasis list. '''
        citem = self.gbasis_combox.currentItem()
        if val == DFT or val == MP2:
            if self.gbasis_combox.count() == 18:
                self.gbasis_combox.removeItem(0)
                self.gbasis_combox.removeItem(0)
                self.gbasis_combox.setCurrentItem(max(0, citem-2))
        else:
            if self.gbasis_combox.count() != 18:
                self.gbasis_combox.insertItem("PM3",0)
                self.gbasis_combox.insertItem("AM1",0)
                self.gbasis_combox.setCurrentItem(citem+2)

    
    def _save_ui_settings(self):
        '''Save the UI settings in the Gamess jig pset.  There is one setting for each pset.
        '''
        self._rename()
        self.pset.ui.comment = str(self.comment_linedit.text()) # Description
        self.pset.ui.runtyp = self.runtyp_combox.currentItem() # RUNTYP = Energy or Optimize
        
        # Electronic Structure Props and Basis Set section.
        self.pset.ui.scftyp = self.scftyp_btngrp.selectedId() # SCFTYP = RHF, UHF, or ROHF
        self.pset.ui.icharg = self.icharg_spinbox.value() # Charge
        self.pset.ui.mult = self.multi_combox.currentItem() # Multiplicity
        
        # System Memory and Usage
        self.pset.ui.memory = self.memory_spinbox.value() # Memory
        self.pset.ui.dirscf = self.dirscf_checkbox.isChecked() # DIRSCF
        
        # Electron Correlation Method
        self.pset.ui.ecm = self.ecm_btngrp.selectedId() # None, DFT or MP2
        #self.pset.ui.inttyp = self.ecm_btngrp.selectedId() # INTTYP
        self.pset.ui.gbasis = self.gbasis_combox.currentItem() # Basis Set
        self.pset.ui.gbasisname = str(self.gbasis_combox.currentText())
        self.pset.ui.dfttyp = self.dfttyp_combox.currentItem() # DFT Functional Type
        self.pset.ui.gridsize = self.gridsize_combox.currentItem() # Grid Size
        self.pset.ui.ncore = self.core_electrons_checkbox.isChecked() # Include core electrons
        
        # Convergence Criteria
        self.pset.ui.conv = self.density_conv_combox.currentItem() # Density Convergence
        self.pset.ui.rmsdconv = self.rmsd_combox.currentItem() # RMSD Convergence
        self.pset.ui.iterations = self.iterations_spinbox.value() # Iterations
        
#        self.pset.ui.extrap = self.extrap_checkbox.isChecked() # EXTRAP
#        self.pset.ui.damp = self.damp_checkbox.isChecked() # DAMP
#        self.pset.ui.diis = self.diis_checkbox.isChecked() # DIIS
#        self.pset.ui.shift = self.shift_checkbox.isChecked() # SHIFT
#        self.pset.ui.soscf = self.soscf_checkbox.isChecked() # SOSCF
#        self.pset.ui.rstrct = self.rstrct_checkbox.isChecked() # RSTRCT


    def _save_job_parms(self):
        calculate = ['Energy', 'Optimization']
        self.job.Calculation = calculate[self.pset.ui.runtyp]
        self.job.Description = self.pset.ui.comment
        self.job.server =  self.server
        ##Copy some  attributes from the server object to job description
        self.job.Server_id = self.server.server_id
        self.job.Engine = self.server.engine

    ######End of private or helper methods.########################
    
    ###### Unused methods ###############   
    
    def openServerManager(self):
        """Pop up ServerManagerDialog to edit the properties of the servers."""
        self.sManager.showDialog(self.server)
        self.servers = self.sManager.getServers()
        self._reloadServerList()
        
    def serverChanged(self, si):
        """User has changed server, so update the DFT comboBox. Currently not used."""
        self.server = self.servers[si]
        self._load_dfttyp_combox()
        
    ###### End of unused methods ###############  
    
    ##########Slot methods for some GUI controls################   

    def calculate_changed(self, val):
        '''
        '''
        if val == 0: # Energy
            self.rmsd_lbl.setEnabled(0)
            self.rmsd_combox.setEnabled(0)
            self.iterations_lbl.setEnabled(0)
            self.iterations_spinbox.setEnabled(0)
#            self.extrap_checkbox.setEnabled(0)
#            self.rstrct_checkbox.setEnabled(0)
#            self.damp_checkbox.setEnabled(0)
#            self.diis_checkbox.setEnabled(0)
#            self.shift_checkbox.setEnabled(0)
#            self.soscf_checkbox.setEnabled(0)
        else: # Optimization
            self.rmsd_lbl.setEnabled(1)
            self.rmsd_combox.setEnabled(1)
            self.iterations_lbl.setEnabled(1)
            self.iterations_spinbox.setEnabled(1)
#            self.extrap_checkbox.setEnabled(1)
#            self.rstrct_checkbox.setEnabled(1)
#            self.damp_checkbox.setEnabled(1)
#            self.diis_checkbox.setEnabled(1)
#            self.shift_checkbox.setEnabled(1)
#            self.soscf_checkbox.setEnabled(1)

    def set_multiplicity(self, val):
        '''Enable/disable widgets when user changes Multiplicity.
        '''
        if val != 0:
            if scftyp[self.scftyp_btngrp.selectedId()] != 'RHF':
                self.rhf_radiobtn.setEnabled(0)
                return
            
            ret = QMessageBox.warning( self, "Multiplicity Conflict",
                "If Multiplicity is greater than 1, then <b>UHF</b> or <b>ROHF</b> must be selected.\n"
                "Select Cancel to keep <b>RHF</b>.",
                "&UHF", "&ROHF", "Cancel",
                0, 2 )
            
            if ret==0: # UHF
                self.uhf_radiobtn.toggle()
                self.rhf_radiobtn.setEnabled(0)
                
            elif ret==1: # ROHF
                self.rohf_radiobtn.toggle()
                self.rhf_radiobtn.setEnabled(0)
            
            elif ret==2: # Cancel
                self.multi_combox.setCurrentItem(0)
        
        elif val == 0:
            self.rhf_radiobtn.setEnabled(1)
    
    def set_ecmethod(self, val):
        '''Enable/disable widgets when user changes Electron Correlation Method.
        '''
#        print "set_ecmethod = ", val
        if val == DFT:
            self.dfttyp_label.setEnabled(1)
            self.dfttyp_combox.setEnabled(1)
            self.gridsize_label.setEnabled(1)
            self.gridsize_combox.setEnabled(1)
            self.core_electrons_checkbox.setChecked(0)
            self.core_electrons_checkbox.setEnabled(0)
            
        elif val == MP2:
            self.core_electrons_checkbox.setEnabled(1)
            self.dfttyp_label.setEnabled(0)
            self.dfttyp_combox.setEnabled(0)
            self.gridsize_label.setEnabled(0)
            self.gridsize_combox.setEnabled(0)
            
        else: # None = Hartree-Fock
            self.dfttyp_label.setEnabled(0)
            self.dfttyp_combox.setEnabled(0)
            self.gridsize_label.setEnabled(0)
            self.gridsize_combox.setEnabled(0)
            self.core_electrons_checkbox.setChecked(0)
            self.core_electrons_checkbox.setEnabled(0)
        
        # AM1 and PM3 are not options for DFT or MP2.
        # We have to remove or add them from the combo box.
        self._update_gbasis_list(val)

    def open_tmp_inputfile(self):
        '''Writes a temporary GAMESS inputfile of the current Gamess jig and opens the
        file in an editor.
        '''
        # Make tmp_inputfile filename (i.e. ~/Nanorex/temp/jigname_parms_info.inp)
        from platform import find_or_make_Nanorex_subdir
        tmpdir = find_or_make_Nanorex_subdir('temp')
        basename = self.gamessJig.name + "-" + self.gamessJig.gms_parms_info('_')
        tmp_inputfile = os.path.join(tmpdir, "%s.inp" % basename)
        
        # Write INP file (in ~/Nanorex/temp subdirectory)
        from files_gms import writegms_inpfile
        writegms_inpfile(tmp_inputfile, self.gamessJig)
        
        from platform import open_file_in_editor
        open_file_in_editor(tmp_inputfile, history = self.history)
                
    def run_job(self):
        """Slot method for the 'Save and Run' button """
        
        self.accept()
        
        # Run GAMESS job.  Return value r:
        # 0 = success
        # 1 = job cancelled
        # 2 = job failed.
        r = self.job.launch()
        
        if r==1: # Job was cancelled
            self.history.message( redmsg( "GAMESS job cancelled."))
            return
            
        if r==2: # Job failed.
            self.history.message( redmsg( "GAMESS job failed. Maybe you didn't set the right Gamess executable file. Make sure you can run the same job manually."))
            return
        
        # Job success.  
        fn = self.gamessJig.outputfile
        
        # Print energy or move atoms
        if self.pset.ui.runtyp == 0: #Energy
            self.gamessJig.print_energy()
        else:  # Optimize
            try:
                r = self.gamessJig.move_optimized_atoms()
                # r = insertgms(self.gamessJig.assy, fn)
            except:
                print_compact_traceback( "GamessProp.run_job(): error reading GAMESS OUT file [%s]: " % fn )
                self.history.message( redmsg( "Internal error while inserting GAMESS geometry: " + fn) )
            else:
                if r:
                    self.history.message(redmsg( "Atoms not adjusted."))
                else:
                    self.gamessJig.assy.changed() # The file and the part are not the same.
                    self.gamessJig.print_energy() # Print the final energy from the optimize OUT file, too.
                    self.history.message( "Atoms adjusted.")
                    
    def accept(self):
        """The slot method for the 'Save' button."""
        QDialog.accept(self)
        self._save_ui_settings()
        self.gamessJig.update_gamess_parms() # Update all the GAMESS parameters.
        self._save_job_parms()
        if self.edit_input_file_cbox.isChecked():
            self.open_tmp_inputfile()

    def choose_color(self):
        """The slot method for the 'Choose...' (color) button."""
        color = QColorDialog.getColor(
            QColor(int(self.gamessJig.normcolor[0]*255), 
                         int(self.gamessJig.normcolor[1]*255), 
                         int(self.gamessJig.normcolor[2]*255)),
                         self, "ColorDialog")
                        
        if color.isValid():
            self.colorPixmapLabel.setPaletteBackgroundColor(color)
            self.gamessJig.color = self.gamessJig.normcolor = (color.red() / 255.0, color.green() / 255.0, color.blue() / 255.0)
            self.glpane.gl_update()
                
    def reject(self):
        """The slot method for the 'Cancel' button."""
        QDialog.reject(self)
        self.gamessJig.color = self.gamessJig.normcolor = self.originalColor
        self.gamessJig.cancelled = True
        self.glpane.gl_update()
        
    def whats_this(self):
        from qt import QWhatsThis
        QWhatsThis.enterWhatsThisMode()