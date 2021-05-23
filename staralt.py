#!/usr/bin/python3
'''
# written by Yuxin Xin
Date: 2020-04-30
function: [show the stars altitude at Lijiang Observatory(GMG) in default or specified date]
 
'''
import sys
import time
import ephem
import numpy as np
from datetime import datetime 
from matplotlib import pyplot as plt

## add zhongwen
#import matplotlib
#matplotlib.rc("font",family='YouYuan')

###################
moon_RA=float((25/60.0+59.55/3600.0)*15)
moon_DEC=float(-3+1/60.0+4.8/3600.0)

##########################################################
# GMG:
timezone = +8              # the timezone of China (UTC+8)
longitude = '100:01.8'    # longitude of Lijiang Gaomeigu (E 100d01m51.0s)
latitude = '26:41.7'   # latitude of Lijiang Gaomeigu (N 26d42m32.0s)
altitude = 3193            # altitude of Lijiang Gaomeigu (3193m)
##########################################################
'''
##########################################################
# Kunming:
timezone = +8              # the timezone of China (UTC+8)
longitude = '102:47.6'    # longitude of Kunming (E 102d47m36.46s)
latitude =  '25:01.7'   # latitude of Kunming (N 25d01m41.45s)
altitude =  1990            # altitude of Kunming (1990m)
##########################################################
'''
moonalt_list=[]
moonphase_list=[]
sunalt_list=[]
time_list=[]
#xlist=[]
time01=''
time02=''
time03=''
time04=''

def get_4timekeys(date):
    time1 = ephem.Date(date)
    # set the location of the observatory
    observer = ephem.Observer()
    observer.lon = longitude
    observer.lat = latitude
    observer.elevation = altitude
    observer.date = time1
    observer.horizon = '0'

    ####################################################################
    sun1 = ephem.Sun()
    sun1.compute(observer)
    sunsetting=ephem.localtime(observer.next_setting(sun1))
    t1=str(sunsetting)
    if len(t1)>20:
        t1=datetime.strptime(t1,"%Y-%m-%d %H:%M:%S.%f")
    else:
        t1=datetime.strptime(t1,"%Y-%m-%d %H:%M:%S")

    timekey1=int(time.mktime(t1.timetuple()))
    timekey1=int(timekey1/60)*60  ## delete the seconds
    print ('Sun_setting is {}'.format(t1))
    #print ('Sun_setting is {}'.format(timekey1))

    sunrising=ephem.localtime(observer.next_rising(sun1))
    t2=str(sunrising)
    if len(t2)>20:
        t2=datetime.strptime(t2,"%Y-%m-%d %H:%M:%S.%f")
    else:
        t2=datetime.strptime(t2,"%Y-%m-%d %H:%M:%S")
    timekey2=int(time.mktime(t2.timetuple()))
    timekey2=int(timekey2/60)*60  ## delete the seconds
    print ('Sun_rising is {}'.format(t2))
    #print ('Sun_rising is {}'.format(timekey2))

    ####################################################################
    observer.horizon = '-13'
    #observer.horizon = '-18'
    sun2 = ephem.Sun()
    sun2.compute(observer)
    sunsetting=ephem.localtime(observer.next_setting(sun2))
    t3=str(sunsetting)
    if len(t3)>20:
        t3=datetime.strptime(t3,"%Y-%m-%d %H:%M:%S.%f")
    else:
        t3=datetime.strptime(t3,"%Y-%m-%d %H:%M:%S")
    timekey3=int(time.mktime(t3.timetuple()))
    timekey3=int(timekey3/60)*60  ## delete the seconds
    print ('Observation_start is {}'.format(t3))
    #print ('Observation_start is {}'.format(timekey3))

    sunrising=ephem.localtime(observer.next_rising(sun2))
    t4=str(sunrising)
    if len(t4)>20:
        t4=datetime.strptime(t4,"%Y-%m-%d %H:%M:%S.%f")
    else:
        t4=datetime.strptime(t4,"%Y-%m-%d %H:%M:%S")
    timekey4=int(time.mktime(t4.timetuple()))
    timekey4=int(timekey4/60)*60  ## delete the seconds
    print ('Observation_stop is {}'.format(t4))
    #print ('Observation_stop is {}'.format(timekey4))

    return timekey1,timekey2,timekey3,timekey4

