pre_collapse:: data before pre_collapse
collapse:: data during collapse


1. pre_collapse: m12/ m15/
   total_nue/ :: nue
   total_nueb/:: nueb
   total_nux/ :: mu, tau, mub, taub neutrino

   spe_all*.dat::spectrum for nue and nueb
      * descirbes the time step. 
      Please see the data file of luminosity.
      array:: neutrino energy [MeV],
      	      number[MeV^-1s^-1]

   lightcurve_nue_all.dat::luminosity of nue
   lightcurve_nueb_all.dat::luminosity of nueb
      array:: time to collapse [s], 
      	      number luminosity [s^-1], 
	      energy luminosity [MeV/s], 
	      time step

   step.dat:: time_step

   spe_sum_mu* :: mub or taub (nux_b)
   spe_sum_mu_nu* :: mu or tau (nux)
      array:: neutrino energy [MeV], 
      	      number[MeV^-1s^-1]
  
   lightcurve.dat :: luminosity of heavy-lepton
      array:: time step,
      	      time to collapse[s],
	      *, *, 
	      energy luminosity of nux_b[Mev/s], 
	      number luminosity of nux or nux_b[s^-1],
	      *, 
	      energy luminosity of nux[MeV/s], *
      please neglect the arrays described as "*".
      we assume that mu- and tau neutrinos have the same spectra and luminosities.

   step.dat
      we write the time step used in our calculations.


   IH/ ::inverted hierarchy
   NH/ ::normal hierarchy

   spe_n*.dat :: nueb spectrum in NH
   spe_n_nu*.dat :: nue spectrum in NH
   spe_i*.dat :: nueb spectrum in IH
   spe_i_nu*.dat :: nue spectrum in IH
      array:: neutrino energy [MeV], 
      	      number[MeV^-1s^-1]


*******************************************************

2. collapse: m12/ m15/ m9/
   total_nue/ :: nue
   total_nueb/ :: nueb
   total_nux/ :: nux

   lightcurve_nue_all.dat :: luminosity of nue
   lightcurve_nueb_all.dat :: luminosity of nueb
      array:: after collapse [s],
      	      number luminosity [s^-1],
	      energy luminosity [MeV/s], 
	      time step

   spe_all* :: spectrum
      * descirbes the time step. 
      Please see the data file of luminosity.
      array:: neutrino energy [MeV],
      	      number[MeV^-1s^-1]

   spe_sum_mu* :: mub or taub (nux_b)
   spe_sum_mu_nu* :: mu or tau (nux)
      array:: neutrino energy [MeV], 
      	      number[MeV^-1s^-1]

   IH/ ::inverted hierarchy
   NH/ ::normal hierarchy

   spe_n*.dat :: nueb spectrum in NH
   spe_n_nu*.dat :: nue spectrum in NH
   spe_i*.dat :: nueb spectrum in IH
   spe_i_nu*.dat :: nue spectrum in IH
      array:: neutrino energy [MeV], 
      	      number[MeV^-1s^-1]
