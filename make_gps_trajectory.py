#coding:utf-8

import os
import glob
from nmea_reader import NMEA_reader
from nmea_reader import NMEA_files
import pandas as pd
import numpy as np
import pylab as pl


# reference:
# https://maps.gsi.go.jp/development/demtile.html
# http://www.trail-note.net/tech/coordinate/
# http://memomemokun.hateblo.jp/entry/2018/11/10/101502
# https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
# https://sorabatake.jp/7325/





def test1():

    path = '/home/kohei/Videos/car/data2/FILE200507-*.NMEA'
    data = NMEA_files(path)

    import pylab as pl
    pl.figure()
    pl.subplot(221)
    pl.plot(data.time_h)

    pl.subplot(222)
    pl.plot(data.qu)
    pl.grid()

    pl.subplot(223)
    pl.scatter(data.lat, data.longi)
    pl.grid()

    pl.subplot(224)
    pl.plot(data.alt)
    pl.grid()

    pl.show()
    print(data.alt)


def test2():

    

    z = 9
    lat=45.178506
    lon=141.242035
    convert(z, lat, lon)
  
    
    lat = np.array(data.lat)
    longi = np.array(data.longi)
    for l in longi:
        if l is None:
            print('None')

    x, y = get_tile_num(z, lat, longi)
    x = x.astype(np.int32)
    y = y.astype(np.int32)
    # 
    #x, y = convert(z, lat, longi)

    print(x)
    print(y)

  
def draw():

    from geography import map
    z= 9
    x1 = 450
    x2 = 451
    y1 = 202
    y2 = 203

    mymap = map(z, x1, x2, y1, y2)

    #path = '/home/kohei/Videos/car/data2/FILE200507-*.NMEA'
    path = '/home/kohei/Videos/car/data2/FILE200508-*.NMEA'
    data = NMEA_files(path)
    lat = np.array(data.lat)
    longi = np.array(data.longi)


    #print(mymap.get_color(450, 202).shape)
    print(mymap.get_color(450, 202).shape)


    arg = mymap.where(lat, longi)

    mymap.colorize(arg, np.array((255, 0, 0)))
    pl.figure()
    pl.imshow(mymap.get_cat_color())

    pl.show()



if __name__ == '__main__':

    print('start')
    
    #test1()

    #test2()
    
    draw()
    