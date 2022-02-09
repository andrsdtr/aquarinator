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
- Raspberry Pi 4
-

** **
## Hardware Setup
Here you can see how the different components have to wired together (bild von schaltplan einfügen)
## Software Setup
The code in aquarinator/implentation is just excecutable on a Raspberry Pi. Therefor there is still the option to view just the webapp on the development container. Both options will be explained in the following:

**Running implementation on Raspberry Pi**
1. ...

**Running Development Container**
1. install docker (including docker-compose)
2. navigate to aquarinator/dev_container_webapp
3. run docker-compose up
4. Once the building process is done and the contaiiner is running you can navigate to "localhost:5000" in your browser