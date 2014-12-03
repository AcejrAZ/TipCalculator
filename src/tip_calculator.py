'''
Created on Oct 29, 2014

@author: venturf2
'''

import tip_calculator_GUIs
import tip_icon
import wx

class tip_calculator_main(tip_calculator_GUIs.tip_calculator_mainframe):
    '''
    classdocs
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        tip_calculator_GUIs.tip_calculator_mainframe.__init__(self, parent)
        '''http://pixabay.com/en/dialog-tip-advice-hint-speaking-148815/
           http://pixabay.com/en/currency-signs-money-signs-33431/'''
        for item in self.advanced:
            item.Show(False)
        self.ico = tip_icon.gettipimg2Icon()
        self.SetIcon(self.ico)

    def click_tip_tailor(self, event):
        checked = self.tip_tailor.IsChecked()
        if checked:
            try:
                self.tailor_instance.Show()
                self.tailor_instance.Raise()
            except AttributeError:
                number_guests=self.get_guests()
                if number_guests is None:
                    self.number_guest.SetValue("0")
                    self.tip_tailor.SetValue(False)
                    return
                self.tailor_instance = tip_tailor_main(self, number_guests)
                self.tailor_instance.Fit()
                self.tailor_instance.Layout()
                self.tailor_instance.Show()
        else:
            #"Do you want to stop tailoring tips? Y/N"
            self.tailor_instance.Destroy()
            self.tailor_instance=None
            self.calculate_all()
            self.calculate_bill_total()
        self.tip_percentage.Enable(not checked)
        self.tip_person.Show(not checked)
        self.tip_tailor_button.Show(checked)
        self.Layout()

    def click_tip_min(self, event):
        try:
            self.validate_minmax()
            self.calculate_all()
        except ValueError:
            pass

    def click_tip_percentage(self, event):
        self.calculate_all()

    def click_tip_max(self, event):
        try:
            self.validate_minmax()
            self.calculate_all()
        except ValueError:
            pass

    def calculate_tip_rate(self):
        if self.tip_rate_manual.GetValue():
            return
        try:
            this_max=float(self.tip_max.GetValue())
            this_min=float(self.tip_min.GetValue())
        except ValueError:
            return
        percent=self.tip_percentage.GetValue()
        range_tip=self.drange(this_min, this_max)
        try:
            tip_rate=range_tip[percent]
        except IndexError:
            return
        self.tip_rate.SetValue(str(round(tip_rate,2)))

    def calculate_tip_rate_tailor(self):
        tip_total=float(self.tip_total.GetLabel())
        bill_total=self.get_bill()
        try:
            tip_rate=tip_total/bill_total
        except ZeroDivisionError:
            return
        self.tip_rate.SetValue(str(tip_rate*100))

    def drange(self, start, stop):
        this_start = start
        step=(stop-start)/10.0
        stop=stop+step
        this_range=[]
        while this_start < stop:
            this_range.append(this_start)
            this_start += step
        return this_range

    def get_deduct(self):
        try:
            return float(self.bill_deduct.GetValue())
        except ValueError:
            return 0

    def get_deduct_tip(self):
        try:
            if self.tip_deduct.GetValue():
                    return self.get_deduct()
            else:
                return 0
        except ValueError:
            return

    def get_tax(self):
        try:
            return float(self.bill_tax.GetValue())
        except ValueError:
            return 0

    def get_tax_tip(self):
        if self.tip_tax.GetValue():
            return self.get_tax()
        else:
            return 0

    def get_bill(self):
        try:
            return float(self.bill_total.GetValue())
        except ValueError:
            return 0

    def get_guests(self):
        try:
            return float(self.number_guest.GetValue())
        except ValueError:
            return None

    def calculate_tip_total(self):
        try:
            bill_total=self.get_bill()
            tip_rate=float(self.tip_rate.GetValue())/100.0
            bill_deduct=self.get_deduct_tip()
            bill_tax=self.get_tax_tip()
        except ValueError:
            return

        total=(bill_total-bill_deduct+bill_tax)*tip_rate
        self.tip_total.SetLabel(str(round(total,2)))

    def calculate_tip_person(self):
        try:
            number_guest=self.get_guests()
            if number_guest is None:
                return
            tip_total=float(self.tip_total.GetLabel())
        except ValueError:
            return
        person_tip=tip_total/number_guest
        self.tip_person.SetLabel(str(round(person_tip,2)))

    def calculate_bill_total(self):
        try:
            bill_total=float(self.bill_total.GetValue())
            tip_total=float(self.tip_total.GetLabel())
            bill_deduct=float(self.bill_deduct.GetValue())
            bill_tax=float(self.bill_tax.GetValue())
        except ValueError: return
        total=bill_total-bill_deduct+bill_tax+tip_total
        self.total.SetLabel(str(round(total,2)))

    def validate_minmax(self):
        this_max=float(self.tip_max.GetValue())
        this_min=float(self.tip_min.GetValue())
        if this_max <= this_min and len(str(this_max)) > 3:
            #Need a better way to handle max of single digit less than min
            #Otherwise get error when trying to just type max
            dlg = wx.MessageDialog(None,
                                   "The Maximum tip MUST be greater"
                                   " than the Minimum tip.",
                                   "Value Error",
                                   wx.OK|wx.ICON_ERROR)
            dlg.ShowModal()
            if this_max == 0:
                self.tip_max.SetValue(self.tip_max_default)
            self.tip_min.SetValue(self.tip_min_default)
            self.tip_max.SetValue(self.tip_max_default)
            raise ValueError

    def validate_total(self):
        total=self.get_bill()
        if total == 0:
            dlg = wx.MessageDialog(None,
                                   "The total must be greater than zero."
                                   "\nCLICK OK.",
                                   "Value Error",
                                   wx.OK|wx.ICON_ERROR)
            dlg.ShowModal()
            raise ValueError

    def validate_deduct(self):
        tip_deduct=self.get_deduct()
        total=self.get_bill()
        if tip_deduct >= total and total != 0:
            dlg = wx.MessageDialog(None,
                                   "The deduction amount MUST be less"
                                   " than the total bill.",
                                   "Value Error",
                                   wx.OK|wx.ICON_ERROR)
            dlg.ShowModal()
            self.bill_deduct.SetValue("0")
            raise ValueError

    def validate_tax(self):
        tip_tax=self.get_tax()
        total=self.get_bill()
        if tip_tax >= total and total != 0:
            dlg = wx.MessageDialog(None,
                                   "The tax amount MUST be less"
                                   " than the total bill.",
                                   "Value Error",
                                   wx.OK|wx.ICON_ERROR)
            dlg.ShowModal()
            self.bill_tax.SetValue("0")
            raise ValueError

    def validate_guest(self):
        guests=self.get_guests()
        if guests == 0:
            dlg = wx.MessageDialog(None,
                                   "There must be more than"
                                   " 0 guests.",
                                   "Value Error",
                                   wx.OK|wx.ICON_ERROR)
            dlg.ShowModal()
            self.number_guest.SetValue("1")
            raise ValueError

    def calculate_all(self):
        try:
            self.tailor_instance.calculate_all()
        except AttributeError:
            self.calculate_tip_rate()
            self.calculate_tip_total()
            self.calculate_tip_person()
        self.calculate_bill_total()

    def click_settings(self, event):
        checked = self.settings.GetValue()
        for item in self.advanced:
            item.Show(checked)
        if not checked:
            self.settings.SetLabel("Show Configuration Settings")
        else:
            self.settings.SetLabel("Hide Configuration Settings")
        self.Layout()

    def click_tip_rate_manual(self, event):
        checked=self.tip_rate_manual.GetValue()
        self.tip_rate.Enable(checked)
        if not checked:
            self.calculate_all()

    def click_bill_total(self, event):
        try:
            self.validate_total()
            self.validate_deduct()
            self.validate_tax()
            self.calculate_all()
        except ValueError:
            pass

    def click_bill_deduct(self, event):
        try:
            self.validate_total()
            self.validate_deduct()
            self.calculate_all()
        except ValueError:
            pass    

    def click_bill_tax(self, event):
        try:
            self.validate_total()
            self.validate_tax()
            self.calculate_all()
        except ValueError:
            pass

    def click_tip_deduct(self, event):
        self.calculate_all()

    def click_tip_rate(self, event):
        self.calculate_all()

    def click_tip_tax(self, event):
        self.calculate_all()

    def click_number_guest(self, event):
        try:
            self.validate_guest()
            self.calculate_all()
        except ValueError:
            pass

