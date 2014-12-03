'''
Created on Oct 29, 2014

@author: venturf2
'''

import wx
from tip_calculator import tip_calculator_main

class main(wx.App):
    def OnInit(self):
        self.m_frame = tip_calculator_main(None)
        self.m_frame.Show()
        self.SetTopWindow(self.m_frame)
        return True

app = main(0)
app.MainLoop()