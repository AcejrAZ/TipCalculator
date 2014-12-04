'''
Created on Oct 29, 2014

@author: venturf2
'''

import tip_calculator_GUIs
import tip_icon
import wx
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

class tip_calculator_model:
    def __init__(self):
        self.bill_total=1
        self.bill_deduct=0
        self.bill_tax=0
        self.tip_rate=0
        self.tip_min=0.0
        self.tip_max=20.0
        self.tip_percentage=5
        self.number_guest=1
        self.tip_total=0
        self.tip_deduct=1
        self.tip_tax=0

    def validate_all(self):
        if self.bill_total == 0:
            pub.sendMessage("error", name="bill_total")
        if self.number_guest == 0: 
            pub.sendMessage("error", name="number_guest")
        if self.bill_tax >= self.bill_total and self.bill_total != 0: 
            pub.sendMessage("error", name="bill_tax")
        if self.bill_deduct >= self.bill_total and self.bill_total != 0:
            pub.sendMessage("error", name="bill_deduct")
        if self.tip_max <= self.tip_min and len(str(self.tip_max)) > 3:
            pub.sendMessage("error", name="tip_max")
            #Need a better way to handle max of single digit less than min
            #Otherwise get error when trying to just type max

    def changed_prop(self,name,value):
        '''bill=["total","deduct","tax"]'''
        '''tip=["max","min","percentage"]'''
        setattr(self,name,value)
        self.validate_all()
        type=name.split("_")
        if type[0] == "bill":
            self.calculate_tip_total()
        elif type[0] == "tip" and type[1] != "rate":
            self.calculate_tip_rate()
        else: self.calculate_bill_total()

    def drange(self, start, stop):
        this_start = start
        step=(stop-start)/10.0
        stop=stop+step
        this_range=[]
        while this_start < stop:
            this_range.append(this_start)
            this_start += step
        return this_range

    def calculate_tip_rate(self):
        self.range_tip=self.drange(self.tip_min, self.tip_max)
        try:
            tip_rate=self.range_tip[int(self.tip_percentage)]
        except IndexError:
            return
        self.tip_rate=round(tip_rate,2)
        pub.sendMessage("update", name="tip_rate",value=self.tip_rate)
        self.calculate_tip_total()

    def calculate_tip_total(self):
        rate=self.tip_rate/100.0
        if self.tip_deduct:
            bill_deduct=self.bill_deduct
        else:
            bill_deduct=0
        if self.tip_tax:
            bill_tax=self.bill_tax
        else:
            bill_tax=0
        total=(self.bill_total-bill_deduct+bill_tax)*rate
        self.tip_total=round(total,2)
        pub.sendMessage("update", name="tip_total", value=self.tip_total)
        self.calculate_bill_total()

    def calculate_tip_person(self):
        person_tip=self.tip_total/self.number_guest
        self.tip_person=round(person_tip,2)
        pub.sendMessage("update", name="tip_person", value=self.tip_person)

    def calculate_bill_total(self):
        self.calculate_tip_person()
        total=self.bill_total-self.bill_deduct+self.bill_tax+self.tip_total
        self.total=round(total,2)
        pub.sendMessage("update", name="total", value=self.total)

class tip_calculator_main(tip_calculator_GUIs.tip_calculator_mainframe):
    '''
    classdocs
    '''

    def __init__(self, parent):
        self.model=tip_calculator_model()
        tip_calculator_GUIs.tip_calculator_mainframe.__init__(self, parent)
        '''http://pixabay.com/en/dialog-tip-advice-hint-speaking-148815/
           http://pixabay.com/en/currency-signs-money-signs-33431/'''
        for item in self.advanced:
            item.Show(False)
        self.ico = tip_icon.gettipimg2Icon()
        self.SetIcon(self.ico)
        pub.subscribe(self.update_view,"update")
        pub.subscribe(self.update_view_error,"error")
        self.model.calculate_tip_rate()

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

    def calculate_tip_rate_tailor(self):
        tip_total=float(self.tip_total.GetLabel())
        bill_total=self.get_bill()
        try:
            tip_rate=tip_total/bill_total
        except ZeroDivisionError:
            return
        self.tip_rate.SetValue(str(tip_rate*100))

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

    def update_value(self, event, name):
        obj=event.GetEventObject()
        value = self.get_value(obj)
        self.model.changed_prop(name, value)

    def update_view(self, name, value):
        self.set_value(name, value)

    def update_view_error(self,name):
        self.validation_error(name)

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