def get_sunmoon_alt(date):
    time = ephem.Date(date)
    # set the location of the observatory
    observer = ephem.Observer()
    observer.lon = longitude
    observer.lat = latitude
    observer.elevation = altitude
    observer.date = time
 #   observer.horizon = '-18'

    # Sun
    sun = ephem.Sun()
    sun.compute(observer)
    sun_alt=str(sun.alt)
 #   sun_az=str(sun.az)

    # Moon
    moon = ephem.Moon()
    moon.compute(observer)
    moon_alt=str(moon.alt)
  #  moon_az=str(moon.az)
 #   global moon_phase
    moon_phase=moon.phase

    return sun_alt,moon_alt,moon_phase

def get_star_alt(date,ra,dec):

    time = ephem.Date(date)
    # set the location of the observatory
    observer = ephem.Observer()
    observer.lon = longitude
    observer.lat = latitude
    observer.elevation = altitude
    observer.date = time
 #   observer.horizon = '-18'

    star=ephem.FixedBody()
    star._ra=ra
    star._dec=dec
    star.compute(observer)
    alt=str(star.alt)

    ######## calc the distance to moon
    #moon=ephem.Moon('2021/04/28')
    moon=ephem.Moon(time) ## get all the time's moon distance 
    s=str(ephem.separation(star,moon))
#   print ('The distance to moon: {}'.format(s))

    return alt,s
	

def isValidDate(str):
	try:
		time.strptime(str,"%Y-%m-%d %H:%M:%S")
		return True
	except:
		return False


def plotbar(date0,date1,size,obj_list,staralt_list,moondist_list,offset_str,gmtime_str,localtime_str,twilight01,twilight02):
        n=size
        x=np.arange(n)
        plt.figure(figsize=(9,8))
        #plt.figure()
        ax1=plt.subplot(111)
        ax1.set_xlabel("Beijing Time (UTC+08)")
        #ax1.set_ylabel("Sun and Moon Altitude / $^{\circ}$")
        ax1.set_ylabel("Altitude / $^{\circ}$")
	
        ax1.set_ylim(0,90)
        ax1.set_xlim(0,n)
        ax1.set_yticks(np.arange(0,100,10))
        ax1.set_yticklabels(('0','10','20','30','40','50','60','70','80','90'))
        ax1.set_xticks(offset_str)
        #ax1.set_xticklabels(gmtime_str,rotation='vertical')
        ax1.set_xticklabels(localtime_str)

        #ax2=ax1.twiny()
        #ax2.set_xticks(offset_str)
        #ax2.set_xticklabels(gmtime_str)
        #############################################
        ###############################################3
        c01='purple'
        line1=ax1.axvline(twilight01,color=c01,linewidth=1)
        line1.set_dashes([6,2])
        ax1.text(twilight01-20,91,time03,color=c01,size=8)
        ax1.text(twilight01-20,93,'start',color=c01,size=8)
        line2=ax1.axvline(twilight02,color=c01,linewidth=1)
        line2.set_dashes([6,2])
        ax1.text(twilight02-20,91,time04,color=c01,size=8)
        ax1.text(twilight02-20,93,'stop',color=c01,size=8)
        ######################################################
        c02='gray'
        #line3=ax1.axvline(0,color=c02,linewidth=1)
        #line3.set_dashes([6,2])
        ax1.text(-20,91,time01,color=c02,size=8)
        ax1.text(-20,93,'sunset',color=c02,size=8)
        #line4=ax1.axvline(n,color=c02,linewidth=1)
        #line4.set_dashes([6,2])
        ax1.text(n-20,91,time02,color=c02,size=8)
        ax1.text(n-20,93,'sunrise',color=c02,size=8)
        ######################################################################
	## plot the sun and moon alt 
	#ax1.plot(x,sunalt_list,color='red',label='sun',linewidth=2)
        #ax1.plot(x,moonalt_list,color='red',label='moon',linewidth=2)
        ax1.plot(x,moonalt_list,linestyle='--',color='red',label='moon',linewidth=2)
        ### plot the targets alt
        color_list=['indigo','blue','cyan','green','olive','orange','tan','darkorange','tan','marnoon']
        for i in range(len(obj_list[:][:])): # size of obj_list, num of 2D array in 3D array
                ax1.plot(x,staralt_list[i][:],color=color_list[i],label=obj_list[i][0],linewidth=2)
	#	ax1.plot(x,staralt_list[i][:],color=(0.2,0.2-i*0.05,0.6+i*0.05),label=obj_list[i][0],linewidth=2)
	#	ax1.scatter(x,staralt_list[i][:],marker=i,color='blue',label=obj_list[i][0],linewidth=2)
        ############################################################################
                for xi,yi in zip(x,staralt_list[i]):
                    if xi%120==0 and yi>0:
                            ax1.text(xi+15,yi,'{}'.format(moondist_list[i][xi]),color=color_list[i])
		
	######################################################################################
        phase1=moonphase_list[0]
        phase2=moonphase_list[-1]
        #plt.title('{} @ GMG, Moon_phase: {:.2f}% ~ {:.2f}% '.format(date0,phase1,phase2),y=1.05)
        plt.title('{} @ GMG, YNAO, CAS'.format(date0),y=1.05)
        ax1.text(int(n/2)-100,91,'moonphase: {:.2f}~{:.2f}%'.format(phase1,phase2),color='red',size=8)
	##########################################################################
	##### plot the telescope limit, sunalt=0,-2,-10,-18
        ax1.plot(x,[20]*n,color=c01,linewidth=1)
        ax1.text(n+10,19,'2m4 alt_limit',color=c01)

        ax1.text(n+10,10,"Numbers below curves",size=6,color=c01)
        ax1.text(n+10,8,"are Moon distance",size=6,color=c01)
        ax1.text(n+20,0,"Created by: xyx",size=10,color=c02)

	#plt.legend(loc='lower left')	
        #plt.legend(loc='best')	
        ## set the lengend to the outside of the image
        plt.legend(loc=2,bbox_to_anchor=(1.03,0.95),borderaxespad=0)	
        ## show out all the legend when it out of the image
        plt.subplots_adjust(right=0.75) 
        plt.grid()
        plt.show()
	

