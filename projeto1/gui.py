
from cProfile import label
from tkinter import *
import asyncio
from tkinter.messagebox import showinfo
from tkinter.ttk import *
from tkinter.colorchooser import askcolor
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

f = Figure(figsize = (5,5), dpi = 100)
graph = f.add_subplot(111)
class myGui(Tk):
    def __init__(self, RemoteControl):
        super().__init__()
        self.GraphSize = StringVar()
        self.GraphSize.set("10")
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
        self.performanceString = StringVar()
        self.performanceString.set("0.0")
        self.RemoteControl = RemoteControl
        self.protocol("WM_DELETE_WINDOW", self.RemoteControl.finish)
        self.timeData = list()
        self.refData = list() 
        self.errorData = list() 
        self.out1Data = list() 
        self.out2Data = list() 
        self.Malha = 'Malha Aberta'
        self.Saida = 'Saída 1'
        self.Signal = 'Degrau'
        self.controller = 'Erro'
        self.P = StringVar()
        self.P.set("1.0")
        self.I = StringVar()
        self.I.set("1.0")
        self.D = StringVar()
        self.D.set("1.0")
        self.vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.refColor = 'blue'
        self.errorColor = 'yellow'
        self.exit1 = 'green'
        self.exit2 = 'red'
        self.pause = False
        self.yLimString = StringVar()
        self.yLimString.set("100")

    def pauseGraph(self):
        self.pause = not self.pause

    def refreshParams(self):
        self.RemoteControl.refreshParams(self.Malha, self.Signal, self.Saida, float(self.ampString.get()), float(self.periodString.get()), float(self.offsetString.get()), float(self.ampMinString.get()), float(self.periodMinString.get()), self.controller, float(self.P.get()), float(self.I.get()), float(self.D.get()), float(self.performanceString.get()))

    def change_color_ref(self):
        color = askcolor(title="Choose a color")
        self.refColor = color[1]

    def change_color_error(self):
        color = askcolor(title="Choose a color")
        self.errorColor = color[1]

    def change_color_exit1(self):
        color = askcolor(title="Choose a color")
        self.exit1 = color[1]

    def change_color_exit2(self):
        color = askcolor(title="Choose a color")
        self.exit2 = color[1]

    def updateValues(self, timeData, refData, errorData, out1Data, out2Data):
        if(self.pause):
            return

        self.ax.clear()

        if(len(self.timeData)>2):
            while((self.timeData[-1] - self.timeData[0]) >= int(self.GraphSize.get())):

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

        self.ax.plot(self.timeData[:] ,self.refData[:], linestyle="solid", marker='.', linewidth=2, markersize=1, color=self.refColor)
        self.ax.plot(self.timeData[:] ,self.errorData[:], linestyle="solid", marker='.', linewidth=2, markersize=1, color=self.errorColor)
        self.ax.plot(self.timeData[:] ,self.out1Data[:], linestyle="solid", marker='.', linewidth=2, markersize=1, color=self.exit1)
        self.ax.plot(self.timeData[:] ,self.out2Data[:], linestyle="solid", marker='.', linewidth=2, markersize=1, color=self.exit2)

        self.ax.set_ylim(bottom=-int(self.yLimString.get()), top=int(self.yLimString.get()))

        self.ax.title.set_text("Estados do sistema")
        self.ax.grid()
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
    
    def controllerChanged(self, event):
        self.controller = self.comboController.get()
    
    def saidaChanged(self, event):
        self.Saida = self.comboSaida.get()

    def showPerformancePopUp(self, IAE,ISE,ITAE, goodHart):
        self.performanceString.set("0.0")

        win = Toplevel(self)
        win.resizable(width=False, height=False)
        win.title("Performance info")

        IAEInfo = Label(win, text='IAE:{0}'.format(IAE))
        IAEInfo.grid(column = 0, row = 0, padx=50, pady=(50,10))

        ISEInfo = Label(win, text='ISE:{0}'.format(ISE))
        ISEInfo.grid(column = 0, row = 1, padx=50, pady=(50,10))

        ITAEInfo = Label(win, text='ITAE:{0}'.format(ITAE))
        ITAEInfo.grid(column = 0, row = 2, padx=50, pady=(50,10))

        goodHartInfo = Label(win, text='goodHart:{0}'.format(goodHart))
        goodHartInfo.grid(column = 0, row = 3, padx=50, pady=(50,10))

    def configGraphSize(self):
        win = Toplevel(self)
        win.resizable(width=False, height=False)
        win.title("Graph Size")

        infoGraphSize = Label(win, text='Número de dados exibidos no gráfico:')
        infoGraphSize.grid(column=0, row=0,  padx=50, pady=(50,10))
        GraphSizeEntry = Entry(win, textvariable=self.GraphSize, validate = 'key', validatecommand = self.vcmd)
        GraphSizeEntry.grid(column = 0, row = 1, pady=(10,10))

        infoYLim = Label(win, text='Limites do gráfico:')
        infoYLim .grid(column=0, row=2,  padx=50, pady=(50,10))
        yLimEntry = Entry(win, textvariable=self.yLimString, validate = 'key', validatecommand = self.vcmd)
        yLimEntry.grid(column = 0, row = 3, pady=(10,10))

        infoSaida = Label(win, text='Saída')
        infoSaida.grid(column=0, row=4,  padx=50, pady=(50,10))
        self.comboSaida = Combobox(win, state='readonly', text='Saída',values=['Saída 1', 'Saída 2'])
        if(self.Saida == 'Saída 1'):
            self.comboSaida.current(0)
        else:
            self.comboSaida.current(1)
        self.comboSaida.bind('<<ComboboxSelected>>', self.saidaChanged)
        self.comboSaida.grid(column=0, row=5, padx=50, pady=(10,50))

        button = Button(win, text='Cor Referência', command=self.change_color_ref)
        button.grid(column=0, row=6, padx=50, pady=(10,10))
        button = Button(win, text='Cor Erro', command=self.change_color_error)
        button.grid(column=0, row=7, padx=50, pady=(10,10))
        button = Button(win, text='Cor Saída 1', command=self.change_color_exit1)
        button.grid(column=0, row=8, padx=50, pady=(10,10))
        button = Button(win, text='Cor Saída 2', command=self.change_color_exit2)
        button.grid(column=0, row=9, padx=50, pady=(10,10))
        refreshButton = Button(win, text="Atualizar", command=self.refreshParams)
        refreshButton.grid(column=0, row=10, padx=10, pady=(30,50))

    def stepWaveConfig(self):
        win = Toplevel(self)
        win.resizable(width=False, height=False)
        win.title("Step Wave Config")

        self.Signal = 'Degrau'

        infoMalha = Label(win, text='Malha')
        infoMalha.grid(column=0, row=0,  padx=50, pady=(50,10))
        self.comboMalha = Combobox(win, state='readonly', text='Malha',values=['Malha Aberta', 'Malha Fechada'])
        if(self.Malha == 'Malha Aberta'):
            self.comboMalha.current(0)
        else:
            self.comboMalha.current(1)
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

        infoMalha = Label(win, text='Malha')
        infoMalha.grid(column=0, row=0,  padx=50, pady=(50,10))
        self.comboMalha = Combobox(win, state='readonly', text='Malha',values=['Malha Aberta', 'Malha Fechada'])
        if(self.Malha == 'Malha Aberta'):
            self.comboMalha.current(0)
        else:
            self.comboMalha.current(1)
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

        infoMalha = Label(win, text='Malha')
        infoMalha.grid(column=0, row=0,  padx=50, pady=(50,10))
        self.comboMalha = Combobox(win, state='readonly', text='Malha',values=['Malha Aberta', 'Malha Fechada'])
        if(self.Malha == 'Malha Aberta'):
            self.comboMalha.current(0)
        else:
            self.comboMalha.current(1)
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

        infoMalha = Label(win, text='Malha')
        infoMalha.grid(column=0, row=0,  padx=50, pady=(50,10))
        self.comboMalha = Combobox(win, state='readonly', text='Malha',values=['Malha Aberta', 'Malha Fechada'])
        if(self.Malha == 'Malha Aberta'):
            self.comboMalha.current(0)
        else:
            self.comboMalha.current(1)
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

        infoMalha = Label(win, text='Malha')
        infoMalha.grid(column=0, row=0,  padx=50, pady=(50,10))
        self.comboMalha = Combobox(win, state='readonly', text='Malha',values=['Malha Aberta', 'Malha Fechada'])
        if(self.Malha == 'Malha Aberta'):
            self.comboMalha.current(0)
        else:
            self.comboMalha.current(1)
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

    def configController(self):
        win = Toplevel(self)
        win.resizable(width=False, height=False)
        win.title("Config Controller")

        infoController = Label(win, text='Controlador')
        infoController.grid(column=0, row=0,  padx=50, pady=(50,10))
        self.comboController = Combobox(win, state='readonly', text='Controlador',values=['Erro', 'P', 'PD', 'PI', 'PID', 'PI-D', 'I-PD'])
        if(self.controller == 'Erro'):
            self.comboController.current(0)
        elif(self.controller == 'P'):
            self.comboController.current(1)
        elif(self.controller == 'PD'):
            self.comboController.current(2)
        elif(self.controller == 'PI'):
            self.comboController.current(3)
        elif(self.controller == 'PID'):
            self.comboController.current(4)
        elif(self.controller == 'PI-D'):
            self.comboController.current(5)  
        else:
            self.comboController.current(6)  
        self.comboController.bind('<<ComboboxSelected>>', self.controllerChanged)
        self.comboController.grid(column=0, row=1, padx=50)

        infoPEntry = Label(win, text='P')
        infoPEntry.grid(column=0, row=2,  padx=50, pady=(50,10))
        PEntry = Entry(win, textvariable=self.P, validate = 'key', validatecommand = self.vcmd)
        PEntry.grid(column = 0, row = 3, padx=50)

        infoIEntry = Label(win, text='I')
        infoIEntry.grid(column=0, row=4,  padx=50, pady=(50,10))
        IEntry = Entry(win, textvariable=self.I, validate = 'key', validatecommand = self.vcmd)
        IEntry.grid(column = 0, row = 5, padx=50)

        infoDEntry = Label(win, text='D')
        infoDEntry.grid(column=0, row=6,  padx=50, pady=(50,10))
        DEntry = Entry(win, textvariable=self.D, validate = 'key', validatecommand = self.vcmd)
        DEntry.grid(column = 0, row = 7, padx=50)

        infoPerformance = Label(win, text='Cálcular desempenho (seg.)')
        infoPerformance.grid(column=0, row=8,  padx=50, pady=(50,10))
        performanceEntry = Entry(win, textvariable=self.performanceString, validate = 'key', validatecommand = self.vcmd)
        performanceEntry.grid(column = 0, row = 9, padx=50)

        refreshButton = Button(win, text="Atualizar", command=self.refreshParams)
        refreshButton.grid(column=0, row=10, padx=10, pady=(50,50))

    async def updater(self, interval):
        self.resizable(width=False, height=False)

        self.title('iDynamic Controller')

        self.info = Label(self, text='PROJETO DE SISTEMAS DE CONTROLE - iDYNAMIC')
        self.info.grid(column=0, row=0,  padx=0, pady=0)

        self.menubar = Menu(self)

        self.Signal = Menu(self.menubar)
        self.Signal.add_command(label='Configurar', command=self.configGraphSize)
        self.Signal.add_command(label='Pausar', command=self.pauseGraph)
        self.Signal.add_command(label='Sair', command=self.RemoteControl.finish)
        self.menubar.add_cascade(label="Configurações", menu=self.Signal)

        self.Signal = Menu(self.menubar)
        self.Signal.add_command(label='Degrau', command=self.stepWaveConfig)
        self.Signal.add_command(label='Onda Senoidal', command=self.sinWaveConfig)
        self.Signal.add_command(label='Onda quadrada', command=self.squareWaveConfig)
        self.Signal.add_command(label='Onda dente de serra', command=self.sawToothConfig)
        self.Signal.add_command(label='Sinal aleatório', command=self.aleatoryConfig)
        self.menubar.add_cascade(label="Sinal", menu=self.Signal)

        self.controllerMenu = Menu(self.menubar)
        self.controllerMenu.add_command(label='Configurar', command=self.configController)
        self.menubar.add_cascade(label="Controlador", menu=self.controllerMenu)

        self.config(menu=self.menubar)

        self.configure(background='#c5c6c9')

        self.figure1 = plt.figure(figsize=(25,15), dpi = 50)

        self.figure1.patch.set_facecolor('#c5c6c9')

        self.ax = self.figure1.add_subplot(1,1,1)

        self.ax.title.set_text("Estados do sistema")
        self.ax.set(xlabel='Tempo', ylabel='Posição')
        if(int(self.yLimString.get()) > 0):
            self.ax.set_ylim(bottom=-int(self.yLimString.get()), top=int(self.yLimString.get()))
        self.ax.grid()
        self.ax.set_facecolor('#404142')

        self.canvas=FigureCanvasTkAgg(self.figure1 ,master=self)
        self.graph = self.canvas.get_tk_widget()
        self.graph.grid(row=1,column=0, padx=10)

        while await asyncio.sleep(interval, True):
            self.update()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    gui = myGui(loop)
    loop.run_forever()
    loop.close()

