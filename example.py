#! /usr/bin/env python
from read_file import Read_file
import datetime as dt
import calendar as cal
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
    test_file.config('lat_range',[-5,0])
    test_file.config('lon_range',[0,10])
    test_data=test_file.read()
    test_data.filter('period',7)
    #test_eof=test_data.eof()
    #test_eof.plot_eof(name='bar')
    #test_data.compute_correlation("test.cdf")
    test_data.compute_distances("test_dist.cdf")

