from concurrent.futures import thread
from doctest import master
from msilib.schema import ComboBox
from tkinter import *
import asyncio
from tkinter.ttk import *
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from numpy import arange, sin, pi
from pandas import DataFrame

f = Figure(figsize = (5,5), dpi = 100)
graph = f.add_subplot(111)
class myGui(Tk):
    def __init__(self, RemoteControl):
        super().__init__()
        self.ampString = StringVar()
        self.periodString = StringVar()
        self.offsetString = StringVar()
        self.ampMinString = StringVar()
        self.periodMinString = StringVar()
        self.startButton = False
        self.RemoteControl = RemoteControl
        self.protocol("WM_DELETE_WINDOW", self.RemoteControl.finish)
        self.xinfo = list()
        self.yinfo = list() 

    def startButtonCallback(self):
        self.startButton = not self.startButton
        if(not self.startButton):
            self.comboMalha['state'] = 'disabled'
            self.comboSignals['state'] = 'disabled'
            self.ampEntry['state'] = 'disabled'
            self.PeriodEntry['state'] = 'disabled'
            self.OffsetEntry['state'] = 'disabled'
            self.AmpMinEntry['state'] = 'disabled'
            self.PeriodMinEntry['state'] = 'disabled'
            print('Start Button')
            self.updateValues(self.xinfo[-1] + 1, self.yinfo[-1] + 1)
        else:
            self.comboMalha['state'] = 'readonly'
            self.comboSignals['state'] = 'readonly'
            self.ampEntry['state'] = 'normal'
            self.PeriodEntry['state'] = 'normal'
            self.OffsetEntry['state'] = 'normal'
            self.AmpMinEntry['state'] = 'normal'
            self.PeriodMinEntry['state'] = 'normal'

    def comboMalhaCallback(self):
        print('Combo Malha')

    def updateValues(self, xinfo, yinfo):
        self.graph.destroy() 

        if(len(self.xinfo) >= 20):
            self.xinfo = self.xinfo[1:]
            self.yinfo = self.yinfo[1:]

        self.xinfo.append(xinfo)
        self.yinfo.append(yinfo)

        figure1 = plt.figure(figsize=(3,3), dpi = 200)

        plt.scatter(self.xinfo, self.yinfo,)

        self.canvas=FigureCanvasTkAgg(figure1 ,master=self)
        self.graph = self.canvas.get_tk_widget()
        self.graph.grid(row=0,column=3, rowspan=9)

    async def updater(self, interval):
        self.title('iDynamic Controller')

        self.info = Label(self, text='Projeto 1 - projeto de Sistemas de Controle')
        self.info.grid(column=0, row=0,  padx=10, pady=0, columnspan=2)

        self.startButton = Button(self, text="Ativar/Desativar", command = self.startButtonCallback)
        self.startButton.grid(column=0, row=1, padx=10, pady=0, columnspan=2)

        self.infoMalha = Label(self, text='Malha')
        self.infoMalha.grid(column=0, row=2,  padx=10, pady=0, sticky=E)
        self.comboMalha = Combobox(self, state='readonly', text='Malha',values=['Malha Aberta', 'Malha Fechada'])
        self.comboMalha.grid(column=1, row=2, sticky=W)

        self.infoSignals = Label(self, text='Signals')
        self.infoSignals.grid(column=0, row=3,  padx=10, pady=0, sticky=E)
        self.comboSignals = Combobox(self, state='readonly', values=['Degrau', 'Onda Senoidal', 'Onda quadrada', 'Onda dente de serra', 'Sinal aleatório'])
        self.comboSignals.grid(column=1, row=3, sticky=W)

        self.infoAmpEntry = Label(self, text='Amplitude')
        self.infoAmpEntry.grid(column=0, row=4,  padx=10, pady=0, sticky=E)
        self.ampEntry = Entry(self, textvariable=self.ampString)
        self.ampEntry.grid(column = 1, row = 4, sticky=W)

        self.infoPeriodEntry = Label(self, text='Período')
        self.infoPeriodEntry.grid(column=0, row=5,  padx=10, pady=0, sticky=E)
        self.PeriodEntry = Entry(self, textvariable=self.periodString)
        self.PeriodEntry.grid(column = 1, row = 5, sticky=W)

        self.infoOffsetEntry = Label(self, text='Offset')
        self.infoOffsetEntry.grid(column=0, row=6,  padx=10, pady=0, sticky=E)
        self.OffsetEntry = Entry(self, textvariable=self.offsetString)
        self.OffsetEntry.grid(column = 1, row = 6, sticky=W)

        self.infoAmpMinEntry = Label(self, text='Amplitude mínima')
        self.infoAmpMinEntry.grid(column=0, row=7,  padx=10, pady=0, sticky=E)
        self.AmpMinEntry = Entry(self, textvariable=self.ampMinString)
        self.AmpMinEntry.grid(column = 1, row = 7, sticky=W)

        self.infoPeriodMinEntry = Label(self, text='Período mínimo')
        self.infoPeriodMinEntry.grid(column=0, row=8,  padx=10, pady=0, sticky=E)
        self.PeriodMinEntry = Entry(self, textvariable=self.periodMinString)
        self.PeriodMinEntry.grid(column = 1, row = 8, padx=10, pady=0, sticky=W)

        self.xinfo.append(1)
        self.yinfo.append(1)


        figure1 = plt.figure(figsize=(3,3), dpi = 200)

        plt.scatter(self.xinfo, self.yinfo)

        self.canvas=FigureCanvasTkAgg(figure1 ,master=self)
        self.graph = self.canvas.get_tk_widget()
        self.graph.grid(row=0,column=3, rowspan=9)


        while await asyncio.sleep(interval, True):
            self.update()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    gui = myGui(loop)
    loop.run_forever()
    loop.close()

