#! /usr/bin/env python
from eofs.standard import Eof
import numpy as np
from numpy import mean
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
class Data:
	def __init__(self,data,time,lon,lat):
		self._data=np.array(data)
		self._time=time
		self._lon=np.array(lon)
		self._lat=np.array(lat)
		print self._time[0]-self._time[1]
		return
	def filter(self,key,arg=None):
		if key=='period':		#in days
			period=arg
			data_per_period=period*24/(self._time[1]-self._time[0])
			new_len=int(len(self._time)//data_per_period)
			self._time=np.array(map(lambda x: self._time[x*data_per_period],range(new_len)))
			data=self._data[:]
			self._data=np.zeros([len(self._time),len(self._lat),len(self._lon)])
			for i,lat in enumerate(self._lat):
				for j,lon  in enumerate(self._lon):
					self._data[:,i,j]=np.array(map(lambda x: np.mean(data[x*period:(x+1)*period,i,j]),range(new_len)))
		return self._data
	def eof(self,no_of_eofs=1):
		data_mean = self._data.mean(axis=0)
		coslat = np.cos(np.deg2rad(self._lat)).clip(0., 1.) 	#weighting
		wgts = np.sqrt(coslat)[..., np.newaxis]
		solver = Eof(self._data, weights=wgts)
		# Retrieve the leading EOF, expressed as the covariance between the leading PC
		# time series and the input SLP anomalies at each grid point.
		eof = solver.eofsAsCorrelation(neofs=no_of_eofs)
		fraction=solver.varianceFraction(no_of_eofs)
		return Eof_pattern(eof, fraction,self._lat,self._lon)
class Eof_pattern:
	def __init__(self,eof,fraction,lat,lon):
		self._eof=eof
		self._fraction=fraction
		self._lat=lat
		self._lon=lon
	def plot_eof(self,name,no_eofs=1):
		m = Basemap(projection='ortho', lat_0=-60., lon_0=100.)#todo
		world=[0,-90,360,0]
		min_lat=self._lat[0]
		max_lat=self._lat[-1]
		min_lon=self._lon[0]
		max_lon=self._lon[-1]
		dif_lat=(max_lat-min_lat)
		if max_lon%360==min_lon%360:
			dif_lon=360
		else:	
			dif_lon=(max_lon-min_lon)%360
		lon_line=5
		while dif_lon/lon_line>9:
			lon_line+=5
		lat_line=5
		while dif_lat/lat_line>10:
			lat_line+=5
		for i in range(no_eofs):
			plt.figure(i)
			m=Basemap(projection='gall',llcrnrlat=min_lat,urcrnrlat=max_lat,\
			    llcrnrlon=min_lon,urcrnrlon=max_lon,resolution='c')

			x, y = m(*np.meshgrid(self._lon, self._lat))
			levels = np.linspace(-1,1,11)
			m.contourf(x, y, self._eof[i].squeeze(),levels, cmap=plt.cm.RdBu_r)
			m.drawcoastlines()
			m.drawparallels(np.arange(-80.,86.,lat_line),labels=[True,False,False,False])
			m.drawmeridians(np.arange(-180.,181.,lon_line),labels=[False,False,False,True])
			plt.title("EOF ("+"%0.1f"%(self._fraction[i]*100)+"%)" , fontsize=16)
			cb = plt.colorbar(orientation='horizontal')
			cb.set_label('correlation coefficient', fontsize=12)
		plt.savefig(name+'.pdf',figsize=(15, 6), dpi=300, facecolor='w', edgecolor='w')
		plt.clf()
