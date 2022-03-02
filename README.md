# GDP-system
<h2>Storage conditions monitoring and control system</h2>

Client side app:
-Reads the temperature and humidity from DHT22 sensors connected to the microcontrollers
-Stores the data on microcontrollers in a CSV file or in a database
-Sends the data to the server

Server side app:
-Stores data on the server in a database
-Turns on the cooler when the temperature is above the upper limit
-Turns on the heater when the temperature is below the lower limit

![image](https://user-images.githubusercontent.com/100760333/156370641-e14413b5-4825-4d14-b729-ca45533d9d49.png)
