import React, {Component} from 'react'
import axios from 'axios'
import './Registration.css'
import { API } from '../../Constants'

export default class Registration extends Component {
  constructor(props) {
    super();
    this.state = {
      username: "",
      password: "",
      student_id: "",
      club_name: "",
      user_type: "1"
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
    const { username, password, student_id, club_name, user_type } = this.state
    axios
      .post(
        API + "api/users/register",
        {
          username: username,
          password: password,
          student_id: student_id,
          club_name: club_name,
          user_type: user_type
        }
      )
      .then(response => {
        console.log("Registration response: ", response)
      })
      .catch(error => {
        console.log("Registration error: ", error)
      });
      event.preventDefault();
  }

  render() {
    return (
      <div className="form">
        <form onSubmit={this.handleSubmit}>
          <fieldset>
            <legend>Register User</legend>
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
          <input
            type="text"
            name="student_id"
            placeholder="Student ID"
            value={this.state.student_id}
            onChange={this.handleChange}
            required pattern="[0-9]{9}"
          />
          <input
            type="text"
            name="club_name"
            placeholder="Club Name"
            value={this.state.club_name}
            onChange={this.handleChange}
            required
          />
        <label>User type:</label>
          <select
            name="user_type"
            value={this.state.user_type}
            onChange={this.handleChange}
            required>
            <option disabled defaultValue value="">User Type</option>
            <option value="1">Treasurer</option>
            <option value="2">President</option>
          </select>

          <button type="submit">Register User</button>
        </fieldset>
      </form>
      </div>
    )
  }
}
