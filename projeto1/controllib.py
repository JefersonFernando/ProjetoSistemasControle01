import asyncio
from typing_extensions import Self
import websockets
from collections import deque
from math import *
import numpy as np
import time
from gui import *



class Control:
	def __init__(self, T=0.3, order=3):
		self.T = T
		self._e = deque([0]*order)
		self._u = deque([0]*order)
		self._y = deque([0]*order)
		self._r = deque([0]*order)
		self.currU = 0
		self.time = 0.0
		self.startTime = 0.0
		self.currentAmp = float(0.0)
		self.KP = 0
		self.TI = 0
		self.I = 0
		self.TD = 0
		self.controller = "Erro"
		self.IAE = 0
		self.ISE = 0
		self.ITAE = 0
		self.goodhart = 0
		self.performanceStartTime = 0
		self.performanceTime = 0

	def reference(self, ref):
		self._r.rotate(-1)
		self._r[-1] = ref

	def measured(self, y):

		error = self._r[-1] - y

		self._e.rotate(-1)
		self._e[-1] = error

		self._y.rotate(-1)
		self._y[-1] = y

	def control(self):

		return 0

	def apply(self, controlSignal):

		self._u.rotate(-1)
		self._u[-1] = controlSignal

	def u(self, index = 0):
		return self._u[index]
	def e(self, index = 0):
		return self._e[index-1]
	def r(self, index = 0):
		return self._r[index-1]
	def y(self, index = 0):
		return self._y[index-1]

class RemoteControl:

	def __init__(self, controller, loop, interval=1/120, verbose = False):
		self.startTime = time.time()
		self.controller = controller
		self.verbose = verbose
		self.loop = loop
		self.tasks = []
		self.gui = myGui(self)
		self.tasks.append(loop.create_task(self.gui.updater(interval)))
		self.tasks.append(loop.create_task(self.run()))

		self.malha = 'Malha Aberta'
		self.signal = 'Degrau'
		self.amplitude = 1.0
		self.period = 1.0
		self.offset = 0.0
		self.ampMin = 1.0
		self.periodMin = 1.0

		self.out = 'Saída 1'

	def finish(self):
		for task in self.tasks:
			task.cancel()
		self.loop.stop()
		self.destroy()

	def refreshParams(self, malha, signal, saida, amplitude, period, offset, ampMin, periodMin, controller, P, I, D, performanceTime):	
		self.malha = malha
		self.signal = signal
		self.out = saida
		self.amplitude = amplitude
		self.period = period
		self.offset = offset
		self.ampMin = ampMin
		self.periodMin = periodMin
		self.controller.controller = controller
		self.controller.KP = P
		self.controller.TI = I
		self.controller.TD = D
		self.controller.performanceStartTime = time.time() - self.startTime
		self.controller.performanceTime = performanceTime
		self.controller.IAE = 0.0
		self.controller.ISE = 0.0
		self.controller.ITAE = 0.0
		self.controller.goodhart = 0.0

	async def serverLoop(self, websocket, path):
		while True:

			await asyncio.sleep(self.controller.T)

			self.currentTime = time.time() - self.startTime

			try:

				print('get references') if self.verbose else None
				references = []
				await websocket.send('get references')
				received = (await websocket.recv()).split(',')
				print(received) if self.verbose else None
				ref = float(received[1])

				if isnan(ref):
					ref = 0.0

				print('get outputs') if self.verbose else None
				outputs = []
				await websocket.send('get outputs')
				received = (await websocket.recv()).split(',')
				print(received) if self.verbose else None

				if((self.out == 'Saída 2') and (len(received) > 2)):
					out = float(received[2])
				else:
					out = float(received[1])

				if self.signal == 'Degrau':
					ref = self.controller.stepWave(self.amplitude)
				elif self.signal == 'Onda Senoidal':
					ref = self.controller.sin(self.currentTime, self.offset, self.amplitude, self.period)
				elif self.signal == 'Onda quadrada':
					ref = self.controller.squareWave(self.currentTime, self.period, self.amplitude, self.offset)
				elif self.signal == 'Onda dente de serra':
					ref = self.controller.sawTooth(self.currentTime, self.period, self.amplitude, self.offset)
				else:
					ref = self.controller.aleatory(self.currentTime, self.amplitude, self.ampMin, self.period, self.periodMin)

				self.controller.reference(ref)
				self.controller.measured(out)

				if(len(received) > 2):
					out2 = float(received[2])
				else:
					out2 = 0.0

				if self.malha == 'Malha Fechada':
					u = self.controller.control()
					self.gui.updateValues(self.currentTime, ref, u, float(received[1]), out2)
				else:
					u = ref
					self.gui.updateValues(self.currentTime, ref, ref, float(received[1]), out2)

				self.controller.apply(u)

				if((self.controller.performanceTime != 0) and (self.currentTime - self.controller.performanceStartTime > self.controller.performanceTime)):
					self.performanceStartTime = 0
					self.controller.performanceTime = 0
					self.gui.showPerformancePopUp(self.controller.IAE,self.controller.ISE,self.controller.ITAE, self.controller.goodhart)
				
				print(f'u = {u}') if self.verbose else None
				await websocket.send('set input|'+f"{u}")

				# ellapsedTime = 0.0

				# while ellapsedTime < self.controller.T:
				time.sleep(self.controller.T)
					# endTime = time.time()
					# ellapsedTime = endTime - self.startLoopTime

			except:
				print('System not active...') if self.verbose else None

	def run(self):

		print('Trying connection')

		server = websockets.serve(self.serverLoop, "localhost", 6660)

		print('Connected')

		asyncio.ensure_future(server)
		asyncio.get_event_loop().run_forever()