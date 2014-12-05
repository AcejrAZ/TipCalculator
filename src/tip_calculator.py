'''
Created on Oct 29, 2014

@author: venturf2
'''

import tip_calculator_GUIs
import tip_icon
import wx
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

class model_tip_calculator:
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
        self.tip_person=0
        self.person_deduct=0
        self.person_tax=0
        self.person_bill=0
        self.tip_tailor_values={}
        self.tip_tailor=0
        self.tip_rate_manual=0

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
            self.get_tip_total()
        elif type[0] == "tip" and type[1] != "rate":
            self.calculate_tip_rate()
        else: self.calculate_bill_total()

    def changed_prop_tailor(self,name,num,value):
        self.tip_tailor_values[num]={name:value}
        self.calculate_tip_total_person(num)

    def calculate_tip_total_person(self,num):
        percent=self.tip_tailor_values[num]["tip_percentage"]
        tip_rate=self.calculate_tip_rate(percent)
        tip_total=self.calculate_tip_total(tip_rate, self.person_deduct, 
                                           self.person_tax, self.person_bill)
        self.tip_tailor_values[num]["tip_total"]=tip_total
        tip_total=round(tip_total,2)
        pub.sendMessage("update_tailor", name="tip_total", num=num, value=tip_total)
        self.calculate_bill_total_person(num)

    def calculate_bill_total_person(self,num):
        tip_total=self.tip_tailor_values[num]["tip_total"]
        total=self.person_bill-self.person_deduct+self.person_tax+tip_total
        self.tip_tailor_values[num]["total"]=total
        total=round(total,2)
        pub.sendMessage("update_tailor", name="total", num=num, value=total)

    def drange(self, start, stop):
        this_start = start
        step=(stop-start)/10.0
        stop=stop+step
        this_range=[]
        while this_start < stop:
            this_range.append(this_start)
            this_start += step
        return this_range

    def calculate_tip_rate(self,tip_percent=None):
        self.range_tip=self.drange(self.tip_min, self.tip_max)
        try:
            if tip_percent is None:
                tip_percentage=self.tip_percentage
            else:
                tip_percentage=tip_percent
            tip_rate=self.range_tip[int(tip_percentage)]
        except IndexError:
            return
        if tip_percent is None:
            if not self.tip_rate_manual:
                self.tip_rate=round(tip_rate,2)
                pub.sendMessage("update", name="tip_rate",value=self.tip_rate)
            self.get_tip_total()
        else:
            return tip_rate

    def update_tip_total(self):
        total=[]
        for num in range(int(self.number_guest)):
            self.calculate_tip_total_person(num)
            total.append(self.tip_tailor_values[num]["tip_total"])
        total=sum(total)
        self.tip_total=round(total,2)
        pub.sendMessage("update", name="tip_total", value=self.tip_total)

    def update_bill_total(self):
        total=[]
        for num in range(int(self.number_guest)):
            self.calculate_bill_total_person(num)
            total.append(self.tip_tailor_values[num]["total"])
        total=sum(total)
        self.total=round(total,2)
        pub.sendMessage("update", name="total", value=self.total)

    def calcualte_tip_rate_person(self):
        total=self.total-self.tip_total
        self.tip_rate=self.tip_total/total
        value=self.tip_rate*100.0
        print value
        pub.sendMessage("update", name="tip_rate",value=value)

    def get_tip_total(self):
        self.calculate_tip_person()
        if self.tip_tailor:
            self.update_tip_total()
            self.update_bill_total()
            self.calcualte_tip_rate_person()
            return
        tip_total=self.calculate_tip_total(self.tip_rate, self.bill_deduct, 
                                               self.bill_tax, self.bill_total)
        self.tip_total=round(tip_total,2)
        pub.sendMessage("update", name="tip_total", value=self.tip_total)
        self.calculate_bill_total()

    def calculate_tip_total(self,rate,bill_deduct,bill_tax,bill_total):
        rate=rate/100.0
        if not self.tip_deduct:
            bill_deduct=0
        if not self.tip_tax:
            bill_tax=0
        total=(bill_total-bill_deduct+bill_tax)*rate
        return total

    def calculate_tip_person(self):
        self.tip_person=self.tip_total/self.number_guest
        self.person_deduct=self.bill_deduct/self.number_guest
        self.person_tax=self.bill_tax/self.number_guest
        self.person_bill=self.bill_total/self.number_guest
        tip_person=round(self.tip_person,2)
        pub.sendMessage("update", name="tip_person", value=tip_person)

    def calculate_bill_total(self):
        self.calculate_tip_person()
        if self.tip_tailor:
            self.update_tip_total()
            self.update_bill_total()
            self.calcualte_tip_rate_person()
            return
        total=self.bill_total-self.bill_deduct+self.bill_tax+self.tip_total
        self.total=round(total,2)
        pub.sendMessage("update", name="total", value=self.total)

    def get_value(self,name):
        return getattr(self, name)

class controller_tip_calculator(tip_calculator_GUIs.tip_calculator_mainframe):
    '''
    classdocs
    '''

    def __init__(self, parent):
        self.model=model_tip_calculator()
        tip_calculator_GUIs.tip_calculator_mainframe.__init__(self, parent)
        '''http://pixabay.com/en/dialog-tip-advice-hint-speaking-148815/
           http://pixabay.com/en/currency-signs-money-signs-33431/'''
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
                number_guest=self.model.get_value("number_guest")
                self.tailor_instance = controller_tip_tailor(self, number_guest)
                self.tailor_instance.Fit()
                self.tailor_instance.Layout()
                self.tailor_instance.Show()
        else:
            #"Do you want to stop tailoring tips? Y/N"
            self.tailor_instance.Destroy()
            self.tailor_instance=None
        self.tip_percentage.Enable(not checked)
        self.tip_person.Show(not checked)
        self.tip_tailor_button.Show(checked)
        self.model.changed_prop("tip_tailor", checked)
        self.Layout()

    def click_tip_rate_manual(self, event):
        checked=self.tip_rate_manual.GetValue()
        self.model.changed_prop("tip_rate_manual", checked)
        self.tip_rate.Enable(checked)

    def update_value(self, event, name):
        obj=event.GetEventObject()
        value = self.get_value(obj)
        self.model.changed_prop(name, value)

    def update_view(self, name, value):
        self.set_value(name, value)

    def update_view_error(self,name):
        self.validation_error(name)

class controller_tip_tailor(tip_calculator_GUIs.tip_tailor_dialog):
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
        self.model=self.GetParent().model
        pub.subscribe(self.update_view,"update_tailor")
        pub.subscribe(self.update_all,"update")
        self.number_guests=int(number_guests)
        for num in range(self.number_guests):
            self.model.changed_prop_tailor("tip_percentage", num, 5)

    def update_value(self, event, name, num):
        obj=event.GetEventObject()
        value = self.get_value(obj)
        self.model.changed_prop_tailor(name, num, value)
        self.model.update_bill_total()
        self.model.update_tip_total()
        self.model.calcualte_tip_rate_person()

    def update_all(self, name, value):
        for num in range(self.number_guests):
            self.model.calculate_tip_total_person(num)

    def update_view(self,name,num,value):
        self.set_value(name, num, value)

