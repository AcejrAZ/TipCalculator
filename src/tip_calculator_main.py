'''
Created on Oct 29, 2014

@author: venturf2
'''

import wx
from tip_calculator import controller_tip_calculator

class main(wx.App):
    def OnInit(self):
        self.m_frame = controller_tip_calculator(None)
        self.m_frame.Show()
        self.SetTopWindow(self.m_frame)
        return True

app = main(0)
app.MainLoop()