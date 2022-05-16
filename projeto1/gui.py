
from cProfile import label
from tkinter import *
import asyncio
from tkinter.messagebox import showinfo
from tkinter.ttk import *
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

f = Figure(figsize = (5,5), dpi = 100)
graph = f.add_subplot(111)
class myGui(Tk):
    def __init__(self, RemoteControl):
        super().__init__()
        self.GraphSize = StringVar()
        self.GraphSize.set("100")
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
        self.Malha = 'Malha Aberta'
        self.Signal = 'Degrau'
        self.vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    def refreshParams(self):
        self.RemoteControl.refreshParams(self.Malha, self.Signal, float(self.ampString.get()), float(self.periodString.get()), float(self.offsetString.get()), float(self.ampMinString.get()), float(self.periodMinString.get()))

    def updateValues(self, timeData, refData, errorData, out1Data, out2Data):
        self.ax.clear()

        if(len(self.timeData) >= int(self.GraphSize.get())):

            self.timeData = self.timeData[-int(self.GraphSize.get()):]
            self.refData = self.refData[-int(self.GraphSize.get()):]
            self.errorData = self.errorData[-int(self.GraphSize.get()):]
            self.out1Data = self.out1Data[-int(self.GraphSize.get()):]
            self.out2Data = self.out2Data[-int(self.GraphSize.get()):]

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

        self.ax.title.set_text("Estados do sistema")
        self.ax.set(xlabel='Tempo', ylabel='Posição')

        self.canvas.draw()

    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

    def malhaChanged(self, event):
        self.Malha = self.comboMalha.get()
        print(self.Malha)

    def configGraphSize(self):
        win = Toplevel(self)
        win.resizable(width=False, height=False)
        win.title("Graph Size")

        infoGraphSize = Label(win, text='Número de dados exibidos no gráfico:')
        infoGraphSize.grid(column=0, row=0,  padx=50, pady=(50,10))
        GraphSizeEntry = Entry(win, textvariable=self.GraphSize, validate = 'key', validatecommand = self.vcmd)
        GraphSizeEntry.grid(column = 0, row = 1, pady=(50,50))

    def stepWaveConfig(self):
        win = Toplevel(self)
        win.resizable(width=False, height=False)
        win.title("Step Wave Config")

        self.Signal = 'Degrau'

        self.Malha = 'Malha Aberta'
        infoMalha = Label(win, text='Malha')
        infoMalha.grid(column=0, row=0,  padx=50, pady=(50,10))
        self.comboMalha = Combobox(win, state='readonly', text='Malha',values=['Malha Aberta', 'Malha Fechada'])
        self.comboMalha.current(0)
        self.comboMalha.bind('<<ComboboxSelected>>', self.malhaChanged)
        self.comboMalha.grid(column=0, row=1, padx=50)

        infoAmpEntry = Label(win, text='Amplitude')
        infoAmpEntry.grid(column=0, row=2,  padx=50, pady=(50,10))
        ampEntry = Entry(win, textvariable=self.ampString, validate = 'key', validatecommand = self.vcmd)
        ampEntry.grid(column = 0, row = 3, padx=50)

        refreshButton = Button(win, text="Atualizar", command=self.refreshParams)
        refreshButton.grid(column=0, row=4, padx=10, pady=(50,50))

    def sinWaveConfig(self):
        win = Toplevel(self)
        win.resizable(width=False, height=False)
        win.title("Sin Wave Config")

        self.Signal = 'Onda Senoidal'

        self.Malha = 'Malha Aberta'
        infoMalha = Label(win, text='Malha')
        infoMalha.grid(column=0, row=0,  padx=50, pady=(50,10))
        self.comboMalha = Combobox(win, state='readonly', text='Malha',values=['Malha Aberta', 'Malha Fechada'])
        self.comboMalha.current(0)
        self.comboMalha.bind('<<ComboboxSelected>>', self.malhaChanged)
        self.comboMalha.grid(column=0, row=1, padx=50)

        infoPeriodEntry = Label(win, text='Período')
        infoPeriodEntry.grid(column=0, row=2,  padx=50, pady=(50,10))
        PeriodEntry = Entry(win, textvariable=self.periodString, validate = 'key', validatecommand = self.vcmd)
        PeriodEntry.grid(column = 0, row = 3, padx=50)

        infoAmpEntry = Label(win, text='Amplitude')
        infoAmpEntry.grid(column=0, row=4,  padx=50, pady=(50,10))
        ampEntry = Entry(win, textvariable=self.ampString, validate = 'key', validatecommand = self.vcmd)
        ampEntry.grid(column = 0, row = 5, padx=50)

        infoOffsetEntry = Label(win, text='Offset')
        infoOffsetEntry.grid(column=0, row=6,  padx=50, pady=(50,10))
        OffsetEntry = Entry(win, textvariable=self.offsetString, validate = 'key', validatecommand = self.vcmd)
        OffsetEntry.grid(column = 0, row = 7, padx=50)

        refreshButton = Button(win, text="Atualizar", command=self.refreshParams)
        refreshButton.grid(column=0, row=8, padx=10, pady=(50,50))

    def squareWaveConfig(self):
        win = Toplevel(self)
        win.resizable(width=False, height=False)
        win.title("Square Wave Config")

        self.Signal = 'Onda quadrada'

        self.Malha = 'Malha Aberta'
        infoMalha = Label(win, text='Malha')
        infoMalha.grid(column=0, row=0,  padx=50, pady=(50,10))
        self.comboMalha = Combobox(win, state='readonly', text='Malha',values=['Malha Aberta', 'Malha Fechada'])
        self.comboMalha.current(0)
        self.comboMalha.bind('<<ComboboxSelected>>', self.malhaChanged)
        self.comboMalha.grid(column=0, row=1, padx=50)

        infoPeriodEntry = Label(win, text='Período')
        infoPeriodEntry.grid(column=0, row=2,  padx=50, pady=(50,10))
        PeriodEntry = Entry(win, textvariable=self.periodString, validate = 'key', validatecommand = self.vcmd)
        PeriodEntry.grid(column = 0, row = 3, padx=50)

        infoAmpEntry = Label(win, text='Amplitude')
        infoAmpEntry.grid(column=0, row=4,  padx=50, pady=(50,10))
        ampEntry = Entry(win, textvariable=self.ampString, validate = 'key', validatecommand = self.vcmd)
        ampEntry.grid(column = 0, row = 5, padx=50)

        infoOffsetEntry = Label(win, text='Offset')
        infoOffsetEntry.grid(column=0, row=6,  padx=50, pady=(50,10))
        OffsetEntry = Entry(win, textvariable=self.offsetString, validate = 'key', validatecommand = self.vcmd)
        OffsetEntry.grid(column = 0, row = 7, padx=50)

        refreshButton = Button(win, text="Atualizar", command=self.refreshParams)
        refreshButton.grid(column=0, row=8, padx=10, pady=(50,50))

    def sawToothConfig(self):
        win = Toplevel(self)
        win.resizable(width=False, height=False)
        win.title("Saw Tooth Config")

        self.Signal = 'Onda dente de serra'

        self.Malha = 'Malha Aberta'
        infoMalha = Label(win, text='Malha')
        infoMalha.grid(column=0, row=0,  padx=50, pady=(50,10))
        self.comboMalha = Combobox(win, state='readonly', text='Malha',values=['Malha Aberta', 'Malha Fechada'])
        self.comboMalha.current(0)
        self.comboMalha.bind('<<ComboboxSelected>>', self.malhaChanged)
        self.comboMalha.grid(column=0, row=1, padx=50)

        infoPeriodEntry = Label(win, text='Período')
        infoPeriodEntry.grid(column=0, row=2,  padx=50, pady=(50,10))
        PeriodEntry = Entry(win, textvariable=self.periodString, validate = 'key', validatecommand = self.vcmd)
        PeriodEntry.grid(column = 0, row = 3, padx=50)

        infoAmpEntry = Label(win, text='Amplitude')
        infoAmpEntry.grid(column=0, row=4,  padx=50, pady=(50,10))
        ampEntry = Entry(win, textvariable=self.ampString, validate = 'key', validatecommand = self.vcmd)
        ampEntry.grid(column = 0, row = 5, padx=50)

        infoOffsetEntry = Label(win, text='Offset')
        infoOffsetEntry.grid(column=0, row=6,  padx=50, pady=(50,10))
        OffsetEntry = Entry(win, textvariable=self.offsetString, validate = 'key', validatecommand = self.vcmd)
        OffsetEntry.grid(column = 0, row = 7, padx=50)

        refreshButton = Button(win, text="Atualizar", command=self.refreshParams)
        refreshButton.grid(column=0, row=8, padx=10, pady=(50,50))

    def aleatoryConfig(self):
        win = Toplevel(self)
        win.resizable(width=False, height=False)
        win.title("Aleatory Config")

        self.Signal = 'Sinal aleatório'

        self.Malha = 'Malha Aberta'
        infoMalha = Label(win, text='Malha')
        infoMalha.grid(column=0, row=0,  padx=50, pady=(50,10))
        self.comboMalha = Combobox(win, state='readonly', text='Malha',values=['Malha Aberta', 'Malha Fechada'])
        self.comboMalha.current(0)
        self.comboMalha.bind('<<ComboboxSelected>>', self.malhaChanged)
        self.comboMalha.grid(column=0, row=1, padx=50)

        infoPeriodEntry = Label(win, text='Período máximo')
        infoPeriodEntry.grid(column=0, row=2,  padx=50, pady=(50,10))
        PeriodEntry = Entry(win, textvariable=self.periodString, validate = 'key', validatecommand = self.vcmd)
        PeriodEntry.grid(column = 0, row = 3, padx=50)

        infoMinPeriodEntry = Label(win, text='Período mínimo')
        infoMinPeriodEntry.grid(column=0, row=4,  padx=50, pady=(50,10))
        MinPeriodEntry = Entry(win, textvariable=self.periodMinString, validate = 'key', validatecommand = self.vcmd)
        MinPeriodEntry.grid(column = 0, row = 5, padx=50)

        infoAmpEntry = Label(win, text='Amplitude máxima')
        infoAmpEntry.grid(column=0, row=6,  padx=50, pady=(50,10))
        ampEntry = Entry(win, textvariable=self.ampString, validate = 'key', validatecommand = self.vcmd)
        ampEntry.grid(column = 0, row = 7, padx=50)

        infoMinAmpEntry = Label(win, text='Amplitude mínima')
        infoMinAmpEntry.grid(column=0, row=8,  padx=50, pady=(50,10))
        MinAmpEntry = Entry(win, textvariable=self.ampMinString, validate = 'key', validatecommand = self.vcmd)
        MinAmpEntry.grid(column = 0, row = 9, padx=50)

        refreshButton = Button(win, text="Atualizar", command=self.refreshParams)
        refreshButton.grid(column=0, row=10, padx=10, pady=(50,50))


    async def updater(self, interval):
        self.resizable(width=False, height=False)

        self.title('iDynamic Controller')

        self.info = Label(self, text='PROJETO DE SISTEMAS DE CONTROLE - iDYNAMIC')
        self.info.grid(column=0, row=0,  padx=10, pady=0)

        self.menubar = Menu(self)

        self.Signal = Menu(self.menubar)
        self.Signal.add_command(label='Tam. Dados', command=self.configGraphSize)
        self.Signal.add_command(label='Sair', command=self.RemoteControl.finish)
        self.menubar.add_cascade(label="Configurações", menu=self.Signal)

        self.Signal = Menu(self.menubar)
        self.Signal.add_command(label='Degrau', command=self.stepWaveConfig)
        self.Signal.add_command(label='Onda Senoidal', command=self.sinWaveConfig)
        self.Signal.add_command(label='Onda quadrada', command=self.squareWaveConfig)
        self.Signal.add_command(label='Onda dente de serra', command=self.sawToothConfig)
        self.Signal.add_command(label='Sinal aleatório', command=self.aleatoryConfig)
        self.menubar.add_cascade(label="Sinal", menu=self.Signal)

        self.Controlador = Menu(self.menubar)
        self.Controlador.add_command(label='Erro')
        self.Controlador.add_command(label='P')
        self.Controlador.add_command(label='PD')
        self.Controlador.add_command(label='PI')
        self.Controlador.add_command(label='PID')
        self.Controlador.add_command(label='PI-D')
        self.Controlador.add_command(label='I-PD')
        self.menubar.add_cascade(label="Controlador", menu=self.Controlador)

        self.config(menu=self.menubar)

        self.figure1 = plt.figure(figsize=(25,15), dpi = 50)

        self.ax = self.figure1.add_subplot(1,1,1)

        self.ax.title.set_text("Estados do sistema")
        self.ax.set(xlabel='Tempo', ylabel='Posição')

        self.canvas=FigureCanvasTkAgg(self.figure1 ,master=self)
        self.graph = self.canvas.get_tk_widget()
        self.graph.grid(row=1,column=0)

        while await asyncio.sleep(interval, True):
            self.update()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    gui = myGui(loop)
    loop.run_forever()
    loop.close()

