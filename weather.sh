#!/bin/bash
#
# Daylen Nguyen 
# weather.sh
# IP Geolocation -> Weather Information
# 
# ************************************************************ #
# 
# Bash Script to retrieve the location information (from IP)
# which is then used to retrieve the weather forcast (16 days)
# The APIs used were 'ipinfo.io' and 'weatherbit.io'
# 
# ************************************************************ #
# DAYLEN NGUYEN'S API KEYs
# (TO BE REMOVED AFTER SUBMITTION)
	IPTOKEN='3f3eb6791a6ae2'
	WEATHER='99bfc350daca40528068893489d8f678'
#
# ************************************************************ #




# function to test whether the ip addr has been previously cached.
# 1 = (HAS BEEN CACHED) 0 = (NOT CACHED, FIRST TIME RUNNING PROGRAM)
testForIPCache () {
	#check the existence of ip addr
	if [ -e ".ipaddr" ]
	then
		echo
		echo "IP READ FROM CACHE"
		return 1
	#(does not exist)
	else
		echo 
		echo "CALLING API TO QUERY MY IP"
		curl -s -u $IPTOKEN: ipinfo.io > ./.ipaddr # call the api with the token
		return 0
	fi
}

# Location information is retrieved from the ipinfo.io api 
# which is then filtered to retrieve latitude and longitude
LocationFromAPI () {
	LAT=$( cat './.ipaddr' | jq '.loc' | sed -e 's/^"//' -e 's/"$//' | cut -d ',' -f 1)
	LON=$( cat './.ipaddr' | jq '.loc' | sed -e 's/^"//' -e 's/"$//' | cut -d ',' -f 2)
	echo Forecast for my lat=$LAT°, lon=$LON°
}


# weather info is retrieved from the weatherbit.io api this is then filtered
# to retrieve latitude and longitude of the retrieved ip and location 
# and is formatted through the use of string interpolation
ForecastFromAPI () {
	# Make request and retrieve data in the form of an array
	WEATHERINFO=$(curl -s -g "https://api.weatherbit.io/v2.0/forecast/daily?lat=${LAT}&lon=${LON}&key=${WEATHER}" | jq '.data[]')
	for i in "${WEATHERINFO[@]}" 
	# iterate over each element, retrieve data, temp max and min then format without quotes
	do   
		echo $i | jq '"Forecast for \(.datetime) HI: \(.max_temp)° LOW: \(.min_temp)°"' | sed -e 's/^"//' -e 's/"$//'
	done
}

# Function calls
testForIPCache
LocationFromAPI
ForecastFromAPI
