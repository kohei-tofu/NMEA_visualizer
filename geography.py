# -*- coding:utf-8 -*-

import numpy as np
#import pylab as pl
from map_download import load_imgs, cat_imgs
from nmea_reader import NMEA_reader

import skimage
from skimage.draw import circle

def get_tile_bbox(z, x, y):
    """
    Get BBox from tile coordinate
    """
    def num2deg(xtile, ytile, zoom):
        n = 2.0 ** zoom
        lon_deg = xtile / n * 360.0 - 180.0
        lat_rad = np.arctan(np.sinh(np.pi * (1 - 2 * ytile / n)))
        lat_deg = np.rad2deg(lat_rad)
        return (lon_deg, lat_deg)
    
    right_top = num2deg(x + 1, y, z)
    left_bottom = num2deg(x, y + 1, z)
    return (left_bottom[0], left_bottom[1], right_top[0], right_top[1])


def get_tile_approximate_lonlats(z, x, y, pix=256):
    """
    Get LatiLongi on the left upper edge of the tile
    """
    bbox = get_tile_bbox(z, x, y)
    width = abs(bbox[2] - bbox[0])
    height = abs(bbox[3] - bbox[1])
    width_per_px = width/pix
    height_per_px = height/pix
    
    lonlats = np.zeros((pix,pix,2))
    lat = bbox[3]
    for i in range(pix):
        lon = bbox[0]
        for j in range(pix):
            #lonlats[i,j,:] = [lon, lat]
            lonlats[i,j,:] = [lat, lon]
            lon += width_per_px 
        lat -= height_per_px
    return lonlats


def get_tile_lonlats(zoom, xtile, ytile):
    """
    Get LatiLongi on the left upper edge of the tile
    """
    x = int(xtile * 2**8)
    y = int(ytile * 2**8)
    z = zoom + 8

    lonlats = np.zeros((256,256,2))
    for i in range(256):
        for j in range(256):
            bbox = get_tile_bbox(z, x + j, y + i)
            lonlats[i,j,:] = [bbox[3], bbox[0]]
    return lonlats


def get_tile_num(z, lat, lon):
    lat_rad = np.deg2rad(lat)
    n = 2.0 ** z
    xtile = ((lon + 180.0) / 360.0 * n)
    ytile = ((1.0 - np.log(np.tan(lat_rad) + (1. / np.cos(lat_rad))) / np.pi) / 2.0 * n)
    return (xtile, ytile)


def cat_imgs(imgs):

    for i, i_row in enumerate(imgs):
        for j, j_e in enumerate(i_row):
            if j == 0:
                im_v = j_e
            else:
                im_v = np.concatenate((im_v, j_e), axis = 0) 
        if i == 0:
            im = im_v
        else:
            im = np.concatenate((im, im_v), axis = 1) 
    return im

class map():
    def __init__(self, z, x1, x2, y1, y2):
        
        path = './data/'
        self.z = z
        self.imgs, self.idx = load_imgs(path, z, x1, x2, y1, y2, 'color')
        self.geos, self.idx = load_imgs(path, z, x1, x2, y1, y2, 'gis')
        self.imgs = np.array(self.imgs)
        self.geos = np.array(self.geos)

        self.latilongi = self.make_latilong(z, x1, x2, y1, y2)
        self.pix = 256



    def make_latilong(self, z, x1, x2, y1, y2):
        imgs = []
        for ix, x in enumerate(range(x1, x2+1)):
            temp = []
            for iy, y in enumerate(range(y1, y2+1)):
                #img = np.load(path + dtype + '-' + str(z) + '-' + str(x) + '-' + str(y) + '.npy')
                img = get_tile_lonlats(z, x, y)
                temp.append(img)
                #idx[str(x) + '-' + str(y)] = [ix, iy]
            imgs.append(temp)
        return np.array(imgs)


    def where_each(self, ix, iy, lati, longi):

        #(256, 256, 2)
        #print('input', lati, longi)
        #print('max, min',np.max(self.latilongi[ix][iy][:, :, 0]), np.min(self.latilongi[ix][iy][:, :, 0]))
        #print('max, min',np.max(self.latilongi[ix][iy][:, :, 1]), np.min(self.latilongi[ix][iy][:, :, 1]))

        temp = np.abs(self.latilongi[ix, iy] - np.array([lati, longi]))
        #temp = np.abs(self.latilongi[ix][iy] - np.broadcast_to([lati, longi], self.latilongi[ix][iy].shape))
        diff = np.sum(temp, 2)
        arg = np.unravel_index(np.argmin(diff), diff.shape)

        return arg


    def where(self, lati, longi):

        tx, ty = get_tile_num(self.z, lati, longi)
        tx, ty = tx.astype(np.int32), ty.astype(np.int32)
        arg_list = []
        for l1, l2, x, y in zip(lati, longi, tx, ty):
            #if error, out of range
            i = self.idx[str(x) + '-' + str(y)]
            

            arg = self.where_each(i[0], i[1], l1, l2)
            _input = [x, y, arg[0], arg[1]]
            #print(_input, i[0], i[1])
            arg_list.append(_input)

        return arg_list


    def colorize(self, arg_list, c):
        
        for arg in arg_list:
            i = self.idx[str(arg[0]) + '-' + str(arg[1])]

            rr, cc = circle(arg[2], arg[3], 5)

            cc[cc < 0] = 0
            rr[cc < 0] = 0
            cc[cc > self.pix - 1] = self.pix - 1
            rr[rr > self.pix - 1] = self.pix - 1
            self.imgs[i[0], i[1], rr, cc] = c
            #self.imgs[i[0], i[1], arg[2], arg[3]] = c
            #print(self.imgs[i[0], i[1]][arg[2], arg[3]].shape)
            #print(self.imgs[i[0], i[1]][arg[2], arg[3]])

    def get_cat_color(self):
        return cat_imgs(self.imgs)

    def get_cat_geos(self):
        return cat_imgs(self.geos)
    
    def get_cat_latilongi(self):
        return cat_imgs(self.latilongi)

    #@property
    def get_color(self, x, y):
        i = self.idx[str(x) + '-' + str(y)]
        return self.imgs[i[0], i[1]]
    
    def get_geos(self, x, y):
        i = self.idx[str(x) + '-' + str(y)]
        return self.geos[i[0], i[1]]



    def latilongi_00(self):
        return self.latilongi[0, 0, 0, 0]
    def latilongi_10(self):
        return self.latilongi[0, -1, 0, -1]
    def latilongi_01(self):
        return self.latilongi[-1, 0, -1, 0]
    def latilongi_01(self):
        return self.latilongi[-1, -1, -1, -1]

    def latilongi_range(self):
        return np.array([self.latilongi[0, 0, 0, 0].tolist(), self.latilongi[-1, -1, -1, -1].tolist()])

if __name__ == '__main__':

    z= 9
    x1 = 450
    x2 = 451
    y1 = 202
    y2 = 203

    mymap = map(z, x1, x2, y1, y2)

