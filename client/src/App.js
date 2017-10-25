import React, { Component } from 'react';
import './App.css';
import ReactMapboxGl, { Layer, Feature } from "react-mapbox-gl";
// import from "react-mapbox-gl/css";

const Map = ReactMapboxGl({
  accessToken: "pk.eyJ1Ijoia2V2aW5jYWk3OSIsImEiOiJjajk2YXBqMHUwMjd6MnpvbHU3a3FiODE4In0.Akrpxhy1oIxzIQ34EB1adg"
});

class App extends Component {

  render() {
    return (
      <div className="App">
        <h1>Parking Predixion</h1>
        <Map
          style="mapbox://styles/mapbox/streets-v9"
          containerStyle={{
            height: "90vh",
            width: "60vw"
          }}
          center={[-117.1611, 32.7157]}
          zoom={[15]}
          >
          <Layer
            type="symbol"
            id="marker"
            layout={{ "icon-image": "marker-15" }}>
            <Feature coordinates={[-0.481747846041145, 51.3233379650232]}/>
          </Layer>
      </Map>
      </div>
    );
  }
}

export default App;
