# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sps


from numpy import ndarray


from LoadSizeDistribution import *
from LoadProjectorSpectrum import *


#!pip install miepython
try:
    import miepython

except ModuleNotFoundError:
    print('miepython not installed. To install, uncomment and run the cell above.')
    print('Once installation is successful, rerun this cell again.')


def N2V_distribution(Radii, N_Distribition):
    #V_Distribition = N_Distribition

    V_Distribution = np.zeros(len(Radii))
    i: int
    for i in range(len(Radii)):
      volume = (4*np.pi/3) * Radii[i]**3
      V_Distribution[i] = N_Distribition[i] * volume

    V_Distribution = V_Distribution / np.sum(V_Distribution)
    return V_Distribution


def lux_2_watts_m2_full_spectrum(LUX, Ilumination_type):
    # https: // ieee - dataport.org / open - access / conversion - guide - solar - irradiance - and -lux - illuminance

    if Ilumination_type == 'Sun':
        W_m2 = LUX * 0.0079
        return W_m2
    elif Ilumination_type == 'Halogen lamp':
        W_m2 = LUX / 20
        return W_m2
    elif Ilumination_type == 'Tungsten incandescent':
        W_m2 = LUX / 15
        return W_m2
    elif Ilumination_type == 'Fluorescent lamp':
        W_m2 = LUX / 60
        return W_m2
    elif Ilumination_type == 'LED lamp':
        W_m2 = LUX / 90
        return W_m2
    elif Ilumination_type == 'Metal Halide lamp':
        W_m2 = LUX / 87
        return W_m2
    elif Ilumination_type == 'High pressure sodium vapor lamp':
        W_m2 = LUX / 117
        return W_m2
    elif Ilumination_type == 'Low pressure sodium vapor lamp':
        W_m2 = LUX / 150
        return W_m2
    elif Ilumination_type == 'Mercury vapor lamp':
        W_m2 = LUX / 50
        return W_m2

def lux_2_watts_m2_projector(LUX, WL_min_nm, WL_max_nm):
    # conversion :  683.0 lux to 1 w/

    proj_file = r'Data_From_Experiment/projector.txt'
    Photopic_file = r'Data_From_Experiment/eye_sensitivity.xls'
    Wavelength_photopic_nm, photopic_response = load_photopic_function(Photopic_file)
    ProjWavelength_nm, ProjIntensity = LoadProjectorSpectrum(proj_file)

    photopic_responseInterp = np.interp(ProjWavelength_nm, Wavelength_photopic_nm, photopic_response, 0, 0)
    ProjPhotopicPortion = ProjIntensity * photopic_responseInterp
    tmp = np.argwhere(ProjWavelength_nm > 400)
    Inx1 = int(tmp[0])
    tmp = np.argwhere(ProjWavelength_nm < 700)
    Inx2 = int(tmp[-1])

    ProjPowerPhotopic = np.sum(ProjPhotopicPortion[Inx1: Inx2])
    ProjPower = np.sum(ProjIntensity[Inx1: Inx2])

    Inx1 = np.argwhere(ProjWavelength_nm > WL_min_nm)
    Inx1 = int(Inx1[0])
    Inx2 = np.argwhere(ProjWavelength_nm < WL_max_nm)
    Inx2 = int(Inx2[-1])
    ProjPowerBand = np.sum(ProjIntensity[Inx1: Inx2])

    C_Photopic = ProjPower / ProjPowerPhotopic
    C_band = ProjPowerBand / ProjPower
    tmp = np.argwhere(ProjWavelength_nm > 555)
    Inx = int(tmp[1])

    dlabda = ProjWavelength_nm[Inx+1] - ProjWavelength_nm[Inx]

    C_units = 1/(dlabda*683.002)
    W_m2 = float(LUX) * C_Photopic * C_band * C_units
    return W_m2




def VisRange2Sigma(VisRange_m):
    Sigma_1_over_m = 3.912 / VisRange_m
    return Sigma_1_over_m

def Sigma2VisRange(Sigma_1_over_m):
    VisRange_m   = 3.912 / Sigma_1_over_m
    return VisRange_m

