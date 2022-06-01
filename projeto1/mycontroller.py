from controllib import *
from gui import *
import numpy as np
from scipy import signal
import random

class firstControl(Control): 

	def sin(self, time, offset, amplitude, period):
		return ((amplitude * np.sin(2* np.pi * (1/period) * time )) + offset)

	def sawTooth(self, time, period, amplitude, offset):
		return (amplitude*signal.sawtooth(2*np.pi*(time/period)) + offset)

	def squareWave(self, time, period, amplitude, offset):
		return (amplitude*signal.square(2*np.pi*(time/period)) + offset)

	def stepWave(self, amplitude):
		return amplitude

	def aleatory(self, time, maxAmplitude, minAmplitude, maxPeriod, minPeriod):
		if((time - self.startTime) >= maxPeriod):
			self.currentAmp = random.uniform(minAmplitude, maxAmplitude)
			self.startTime = time
		elif((time - self.startTime) >= minPeriod):
			if(random.randint(0,1) == 1):
				self.currentAmp = random.uniform(minAmplitude, maxAmplitude)
				self.startTime = time

		return self.currentAmp

	def errorControl(self):
		u0 = 0.9*self.e(0)

		return u0

	def PController(self):
		P = self.KP*self.e(0)

		return P

	def PIController(self):
		P = self.KP*self.e(0)
		self.I += self.TI*(self.e(0)*self.T)

		return P+self.I

	def PDController(self):
		P = self.KP*self.e(0)
		D = self.TD*(self.e(0) - self.e(-1))
		return P+D

	def PIDController(self):
		P = self.KP*self.e(0)
		self.I += self.TI*(self.e(0)*self.T)
		D = self.TD*(self.e(0) - self.e(-1))

		return P+self.I+D

	def I_PDController(self):
		P = self.KP*self.y(0)
		self.I += self.TI*self.e(0)*self.T
		D = self.TD * (self.y(0) - self.y(-1))
		return P + self.I + D

	def calculateIAE(self):
		self.IAE += np.abs(self.e(0))
		return

	def calculateISE(self):
		self.ISE += np.abs(self.e(0))**2
		return

	def calculateITAE(self):
		self.ITAE += self.T*np.abs(self.e(0))
		return

	def calculategoodhart(self):
		currentU = self.u(0)
		currentE = self.e(0)

		self.goodhart += (0.4*currentU)/self.performanceTime
		self.goodhart += (0.4*((currentU - currentE)**2))/self.performanceTime
		self.goodhart += (0.2*(currentE**2))/self.performanceTime
		return

	def control(self):

		if(self.performanceStartTime != 0 and self.performanceTime != 0):
			self.calculateIAE()
			self.calculateISE()
			self.calculateITAE()
			self.calculategoodhart()

		if (self.controller == 'Erro'):
			return self.errorControl()
		if (self.controller == 'P'):
			return self.PController()
		if (self.controller == 'PD'):
			return self.PDController()
		if (self.controller == 'PI'):
			return self.PIController()
		if (self.controller == 'PID'):
			return self.PIDController()
		if (self.controller == 'PI-D'):
			return self.PIDController()
		if (self.controller == 'I-PD'):
			return self.I_PDController()

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	controller = firstControl(0.01, 3)
	rc = RemoteControl(controller, loop, verbose=False)
	loop.run_forever()
	loop.close()