class tip_tailor_main(tip_calculator_GUIs.tip_tailor_dialog):
    def __init__(self,parent,number_guests):
        tip_calculator_GUIs.tip_tailor_dialog.__init__(self,parent,
                                                       number_guests)
        if wx.VERSION[0]>2:
            self.EnableLayoutAdaptation(True)
        else:
            dlg = wx.MessageDialog(None,
                                   "You have an old version of"
                                   " wxpython. Therefore, scrollbars"
                                   " will not work. Please upgrade to"
                                   " >3.0.",
                                   "Version Error",
                                   wx.OK|wx.ICON_ERROR)
            dlg.ShowModal()
#        self.SetLayoutAdaptationMode(wx.DIALOG_ADAPTATION_MODE_ENABLED)
        self.SetIcon(self.GetParent().ico)
        self.calculate_all()

    def click_name(self, event):
        self.calculate_all()

    def click_bill_total(self, event):
        event.Skip()

    def click_tip_percentage(self, event):
        self.calculate_all()

    def calculate_all(self):
        number_guest=self.GetParent().get_guests()
        bill_total_person=self.GetParent().get_bill()/number_guest
        bill_deduct_person_tip=self.GetParent().get_deduct_tip()/number_guest
        bill_tax_person_tip=self.GetParent().get_tax_tip()/number_guest
        bill_deduct_person=self.GetParent().get_deduct()/number_guest
        bill_tax_person=self.GetParent().get_tax()/number_guest
        bill_person_tip=bill_total_person-bill_deduct_person_tip+bill_tax_person_tip
        total_tips=[]
        for person in self.objectdict:
