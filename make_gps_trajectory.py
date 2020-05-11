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
    if False:
        z= 9
        x1 = 450
        x2 = 451
        y1 = 202
        y2 = 203
    elif False:
        z= 10
        x1 = 901
        x2 = 903
        y1 = 404
        y2 = 406
    elif True:
        z= 11
        x1 = 1802
        x2 = 1806
        y1 = 809
        y2 = 812

    mymap = map(z, x1, x2, y1, y2)

    #path = '/home/kohei/Videos/car/data2/FILE200507-*.NMEA'
    path = '/home/kohei/Videos/car/data2/FILE200508-*.NMEA'
    data = NMEA_files(path)
    lat = np.array(data.lat)
    longi = np.array(data.longi)



    arg = mymap.where(lat, longi)

    mymap.colorize(arg, np.array((255, 0, 0)))
    pl.figure()
    pl.imshow(mymap.get_cat_color())

    pl.show()

    import plotly.graph_objects as go

    Z = mymap.get_cat_geos()
    make3D_matplot(Z, mymap)



def make3D_matplot(Z, map): 

    from matplotlib import ticker
    from mpl_toolkits.mplot3d import axes3d, Axes3D
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter

    sh_0, sh_1 = Z.shape
    X = map.get_cat_latilongi()[:, :, 0]
    Y = map.get_cat_latilongi()[:, :, 1]

    #Y, X = np.linspace(_range[0, 0], _range[1, 0], sh_1), np.linspace(_range[0, 1], _range[0, 1], sh_0)
    #Y, X = np.linspace(_range[0, 0], _range[1, 0], sh_1), np.linspace(_range[0, 1], _range[0, 1], sh_0)
    #X, Y = np.meshgrid(X, Y)
    #Z = Z.T
    #print(_range)
    print(X.shape, Y.shape, Z.shape)

    pl.clf()
    fig = pl.figure()
    ax = fig.gca(projection='3d')
    ax.invert_xaxis()
    #ax.plot_wireframe(X, Y, Z, color='green')
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=True)

    #ax.set_zlim(-1.01, 1.01)

    #add scale on each xxx step
    ax.zaxis.set_major_locator(ticker.MultipleLocator(200))
    ax.zaxis.set_major_locator(ticker.MaxNLocator(7))
    #ax.zaxis.set_major_locator(LinearLocator(200))
    

    
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.00f'))
    #fig.colorbar(surf, shrink=0.5, aspect=5)

    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Altitude')
    ax.view_init(elev=28., azim=-31)
    #savefig("movie%d.png" % ii)

    pl.show()

def make3D_ploty(Z):
    sh_0, sh_1 = Z.shape
    x, y = np.linspace(0, 1, sh_0), np.linspace(0, 1, sh_1)
    fig = go.Figure(data=[go.Surface(z=Z, x=x, y=y)])
    fig.update_layout(title='Mt Bruno Elevation', autosize=False,
                    width=500, height=500,
                    margin=dict(l=65, r=50, b=65, t=90))
    fig.show()


if __name__ == '__main__':

    print('start')
    
    #test1()

    #test2()
    
    draw()
    