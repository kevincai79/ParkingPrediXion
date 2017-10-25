import React, { Component } from 'react';
import './App.css';
import axios from 'axios';
import ReactMapboxGl, { Layer, Feature } from "react-mapbox-gl";
// import from "react-mapbox-gl/css";

const Map = ReactMapboxGl({
  accessToken: "pk.eyJ1Ijoia2V2aW5jYWk3OSIsImEiOiJjajk2YXBqMHUwMjd6MnpvbHU3a3FiODE4In0.Akrpxhy1oIxzIQ34EB1adg"
});

class App extends Component {

  componentDidMount() {
    axios.get(`http://192.168.1.119:8081`)
      .then(res => {
        this.setState({parking: res.data});
      });
  }

  _onStyleLoad(map, event) {
    this.state.parking.forEach(spot => {
      map.addLayer(spot)
    });
  }

  render() {
    return (
      <div className="App">
        <h1>Parking Predixion</h1>
        <Map
          style="mapbox://styles/mapbox/streets-v9"
	  onStyleLoad={this._onStyleLoad.bind(this)}
	  center={[-117.15755482515063, 32.71359092522689]}
	  zoom={[15]}
          containerStyle={{
            height: "100vh",
            width: "100vw"
          }}>
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
