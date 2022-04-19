
from tkinter import *
import asyncio
from tkinter.ttk import *
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

f = Figure(figsize = (5,5), dpi = 100)
graph = f.add_subplot(111)
class myGui(Tk):
    def __init__(self, RemoteControl):
        super().__init__()
        self.ampString = StringVar()
        self.ampString.set("0.0")
        self.periodString = StringVar()
        self.periodString.set("0.0")
        self.offsetString = StringVar()
        self.offsetString.set("0.0")
        self.ampMinString = StringVar()
        self.ampMinString.set("0.0")
        self.periodMinString = StringVar()
        self.periodMinString.set("0.0")
        self.RemoteControl = RemoteControl
        self.protocol("WM_DELETE_WINDOW", self.RemoteControl.finish)
        self.timeData = list()
        self.refData = list() 
        self.errorData = list() 
        self.out1Data = list() 
        self.out2Data = list() 

    def startButtonCallback(self):
        self.RemoteControl.refreshParams(self.comboMalha.get(), self.comboSignals.get(), float(self.ampEntry.get()), float(self.PeriodEntry.get()), float(self.OffsetEntry.get()), float(self.AmpMinEntry.get()), float(self.PeriodMinEntry.get()))

    def updateValues(self, timeData, refData, errorData, out1Data, out2Data):
        self.ax.clear()

        if(len(self.timeData) >= 100):
            self.timeData = self.timeData[1:]
            self.refData = self.refData[1:]
            self.errorData = self.errorData[1:]
            self.out1Data = self.out1Data[1:]
            self.out2Data = self.out2Data[1:]

        self.timeData.append(timeData)
        self.refData.append(refData)
        self.errorData.append(errorData)
        self.out1Data.append(out1Data)
        self.out2Data.append(out2Data)

        self.ax.plot(self.timeData[:] ,self.refData[:], linestyle="solid", marker='.', linewidth=2, markersize=1, color='blue')
        self.ax.plot(self.timeData[:] ,self.errorData[:], linestyle="solid", marker='.', linewidth=2, markersize=1, color='yellow')
        self.ax.plot(self.timeData[:] ,self.out1Data[:], linestyle="solid", marker='.', linewidth=2, markersize=1, color='red')
        self.ax.plot(self.timeData[:] ,self.out2Data[:], linestyle="solid", marker='.', linewidth=2, markersize=1, color='green')

        self.canvas.draw()

    async def updater(self, interval):
        self.title('iDynamic Controller')

        self.info = Label(self, text='Projeto 1 - projeto de Sistemas de Controle')
        self.info.grid(column=0, row=0,  padx=10, pady=0, columnspan=2)

        self.startButton = Button(self, text="Atualizar", command = self.startButtonCallback)
        self.startButton.grid(column=0, row=1, padx=10, pady=0, columnspan=2)

        self.infoMalha = Label(self, text='Malha')
        self.infoMalha.grid(column=0, row=2,  padx=10, pady=0, sticky=E)
        self.comboMalha = Combobox(self, state='readonly', text='Malha',values=['Malha Aberta', 'Malha Fechada'])
        self.comboMalha.current(0)
        self.comboMalha.grid(column=1, row=2, sticky=W)

        self.infoSignals = Label(self, text='Signals')
        self.infoSignals.grid(column=0, row=3,  padx=10, pady=0, sticky=E)
        self.comboSignals = Combobox(self, state='readonly', values=['Degrau', 'Onda Senoidal', 'Onda quadrada', 'Onda dente de serra', 'Sinal aleatório'])
        self.comboSignals.current(0)
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

        self.figure1 = plt.figure(figsize=(15,15), dpi = 50)

        self.ax = self.figure1.add_subplot(1,1,1)

        self.canvas=FigureCanvasTkAgg(self.figure1 ,master=self)
        self.graph = self.canvas.get_tk_widget()
        self.graph.grid(row=0,column=3, rowspan=9)

        while await asyncio.sleep(interval, True):
            self.update()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    gui = myGui(loop)
    loop.run_forever()
    loop.close()

