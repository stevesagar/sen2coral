# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 12:35:53 2017

@author: PaulRyan/stevesagar
"""
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
#from itertools import combinations
#import os
import sambuca_outputs

def output_suite(result_recorder, image_info, coordinates):
    
    # read in subsection of image processed
    
    xs=coordinates[0]
    xe=coordinates[1]
    ys=coordinates[2]
    ye=coordinates[3]
    
    #define some output arrays from the results
    
    skip_mask = (result_recorder.success[xs:xe,ys:ye] < 1)
    chl = ma.masked_array(result_recorder.chl[xs:xe,ys:ye],mask=skip_mask)
    cdom = ma.masked_array(result_recorder.cdom[xs:xe,ys:ye],mask=skip_mask)
    nap = ma.masked_array(result_recorder.nap[xs:xe,ys:ye],mask=skip_mask)
    depth = ma.masked_array(result_recorder.depth[xs:xe,ys:ye],mask=skip_mask)
    substrate_fraction = ma.masked_array(result_recorder.substrate_fraction[xs:xe,ys:ye],mask=skip_mask)
    nit = ma.masked_array(result_recorder.nit[xs:xe,ys:ye],mask=skip_mask)
    kd = ma.masked_array(result_recorder.kd[xs:xe,ys:ye],mask=skip_mask)
    sdi = ma.masked_array(result_recorder.sdi[xs:xe,ys:ye],mask=skip_mask)
     
    # A scaled true colour image to look at closed rrs
    rgbimg=np.zeros(((xe-xs),(ye-ys),3), 'uint8')
    rgbimg[..., 0] = (result_recorder.closed_rrs[xs:xe,ys:ye,2])*1024
    rgbimg[..., 1] = (result_recorder.closed_rrs[xs:xe,ys:ye,1])*1024
    rgbimg[..., 2] = (result_recorder.closed_rrs[xs:xe,ys:ye,0])*1024
    
    sambuca_outputs.writeout('1_depth.tif',depth,image_info['affine'],image_info['crs'],np.float32)
    
    sambuca_outputs.writeout('2_kd550.tif',kd,image_info['affine'],image_info['crs'],np.float32)
    
    sambuca_outputs.writeout('3_rgbimg.tif',rgbimg,image_info['affine'],image_info['crs'],transpose=[2,0,1])
    
    sambuca_outputs.writeout('4_sdi.tif',sdi,image_info['affine'],image_info['crs'],np.float32)
    
#    # single band - convert from float64 to float32
#    sambuca_outputs.writeout('1_rr_chl.tif',result_recorder.chl,src.affine,src.crs,np.float32)
#    
#    # write out masked array and convert type
#    sambuca_outputs.writeout('2_ma_chl.tif',chl,src.affine,src.crs,np.float32)
#    
#    # write out masked array, convert but use np.nan as the fill value
#    sambuca_outputs.writeout('3_ma_chl_nan.tif',chl,src.affine,src.crs,np.float32,fill=np.nan)
#    
#    # write out ndarray, but the band is not the first dimension so use transpose option
#    sambuca_outputs.writeout('4_rgbimg.tif',rgbimg,src.affine,src.crs,transpose=[2,0,1])
#    
#    # write out a single band from multi-band array
#    sambuca_outputs.writeout('7_rr_closedrrs_1band.tif',result_recorder.closed_rrs[:,:,0],src.affine,src.crs,dtype=np.float32)
    
    

