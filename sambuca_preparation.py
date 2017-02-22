# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 10:54:41 2017

@author: Marco
"""


import sambuca as sb
import sambuca_core as sbc
#from os.path import join
#import os.path





def sam_prep(siop, envmeta, image_info):

    a_water=siop['a_water']
    a_ph_star=siop['a_ph_star']
    substrates=siop['substrates']
    substrate_names=siop['substrate_names']
    sensor_filter=image_info['sensor_filter']
    observed_rrs_width=image_info['observed_rrs_width']
    observed_rrs_height=image_info['observed_rrs_height']
    nedr=image_info['nedr']
    
    
    
    
    wavelengths = sbc.spectra_find_common_wavelengths(a_water, a_ph_star, *substrates)
    print('Common wavelength range: {0} - {1}'.format(min(wavelengths), max(wavelengths)))
    
    #Use the common wavelengths to mask the inputs:
    a_water = sbc.spectra_apply_wavelength_mask(a_water, wavelengths)
    a_ph_star = sbc.spectra_apply_wavelength_mask(a_ph_star, wavelengths)
    for i, substrate in enumerate(substrates):
        substrates[i] = sbc.spectra_apply_wavelength_mask(substrate, wavelengths)
        
    print('awater: min: {0}  max: {1}'.format(min(a_water[0]), max(a_water[0])))
    print('a_ph_star: min: {0}  max: {1}'.format(min(a_ph_star[0]), max(a_ph_star[0])))
    for substrate_name, substrate in zip(substrate_names, substrates):
        print('{0}: min: {1}  max: {2}'.format(substrate_name, min(substrate[0]), max(substrate[0])))
    
    
    """Truncate the sensor filter to match the common wavelength range
    It remains to be seen whether this is the best approach, but it works for this demo. An alternative approach would be to truncate the entire band for any band that falls outside the common wavelength range.
    If this approach, or something based on it, is valid, then this should be moved into a sambuca_core function with appropriate unit tests."""
    
    filter_mask = (sensor_filter[0] >= wavelengths.min()) & (sensor_filter[0] <= wavelengths.max())
    sensor_filter = sensor_filter[0][filter_mask], sensor_filter[1][:,filter_mask]
    
    
    fixed_parameters = sb.create_fixed_parameter_set(
                wavelengths=wavelengths,
                a_water=a_water,
                a_ph_star=a_ph_star,
                substrates=substrates,
                substrate_fraction=1,
                chl=None,
                cdom=None,
                nap=None,
                depth=None,
                a_cdom_slope=siop['a_cdom_slope'],
                a_nap_slope=siop['a_nap_slope'],
                bb_ph_slope=siop['bb_ph_slope'],
                bb_nap_slope=siop['bb_nap_slope'],
                lambda0cdom=siop['lambda0cdom'],
                lambda0nap=siop['lambda0nap'],
                lambda0x=siop['lambda0x'],
                x_ph_lambda0x=siop['x_ph_lambda0x'],
                x_nap_lambda0x=siop['x_nap_lambda0x'],
                a_cdom_lambda0cdom=siop['a_cdom_lambda0cdom'],
                a_nap_lambda0nap=siop['a_nap_lambda0nap'],
                bb_lambda_ref=siop['bb_lambda_ref'],
                water_refractive_index=siop['water_refractive_index'],
                theta_air=envmeta['theta_air'],
                off_nadir=envmeta['off_nadir'],
                q_factor=envmeta['q_factor']
                )
    result_recorder = sb.ArrayResultWriter(
            observed_rrs_width,
            observed_rrs_height,
            sensor_filter,  
            nedr,
            fixed_parameters)
    objective = sb.SciPyObjective(sensor_filter, fixed_parameters, error_function=sb.distance_f, nedr=nedr)
    siop['a_water']=a_water
    siop['a_ph_star']=a_ph_star
    siop['substrates']=substrates
    siop['substrate_names']=substrate_names
    image_info['sensor_filter']=sensor_filter
    image_info['observed_rrs_width']=observed_rrs_width
    image_info['observed_rrs_height']=observed_rrs_height
    image_info['nedr']=nedr
    
    
    
    return wavelengths, siop, image_info, fixed_parameters, result_recorder, objective