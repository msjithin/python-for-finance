
from tkinter import Tk, Text, TOP, BOTTOM, BOTH, X, N, RIGHT, LEFT, StringVar, IntVar, END, RAISED, messagebox, Scrollbar
from tkinter.ttk import Frame, Label, Entry, OptionMenu, Radiobutton, Button
from fpdf import FPDF 
from forex_python.converter import CurrencyRates
import pandas as pd 
from datetime import datetime
from assets import *
from ttkwidgets.autocomplete import AutocompleteCombobox
from tax_calculator import get_tax, get_total
from social_security_calculator import get_social_security

class Example(Frame):
    def __init__(self):
        super().__init__()
        
        self.master.title("Income calculator app")
        self.pack(fill=BOTH, expand=True)
        
        # label
        frame0 = Frame(self)
        frame0.pack(fill=X)
        title = Label(frame0, text='Welcome to the app', font=("Times New Roman", 20))
        title.pack()

        # frame 1
        frame1a = Frame(self)
        frame1a.pack(fill=X, padx=10, pady=10)
        name_label = Label(frame1a, text="Employee name :", width=15)
        name_label.pack(side=LEFT, padx=5, pady=5)
        name = Entry(frame1a)
        name.pack(fill=X, padx=5, expand=True)
        frame1b = Frame(self)
        frame1b.pack(fill=X, padx=10, pady=10)
        destination_label = Label(frame1b, text="Destination :", width=15)
        destination_label.pack(side=LEFT, padx=5, pady=5)
        # destination = Entry(frame1b)
        # destination.pack(fill=X, padx=5, expand=True)
        data = pd.read_csv("country_currency.csv") 
        data.dropna(subset=['Country'], inplace=True)
        destination_select = StringVar(frame1b)
        destination = AutocompleteCombobox(frame1b,  textvariable=destination_select, width=20, completevalues= data['Country'].to_list() )
        destination.pack()


        # frame 2
        frame2 = Frame(self)
        frame2.pack(fill=X)
        netIncome_label = Label(frame2, text='Net income (per year)', width=20)
        netIncome_label.pack(side=LEFT, padx=5, pady=5)
        netIncome = Entry(frame2)
        netIncome.pack(fill=X, padx=5, expand=True)

        #frame 3
        frame3 = Frame(self)
        frame3.pack( pady=10)
        maritalStatus_label = Label(frame3, text='Marital status ', width=15)
        maritalStatus_label.pack(side=LEFT, padx=5, pady=5)
        maritalStatus_select = StringVar(frame3)
        maritalStatus_select.set(maritalStatusList[0])
        maritalStatus = OptionMenu(frame3, maritalStatus_select, *maritalStatusList)
        maritalStatus.pack(side=LEFT, padx=10)
     
        nKids_label = Label(frame3, text='Number of kids :', width=20)
        nKids_select = IntVar(frame3)
        nKids_select.set(nKids_list[0])
        nKids_entry = OptionMenu(frame3, nKids_select, *nKids_list)
        nKids_label.pack(side=LEFT )
        nKids_entry.pack( side=LEFT)

        def get_info():
            try:
                df_row = data[data['Country'] == destination_select.get()] 
                currency_code = str(df_row['Currency code'].values[0] )
                currency_name = str(df_row['Currency'].values[0] )
            except:
                messagebox.showwarning('Warning', 'Please select a destination')
                currency_code = 'EUR'
                currecy_name = 'Euros'
            country2_select.set(currency_code)
            currency.set(currency_name)


        #frame 3
        frame3a = Frame(self)
        frame3a.pack( pady=5)

        info_button = Button(frame3a, text='Get info',  command=get_info)
        info_button.pack(side=TOP)


        forex_label = Label(frame3a, text='Currency conversion    From ', width=15)
        forex_label.pack(side=LEFT, padx=5, pady=5)
        country1_select = StringVar(frame3a)
        country1_select.set(currecy_list[0])
        country1 = OptionMenu(frame3a, country1_select, *currecy_list)
        country1.pack(side=LEFT, padx=10)
     
        forex_label2 = Label(frame3a, text='  To  ', width=5)
        country2_select = StringVar(frame3a)
        currency = StringVar(frame3a)
        country2_select.set('EUR')
        currency.set('Euros')
        country2 =  Text(frame3a, height=1, width=10)
        country2.insert(END, country2_select.get() )
        forex_label2.pack(side=LEFT )
        country2.pack( side=LEFT)

        forex_display = Text(frame3a, height=1, width=10)
        c = CurrencyRates()
        forex_display.insert(END, c.get_rate(country1_select.get(), country2_select.get()) )
        forex_display.pack(side=RIGHT, padx=10)
        forex_conversion = StringVar()
        forex_conversion.set('1.0')
        def callback(*args):
            forex_display.delete(1.0, "end")
            country2.delete(1.0, "end")
            try:
                forex_conversion.set(c.get_rate(country1_select.get(), country2_select.get()))
                forex_display.insert(END, forex_conversion.get())
                country2.insert(END, country2_select.get())
            except Exception as exception_error:
                messagebox.showwarning('Warning', exception_error)
                forex_conversion.set('1.0')
                forex_display.insert(END, '0' )

        country2_select.trace("w", callback)
        country1_select.trace("w", callback)

        #frame 4
        frame4 = Frame(self)
        frame4.pack(pady=10 )
        radioInput = IntVar(self)
        radioInput.set(1)
        R1 = Radiobutton(frame4, text="Yearly", variable=radioInput, value=1)
        R2 = Radiobutton(frame4, text="Montly", variable=radioInput, value=2)
        R3 = Radiobutton(frame4, text="Daily", variable=radioInput, value=3)
        period_label = Label(frame4, text='Calculating for period :')
        period_label.pack(side=LEFT)
        R1.pack(side =LEFT, pady=10)
        R2.pack(side =LEFT, pady=10)
        R3.pack(side =RIGHT, pady=10)

        now = datetime.now() # current date and time

        def get_string():
            income = float('0'+netIncome.get())
            status = str(maritalStatus_select.get())
            output_string = "Income calculation        \t {}  \n\n".format(now.strftime("%d/%m/%Y, %H:%M:%S"))
            output_string += "Employee name :{} \n\n".format(name.get())
            output_string += "Destination   :{} \n".format(destination_select.get())
            output_string += "Currency      :{} - {} \n".format(country2_select.get(), currency.get())
            output_string += "\nNet yearly income = {} {}  ".format(income, country1_select.get())
            output_string += "\n\nCalcualting for "+ str(period[radioInput.get()-1])
            if radioInput.get() == 2:
                income = round(income/12, 2)
            elif radioInput.get() == 3:
                income = round(income/365, 2)
            output_string += "\nNet income = {} {} \nMarital status = {} ".format(income, country1_select.get(), status)
            output_string += "\nNumber of kids = "+ str(nKids_select.get())

            try:
                tax_rate = get_tax(country=destination_select.get())
                social_sec_em , social_sec_com = get_social_security(country=destination_select.get())
            except:
                messagebox.showwarning('Warning', 'Tax / social security information NOT found')
                tax_rate = 0
                social_sec_em , social_sec_com = 0, 0
            output_string += "\n\nTax rate : {} %".format( tax_rate )
            output_string += "\nSocial security rates:"
            output_string += "\n   employee : {} %".format(social_sec_em)
            output_string += "\n   company  : {} %".format(social_sec_com)
            output_string += "\n\n Tax amount  : {}".format( round(income*tax_rate/100 ,2 ))
            output_string += "\n Employee social security amount : {}".format( round(income*social_sec_em/100, 2) )
            output_string += "\n Company social security amount  : {}".format( round(income*social_sec_com/100, 2) )
            total = float(get_total(income=income, rate1=tax_rate, rate2=social_sec_em, rate3=social_sec_com))
            output_string += "\n\nTotal  : {} {}".format( total, country1_select.get() )
            output_string += '\n conversion = {}'.format( forex_conversion.get() )
            total *= float(forex_conversion.get())
            output_string += "\n after conversion {} {} ".format( round(total, 2), country2_select.get() )

            return output_string

        def write_pdf():
            pdf = FPDF()
            pdf.add_page()
            pdf.set_margins(30, 50, 25)
            pdf.set_font("Arial", size = 15) 
            output_string = get_string().split('\n')
            for s in output_string:    
                pdf.cell(200, 10, txt = s, ln=1) 
            pdf.output(name.get() + ' '+ str(now.strftime("%d_%m_%Y"))+'_info.pdf')    

        def write_txt():
            with open(name.get() + ' '+str(now.strftime("%d_%m_%Y"))+'_info.txt', 'w'  ) as sfile:
                sfile.write(
                get_string()
                )

        def string_display():
            output_display.delete(1.0,END)
            output_display.insert(END, get_string())



        frame5 = Frame(self, borderwidth=1)
        frame5.pack(fill=BOTH, expand=True, padx=5, pady=5)
        output_display = Text(frame5, height=15)
        scroll_y = Scrollbar(frame5, orient="vertical", command=output_display.yview)
        scroll_y.pack(side="right", expand=True, fill="y",padx=2, pady=2)
        output_display.pack(side='left', fill=X, padx=2, pady=2)
        output_display.configure(yscrollcommand=scroll_y.set)

        frame_final = Frame(self, relief=RAISED, borderwidth=1)
        frame_final.pack(fill=X  ,padx=10, pady=5)
        submit_button = Button(frame_final, text='Submit',  command=string_display)
        submit_button.pack(side=LEFT)
        file_type_label = Label(frame_final, text='Choose file type:')
        file_type_label.pack()
        file_save_type = StringVar()
        file_save_type.set(save_list[0])
        file_save = OptionMenu(frame_final, file_save_type, *save_list)
        
        def save_to_file():
            if file_save_type.get() == 'txt':
                write_txt()
                messagebox.showinfo('Saved!', 'Saved as text file')
            elif file_save_type.get() == 'pdf':
                write_pdf()
                messagebox.showinfo('Saved!', 'Saved as pdf file')
            else:
                messagebox.showwarning('Warning', 'Please select text file or pdf')


        save_button = Button(frame_final, text='Save to file',  command=save_to_file)
        save_button.pack(side=RIGHT)
        file_save.pack(side=RIGHT)



def main():

    root = Tk()
    root.title('Income calculation application')
    root.geometry("480x700")
    app = Example()
    root.mainloop()


if __name__ == '__main__':
    main()