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

	def PIDController(self):
		P = self.KP*self.e(0)
		self.I += self.KI*self.e(0)*self.T
		D = self.KD*(self.e(0) - self.e(-1))/self.T

		return P+self.I+D

	def PController(self):
		P = self.KP*self.e(0)

		return P

	def PIController(self):
		P = self.KP*self.e(0)
		self.I += self.KI*self.e(0)*self.T
		print("E:{0}".format(self.e(0)))
		print("T:{0}".format(self.T))
		print("I:{0}".format(self.I))

		return P+self.I

	def PDController(self):
		P = self.KP*self.e(0)
		D = self.KD*(self.e(0) - self.e(-1))/self.T

		print("E0:{0}".format(self.e(0)))
		print("E-1:{0}".format(self.e(-1)))
		print("T:{0}".format(self.T))
		print("KD:{0}".format(self.KD))
		print("I:{0}".format(D))
		print("P:{0}".format(P))
		return P+D

	def I_PDController(self):
		P = self.KP*self.e(0)
		self.I += self.KI*self.e(0)*self.T
		D = self.KD * (self.y(0) - self.y(-1))
		return P + self.I + D

	def control(self):

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