def alt2alt(ori_alt):
	alt_array=ori_alt.split(':')
	alt_d=float(alt_array[0])
	alt_m=float(alt_array[1])/60.0
	alt_s=float(alt_array[2])/3600.0
#	print (alt_d,alt_m,alt_s)
	alt=0.0
	if ori_alt[0]=='-':
		alt=round(alt_d-alt_m-alt_s,2)
	else:
		alt=round(alt_d+alt_m+alt_s,2)

	return alt

def run():
	argc=len(sys.argv)
	flag=0
	nYear=0
	nMonth=0
	nDay=0
	if argc>=4:
		flag=1
		nYear=int(sys.argv[1])
		nMonth=int(sys.argv[2])
		nDay=int(sys.argv[3])
	elif argc==1:
		flag=1
		nYear=int(time.strftime('%Y',time.localtime(time.time())))
		nMonth=int(time.strftime('%m',time.localtime(time.time())))
		nDay=int(time.strftime('%d',time.localtime(time.time())))
	if flag==1:
                date0="%4d/%02d/%02d"%(nYear,nMonth,nDay)
                jd=ephem.julian_date(date0)
                print ('Date: {},  Julian day: {}'.format(date0,jd))

                ## get sunrise, sunset, twilight time
                date1="%4d-%02d-%02d 5:0:0"%(nYear,nMonth,nDay)
                tk1,tk2,tk3,tk4=get_4timekeys(date1)
                size=int((tk2-tk1)/60)
                hours=int(size/60)
                print ('size is {}, hours: {}'.format(size,hours))
                
                global time01,time02,time03,time04
                time01=time.strftime("%H:%M",time.localtime(tk1))
                time02=time.strftime("%H:%M",time.localtime(tk2))
                time03=time.strftime("%H:%M",time.localtime(tk3))
                time04=time.strftime("%H:%M",time.localtime(tk4))
                print (time01,time02,time03,time04)
                
                twilight01=int((tk3-tk1)/60)
                twilight02=int((tk4-tk1)/60)

                #######################
                ## get the hour time at x axis for plot
                nhour=int(time.strftime("%H",time.localtime(tk1)))
                nmin=int(time.strftime("%M",time.localtime(tk1)))
                if nmin==0:
                    offset=0
                else:
                    offset=60-nmin ## the offset minutes to the nearest hour
                start_tk=tk1+offset*60  # the timekey of the nearest hour
                
                offset_str=[]  ## num since start
                gmtime_str=[]  ## UTC string
                localtime_str=[] ## localtime string
                #for i in range(hours+1):
                for i in range(hours):
                    j=i*3600
                    time_05=time.strftime("%H",time.gmtime(start_tk+j))
                    gmtime_str.append(time_05)
                    time_05=time.strftime("%H",time.localtime(start_tk+j))
                    localtime_str.append(time_05)

                    m=i*60+offset
                    offset_str.append(m)

                print (gmtime_str)
                print (localtime_str)
                ######################################################

                object_list=[]
                staralt_list_3d=[]
                moondist_list_3d=[] # for all the stars' moon distance
                ## calc the alts of stars, sun and moon.
                if isValidDate(date1):
			###################################
			## read stars name ra,dec from stars.txt
                        fp=open('objects.txt','r')
                        index=0
                        for eachline in fp:
                            #print (eachline)
                            if eachline.strip()=='':
                                break
                            index+=1
                            if index>10:
                                print ('Sorry only 9 stars alt will plot!!')
                                break
                            elif index>1 and index<=10:
                                text=eachline.split()
