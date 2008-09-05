# Copyright 2005-2007 Nanorex, Inc.  See LICENSE file for details. 
"""
Pan mode functionality.

@author:    Mark Sims
@version:   $Id$
@copyright: 2005-2007 Nanorex, Inc.  See LICENSE file for details.
@license:   GPL
"""

from temporary_commands.TemporaryCommand import TemporaryCommand_Overdrawing
from utilities.GlobalPreferences import USE_COMMAND_STACK

# == GraphicsMode part

class PanMode_GM( TemporaryCommand_Overdrawing.GraphicsMode_class ):
    """
    Custom GraphicsMode for use as a component of PanMode.
    """    
    def leftDown(self, event):
        """
        Event handler for LMB press event.
        """
        # Setup pan operation
        farQ_junk, self.movingPoint = self.dragstart_using_GL_DEPTH( event)        
        return
        
    def leftDrag(self, event):
        """
        Event handler for LMB drag event.
        """
        point = self.dragto( self.movingPoint, event)
        self.glpane.pov += point - self.movingPoint
        self.glpane.gl_update()
        return
        
    def update_cursor_for_no_MB(self): # Fixes bug 1638. Mark 3/12/2006.
        """
        Update the cursor for 'Pan' mode.
        """
        self.glpane.setCursor(self.win.PanViewCursor)

    pass

# == Command part

class PanMode(TemporaryCommand_Overdrawing): # TODO: rename to PanTool or PanCommand or TemporaryCommand_Pan or ...
    """
    Encapsulates the Pan tool functionality.
    """
    #Temporary attr 'command_porting_status. See baseCommand for details.
    command_porting_status =  None
    
    # class constants
    
    commandName = 'PAN'
    featurename = "Pan Tool"
    from utilities.constants import CL_VIEW_CHANGE
    command_level = CL_VIEW_CHANGE

    GraphicsMode_class = PanMode_GM
    
    if not USE_COMMAND_STACK:
        def init_gui(self):
            self.win.panToolAction.setChecked(1) # toggle on the Pan Tool icon
            return    
            
        def restore_gui(self):
            self.win.panToolAction.setChecked(0) # toggle off the Pan Tool icon
        
    #START new command API methods==============================================   
    def command_enter_misc_actions(self):
        """
        See superclass method for documentation
        """
        self.win.panToolAction.setChecked(True)
    
    def command_exit_misc_actions(self):
        """
        See superclass method for documentation
        """
        self.win.panToolAction.setChecked(False)
    #END new command API methods==============================================
    pass

# end
