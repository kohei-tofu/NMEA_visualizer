import numpy as np
import glob

class time_gps():
    def __init__(self, _input):
        
        self.d = _input
        self.h = _input[0:2]
        self.m = _input[2:4]
        self.s = _input[4::]

    def __str__(self):
        return self.h + ':' + self.m + ':' + self.s

    def get_h(self):
        return int(self.h)
    def get_m(self):
        return int(self.m)
    def get_s(self):
        return float(self.s)

def parse_nmea_one(str):
    str_s = l = str.split(',')
    
    #print(str_s, len(str_s))
    #print(str_s[0])
    data = {}
    data['label'] = str_s[0]
    if str_s[0] == '$GPGGA':
        
        data['UTC'] = time_gps(str_s[1])
        data['latitude'] = str_s[2]
        data['NS'] = str_s[3]
        data['longitude'] = str_s[4]
        data['EW'] = str_s[5]
        data['quality'] = str_s[6]
        data['n_satellite'] = str_s[7]
        data['horizontal_dil'] = str_s[8]
        data['altitude'] = str_s[9]
        data['altitude_units'] = str_s[10]
        data['geo_sep'] = str_s[11]
        data['geo_sep_units'] = str_s[12]
        data['age_gps_data'] = str_s[13]
        data['check_sum'] = str_s[14][4::]

    if str_s[0] == '$GPRMC':
        data['UTC'] = time_gps(str_s[1])
        data['status'] = str_s[2]
        data['latitude'] = str_s[3]
        data['NS'] = str_s[4]
        data['longitude'] = str_s[5]
        data['EW'] = str_s[6]
        data['v_knot'] = str_s[7]
        data['v_dir'] = str_s[8]
        data['day'] = str_s[9]
        data['ang_diff'] = str_s[10]
        data['ang_diff_d'] = str_s[11]
        data['mode'] = str_s[12][0]
        data['check_sum'] = str_s[12][1::]
    
    if str_s[0] == '$GPGSV':
        pass

    return data

def ddmm2decimal(_input):

    str_list = _input.split('.')
    length = len(str_list[0]) - 2
    dd = float(str_list[0][0:(length)])
    mm = float(str_list[0][-2::]) + float('0.' + str_list[1])

    #print(str_list, length, dd, mm)
    return dd + mm / 60.



class NMEA_reader():

    def __init__(self):
        self.nmea_list = []
        #self.GPGGA_list = []
        #self.GPRMC_list = []

    def parse(self, filename):

        try:
            with open(filename, 'r') as f:
                for line in f:
                    msg = parse_nmea_one(line)
                    self.nmea_list.append(msg)
                    #if msg['label'] == '$GPGGA':
                    #    self.GPGGA_list.append(msg)
                    #elif msg['label'] == '$GPRMC':
                    #    self.GPRMC_list.append(msg)

        except IOError:
            print('')

        finally :
            print('')
            self.location()


    def location(self):

        loc = list()
        func = ddmm2decimal
        #func = float
        for nmea in self.nmea_list:
            if nmea['label'] == '$GPGGA':
                #data['latitude']
                #data['longitude']
                #data['NS']
                #data['EW']
                hh = nmea['UTC'].get_h()
                mm = nmea['UTC'].get_m()
                temp = [hh, mm, func(nmea['latitude']), func(nmea['longitude']), float(nmea['altitude']), int(nmea['quality'])]
                loc.append(temp)

            elif nmea['label'] == '$GPRMC':
                hh = nmea['UTC'].get_h()
                mm = nmea['UTC'].get_m()
                temp = [hh, mm, func(nmea['latitude']), func(nmea['longitude']), None, None]
                #loc.append(temp)

        self.loc = np.array(loc)



class NMEA_files():
    def __init__(self, files_cond):
        file_list = sorted(glob.glob(files_cond))

        nmea_list = []
        for f in file_list:
            print(f)
            n = NMEA_reader()
            n.parse(f)
            nmea_list.append(n)

        self.time_h = []
        self.lat = []
        self.longi = []
        self.alt = []    
        self.qu = []
        for n in nmea_list:
            if len(n.loc) != 0:
                self.time_h += n.loc[:, 0].tolist()
                self.lat += n.loc[:, 2].tolist()
                self.longi += n.loc[:, 3].tolist()
                self.alt += n.loc[:, 4].tolist()
                self.qu += n.loc[:, 5].tolist()
        
        
def test1():

    #f = '$GPGGA,100214.000,3458.5203,N,13701.9341,E,1,12,0.7,14.5,M,36.0,M,,0000*6E'
    #f = '$GPRMC,100214.000,A,3458.5203,N,13701.9341,E,16.11,24.87,050520,,,A*61'
    f = '$GPGSV,4,1,16,01,07,083,26,02,16,287,20,03,29,044,42,04,37,093,45*7D'

    msg = parse_nmea_one(f)
    print(msg['UTC'])
    print(msg['check_sum'])


def test2():
    fname = './data/FILE200505-190214.NMEA'
    reader = NMEA_reader()
    reader.parse(fname)


if __name__ == '__main__':

    test2()