#                                print (text)
                                if (len(text)<3):
                                        print ('stars.txt should have three Column: name ra dec ')
                                        break
                                else:
                                    object_list.append(text)
                                    staralt_list=[]
                                    dist_list=[]  ## for moon distance
                                    for i in range(size): # get star_alt at each minute of a whole day 24h
                                        unix_stamp=tk1+i*60
                                        time_utc=time.gmtime(unix_stamp)
                                        dt=time.strftime("%Y-%m-%d %H:%M:%S",time_utc)
                                        ra=text[1]
                                        dec=text[2]
                                        star_alt,dist=get_star_alt(dt,ra,dec)
                                        alt=alt2alt(star_alt)
                                        ## 
                                        dist_array=dist.split(':')
                                        dist_d=int(dist_array[0])

                                        staralt_list.append(alt) ## alt for y axis 2D array
                                        dist_list.append(dist_d) ## moon_distance for y axis 2D array
 #                                   print (len(staralt_list))
                                    staralt_list_3d.append(staralt_list)  ## 3D array for stars'alt
                                    moondist_list_3d.append(dist_list)  ## 3D array for star_moon distance
                                    #print (dist_list)

			###################################
                        global sunalt_list,moonalt_list,moonphase_list
                        for i in range(size): # get sun_alt at each minute of a whole day 24h
                            unix_stamp=tk1+i*60
                            #time_local=time.localtime(unix_stamp)
                            time_utc=time.gmtime(unix_stamp)
                            dt=time.strftime("%Y-%m-%d %H:%M:%S",time_utc)
                            sun_alt,moon_alt,moon_phase=get_sunmoon_alt(dt)
			    ########################################################
                            alt=alt2alt(sun_alt)
                            sunalt_list.append(alt) ## alt for y axis
                            alt=alt2alt(moon_alt)
                            moonalt_list.append(alt) ## alt for y axis
                            moonphase_list.append(moon_phase) ## moon phase
                print ('size is: {} , {}'.format(len(sunalt_list),len(moonalt_list)))
                plotbar(date0,date1,size,object_list,staralt_list_3d,moondist_list_3d,offset_str,gmtime_str,localtime_str,twilight01,twilight02)
	else:
		print ('Please input ./filename.py 2019 12 20  !!\
			        \n or ./filename.py for today')
	

if __name__ == '__main__':
	run()

