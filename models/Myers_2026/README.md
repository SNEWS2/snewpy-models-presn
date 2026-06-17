Included here are the neutrino luminosities for the stellar models included in Myers et al. (2026) (http://arxiv.org/abs/2604.22605)

The directories are named as "{ZAMS mass}_{eta}_{bounds}".  The values covered are:

ZAMS Mass = {12, 15, 18, 20}
eta = {0.2, 0.4, 0.8, 1.0}
bounds = {all, core}

Within each directory are subdirectories names "betaLuminosity" and "pairLuminosity", which include the volume integrated spectra as a function of energy for the beta processes and pair annihilation, respectively.

The files in those subdirectories are named "totalBeta{ZAMS mass}_{eta}_{bounds}LuminosityProfile{profile}.dat" and "totalPair{ZAMS mass}_{eta}_{bounds}LuminosityProfile{profile}.dat".  In these file names, the decimal has been removed from eta (eg. 0.2 becomes 02).  The profile number is the corresponding MESA profile for that model. 

Every file includes a header which describes each column and also gives the corresponding t_cc (time to collapse) in hours for the profile.

Each beta file has columns:

# 1 - energy (MeV)
# 2 - electron neutrino number luminosity (1/MeV/s)
# 3 - electron antineutrino number luminosity (1/MeV/s)
# 4 - electron neutrino energy luminosity (1/s)
# 5 - electron antineutrino energy luminosity (1/s)

Each pair annihilation file has columns:

# 1 - energy (MeV)
# 2 - electron neutrino number luminosity (1/MeV/s)
# 3 - electron antineutrino number luminosity (1/MeV/s)
# 4 - mu/tau neutrino number luminosity (1/MeV/s)
# 5 - mu/tau antineutrino number luminosity (1/MeV/s)