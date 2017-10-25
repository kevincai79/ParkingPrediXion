import React, { Component } from 'react';
import './App.css';
import axios from 'axios';
import ReactMapboxGl, { Layer, Feature, Marker, ScaleControl } from "react-mapbox-gl";

const Map = ReactMapboxGl({
  accessToken: "pk.eyJ1Ijoia2V2aW5jYWk3OSIsImEiOiJjajk2YXBqMHUwMjd6MnpvbHU3a3FiODE4In0.Akrpxhy1oIxzIQ34EB1adg"
});

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {coordinates: [-117.1611, 32.7157], parking: []};
  }

  componentDidMount() {
    navigator.geolocation.getCurrentPosition((position) => {
      this.setState({coordinates: [position.coords.longitude, position.coords.latitude]});
    });
    axios.get(`http://localhost:8081`)
      .then(res => {
        console.log(res)
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
        <h1>Smart Park</h1>
        <Map
          center={this.state.coordinates}
          style="mapbox://styles/mapbox/streets-v9"
	        onStyleLoad={this._onStyleLoad.bind(this)}
	        zoom={[15]}
          containerStyle={{
            height: "100vh",
            width: "100vw"
          }}
        >
            <Marker
              coordinates={this.state.coordinates}
            >
              <img src="pin.png" style={{height: "45px", width: "45px"}}/>
            </Marker>
      </Map>
      </div>
    );
  }
}

export default App;
