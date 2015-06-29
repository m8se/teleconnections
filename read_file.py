#! /usr/bin/env python
from netCDF4 import Dataset
import numpy as np
import datetime as dt
import calendar as cal
from data import Data

class Read_file:
    def __init__(self,filename,arg=None):
        self.__filename=filename
#	    self.__structure=structure
        self.__arg=arg
        self._cdf_conf={}
        self._cdf_conf['dimensions']=3
        self._cdf_conf['lat_name']='lat'
        self._cdf_conf['lat_pos']=1
        self._cdf_conf['lat_range']=[-90,0]
        self._cdf_conf['lon_name']='lon'
        self._cdf_conf['lon_pos']=2
        self._cdf_conf['lon_range']=[0,360]
        self._cdf_conf['time_name']='time'
        self._cdf_conf['time_range']=[0,np.inf]
        self._cdf_conf['time_pos']=0
        self._cdf_conf['variable']='msl'
        self._data=None
        self._time=None
        self._lon=None
        self._lat=None
        return		
    def config(self,key,val):
        self._cdf_conf[key]=val
    def read(self,key=None):
        ncin = Dataset(self.__filename, 'r')
        if key is not None: 
            if key=='am_re':
                self.__read_am_re()
            print 'no read in specified for key %s'%key 
        else:
            #filtering the range of values
            time=ncin.variables[self._cdf_conf['time_name']][:]
            tr=self._cdf_conf['time_range']
            time_ind=filter(lambda i: (time[i]>=tr[0])&(time[i]<=tr[1]),range(len(time)))
            self._time=time[time_ind]
            lons=ncin.variables[self._cdf_conf['lon_name']][:]%360
            lonr=self._cdf_conf['lon_range']
            lon_ind=filter(lambda i: (lons[i]>=lonr[0])&(lons[i]<=lonr[1]),range(len(lons)))
            self._lon=lons[lon_ind]
            lats=ncin.variables[self._cdf_conf['lat_name']][:]
            latr=self._cdf_conf['lat_range']
            lat_ind=filter(lambda i: (lats[i]>=latr[0])&(lats[i]<=latr[1]),range(len(lats)))
            self._lat=lats[lat_ind]
            if self._cdf_conf['dimensions']==3:
                indices=range(3)#sorting the order of indices for the netcdf file
                indices[self._cdf_conf['time_pos']]=time_ind
                indices[self._cdf_conf['lon_pos']]=lon_ind
                indices[self._cdf_conf['lat_pos']]=lat_ind
                self._data=ncin.variables[self._cdf_conf['variable']][indices]
                if self._cdf_conf['time_pos']!=0:
                    np.swapaxes(self._data,0,elf._cdf_conf['time_pos'])
                if (not ((self._cdf_conf['lat_pos']==1)|(self._cdf_conf['lon_pos']==2))):
                    np.swapaxes(self._data,1,2) #data(time,lat,lon)
            else:#		elif self._cdf_conf[dimensions]==4:
                print 'data structure unknown'
            return Data( self._data, self._time, self._lon,self._lat)
    def __read_am_re(self):
        return
if __name__ == "__main__":
    test_file=Read_file('../Data/prmsl.1969-2000.nc')
    test_file.config('lat_name','lat')
    test_file.config('lat_pos',1)
    test_file.config('lon_name','lon')
    test_file.config('lon_pos',2)
    test_file.config('time_name','time')
    test_file.config('time_pos',0)
    test_file.config('dimensions',3)
    test_file.config('variable','prmsl')
    #convert to utc timestamp
    test_file.config('time_range',[cal.timegm(dt.date(1968,1,1).timetuple()),cal.timegm(dt.date(2000,1,1).timetuple())])
    test_file.config('lat_range',[-45,0])
    test_file.config('lon_range',[0,360])
    test_data=test_file.read()
    bla=test_data.filter('period',7)
    test_eof=test_data.eof()
    test_eof.plot_eof(name='bar')
