Data of presupernova neutrino spectra for 12M, 15M, and 20M stars
in Yoshida et al. (2016), PRD 93, 123012.

Spectrum data files:
t_spc_m12_1.2.txt
144761 lines (401 lines x 361 steps: every 5 steps from 6980 to 8780
t_spc_m15_1.2.txt
112681 lines (401 lines x 281 steps: every 5 steps from 5220 to 6620
t_spc_m20_1.2.txt
90225 lines (401 lines x 225 steps: every 5 steps from 6600 to 7720


In each step (401 lines):
1st line: step number, time to the last step (s), 
the central temperature (logTc), the central density (logrhoc)
2-101 lines: dn/dtdE for electron neutrinos
102-201 lines: dn/dtdE for electron antineutrinos
202-301 lines: dn/dtdE for (mu + tau) neutrinos
302-401 lines: dn/dtdE for (mu + tau) antineutrinos
The data are written in increments of 0.01 MeV in the range of 0.01-10 MeV
and in increments of 0.02 MeV in 10.02-20 MeV. 
The data format is 15(1e12.4) x 100 lines.
The total data number of dn/dtdE (N/s/MeV) is 1500 in the 100 lines.
