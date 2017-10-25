import React, { Component } from 'react';
import './App.css';
import ReactMapboxGl, { Layer, Feature, Marker, ScaleControl } from "react-mapbox-gl";
import axios from 'axios'

const Map = ReactMapboxGl({
  accessToken: "pk.eyJ1Ijoia2V2aW5jYWk3OSIsImEiOiJjajk2YXBqMHUwMjd6MnpvbHU3a3FiODE4In0.Akrpxhy1oIxzIQ34EB1adg"
});

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      coordinates: [-117.1611, 32.7157],
      textInput: ''
    }
    this.updateTextInput = this.updateTextInput.bind(this)
    this.submitTextInput = this.submitTextInput.bind(this)
  }

  componentDidMount() {
    navigator.geolocation.getCurrentPosition((position) => {
      this.setState({coordinates: [position.coords.longitude, position.coords.latitude]});
    });
  }

  updateTextInput(e) {
    this.setState({
      textInput: e.target.value
    })
  }

  submitTextInput(e) {
    if(e.key === 'Enter') {
      let url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURI(this.state.textInput)}.json?access_token=pk.eyJ1Ijoia2V2aW5jYWk3OSIsImEiOiJjajk2YXBqMHUwMjd6MnpvbHU3a3FiODE4In0.Akrpxhy1oIxzIQ34EB1adg`
      console.log(url)
      axios.get(url)
        .then(({data}) => this.setState({
          coordinates: data.features[0].center
        }))
        .catch(error => console.log("MapBox Place API FAIL: ", error))
    }
  }

  render() {
    return (
      <div className="App">
        <h1>Smart Park</h1>
        <Map
          center={this.state.coordinates}
          style="mapbox://styles/mapbox/streets-v9"
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
        <input type="text" 
          onChange={this.updateTextInput} 
          onKeyUp={this.submitTextInput} 
          value={this.state.textInput}
          placeholder="Enter a location"
          style={{
            position: "absolute",
            bottom: "50px",
            left: "20px",
            width: "400px",
            fontSize: "1.5em"
          }}
        />
      </div>
    );
  }
}

export default App;
