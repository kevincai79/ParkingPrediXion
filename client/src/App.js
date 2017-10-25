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
      coordinates: [-117.157122, 32.712854],
      textInput: '',
      parking: [],
      suggestions: []
    }
    this.updateTextInput = this.updateTextInput.bind(this)
    this.submitTextInput = this.submitTextInput.bind(this)
  }

  componentDidMount() {
    // navigator.geolocation.getCurrentPosition((position) => {
    //   this.setState({coordinates: [position.coords.longitude, position.coords.latitude]});
    // });
    console.log(`https://fiery-doves-server-v2.run.aws-usw02-pr.ice.predix.io?ts=${Number(new Date)}&long=${this.state.coordinates[0]}&lat=${this.state.coordinates[1]}`)
    axios.get(`https://fiery-doves-server-v2.run.aws-usw02-pr.ice.predix.io?ts=${Number(new Date)}&long=${this.state.coordinates[0]}&lat=${this.state.coordinates[1]}`)
      .then(({ data: {zones, suggestions}}) => {
        console.log("zones: ", zones, "suggestions: ", suggestions)
        this.setState({
          parking: zones,
          suggestions: suggestions
        });
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
      axios.get(url)
        .then(({data}) => this.setState({
          coordinates: data.features[0].center
        }))
        .catch(error => console.log("MapBox Place API FAIL: ", error))
    }
  }

  _onStyleLoad(map, event) {
    this.state.parking.forEach(spot => {
      map.addLayer(spot)
    });
  }

  render() {
    return (
      <div className="App">
        <h1>Parking PrediXion</h1>
        <Map
          center={this.state.coordinates}
          style="mapbox://styles/mapbox/streets-v9"
	        onStyleLoad={this._onStyleLoad.bind(this)}
	        zoom={[16.5]}
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
            bottom: "20px",
            left: "9%",
            width: "80%",
            fontSize: "1.4em"
          }}
        />
        <div
          className="recommendation"
          style={{
            borderRadius: "5px",
            position: "absolute",
            top: "80px",
            left: "20px",
            backgroundColor: "rgba(255, 255, 255, .7)",
            padding: "1.5em"

          }}
        >
          This stuff is happending
        </div>
      </div>
    );
  }
}

export default App;
