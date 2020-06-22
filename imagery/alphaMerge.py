'''
Alpha Convert
Created on 19/06/2020
@author: jramsay

Script to convert RGBA to RGB preserving alpha transparency by allocating nodata to 0 or 255
if the full black/white colours are unoccupied. If not a single colour gradient shift is used 
to clear the upper 255x3 colour for nodata

usage: python alphaMerge [-h|--help] src <source path> [dst <destination path>]
-h/--help : Print out this help message
src <source path> : The path to the source imagery
dst <destination path> : The path where converted imagery is written (same as src if omitted, with _ prefix)

'''

import warnings
import imageio
import rasterio
import sys
import os
import re
import shutil
import getopt, argparse
import numpy as np
from PIL import Image

prefix = '_'

warnings.filterwarnings('error')

class AlphaConvert(object):

    def __init__(self,test=False):
        self.test = test

    def _blankalpha(self,x1,x2,y1,y2,img,transparent):
        '''Overwrite the alpha channel of an XY range, for testing'''
        img[3,x1:x2,y1:y2] = transparent
        return img
        
    def _setrange(self,x1,x2,y1,y2,img,nodata=0):
        '''Overwrite an XY range, for testing'''
        img[:,x1:x2,y1:y2] = nodata
        return img
    
    def convert(self,fin,fout):
        '''Convert RGBA image to RGB preserving alpha as nodata'''
        rgba,rgb,dst_profile,nodata = None,None,None,0
        try:
            with rasterio.open(fin) as src:
                dst_profile = src.profile
                rgba = src.read()
        except Warning as w:
            print('Warn. Something is wrong with {}, ignoring.\n\t{}'.format(fin,w))
            return
        except Exception as e:
            print('Error. {} is not a valid tif, ignoring.\n\t{}'.format(fin,e))
            return

        ch, row, col = rgba.shape

        if ch == 3: 
            print('Warn. Already 3 channel RGB, copying {} to {}'.format(fin,fout))
            shutil.copyfile(fin,fout)
            return
        if ch != 4:
            print('Error. {} is not 4 channels but {}, ignoring'.format(fin,ch))
            return

        ### Make transparent area for testing
        if self.test:
            rng = (round(row*0.4),round(row*0.6),round(col*0.4),round(col*0.6))
            rgba = self._blankalpha(*rng,rgba,0)
        ###

        rgb = np.zeros( (3, row, col), dtype='uint8' )

        r, g, b = rgba[0,:,:], rgba[1,:,:], rgba[2,:,:]
        a = np.asarray( rgba[3,:,:] / 255.0, dtype='uint8' ) 

        #check for any 255,255,255 pixels
        if all([i.max()<255 for i in (r,g,b)]):
            print('Info. Setting nodata on {} to #FFFFFF'.format(fout))
            nodata = 255
        #check for any 0,0,0 pixels
        elif all([i.min()>0 for i in (r,g,b)]):
            print('Info. Setting nodata on {} to #000000'.format(fout))
            nodata = 0
        else:
            #if the whole band is occupied shift everything down a bit
            print('Warn. Shifting {} colours zero-ward and setting nodata to #FFFFFF'.format(fout))
            r,g,b = np.round(254*r/255,254*g/255,254*b/255)
            nodata = 255

        rgb[0,:,:] = r * a + (1.0 - a) * nodata #nodat :: 0+1*255=255 or dat :: r+0*255=r
        rgb[1,:,:] = g * a + (1.0 - a) * nodata
        rgb[2,:,:] = b * a + (1.0 - a) * nodata
            
        dst_profile.update(dtype=rasterio.uint8, count=3, compress='lzw', nodata=nodata)

        with rasterio.open(fout, 'w', **dst_profile) as dst:
            dst.write(rgb.astype(rasterio.uint8))

        return 1

class SimpleConvert(object):
    
    def convert(self,p1,p2,test=False):
        '''Image lib sonvert function, just strips the alpha'''
        img = Image.open(p1)
        rgb = img.convert('RGB')
        Image.save(rgb)

class Control(object):

    def __init__(self,converter=AlphaConvert):
        self.converter = converter

    def process(self,pin, pout=None,test=False):
        '''Read the supplied directory and send found tifs for processing'''
        p = ''
        if not pout:
            pout = pin
            p = prefix

        ac = self.converter(test)

        for fin in os.listdir(pin):
            if re.match('.*\.tif+',fin): 
                ac.convert(os.path.join(pin,fin),os.path.join(pout,p,fin))
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('src',help='The path to the source imagery')
    parser.add_argument('dst',nargs='?',help='The path where converted imagery is written (same as src if omitted, with _ prefix)')
    
    args = parser.parse_args()#['test'])
    control = Control()
    if args.src == 'test':
        testargs = [os.path.expanduser('~/Pictures/test/'),os.path.expanduser('~/Pictures/test/_/'),True]
        control.process(*testargs)
    else:
        control.process(os.path.abspath(args.src),os.path.abspath(args.dst))


if __name__ == "__main__":
    main()