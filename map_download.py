import requests
import string
import pandas as pd
import numpy as np
import io
# import StringIO, BytesIO
import cv2
import skimage
import skimage.io
import pylab as plt
import time


def get_color(urlFormat, z, x, y):

    url = urlFormat.format(z,x,y)
    response = requests.get(url)

    print('status_code', response.status_code)
    if response.status_code == 404:
        colors=np.ones((256, 256, 3), dtype=object)
    else:
        temp = io.BytesIO(response.content)
        img = skimage.io.imread(temp)

    return img

def get_Gis(urlFormat, z, x, y):
    url = urlFormat.format(z,x,y)
    response = requests.get(url)

    print('status_code', response.status_code)
    if response.status_code == 404:
            Z = np.zeros((256, 256))
    else:
            maptxt = response.text.replace('e', '0.0')
            Z = pd.read_csv(io.StringIO(maptxt), header=None)
            Z = Z.values
    return Z

def cat_imgColors(urlFormat, z, x1, x2, y1, y2, t_sleep=1):

    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            time.sleep(t_sleep)
            img = get_color(urlFormat, z, x, y)

            if y == y1:
                im_v = img
            else:
                im_v = np.concatenate((im_v, img), axis = 0) 
            
        if x == x1:
            im = im_v
        else:
            im = np.concatenate((im,im_v), axis = 1) 
            
    return im


def cat_imgGis(urlFormat, z, x1, x2, y1, y2, t_sleep =1):

    for x in range(x1, x2+1):
        for y in range(y1, y2+1):

            time.sleep(t_sleep)
            Z = get_Gis(urlFormat, z, x, y)
            
            if y == y1:
                 gis_v = Z
            else:
                 gis_v = np.concatenate((gis_v, Z), axis = 0)
                
        if x == x1:
            gis = gis_v
        else:
            gis = np.concatenate((gis,gis_v), axis = 1)
            
    return gis



def save_imgColors(path, urlFormat, z, x1, x2, y1, y2, t_sleep=1):

    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            print(x, y)
            time.sleep(t_sleep)
            img = get_color(urlFormat, z, x, y)
            print(img.shape)
            np.save(path + 'color-' + str(z) + '-' + str(x) + '-' + str(y) + '.npy' , img)


def save_imgGis(path, urlFormat, z, x1, x2, y1, y2, t_sleep =1):

    for x in range(x1, x2+1):
        for y in range(y1, y2+1):

            time.sleep(t_sleep)
            Z = get_Gis(urlFormat, z, x, y)
            print(Z.shape)
            np.save(path + 'gis-' + str(z) + '-' + str(x) + '-' + str(y) + '.npy' , Z)

def test1():
    z=8
    x = 225
    y = 101
    urlFormat = 'https://cyberjapandata.gsi.go.jp/xyz/std/{0}/{1}/{2}.png'

    img = get_color(urlFormat, z, x, y)

    plt.figure()
    plt.imshow(img)
    plt.show()


def test2():
    z= 9
    x = 450
    y = 202
    urlFormat = 'https://cyberjapandata.gsi.go.jp/xyz/english/{0}/{1}/{2}.png'

    img = get_color(urlFormat, z, x, y)

    plt.figure()
    plt.imshow(img)
    plt.show()
    


def loandANDcat_img(path, z, x1, x2, y1, y2, dtype = 'color'):

    imgs = []
    for x in range(x1, x2+1):

        for y in range(y1, y2+1):
            img = np.load(path + dtype + '-' + str(z) + '-' + str(x) + '-' + str(y) + '.npy')

            if y == y1:
                im_v = img
            else:
                im_v = np.concatenate((im_v, img), axis = 0) 
        if x == x1:
            im = im_v
        else:
            im = np.concatenate((im,im_v), axis = 1) 
            
    return im

def load_imgs(path, z, x1, x2, y1, y2, dtype = 'color'):

    imgs = []
    idx = {}
    for ix, x in enumerate(range(x1, x2+1)):
        temp = []
        for iy, y in enumerate(range(y1, y2+1)):
            img = np.load(path + dtype + '-' + str(z) + '-' + str(x) + '-' + str(y) + '.npy')
            temp.append(img)
            idx[str(x) + '-' + str(y)] = [ix, iy]
        imgs.append(temp)

    return imgs, idx

def cat_imgs(imgs):

    for i, i_row in enumerate(imgs):
        for j, j_e in enumerate(i_row):
            
            #print(j_e.shape)
            if j == 0:
                im_v = j_e
            else:
                im_v = np.concatenate((im_v, j_e), axis = 0) 

        if i == 0:
            im = im_v
        else:
            im = np.concatenate((im, im_v), axis = 1) 

    return im

def test_cat1():
    z= 9
    x1 = 450
    x2 = 451
    y1 = 202
    y2 = 203

    path = './data/'
    urlFormat_color = 'https://cyberjapandata.gsi.go.jp/xyz/english/{0}/{1}/{2}.png'
    urlFormat_geo = 'https://cyberjapandata.gsi.go.jp/xyz/dem/{0}/{1}/{2}.txt'

    img = cat_imgColors(urlFormat_color, z, x1, x2, y1, y2)
    geo = cat_imgGis(urlFormat_geo, z, x1, x2, y1, y2)

    np.save('color.npy', img)
    np.save('geo.npy', geo)

    plt.figure()
    plt.subplot(121)
    plt.imshow(img)
    plt.subplot(122)
    plt.imshow(geo)
    plt.show()




def load_images(path, z, x1, x2, y1, y2):
    
    imgs, idx = load_imgs(path, z, x1, x2, y1, y2, 'color')
    img = cat_imgs(imgs)
    np.save('color.npy', img)

    geos, idx = load_imgs(path, z, x1, x2, y1, y2, 'gis')
    geo = cat_imgs(geos)
    np.save('geo.npy', geo)

    plt.figure()
    plt.subplot(121)
    plt.imshow(img)
    plt.subplot(122)
    plt.imshow(geo)
    plt.show()


def download_images(path, z, x1, x2, y1, y2):

    urlFormat_color = 'https://cyberjapandata.gsi.go.jp/xyz/english/{0}/{1}/{2}.png'
    save_imgColors(path, urlFormat_color, z, x1, x2, y1, y2)

    urlFormat_geo = 'https://cyberjapandata.gsi.go.jp/xyz/dem/{0}/{1}/{2}.txt'
    save_imgGis(path, urlFormat_geo, z, x1, x2, y1, y2)


if __name__ == '__main__':
    
    print('start')
    path = './data/'

    #if True:
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

    #check at here 
    #https://maps.gsi.go.jp/development/tileCoordCheck.html#10/35.0379/137.7143

    download_images(path, z, x1, x2, y1, y2)

    load_images(path, z, x1, x2, y1, y2)
