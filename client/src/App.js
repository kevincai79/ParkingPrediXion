import React, { Component } from 'react';
import './App.css';
import ReactMapboxGl, { Layer, Popup, Feature, Marker, ScaleControl } from "react-mapbox-gl";
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
      suggestions: [],
      showSuggestions: false
    }
    this.updateTextInput = this.updateTextInput.bind(this)
    this.submitTextInput = this.submitTextInput.bind(this)
  }

  componentDidMount() {
    axios.get(`https://fiery-doves-server-v2.run.aws-usw02-pr.ice.predix.io?ts=${Math.floor(Number(new Date()) / 1000)}&long=${this.state.coordinates[0]}&lat=${this.state.coordinates[1]}`)
      .then(({ data: {zones, suggestions}}) => {
        console.log("zones: ", zones, "suggestions: ", suggestions)
        this.setState({
          parking: zones,
          suggestions: suggestions
        });
      })
      .catch(error => console.log("Ali Server error: ", error))
  }

  componentDidUpdate() {
    console.log("update")
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
        <h1><span className="big-p">P</span>arking <span className="big-p">P</span>redi<span className="big-p">X</span>ion</h1>
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
          {this.state.suggestions.map(({msg, long, lat}, idx) => (
            <Popup
              coordinates={[long, lat]}
              key={idx}
            >
              {msg}
            </Popup>
          ))}
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
            textAlign: "left"

          }}
        >
          <h2>
            <a 
              href="#"
              onClick={() => this.setState({
                showSuggestions: !this.state.showSuggestions
              })}
            >
              Parking Suggestions
            </a>
          </h2>
          <ul style={{padding: "0"}} className={this.state.showSuggestions ? "" : "hidden"}>
          {this.state.suggestions.map(({msg, long, lat}, idx) => (
            <li style={{listStyleType: "none"}} key={idx}>
            <a  href="#"
                onClick={() => this.setState({
              coordinates: [long, lat]
            })}
          >
            {msg.trim()}
          </a>
        </li>
          ))}
        </ul>
        </div>
      </div>
    );
  }
}

export default App;
