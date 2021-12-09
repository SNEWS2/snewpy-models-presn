import numpy as np

def readBetaLuminosityTotal(filename):
	"""
	Reads a file with total beta luminosity for neutrinos and antineutrinos
	
	:param filename: Filename to be read
	:return: numpy array:
		neutrino_energy in MeV
		lnue electron neutrino flux in 1/MeV/s
		lnuebar electron anit-neutrino flux in 1/MeV/s
	:return: float, tau_cc time till CC in hours
	
	"""
	with open(filename,'r') as f:
		_ = f.readline()
		l = f.readline()
	time = l.split()[-1]

	data = np.genfromtxt(filename,names=['neutrino_energy','lnue','lnuebar'])
	return data,time

def readBetaLuminosityIsotopes(filename):
	"""
	Reads a file with isotope data for capture and decay luminosities.
	
	These files have both Nu and NuBar versions
	
	:param filename: Filename to be read
	:return: dict where each key is one reaction, and each item is a numpy array of:
			neutrino_energy in MeV
			capture rate in MeV^-1 s^-1
			decay rate in MeV^-1 s^-1
	:return: float, tau_cc time till CC in hours
	
	"""

	data = {}

	with open(filename,'r') as f:
		for i in range(7):
			_=f.readline()
		
		while True:
			l = f.readline()
			if len(l)==0:
				break
			reaction = l.split()[1]
			time = l.split()[-1]
			_ = f.readline()
			tmp = []
			while True:
				l = f.readline()
				if len(l.strip()) == 0:
					_ = f.readline()
					break
				tmp.append(l.strip().split('\t'))
			data[reaction] = np.array(tmp,dtype=[('neutrino_energy',float),('capture',float),('decay',float)])
	return data,time
	
def readPairLuminosity(filename):
	"""
	Reads a file with total pair luminosity for neutrinos and antineutrinos
	
	:param filename: Filename to be read
	:return: numpy array, with columns 
		tau_cc time to CC in hrs
		neutrino_energy in MeV
		lnue  electron neutrino luminosity (1/MeV/s)
		lnuebar electron antineutrino luminosity (1/MeV/s)
		lnux mu/tau neutrino luminosity (1/MeV/s)
		lnuxbar mu/tau antineutrino luminosity (1/MeV/s)
		Columns for mu/tau flavors should be doubled to account for both flavors
	"""

	with open(filename,'r') as f:
		_ = f.readline()
		l = f.readline()
	time = l.split()[-1]

	data = np.genfromtxt(filename,names=['neutrino_energy','lnue',
							'lnuebar','lnux','lnuxbar'])
	return data, time

def readTotalLuminosity(filename):
	"""
	Reads a file with total pair+beta luminosity for neutrinos and antineutrinos
	
	:param filename: Filename to be read
	:return: numpy array, with columns 
		tau_cc time to CC in hrs
		neutrino_energy in MeV
		lnue  electron neutrino luminosity (1/MeV/s)
		lnuebar electron antineutrino luminosity (1/MeV/s)
		lnux mu/tau neutrino luminosity (1/MeV/s)
		lnuxbar mu/tau antineutrino luminosity (1/MeV/s)
		lnue_beta electron neutrino luminosity from beta processes (1/MeV/s)
		lnuebar_beta electron antineutrino luminosity from beta processes (1/MeV/s)
		lnue_pair electron neutrino luminosity from pair processes (1/MeV/s)
		lnuebar_pair electron antineutrino luminosity from pair processes (1/MeV/s)
		Columns for mu/tau flavors should be doubled to account for both flavors
		All mu/tau flavors come from the pair process
	"""

	data = np.genfromtxt(filename,names=['tau_cc','neutrino_energy','lnue',
							'lnuebar','lnux','lnuxbar','lnue_beta','lnuebar_beta',
							'lnue_pair','lnuebar_pair'])
	return data
	
