from controllib import *
from gui import *
import numpy as np
from scipy import signal
import random

class firstControl(Control): 

	def sin(self, time, offset, amplitude, period):
		print(time)
		print(offset)
		print(amplitude)
		print(period)
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

	def control(self):
		""" 
		Return the control signal.
		You can access the error at instant 0, -1, and -2 as:
		self.e(0), self.e(-1) and self.e(-2) respectively 
		Obs.: To access more errors, create your controller with the 
		command:
		controller = MyControllerName(T, n)		
		where T is the sampling time (normally 0.3) and n is the order 
		of the controller (how many errors you can access)
		For instance:
		controller = MyControllerName(0.5, 6)
		Will use a controller with 0.5s sampling time and will access
		from self.e(0) up to self.e(-5)
		"""

		# in this simple controller, it applies a control signal that 
		# is 90% the current error


		u0 = 0.9*self.e(0)

		return u0

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	controller = firstControl(0.1, 3)
	rc = RemoteControl(controller, loop, verbose=False)
	loop.run_forever()
	loop.close()