def Visibilty2OpticalDepth(VisRange_m, Length_m):
      Sigma_1_over_m = 3.912 / VisRange_m          # Ref. : https://en.wikipedia.org/wiki/Visibility x_\text{V} = \frac{3.912}{b_\text{ext}}
      transmittance = np.exp(-Sigma_1_over_m*Length_m)
      OpticalDepth = -np.log(transmittance)        # OpticalDepth = -log(Trans) REf. : https://en.wikipedia.org/wiki/Optical_depth
      return OpticalDepth


def OpticalDepth2Visibilty(max_OD_m, Length_m):
       Sigma_1_over_m = max_OD_m / Length_m
       VisRange_m = 3.912 / Sigma_1_over_m
       # Ref. : https://en.wikipedia.org/wiki/Visibility x_\text{V}
       # = \frac{3.912}{b_\text{ext}}
       return VisRange_m

def LWC2TotalVDist(LWC_gr_cm3, V_Distribition):
    WaterDensity_gr_cm3 = 0.99802  # gr/cm3
    TotalVDist = V_Distribition * (LWC_gr_cm3 / WaterDensity_gr_cm3)
    TotalVDist = TotalVDist

    return TotalVDist

def LUX2Intensity(LUX_level, w1_micron, w2_micron):
    intensity_W = 1
    return intensity_W


def LWC2Visibility(C_ext, Cloud_LWC_gr_cm3, Radii_micron, V_disrib):

    print(f'Not active yet')
    WaterDensity_gr_cm3 = 0.99802  # gr/cm3
    Norm_C_ext = np.zeros(np.length(Radii_micron))   # distribution normalised extinction cross section

    for i in range(len(Radii)):
        Norm_C_ext[i] = V_disrib[i] * C_ext[i]
        Sigma_1_over_m = np.sum(Norm_C_ext) * (Cloud_LWC_gr_cm3 / WaterDensity_gr_cm3)*1E6

        VisRange_m = Sigma2VisRange(Sigma_1_over_m)
    return VisRange_m



