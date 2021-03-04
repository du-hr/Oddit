import React, {Component} from 'react'
import axios from 'axios'
import './Registration.css'
import { API } from '../../Constants'

export default class Login extends Component {
  constructor(props) {
    super(props)
    this.state = {
      username: "",
      password: "",
      token: null,
      onSuccess: props.onSuccess
    }

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.setState({
      [event.target.name]: event.target.value
    })
  }

  handleSubmit(event) {
    const { username, password, onSuccess } = this.state
    axios
      .post(
        API + "api-token-auth/",
        {
          username: username,
          password: password
        }
      )
      .then(response => {
        onSuccess(response.data.token, this.state.username)
      })
      .catch(error => {
        console.log("Login error: ", error)
      });
      event.preventDefault();
  }

  render() {
    return (
      <div className="form">
        <form onSubmit={this.handleSubmit}>
          <fieldset>
            <legend>Login</legend>
          <input
            type="text"
            name="username"
            placeholder="Username"
            value={this.state.username}
            onChange={this.handleChange}
            required
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={this.state.password}
            onChange={this.handleChange}
            required
          />
          <button type="submit">Login</button>
        </fieldset>
      </form>
      </div>
    )
  }
}