#            bill_total=float(self.objectdict[person][1].GetValue())
            #TODO Unhide for bill per person
            percent=self.objectdict[person][2].GetValue()
            tip_percentage=self.calculate_tip_rate(percent)/100.0
            tip_total=self.objectdict[person][3]
            total_tip=tip_percentage*bill_person_tip
            tip_total.SetLabel(str(round(total_tip,2)))
            total=self.objectdict[person][4]
            total_total=total_tip+bill_total_person-bill_deduct_person+bill_tax_person
            total.SetLabel(str(round(total_total,2)))
            total_tips.append(total_tip)
        self.GetParent().tip_total.SetLabel(str(round(sum(total_tips),2)))
        self.GetParent().calculate_tip_rate_tailor()
        self.GetParent().calculate_bill_total()

    def calculate_tip_rate(self,percent):
        try:
            this_max=float(self.GetParent().tip_max.GetValue())
            this_min=float(self.GetParent().tip_min.GetValue())
        except ValueError:
            return
        range_tip=self.drange(this_min, this_max)
        try:
            tip_rate=range_tip[percent]
        except IndexError:
            return
        return tip_rate

    def drange(self, start, stop):
        this_start = start
        step=(stop-start)/10.0
        stop=stop+step
        this_range=[]
        while this_start < stop:
            this_range.append(this_start)
            this_start += step
        return this_range
