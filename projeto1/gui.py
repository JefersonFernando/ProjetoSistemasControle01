from concurrent.futures import thread
from msilib.schema import ComboBox
from tkinter import *
import asyncio
from tkinter.ttk import Combobox

class myGui(Tk):
    def __init__(self, loop, interval=1/120):
        super().__init__()
        self.ampString = ''
        self.
        self.loop = loop
        self.startButton = False
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.tasks = []
        self.tasks.append(loop.create_task(self.updater(interval)))

    def close(self):
        for task in self.tasks:
            task.cancel()
        self.loop.stop()
        self.destroy()

    def startButtonCallback(self):
        if(not self.startButton):
            self.startButton = True
            self.comboMalha['state'] = 'disabled'
            self.comboSignals['state'] = 'disabled'
            print('Start Button')
        else:
            self.startButton = False
            self.comboMalha['state'] = 'readonly'
            self.comboSignals['state'] = 'readonly'

    def comboMalhaCallback(self):
        print('Combo Malha')

    async def updater(self, interval):
        self.title('iDynamic Controller')

        self.info = Label(self, text='Projeto 1 - projeto de Sistemas de Controole')
        self.info.grid(column=0, row=0,  padx=10, pady=10)

        self.startButton = Button(self, text="Ativar/Desativar", command = self.startButtonCallback)
        self.startButton.grid(column=0, row=1, padx=10, pady=10)

        self.infoMalha = Label(self, text='Malha')
        self.infoMalha.grid(column=0, row=2,  padx=10, pady=10)
        self.comboMalha = Combobox(self, state='readonly', text='Malha',values=['Malha Aberta', 'Malha Fechada'])
        self.comboMalha.grid(column=0, row=3)

        self.infoSignals = Label(self, text='Signals')
        self.infoSignals.grid(column=0, row=4,  padx=10, pady=10)
        self.comboSignals = Combobox(self, state='readonly', values=['Degrau', 'Onda Senoidal', 'Onda quadrada', 'Onda dente de serra', 'Sinal aleatório'])
        self.comboSignals.grid(column=0, row=5)

        self.infoAmpEntry = Label(self, text='Amplitude')
        self.infoAmpEntry.grid(column=0, row=6,  padx=10, pady=10)
        self.ampEntry = Entry(self, textvariable=self.ampString)
        self.ampEntry.grid(column = 0, row = 7)

        self.infoPeriodEntry = Label(self, text='Período')
        self.infoPeriodEntry.grid(column=0, row=8,  padx=10, pady=10)
        self.PeriodEntry = Entry(self, textvariable=self.ampString)
        self.PeriodEntry.grid(column = 0, row = 9)

        self.infoOffsetEntry = Label(self, text='Offset')
        self.infoOffsetEntry.grid(column=0, row=10,  padx=10, pady=10)
        self.OffsetEntry = Entry(self, textvariable=self.ampString)
        self.OffsetEntry.grid(column = 0, row = 11)

        self.infoAmpMinEntry = Label(self, text='Amplitude mínima')
        self.infoAmpMinEntry.grid(column=0, row=12,  padx=10, pady=10)
        self.AmpMinEntry = Entry(self, textvariable=self.ampString)
        self.AmpMinEntry.grid(column = 0, row = 13)

        self.infoPeriodMinEntry = Label(self, text='Período mínimo')
        self.infoPeriodMinEntry.grid(column=0, row=14,  padx=10, pady=10)
        self.PeriodMinEntry = Entry(self, textvariable=self.ampString)
        self.PeriodMinEntry.grid(column = 0, row = 15)

        while await asyncio.sleep(interval, True):
            self.update()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    gui = myGui(loop)
    loop.run_forever()
    loop.close()