def MieCalc(Wavelength, Radii, Dist):
    # import the Segelstein data

    #h2o = np.genfromtxt('http://omlc.org/spectra/water/data/segelstein81_index.txt', delimiter='\t', skip_header=4)
    h2o = np.genfromtxt('segelstein81_index.txt', delimiter='\t', skip_header=4)
    h2o_lam = h2o[:, 0]
    h2o_mre = h2o[:, 1]
    h2o_mim = h2o[:, 2]

    # plot it
    plt.figure(3)
    plt.plot(h2o_lam, h2o_mre)
    plt.plot(h2o_lam, h2o_mim)
    plt.xlim((1, 15))
    plt.ylim((0, 1.8))
    plt.xlabel('Wavelength (microns)')
    plt.ylabel('Refractive Index')
    plt.annotate(r'$m_\mathrm{re}$', xy=(3.4, 1.5))
    plt.annotate(r'$m_\mathrm{im}$', xy=(3.4, 0.2))

    plt.title('Complex Refractive Index of Water')

    plt.show(block=False)


    #x = np.linspace(0.1, 100, 300)
    #refWavelength = [0.200, 0.225, 0.250, 0.275, 0.300, 0.325, 0.350, 0.375, 0.400, 0.425, 0.450, 0.475, 0.500, 0.525,
    #                 0.550, 0.575, 0.600, 0.625, 0.650, 0.675, 0.700, 0.725, 0.750, 0.775, 0.800, 0.825, 0.850, 0.875,
    #                 0.900, 0.925, 0.950, 0.975, 1.0,   1.2,   1.4,   1.6,   1.8,   2.0]
    #ref_n         = [1.396, 1.373, 1.362, 1.354, 1.349, 1.346, 1.343, 1.341, 1.339, 1.338, 1.337, 1.336, 1.335, 1.334,
    #                 1.333, 1.333, 1.332, 1.332, 1.331,	1.331, 1.331, 1.330, 1.330, 1.330, 1.329, 1.329, 1.329, 1.328,
    #                 1.328, 1.328, 1.327, 1.327, 1.327, 1.324, 1.321, 1.317, 1.312, 1.306]

    #ref_k = [1.1e−7, 4.9e−8 , 3.35e−8, 2.35e−8, 1.6e−8, 1.08e−8, 6.5e−9, 3.5e−9, 1.86e−9, 	1.3e−9, 1.02e−9, 9.35×10−10, 1.00e−9,
    # 1.32e−9, 1.96e−9, 3.60e−9, 1.09e−8, 1.39e−8, 1.64e−8, 2.23e−8, 3.35e−8, 9.15e−8, 1.56e−7, 1.48e−7, 1.25e−7, 1.82e−7, 2.93e−7,
    # 3.91e−7, 4.86e−7, 1.06e−6, 2.93e−6, 3.48e−6, 	2.89e−6, 9.89e−6, 1.38e−4, 8.55e−5, 1.15e−4, 1.1e−3

    x = (2 * np.pi * Radii) / Wavelength     # size parameter in vacuume https://miepython.readthedocs.io/en/latest/01_basics.html
    ref_n_wl = np.interp(Wavelength, h2o_lam, h2o_mre)
    ref_k_wl = np.interp(Wavelength, h2o_lam, h2o_mim)
    qext, qsca, qback, g = miepython.mie(ref_n_wl - 1.0j * ref_k_wl, x)  # https://miepython.readthedocs.io/en/latest/
    cross_section_area = np.pi * Radii ** 2
    sca_cross_section = qsca * cross_section_area
    mean_scs = np.mean(sca_cross_section* Dist)
    #abs_cross_section = (qext - qsca) * cross_section_area


    plt.figure(4)
    plt.plot(Radii, qext, color='red', label=str(ref_n_wl))

    plt.title("Water droplets Qext")
    plt.xlabel("Droplet Radius [microns]")
    plt.ylabel("Qext")
    plt.show(block=False)

    theta = np.linspace(-180, 180, 180)
    mu = np.cos(theta / 180 * np.pi)
    s1: ndarray = np.zeros([x.shape[0], mu.shape[0]], dtype=np.complex_)
    s2: ndarray = np.zeros([x.shape[0], mu.shape[0]], dtype=np.complex_)
    I1: ndarray = np.zeros([x.shape[0], mu.shape[0]], dtype=np.float)
    I2: ndarray = np.zeros([x.shape[0], mu.shape[0]], dtype=np.float)
    I3: ndarray = np.zeros([x.shape[0], mu.shape[0]], dtype=np.float)

    for i in range(len(x)):
        s1[i, :], s2[i, :] = miepython.mie_S1_S2(ref_n_wl - 1.0j * ref_k_wl, x[i], mu)
        I1[i, :] = abs(s1[i, :])**2
        I2[i, :] = abs(s2[i, :])**2
        I3[i, :] = abs(s1[i, :] * (s2[i, :].conj())+s2[i, :]*(s1[i, :].conj()))

    I1 = np.transpose(I1)*Dist*sca_cross_section
    I1 = np.sum(np.transpose(I1 ), 0)/mean_scs
    I2 = np.transpose(I2)*Dist*sca_cross_section
    I2 = np.sum(np.transpose(I2), 0)/mean_scs
    I3 = np.transpose(I3)*Dist*sca_cross_section
    I3 = np.sum(np.transpose(I3), 0)/mean_scs


    scat = (I1 + I2)/2 # unpolarized scattered light
    pol_scat = np.sqrt((I1-I2)**2)/(I1+I2) # polarized scattered light+I3**2
    plt.figure(5)
    plt.polar(theta/180 * np.pi, np.log10(scat))
    plt.title("Log scattering")

    plt.figure(6)
    plt.polar(theta / 180 * np.pi, np.log10(pol_scat))
    plt.title("Polarized scattering")

    plt.show()

    return qext, qsca, qback, theta, s1 , s2


def calc_reff(radii, N_dist):
    Sum1 = np.sum(radii**3*N_dist)
    Sum2 = np.sum(radii**2*N_dist)
    reff = Sum1/Sum2
    return reff

#------------------------------------------------------------------------------------
#----------------------------- Start of test code -----------------------------------
#------------------------------------------------------------------------------------


