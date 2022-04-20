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

	def finish(self):
		for task in self.tasks:
			task.cancel()
		self.loop.stop()
		self.destroy()

	def refreshParams(self, malha, signal, amplitude, period, offset, ampMin, periodMin):	
		self.malha = malha
		self.signal = signal
		self.amplitude = amplitude
		self.period = period
		self.offset = offset
		self.ampMin = ampMin
		self.periodMin = periodMin

	async def serverLoop(self, websocket, path):

		while True:
			startTime = time.time()

			await asyncio.sleep(self.controller.T)

			self.controller.time += self.controller.T

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
				out = float(received[1])


				if self.signal == 'Degrau':
					ref = self.controller.stepWave(self.amplitude)
				elif self.signal == 'Onda Senoidal':
					ref = self.controller.sin(self.controller.time, self.offset, self.amplitude, self.period)
				elif self.signal == 'Onda quadrada':
					ref = self.controller.squareWave(self.controller.time, self.period, self.amplitude, self.offset)
				elif self.signal == 'Onda dente de serra':
					ref = self.controller.sawTooth(self.controller.time, self.period, self.amplitude, self.offset)
				else:
					ref = self.controller.aleatory(self.controller.time, self.amplitude, self.ampMin, self.period, self.periodMin)

				


				if self.malha == 'Malha Fechada':
					self.controller.reference(ref)

					self.controller.measured(out)

					u = self.controller.control()	

					self.gui.updateValues(self.controller.time, ref, u, float(received[1]), float(received[2]))
					
				else:
					u = ref
					self.gui.updateValues(self.controller.time, ref, ref, float(received[1]), float(received[2]))

				self.controller.apply(u)
				
				print(f'u = {u}') if self.verbose else None
				await websocket.send('set input|'+f"{u}")


				ellapsedTime = 0.0

				while ellapsedTime < self.controller.T:
					time.sleep(0.0001)
					endTime = time.time()
					ellapsedTime = endTime - startTime

			except:
				print('System not active...') if self.verbose else None

	def run(self):

		print('Trying connection')

		server = websockets.serve(self.serverLoop, "localhost", 6660)

		print('Connected')

		asyncio.ensure_future(server)
		asyncio.get_event_loop().run_forever()