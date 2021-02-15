## This is a document sketching out the whole architecture 



Android -->> RPI
==============

This JSON is the init coming from the Android phone to start the the stuff on the RPI 




    	{	
	calling_number:<STRING>,
	call duration:<INT>,
	MAP_NAME:<STRING>,
	who_is_creating_the_map:<STRING>,
	GPS{LAT:<FLOAT> , LONG:<FLOAT>},
	TIME_BASE_TRIGGER:<BOOL>,
	DISTANCE_BASED_TRIGGER:<BOOL>	
	IP_ADR_RPI:<192.168.x.x>


	}






RPI  -->> Android
=================


       	{CALL_TRIGGER{Phone_ID:<INT>} 
         
        }





New changes required
-----------------------

1)Delta time , for adjusting the time zones 
2) Attach 4 phone , 
   Get time from phone , 
   trigger phone calls from the raspberry pi , 
   automated and customisable calls(call duration) 
3)Put the above module in a repetive manner
	* trigger based on movement  (A VARIABLE STEP SIZE)
	OR	
	* time based                 (A VARIABLE TIME)
	



RPI <<-->> Phone APP with the interface (WIFI)


Information that needs to go out of the RPI
-------------------------------------------

---> call trigger (Phone # , Call duration , Call Destination)
	---> call duration 
		--> PHONE ID
	
---> KEEP a log of the executed commands 
	


Data from Smartphone(ANDROID) to and RPI ,
-------------------------------------
 //RESTART_MAP <-- (some input from the user)
 //CALL Quality <--
 
	Meta data that needs to come from Phone over the Wifi via JSON
	-----------------
	* number of test phones
		* Phone and its corresponsing  IP address , MAC address
	* Calling Number (Need not send to Raspberry pi)
	* Call duration  (Need not send to Raspberry pi)
	* Map name  <--
 	* Map creator(person who did the mapping) <--
 	* GPS lat,long <-- origin (manually add OR from phone )
 	* 	Time based 
 			* Interval
 		OR 
 		Distance based 
 		