print('Test LUX to W per m^2')
LUX = 100
LightSource = 'Metal Halide lamp'# 'Sun' # 'Tungsten incandescent' # 'Halogen lamp'
W_m2 = lux_2_watts_m2_full_spectrum(LUX,  LightSource)
#print('reference value for halogen lamp: 100 LUX = 5 w/m^2')
print('calculated value for', LightSource, '  lamp:', LUX , 'LUX = ', W_m2 , ' w/m^2')

W_m2 = lux_2_watts_m2_projector(LUX, 200, 2500)
print('No reference value for our projector')
print('calculated value for Ofers projrctor:', LUX, 'LUX = ', float(W_m2), ' w/m^2')

print('Test Cloud droplets distribution functions')

type_num = 1
type = ['mist', 'green clouds']
#filename = [r'C:\Users\masadatz\Google Drive\CloudCT\svs_vistek\mesibot.txt',
#            r'C:\Users\masadatz\Google Drive\CloudCT\svs_vistek\Data_From_Experiment\distributions\greenclouds.txt']
filename = [r'C:\Users\User\Documents\GitHub\PolCam\Data_From_Experiment\distributions\mesibot.txt',
            r'C:\Users\User\Documents\GitHub\PolCam\Data_From_Experiment\distributions\greenclouds.txt']

DEBUG = 0
if DEBUG == 1:

    # try distribution functions conversions
    shape, scale = 3., 3.  # mean=4, std=2*sqrt(2)
    Radii = np.linspace(0.1, 40.0, num=200)
    N_Distribution = Radii**(shape-1)*(np.exp(-Radii/scale) / (sps.gamma(shape)*scale**shape)) # create a gamma  distribution
    N_Distribution = N_Distribution / np.sum(N_Distribution)

else:
    Radii, num_Distribution = LoadSizeDistribution(filename[type_num])
    num_Distribution / np.sum(num_Distribution)

print_plots = True
# calculate gamma distribution, just to check the fit
shape, scale = 35., 0.1 # mean=4, std=2*sqrt(2)
#N_Distribition_gamma = Radii**(shape-1)*(np.exp(-Radii/scale) / (sps.gamma(shape)*scale**shape)) # create a gamma  distribution
#N_Distribition_gamma = N_Distribition_gamma / np.sum(N_Distribition_gamma)



# calculate the volume distribution
vol_Distribition = N2V_distribution(Radii, num_Distribution)
#V_Distribition = N2V_distribution(Radii, N_Distribution)
#V_Distribition = V_Distribition / np.sum(V_Distribition)
#V_Distribition_gamma = N2V_distribution(Radii, N_Distribition_gamma)

if (print_plots):
    plt.figure(1)
    plt.plot(Radii, num_Distribution)
#    plt.plot(Radii, N_Distribition_gamma)
    plt.plot(Radii, vol_Distribition)
    plt.title(type[type_num] + " droplets Size distribution")
    plt.xlabel("Droplet Radius [microns]")
    plt.ylabel("Number/volume percentage")
#    plt.legend(['Number Dist.', 'Gamma Number dist.', 'Volume Dist.'])
    plt.legend(['Number Dist.', 'Volume Dist.'])
    plt.show(block=False)



Sigma_1_over_m = VisRange2Sigma(30) # 30 meter visibility
VisRange = Sigma2VisRange(Sigma_1_over_m) # we should receive back 30 meter visibility

LWC_gr_cm3 = 0.3*1E-6  # gr/m^3
TotalVDist = LWC2TotalVDist(LWC_gr_cm3, vol_Distribition)
if (print_plots):
    plt.figure(2)
    plt.plot(Radii, TotalVDist )
    plt.legend(['Number Dist.','Volume Dist.'])
    plt.xlabel('Radius [\mum]')
    plt.ylabel('TotalVDist')
    plt.show(block=False)

# try visibility to optical depth function
OD = Visibilty2OpticalDepth(3, 2.8)
VisRange = OpticalDepth2Visibilty(2.7,2.8)
print(OD)
print(VisRange)
# Run Mie Calculations
Wavelength = 0.55 # microns
MieCalc(Wavelength, Radii, vol_Distribition)

reff = calc_reff(Radii, num_Distribution)
print(reff)