# Countdown
A countdown timer made with Python

## Features
- Frequent updates (as long as I can keep thinking of things to add)
- The ability to save data to Home Assistant (given enough setup) or local files
- Custom themes (fonts/colors)
- Autosaving new events/themes
- Color change based on time until event

## Possible features that I may add:
- The ability to save to multiple locations at once (for instance, `data.json` as well as Home Assistant)
- Add tabs to the theme creation process
- Resizable GUI

## Screenshots
![image](https://user-images.githubusercontent.com/87204246/224436282-584db486-e315-4cbe-852b-f9a23726b303.png)
![image](https://user-images.githubusercontent.com/87204246/224436449-50db4e81-af7b-4190-8346-e36bff0f03bb.png)
![image](https://user-images.githubusercontent.com/87204246/224436540-5ab9fc67-4091-49d1-aa76-649e981a6147.png)

## Installation instructions
0. Have Python 3 installed on a Windows computer (would probably work on other OS's with very minor tweaking)
1. Download or clone
2. Run `countdown.pyw`
### Command line options:
```
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        The file to load data from initally (default: data.json), after first load, loads from
                        --outfile.
  -o OUTFILE, --outfile OUTFILE
                        The file to write data to (default: data.json)

Use `hass` for --infile or --outfile to save to/load from Home Assistant.
```

## To use with Home Assistant
DISCLAIMER: There may be other ways, maybe even better ways to do this. This is just a solution that worked for me. Also, my instructions may be somewhat lacking, since I don't want to reinstall Home Assistant for testing.
1. Make sure Home Assistant is accessible. If it's not reachable at `http://homeassistant:8123`, change `hass_url` on line 17 of `hass.py` to the correct URL.
2. Create a Home Assistant long-lived access token (click on profile picture, scroll down to the bottom), and put it in TOKEN.txt in the same folder as `countdown.py`.
3. Install and set up Node Red through Home Assistant (if you haven't already)
4. In Node Red, hit Ctrl/Cmd+I to open the Import menu, then paste the following flow in (this is copied from mine, but I don't know whether exporting/importing will work the way I hope it does, so be aware that it may not work):
```
[{"id":"63755a44942c36f0","type":"tab","label":"Flow 1","disabled":false,"info":"","env":[]},{"id":"c9f84fd6c5cb7c60","type":"ha-sensor","z":"63755a44942c36f0","name":"Countdown Data","entityConfig":"d111abeb7e8729d5","version":0,"state":"Foo","stateType":"str","attributes":[{"property":"countdown_data","value":"payload.event","valueType":"msg"}],"inputOverride":"allow","outputProperties":[],"x":470,"y":240,"wires":[["aa69980703e74c10"]]},{"id":"b216ef718851daf6","type":"debug","z":"63755a44942c36f0","name":"debug 1","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"true","targetType":"full","statusVal":"","statusType":"auto","x":640,"y":320,"wires":[]},{"id":"5aa4df2f859774d5","type":"server-events","z":"63755a44942c36f0","name":"","server":"53eca0699b20e0a3","version":2,"eventType":"countdown_data","exposeToHomeAssistant":false,"eventData":"","haConfig":[{"property":"name","value":""},{"property":"icon","value":""}],"waitForRunning":true,"outputProperties":[{"property":"payload","propertyType":"msg","value":"$outputData(\"eventData\")","valueType":"jsonata"},{"property":"topic","propertyType":"msg","value":"$outputData(\"eventData\").event_type","valueType":"jsonata"}],"event_type":"","x":230,"y":280,"wires":[["b216ef718851daf6","c9f84fd6c5cb7c60"]]},{"id":"aa69980703e74c10","type":"debug","z":"63755a44942c36f0","name":"debug 2","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"true","targetType":"full","statusVal":"","statusType":"auto","x":660,"y":240,"wires":[]},{"id":"d111abeb7e8729d5","type":"ha-entity-config","server":"53eca0699b20e0a3","deviceConfig":"b8d832a9c5957b29","name":"Countdown data","version":"6","entityType":"sensor","haConfig":[{"property":"name","value":""},{"property":"icon","value":""},{"property":"entity_category","value":""},{"property":"device_class","value":""},{"property":"unit_of_measurement","value":""},{"property":"state_class","value":""}],"resend":true,"debugEnabled":true},{"id":"53eca0699b20e0a3","type":"server","name":"Home Assistant","version":5,"addon":false,"rejectUnauthorizedCerts":true,"ha_boolean":"y|yes|true|on|home|open","connectionDelay":true,"cacheJson":true,"heartbeat":false,"heartbeatInterval":"30","areaSelector":"friendlyName","deviceSelector":"friendlyName","entitySelector":"friendlyName","statusSeparator":": ","statusYear":"hidden","statusMonth":"short","statusDay":"numeric","statusHourCycle":"default","statusTimeFormat":"h:m","enableGlobalContextStore":false},{"id":"b8d832a9c5957b29","type":"ha-device-config","name":"Countdown data","hwVersion":"","manufacturer":"Node-RED","model":"","swVersion":""}]
```
5. Deploy Node Red. You may need to go looking through the entity list for something like `sensor.nodered_<SomeHexNumber>` and change the entity ID to `sensor.countdown_data`.
6. HOPEFULLY it will just work.
