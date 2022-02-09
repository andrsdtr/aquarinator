# Aquarinator

## Use-Case
With the help of this irrigation system, the plants can be watered automatically. So the user no longer has to worry that his plants are not sufficiently watered, because the irrigation is controlled by sensors. This also controls the aspect of targeted watering, because watering is only done when it is really necessary. In addition to this function, the user also has the option to view the data of his monitoring on a web app and can thus also perform some functions such as manual watering or measuring the humidity.

**Aquarinator was developed by the following team members:**
- Andreas Dichter (6104795)
- Can Berkil (2087362)
- Simon Schmid (9917195)

**Development Teams**
- Webapp and Database (Andreas Dichter, Can Berkil)
- Irrigation system (Simon Schmid)

**Software components**
- Raspberry Pi OS
- Python
- Flask
- Firebase

**Hardware components**
- Raspberry Pi 4B (tested on this one, probably works on older ones too)
- Water pump
- Relay module
- Moisture sensor
- A/D Converter
- Wires

** **
## Hardware Setup
Here you can see how the different components have to be wired together:
<img width="1049" alt="Bildschirmfoto 2022-02-09 um 17 03 24" src="https://user-images.githubusercontent.com/61969721/153240309-14dfd319-495d-465a-b8f8-ecee8bad288a.png">

## Software Setup
The code in aquarinator/implentation is just excecutable on a Raspberry Pi. Therefor there is still the option to view just the webapp on the development container. Both options will be explained in the following:


**Running implementation on Raspberry Pi**
1. install python3
2. the following packages are necessary:
    - Flask
    - pyrebase
    - RPi.GPIO
3. navigate to the implementation/app folder
4. run "python3 app.py"
5. the webapp is available at 0.0.0.0:4321 on the Pi and on the local network via the IP of the Pi and the port 4321 (in testcase: 192.168.0.4:4321)

**Running Development Container**
1. install docker (including docker-compose)
2. navigate to aquarinator/dev_container_webapp
3. run docker-compose up
4. Once the building process is done and the contaiiner is running you can navigate to "localhost:5000" in your browser

**Connect your own Firebase RT Database**
- To conect your own Fireabse Real Time Database just change the config variable in the top of the app.py file to the information of your database. The tables and entrys will be created automatically.