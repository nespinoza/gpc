# gpc

Giant Planets Cores (GPCs): Interpolation of Core Masses for Giant Planets
--------------------------------------------------------------------------

Given a planet mass (in Jupiter masses), radius (in Jupiter radii), system 
age (in Gyrs), distance from parent star (in AU) and stellar luminosity (in solar 
luminosities), the code interpolates the tables given in Fortney, Marley and Barnes 
(2007; ApJ, 659, 1661) and calculates a core mass for the given properties. It 
also estimates the error on this estimate via Monte-Carlo simulations.

This code uses the models published in Jonathan Fortney's webpage: 
http://www.ucolick.org/~jfortney/models.htm

USAGE
-----
To use the code, simply modify the `input_data.gpc` file with the data of your 
system. The code will then download the Fortney, Marley and Barnes (2007) models 
if you don't have them already and will use Monte Carlo simulations to provide an 
estimate of the core-mass of your giant planet by interpolating these tables. 

The results will be printed on the console and also all the simulated values will 
be saved under a `results` folder in case you want to study the resulting 
distribution of core masses.

TODO
----
- Use Gaussian Proccesses to extrapolate values.
