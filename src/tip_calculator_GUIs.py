'''
Created on Oct 29, 2014

@author: venturf2
'''
import wx
import wx.xrc
import string

class CharValidator(wx.PyValidator):
    ''' Validates data as it is entered into the text controls. '''

    def __init__(self, flag):
        wx.PyValidator.__init__(self)
        self.flag = flag
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        '''Required Validator method'''
        return CharValidator(self.flag)

    def Validate(self, win):
        return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True

    def OnChar(self, event):
        keycode = int(event.GetKeyCode())
        allowed_keycodes=[8,13,46]
        if keycode < 256:
            key = chr(keycode)
            if self.flag == 'no-alpha' and\
                key not in string.digits and\
                keycode not in allowed_keycodes:
                return
            if self.flag == 'no-digit' and key in string.digits:
                return
        event.Skip()

class tip_calculator_mainframe(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY,
                          title=u"Tip Splitting Calculator",
                          pos=wx.DefaultPosition, size=wx.Size(350, 560),
                          style=wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
        self.advanced=[]
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        titlesizer = wx.GridBagSizer(0, 0)
        titlesizer.SetFlexibleDirection(wx.BOTH)
        titlesizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_statictext2 = wx.StaticText(self, wx.ID_ANY,
                                           u"Tip Splitting Calculator",
                                           wx.DefaultPosition, wx.DefaultSize,
                                           wx.ALIGN_CENTRE|wx.DOUBLE_BORDER)
        self.m_statictext2.Wrap(-1)
        titlesizer.Add(self.m_statictext2, wx.GBPosition(0, 0), wx.GBSpan(1, 3),
                       wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 5)

        quality_service_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY,
                                                               wx.EmptyString),
                                                  wx.VERTICAL)

        sizer_quality = wx.GridBagSizer(0, 0)
        sizer_quality.SetFlexibleDirection(wx.BOTH)
        sizer_quality.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_statictext4 = wx.StaticText(self, wx.ID_ANY,
                                            u"Quality of Service (%)",
                                            wx.DefaultPosition, wx.DefaultSize,
                                            wx.ALIGN_CENTRE)
        self.m_statictext4.Wrap(-1)
        sizer_quality.Add(self.m_statictext4, wx.GBPosition(0, 0),
                           wx.GBSpan(1, 1), wx.ALL, 5)

        self.tip_tailor = wx.CheckBox(self, wx.ID_ANY, u"Tailor Tip?",
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.tip_tailor.SetToolTipString(u"Tailor the tip percentage "
                                            "for each person?")

        sizer_quality.Add(self.tip_tailor, wx.GBPosition(0, 1),
                           wx.GBSpan(1, 1), wx.ALL, 5)

        quality_service_sizer.Add(sizer_quality, 0, wx.ALIGN_CENTER, 5)

        self.sizer_tip_percentage = wx.GridBagSizer(0, 0)
        self.sizer_tip_percentage.SetFlexibleDirection(wx.BOTH)
        self.sizer_tip_percentage.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        self.tip_min_default="0"
        self.tip_min = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition,
                                   wx.Size(60, -1), wx.TE_CENTRE,
                                   validator=CharValidator('no-alpha'))
        self.tip_min.SetMaxLength(5)
        self.tip_min.SetToolTipString(u"Minimum Percentage for Tips")
        self.advanced.append(self.tip_min)

        self.sizer_tip_percentage.Add(self.tip_min, wx.GBPosition(1, 0),
                     wx.GBSpan(1, 1), wx.ALIGN_RIGHT|wx.ALIGN_TOP, 5)

        self.tip_percentage = wx.Slider(self, wx.ID_ANY,
                                        5,
                                        0,
                                        10,
                                        wx.DefaultPosition,
                                        wx.DefaultSize, wx.SL_LABELS)
        self.tip_percentage.SetToolTipString(u"The quality of service"
                                                "on a scale of 1-10. "
                                                "\n(Larger number is "
                                                "better service.)")

        self.sizer_tip_percentage.Add(self.tip_percentage, wx.GBPosition(0, 1),
                     wx.GBSpan(2, 1), wx.ALL, 5)

        self.tip_max = wx.TextCtrl(self, wx.ID_ANY,
                                   u"20",
                                   wx.DefaultPosition, wx.Size(60, -1),
                                   wx.TE_CENTRE,
                                   validator=CharValidator('no-alpha'))
        self.tip_max_default="20"
        self.tip_max.SetMaxLength(5)
        self.advanced.append(self.tip_max)
        self.tip_max.SetToolTipString(u"Maximum Percentage for Tips")

        self.sizer_tip_percentage.Add(self.tip_max, wx.GBPosition(1, 2),
                     wx.GBSpan(1, 1), wx.ALIGN_LEFT|wx.ALIGN_TOP, 5)

        self.m_statictext6 = wx.StaticText(self, wx.ID_ANY, u"Tip Min",
                                           wx.DefaultPosition, wx.DefaultSize,
                                           wx.ALIGN_CENTRE)
        self.m_statictext6.Wrap(-1)
        self.advanced.append(self.m_statictext6)
        self.sizer_tip_percentage.Add(self.m_statictext6, wx.GBPosition(0, 0),
                     wx.GBSpan(1, 1),
                     wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT,
                     5)

        self.m_statictext7 = wx.StaticText(self, wx.ID_ANY,
                                           u"Tip Max",
                                           wx.DefaultPosition, wx.DefaultSize,
                                           wx.ALIGN_CENTRE)
        self.advanced.append(self.m_statictext7)
        self.m_statictext7.Wrap(-1)
        self.sizer_tip_percentage.Add(self.m_statictext7, wx.GBPosition(0, 2),
                     wx.GBSpan(1, 1), wx.ALIGN_BOTTOM|wx.ALIGN_LEFT, 5)


        quality_service_sizer.Add(self.sizer_tip_percentage, 0,
                                  wx.ALIGN_CENTER, 5)


        titlesizer.Add(quality_service_sizer, wx.GBPosition(2, 0),
                       wx.GBSpan(1, 3), wx.EXPAND, 5)

        sizer_bill = wx.GridBagSizer(0, 0)
        sizer_bill.SetFlexibleDirection(wx.BOTH)
        sizer_bill.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_statictext8 = wx.StaticText(self, wx.ID_ANY, u"Bill Total ($)",
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_statictext8.Wrap(-1)
        sizer_bill.Add(self.m_statictext8, wx.GBPosition(0, 0),
                       wx.GBSpan(1, 1), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)


        sizer_bill.AddSpacer((172, 0), wx.GBPosition(0, 1),
                              wx.GBSpan(1, 1), wx.EXPAND, 5)


        titlesizer.Add(sizer_bill, wx.GBPosition(3, 0),
                       wx.GBSpan(1, 2), wx.EXPAND, 5)

        self.bill_total = wx.TextCtrl(self, wx.ID_ANY, u"0",
                                      wx.DefaultPosition, wx.Size(60, -1),
                                      wx.TE_CENTRE,
                                      validator=CharValidator('no-alpha'))
        titlesizer.Add(self.bill_total, wx.GBPosition(3, 2),
                       wx.GBSpan(1, 1), wx.ALIGN_CENTER|wx.ALL, 5)

        self.bill_deduct = wx.TextCtrl(self, wx.ID_ANY, u"0",
                                       wx.DefaultPosition, wx.Size(60, -1),
                                       wx.TE_CENTRE,
                                       validator=CharValidator('no-alpha'))
        self.bill_deduct.SetToolTipString(u"Any coupons or discounts "
                                            "for the bill?")

        titlesizer.Add(self.bill_deduct, wx.GBPosition(4, 2),
                       wx.GBSpan(1, 1), wx.ALIGN_CENTER|wx.ALL, 5)

        self.bill_tax = wx.TextCtrl(self, wx.ID_ANY, u"0",
                                    wx.DefaultPosition, wx.Size(60, -1),
                                    wx.TE_CENTRE,
                                    validator=CharValidator('no-alpha'))

        titlesizer.Add(self.bill_tax, wx.GBPosition(5, 2),
                       wx.GBSpan(1, 1), wx.ALIGN_CENTER|wx.ALL, 5)

        sizer_deduct = wx.GridBagSizer(0, 0)
        sizer_deduct.SetFlexibleDirection(wx.BOTH)
        sizer_deduct.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_statictext9 = wx.StaticText(self, wx.ID_ANY,
                                           u"Bill Deductions($)",
                                           wx.DefaultPosition, wx.DefaultSize,
                                           0)
        self.m_statictext9.Wrap(-1)
        self.m_statictext9.SetToolTipString(u"Any coupons or discounts "
                                                "for the bill?")

        sizer_deduct.Add(self.m_statictext9, wx.GBPosition(0, 0),
                         wx.GBSpan(1, 1), wx.ALL, 5)

        self.tip_deduct = wx.CheckBox(self, wx.ID_ANY, u"Include in Tip?",
                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.advanced.append(self.tip_deduct)
        self.tip_deduct.SetValue(True)
        self.tip_deduct.SetToolTipString(u"Check if deductions should be "
                                            "included in the tip calculations."
                                            "\n(Normally it is customary to "
                                            "tip on the total bill amount. "
                                            "*Unchecked*)")

        sizer_deduct.Add(self.tip_deduct, wx.GBPosition(0, 1),
                         wx.GBSpan(1, 1), wx.ALL, 5)


        titlesizer.Add(sizer_deduct, wx.GBPosition(4, 0),
                       wx.GBSpan(1, 2), wx.EXPAND, 0)

        sizer_tax = wx.GridBagSizer(0, 0)
        sizer_tax.SetFlexibleDirection(wx.BOTH)
        sizer_tax.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_statictext91 = wx.StaticText(self, wx.ID_ANY, u"Tax($)",
                                            wx.DefaultPosition, wx.DefaultSize,
                                            0)
        self.m_statictext91.Wrap(-1)
        sizer_tax.Add(self.m_statictext91, wx.GBPosition(0, 0),
                      wx.GBSpan(1, 1), wx.ALL, 5)

        sizer_tax.AddSpacer((75, 0), wx.GBPosition(0, 1),
                            wx.GBSpan(1, 1), wx.EXPAND, 5)

        self.tip_tax = wx.CheckBox(self, wx.ID_ANY, u"Include in Tip?",
                                   wx.DefaultPosition, wx.DefaultSize, 0)
        self.advanced.append(self.tip_tax)
        self.tip_tax.SetToolTipString(u"Check if tax should be included "
                                        "in the tip calculations. "
                                        "\n(Normally it is NOT customary to "
                                        "calculate tip with tax. *Unchecked*)")

        sizer_tax.Add(self.tip_tax, wx.GBPosition(0, 2),
                      wx.GBSpan(1, 1), wx.ALL, 5)


        titlesizer.Add(sizer_tax, wx.GBPosition(5, 0),
                       wx.GBSpan(1, 2), wx.EXPAND, 0)

        self.m_staticline1 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition,
                                           wx.DefaultSize, wx.LI_HORIZONTAL)
        titlesizer.Add(self.m_staticline1, wx.GBPosition(6, 0),
                       wx.GBSpan(1, 3), wx.EXPAND |wx.ALL, 5)

        sizer_rate = wx.GridBagSizer(0, 0)
        sizer_rate.SetFlexibleDirection(wx.BOTH)
        sizer_rate.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText12 = wx.StaticText(self, wx.ID_ANY, u"Tip Rate (%)",
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText12.Wrap(-1)
        sizer_rate.Add(self.m_staticText12, wx.GBPosition(0, 0),
                       wx.GBSpan(1, 1), wx.ALL, 5)

        sizer_rate.AddSpacer((35, 0), wx.GBPosition(0, 1),
                             wx.GBSpan(1, 1), wx.EXPAND, 5)

        self.tip_rate_manual = wx.CheckBox(self, wx.ID_ANY, u"Set Manually?",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.tip_rate_manual.SetToolTipString(u"Set the tip rate manually?"
                                              "\nAdjust the Tip for exceedingly"
                                              " good service, bad service,\nor"
                                              " some predetermined rate set by the"
                                              " restaurant for large group sizes.")
        self.advanced.append(self.tip_rate_manual)

        sizer_rate.Add(self.tip_rate_manual, wx.GBPosition(0, 2),
                       wx.GBSpan(1, 1), wx.ALL, 5)

        titlesizer.Add(sizer_rate, wx.GBPosition(7, 0),
                       wx.GBSpan(1, 2), wx.EXPAND, 5)

        self.tip_rate = wx.TextCtrl(self, wx.ID_ANY, u"0.0",
                                    wx.DefaultPosition, wx.Size(60, -1),
                                    wx.TE_CENTRE,
                                    validator=CharValidator('no-alpha'))
        self.tip_rate.Enable(False)
        self.tip_rate.SetMaxLength(5)
        titlesizer.Add(self.tip_rate, wx.GBPosition(7, 2),
                       wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_statictext92 = wx.StaticText(self, wx.ID_ANY, u"Total Tip($)",
                                            wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_statictext92.Wrap(-1)
        titlesizer.Add(self.m_statictext92, wx.GBPosition(8, 0),
                       wx.GBSpan(1, 2), wx.ALL, 5)

        self.tip_total = wx.StaticText(self, wx.ID_ANY, u"0.0",
                                       wx.DefaultPosition, wx.Size(60, -1),
                                       wx.ALIGN_CENTRE|wx.SUNKEN_BORDER)
        self.tip_total.Wrap(-1)
        titlesizer.Add(self.tip_total, wx.GBPosition(8, 2),
                       wx.GBSpan(1, 1), wx.ALL, 5)

        sizer_tailor = wx.GridBagSizer(0, 0)
        sizer_tailor.SetFlexibleDirection(wx.BOTH)
        sizer_tailor.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.tip_tailor_button = wx.Button(self, wx.ID_ANY, u"Tailor Tips",
                                           wx.DefaultPosition,
                                           wx.Size(-1,-1), 0)
        self.tip_tailor_button.Show(False)
        sizer_tailor.Add(self.tip_tailor_button, wx.GBPosition(0, 1),
                         wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_statictext10 = wx.StaticText(self, wx.ID_ANY,
                                            u"Per Person Tip($)",
                                            wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_statictext10.Wrap(-1)
        sizer_tailor.Add(self.m_statictext10, wx.GBPosition(0, 0),
                           wx.GBSpan(1, 1), wx.ALIGN_CENTER|wx.ALL, 5)

        titlesizer.Add(sizer_tailor, wx.GBPosition(9, 0),
                        wx.GBSpan(1, 1), wx.EXPAND, 5)

        self.tip_person = wx.StaticText(self, wx.ID_ANY, u"0.0",
                                        wx.DefaultPosition, wx.Size(60, -1),
                                        wx.ALIGN_CENTRE|wx.SUNKEN_BORDER)
        self.tip_person.Wrap(-1)
        titlesizer.Add(self.tip_person, wx.GBPosition(9, 2),
                       wx.GBSpan(1, 1), wx.ALIGN_CENTER|wx.ALL, 5)

        self.m_statictext11 = wx.StaticText(self, wx.ID_ANY, u"Total($)",
                                            wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_statictext11.Wrap(-1)
        titlesizer.Add(self.m_statictext11, wx.GBPosition(10, 0),
                       wx.GBSpan(1, 2), wx.ALL, 5)

        self.total = wx.StaticText(self, wx.ID_ANY, u"0.0",
                                   wx.DefaultPosition, wx.Size(60, -1),
                                   wx.ALIGN_CENTRE|wx.SUNKEN_BORDER)
        self.total.Wrap(-1)
        titlesizer.Add(self.total, wx.GBPosition(10, 2),
                       wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_statictext3 = wx.StaticText(self, wx.ID_ANY, u"Number of Guests",
                                           wx.DefaultPosition,
                                           wx.Size(-1, -1), 0)
        self.m_statictext3.Wrap(-1)
        titlesizer.Add(self.m_statictext3, wx.GBPosition(1, 0),
                       wx.GBSpan(1, 2), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.number_guest = wx.TextCtrl(self, wx.ID_ANY, u"1",
                                        wx.DefaultPosition, wx.Size(60, -1),
                                        wx.TE_CENTRE,
                                        validator=CharValidator('no-alpha'))
        self.number_guest.SetMaxLength(2)
        titlesizer.Add(self.number_guest, wx.GBPosition(1, 2),
                       wx.GBSpan(1, 1), wx.ALIGN_CENTER|wx.ALL, 5)
        self.settings = wx.ToggleButton(self, wx.ID_ANY, u"Show Configuration Settings",
                                  wx.DefaultPosition, wx.DefaultSize, 0)
        titlesizer.Add(self.settings, wx.GBPosition(11, 0), wx.GBSpan(1, 3),
                       wx.ALL|wx.EXPAND, 5)

        self.SetSizer(titlesizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.tip_tailor.Bind(wx.EVT_CHECKBOX, self.click_tip_tailor)
        self.tip_min.Bind(wx.EVT_TEXT, self.click_tip_min)
        self.tip_min.Bind(wx.EVT_KEY_UP, self.click_tip_min)
        self.tip_percentage.Bind(wx.EVT_SCROLL_CHANGED,
                                 self.click_tip_percentage)
        self.tip_max.Bind(wx.EVT_TEXT, self.click_tip_max)
        self.tip_max.Bind(wx.EVT_KEY_UP, self.click_tip_max)
        self.bill_total.Bind(wx.EVT_TEXT, self.click_bill_total)
        self.bill_total.Bind(wx.EVT_KEY_UP, self.click_bill_total)
        self.bill_deduct.Bind(wx.EVT_TEXT, self.click_bill_deduct)
        self.bill_deduct.Bind(wx.EVT_KEY_UP, self.click_bill_deduct)
        self.bill_tax.Bind(wx.EVT_TEXT, self.click_bill_tax)
        self.bill_tax.Bind(wx.EVT_KEY_UP, self.click_bill_tax)
        self.tip_deduct.Bind(wx.EVT_CHECKBOX, self.click_tip_deduct)
        self.tip_tax.Bind(wx.EVT_CHECKBOX, self.click_tip_tax)
        self.tip_rate.Bind(wx.EVT_KEY_UP, self.click_tip_rate)
        self.tip_tailor_button.Bind(wx.EVT_BUTTON, self.click_tip_tailor)
        self.number_guest.Bind(wx.EVT_TEXT, self.click_number_guest)
        self.number_guest.Bind(wx.EVT_KEY_UP, self.click_number_guest)
        self.settings.Bind(wx.EVT_TOGGLEBUTTON, self.click_settings)
        self.tip_rate_manual.Bind(wx.EVT_CHECKBOX, self.click_tip_rate_manual)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def click_tip_tailor(self, event):
        event.Skip()

    def click_tip_min(self, event):
        event.Skip()

    def click_tip_percentage(self, event):
        event.Skip()

    def click_tip_max(self, event):
        event.Skip()

    def click_bill_total(self, event):
        event.Skip()

    def click_bill_deduct(self, event):
        event.Skip()

    def click_bill_tax(self, event):
        event.Skip()

    def click_tip_deduct(self, event):
        event.Skip()

    def click_tip_rate(self, event):
        event.Skip()

    def click_tip_tax(self, event):
        event.Skip()

    def click_number_guest(self, event):
        event.Skip()

    def click_settings(self, event):
        event.Skip()

    def click_tip_rate_manual(self, event):
        event.Skip()

class tip_tailor_dialog(wx.Dialog):

    def __init__(self, parent,number_guests):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY,
                           title=u"Tip Tailoring", pos=wx.DefaultPosition,
                           size=wx.Size(636, 188),
                           style=wx.DEFAULT_DIALOG_STYLE)
#        self.SetLayoutAdaptationMode(wx.DIALOG_ADAPTATION_MODE_ENABLED)
        #DOESN"T WORK ON WX <3.0
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        gbsizer3 = wx.GridBagSizer(0, 0)
        gbsizer3.SetFlexibleDirection(wx.BOTH)
        gbsizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.text_name = wx.StaticText(self, wx.ID_ANY, u"Name",
                                       wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.text_name.Wrap(-1)
        self.text_name.SetToolTipString(u"The name of each person.")

        gbsizer3.Add(self.text_name, wx.GBPosition(0, 0),
                     wx.GBSpan(1, 1), wx.ALL, 5)

        self.text_bill = wx.StaticText(self, wx.ID_ANY, u"Bill Amount($)",
                                       wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_bill.Wrap(-1)
        self.text_bill.SetToolTipString(u"The amount each person "
                                            "owes from the bill.")
        self.text_bill.Hide()
        #Unhide for bill per person

        gbsizer3.Add(self.text_bill, wx.GBPosition(0, 1),
                     wx.GBSpan(1, 1), wx.ALL, 5)

        self.text_quality = wx.StaticText(self, wx.ID_ANY,
                                          u"Quality of Service",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_quality.Wrap(-1)
        self.text_quality.SetToolTipString(u"The quality of service each "
                                                "person feels they recieved.")

        gbsizer3.Add(self.text_quality, wx.GBPosition(0, 2),
                     wx.GBSpan(1, 1), wx.ALL, 5)

        self.text_tip = wx.StaticText(self, wx.ID_ANY, u"Tip Amount($)",
                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_tip.Wrap(-1)
        self.text_tip.SetToolTipString(u"The amount each person should tip.")

        gbsizer3.Add(self.text_tip, wx.GBPosition(0, 3),
                     wx.GBSpan(1, 1), wx.ALL, 5)

        self.text_total = wx.StaticText(self, wx.ID_ANY, u"Total/Person($)",
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_total.Wrap(-1)
        self.text_total.SetToolTipString(u"The total bill for each person "
                                            "including portion of bill, "
                                           "tax, and tip.")

        gbsizer3.Add(self.text_total, wx.GBPosition(0, 4),
                     wx.GBSpan(1, 1), wx.ALL, 5)
        self.objectdict={}
        for person_num in range(int(number_guests)):
            name=wx.TextCtrl(self, wx.ID_ANY, u"Name "+str(person_num),
                                      wx.DefaultPosition, wx.DefaultSize, 0)
#            setattr(self, "name_"+str(person_num), control)
##            self.name_1 = wx.TextCtrl(self, wx.ID_ANY, u"Name 1",
##                                      wx.DefaultPosition, wx.DefaultSize, 0)
#            thiscontrol=getattr(self, "name_"+str(person_num))
            row = 1 + person_num*2
            gbsizer3.Add(name, wx.GBPosition(row, 0),
                         wx.GBSpan(2, 1), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

            bill_total = wx.TextCtrl(self, wx.ID_ANY, u"0.0",
                                            wx.DefaultPosition, wx.Size(-1, -1),
                                            wx.TE_CENTRE,
                                            validator=CharValidator('no-alpha'))
            bill_total.SetToolTipString(u"The amount this person "
                                                    "owes from the bill.")
            bill_total.Hide()
            #Unhide for bill per person

            gbsizer3.Add(bill_total, wx.GBPosition(row, 1),
                         wx.GBSpan(2, 1), wx.ALIGN_CENTER|wx.ALL, 5)

            tip_percentage = wx.Slider(self, wx.ID_ANY, 5, 0, 10,
                                              wx.DefaultPosition, wx.DefaultSize,
                                              wx.SL_HORIZONTAL|wx.SL_LABELS)
            tip_percentage.SetToolTipString(u"The quality of service this "
                                                    "person recieved on a scale of 1-10. "
                                                    "\n(Larger number is better "
                                                    "service.)")

            gbsizer3.Add(tip_percentage, wx.GBPosition(row, 2),
                         wx.GBSpan(2, 1), wx.ALL, 5)

            tip_total = wx.StaticText(self, wx.ID_ANY, u"0.0",
                                             wx.DefaultPosition, wx.DefaultSize,
                                             wx.ALIGN_CENTRE|wx.SUNKEN_BORDER)
            tip_total.Wrap(-1)
            tip_total.SetToolTipString(u"The amount this person should tip.")

            gbsizer3.Add(tip_total, wx.GBPosition(row, 3),
                         wx.GBSpan(2, 1), wx.ALIGN_CENTER|wx.ALL, 5)

            total = wx.StaticText(self, wx.ID_ANY, u"0.0",
                                         wx.DefaultPosition, wx.DefaultSize,
                                         wx.ALIGN_CENTRE|wx.SUNKEN_BORDER)
            total.Wrap(-1)
            total.SetToolTipString(u"The total bill for this person "
                                            "including portion of bill, tax, "
                                            "and tip.")

            gbsizer3.Add(total, wx.GBPosition(row, 4),
                         wx.GBSpan(2, 1), wx.ALIGN_CENTER|wx.ALL, 5)
            self.objectdict["person"+str(person_num)]=[name,
                                                       bill_total,
                                                       tip_percentage,
                                                       tip_total,
                                                       total
                                                       ]
            name.Bind(wx.EVT_TEXT, self.click_name)
            name.Bind(wx.EVT_TEXT_ENTER, self.click_name)
            bill_total.Bind(wx.EVT_TEXT, self.click_bill_total)
            bill_total.Bind(wx.EVT_TEXT_ENTER, self.click_bill_total)
            tip_percentage.Bind(wx.EVT_SCROLL, self.click_tip_percentage)
            tip_percentage.Bind(wx.EVT_SCROLL_CHANGED,
                                   self.click_tip_percentage)

        self.SetSizer(gbsizer3)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def click_name(self, event):
        event.Skip()

    def click_bill_total(self, event):
        event.Skip()

    def click_tip_percentage(self, event):
        event.Skip()


