# SmartParking
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
