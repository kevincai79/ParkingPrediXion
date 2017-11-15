# Parking PrediXion
## About
Winner at the 2017 GE Minds + Machines Appathon.
<p align="center">
  <img width="262" height="528" src="https://github.com/joshleichtung/ParkingPrediXion/blob/development/readme_assets/parking-predixion-example.gif?raw=true">
</p>
Parking PrediXion is mobile web and mobile application built in React, Node and Python, integrating Predix's CityIQ API and hosted on Predix. Parking PrediXion collects data from the CityIQ API while our algorithm processes this data in order to offer users an accurate prediction as to city conditions and parking availability up to an hour in advance. This will allow users to plan their time as well as their travel decisions to allow for reduced travel time as well as carbon dioxide emissions. Parking PrediXion in the near future will be able to predict urban parking conditions a week up to a month in advance to allow users to make travel plans much more efficiently and lower their carbon dioxide emissions in the process.

## Build Instruction
* Clone repo.
* Run `npm install` from the root. This installs the dependencies for the server.
* `cd client`, then `npm install`, which installs dependencies for the react front
  end.
* You will need to run two servers, so will need 2 terminal tabs. In the root
  directory, run `PORT=3001 node bin/www`
* In a new terminal tab, `cd client` and run `npm start` to start the react app.

## Development Notes
* You should only need to work inside the `/client` folder to start. The entry
  point is `client/src/App.js`. Build further in the components directory.
* The mapbox package repo and demo info is at [react-mapbox-gl](https://github.com/alex3165/react-mapbox-gl)
