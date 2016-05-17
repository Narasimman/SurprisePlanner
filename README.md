# SurprisePlanner

This is a mobile app developed for web development and programming course at NYU by Professor. Norman White

Please find the apk file in the build directory to install the app to your mobile.

The directory UI/www contains the ui related stuff. 
index.html is the entry point to the cordova app.


On the server side, 
Look into the server directory where the python modules are built on top of flask web framework that serves RESTFUL api service.
run python api.py to start the server and the client app should be able to get the data from the server using its available end points.

The available api endpoints are
/login
/register
/plan
/orders

The app server is deployed on nyu server dedicated to the team.