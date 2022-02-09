import logo from './logo.svg';
import './App.css';
import React, { Component } from "react";
import { Button } from 'reactstrap';

import axios from "axios";
import 'bootstrap/dist/css/bootstrap.min.css';

axios.defaults.baseURL = 'http://localhost:8000';


const characters = [
  {
    id: 1,
    name: "Tom",
    hp: 13,
    ac: 20,
  },
  {
    id: 2,
    name: "Jerry",
    hp: 20,
    ac: 12,
  },
];

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      characterList: [],
      modal: false,
      characterData: {
        name: "",
        total_health_points: 0,
        armour_class: 0,
      },
    };
  }

  refreshList = () => {
    axios
      .get("/characters/")
      .then((res) => this.setState({ characterList: res.data }))
      .catch((err) => console.log(err));
  };

  componentDidMount() {
    this.refreshList();
  }

  renderItems = () => {
    const characterList = this.state.characterList

    return characterList.map((character) => (
        <li key={character.id} className="list-group-item">
            <div className="d-flex justify-content-between align-items-center">
              <p>{character.name}</p>
              <p>{character.total_health_points}</p>
              <p>{character.armour_class}</p>
            </div>

            <div>
                <button className="btn btn-secondary">
                    Edit
                </button>
                <button className="btn btn-warning">
                    Fight a monster
                </button>
            </div>
        </li>
    ));
  };
  createCharacter = () => {
    const character = { name: "", total_health_points: 0, armour_class: 0 };

    this.setState({ activcharacterData: character, modal: !this.state.modal });
  };
  handleSubmit = (e) => {
      e.preventDefault();
      let formData = new FormData(e.target);
      console.log(formData);
      // axios.post(
      //   '/characters/', 
      //   formData,
      // )
      // .then(function (response) {
      //   console.log(response);
      //   this.refreshList();
      // })
      // .catch(function (error) {
      //   console.log(error);
      // });
  };
  render() {
      return (
          <main className="container">
              <h1 className="text-white text-uppercase text-center my-4">Todo app</h1>
              <div className="row">
                  <div className="col-md-6 col-sm-10 mx-auto p-0">
                      <div className="card p-3">
                          {/* <div className="mb-4">
                              <Button className="btn btn-primary" onClick={this.createCharacter}>
                                Add Character
                              </Button>
                          </div> */}

                          <ul className="list-group">
                              <li
                                  className="list-group-item d-flex justify-content-between align-items-center"
                              >
                                  <p className="list-group-item-heading">Character name</p>
                                  <p className="list-group-item-heading">Hitpoints</p>
                                  <p className="list-group-item-heading">Armour class</p>
                              </li>
                              {this.renderItems()}
                          </ul>
                      </div>
                    <form className='form' onSubmit={this.handleSubmit}>
                      <input
                        type="text"
                        name="name"
                        placeholder="Name"
                      />
                      <input
                        type="text"
                        name="total_health_points"
                        placeholder="0"
                      />
                      <input
                        type="text"
                        name="armour_class"
                        placeholder="0"
                      />
                      <button type="submit">Create</button>
                    </form>
                  </div>
              </div>
          </main>
      );
    }
}
export default App;
