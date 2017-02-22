# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 16:40:19 2017

@author: Marco
"""

from os.path import join
import os.path
import rasterio
import sambuca as sb
import sambuca_core as sbc
#import nibabel as nib
#import snappy
import numpy as np
def sam_obs(base_path, Rrs = False):
    if __name__=='sambuca_input_rrs':
        #print (os.path.isfile('bioopti_data\\..\\sambuca\\reference\\wl_alos_data\\inputs\\WL_ALOS_R_0_sub120.img'))
        
        
        #base_path = 'C:\\Users\\PCUSER\\sambuca_project\\input_data\\'
        
        observed_rrs_base_path = base_path + 'image\\'
        observed_rrs_raster_path = join(observed_rrs_base_path, 'WL_ALOS_R_0_sub120.img')
        observed_rrs_filename='WL_ALOS_R_0_sub120.img'
        sensor_filter_path = join(base_path, 'sensor_filters')
        sensor_filter_name = 'ALOS'
        nedr_path = join(base_path + 'nedr\\', 'WL_ALOS_NEDR_0_4bands.hdr')
        
      
        observed_rrs_width = 0
        observed_rrs_height = 0
        observed_rrs = None
        
        with rasterio.Env():
            with rasterio.open(observed_rrs_raster_path) as src:
                print('Observed rrs file: ', observed_rrs_raster_path)
                print('Width, height: ', src.width, src.height)
                print('crs: ', src.crs)
                print('affine: ', src.affine)
                print('num bands: ', src.count)
                print('band indicies: ', src.indexes)
                
                observed_rrs_width = src.width
                observed_rrs_height = src.height
                observed_rrs = src.read()
                
                crs=src.crs
                affine=src.affine
                count=src.count
                indexes=src.indexes
        
        sensor_filters = sbc.load_sensor_filters(sensor_filter_path)
        # We don't need to do this, but it lets us see the name of all loaded filters
        sensor_filters.keys()
        
        
        # retrieve the specified filter
        sensor_filter = sensor_filters[sensor_filter_name]
        
        # If Above surface remote sensing reflectance (Rrs) tag is true, convert to 
        # below surface (rrs) after Lee et al. (1999)
        
        if Rrs == True:
            observed_rrs = (2*observed_rrs)/((3*observed_rrs)+1)
        
        
        nedr = sbc.load_spectral_library(nedr_path, validate=False)['wl_alos_nedr_0_4bands:33']
        nedr
        image_info={'observed_rrs_width':observed_rrs_width, 'observed_rrs_height':observed_rrs_height, 'crs':crs,
                    'affine':affine, 'count':count, 'indexes':indexes, 'nedr': nedr, 'sensor_filter':sensor_filter,
                    'base_path': base_path, 'observed_rrs_filename':observed_rrs_filename}
        
        
        
        return observed_rrs, image_info 
        #return observed_rrs, observed_rrs_width, observed_rrs_height,  nedr, sensor_filter, xstart, xend, ystart, yend, num_pixels, base_path, observed_rrs_filename
        
def sam_obs_s2():
        if __name__=='sambuca_input_rrs':
            print (os.path.isfile('bioopti_data\\..\\sambuca\\reference\\wl_alos_data\\inputs\\WL_ALOS_R_0_sub120.img'))
            
            
            base_path = 'C:\\Users\\PCUSER\\sambuca_project\\bioopti_data\\'
            
            observed_rrs_base_path = base_path + '..\\sambuca\\reference\\wl_alos_data\\inputs\\'
            observed_rrs_raster_path = join(observed_rrs_base_path, 'S2_lampi_05021_atm_rrs')
            observed_rrs_filename='S2_lampi_05021_atm_rrs'
            sensor_filter_path = join(base_path, 'sensor_filters')
            sensor_filter_name = 'ALOS'
            
            
            nedr_path = join(observed_rrs_base_path, 'WL_ALOS_NEDR_0_4bands.hdr')
            
            sensor_filter_path = join(base_path, 'sensor_filters')
            sensor_filter_name = 'ALOS'
            observed_rrs_width = 0
            observed_rrs_height = 0
            observed_rrs = None
            
       # with rasterio.drivers():
            with rasterio.open(observed_rrs_raster_path) as src:
                print('Observed rrs file: ', observed_rrs_raster_path)
                print('Width, height: ', src.width, src.height)
                print('crs: ', src.crs)
                print('affine: ', src.affine)
                print('num bands: ', src.count)
                print('band indicies: ', src.indexes)
                
                observed_rrs_width = src.width
                observed_rrs_height = src.height
                observed_rrs_o = src.read()
                crs=src.crs
                affine=src.affine
                count=src.count
                indexes=src.indexes
            observed_rrs=np.array([np.transpose(observed_rrs_o[0]), np.transpose(observed_rrs_o[2]), np.transpose(observed_rrs_o[3]), np.transpose(observed_rrs_o[6])])
                    
                    
            
            sensor_filters = sbc.load_sensor_filters(sensor_filter_path)
            # We don't need to do this, but it lets us see the name of all loaded filters
            sensor_filters.keys()
            
            
            # retrieve the specified filter
            sensor_filter = sensor_filters[sensor_filter_name]
            
            
            #Plot the sensor filter:
            #plot_items.clear()  #Python 3.3 and later only
            
            nedr = sbc.load_spectral_library(nedr_path, validate=False)['wl_alos_nedr_0_4bands:33']
            nedr
            
            image_info={'observed_rrs_width':observed_rrs_width, 'observed_rrs_height': observed_rrs_height, 'crs': crs,
                        'affine': affine, 'count': count, 'indexes':indexes, 'nedr': nedr, 'sensor_filter':sensor_filter,
                        'base_path':base_path, 'observed_rrs_filename':observed_rrs_filename}
            
            
            
            
            
            
            #return observed_rrs, observed_rrs_width, observed_rrs_height,  nedr, sensor_filter, xstart, xend, ystart, yend, num_pixels, base_path, observed_rrs_filename
            return observed_rrs, image_info
        
