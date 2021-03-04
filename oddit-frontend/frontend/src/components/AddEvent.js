import React, { Component } from 'react'
import './auth/Registration.css'
import axios from 'axios'
import { API } from '../Constants'

export default class AddEvent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      event_name: "",
      event_date: ""
    }

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);    
  }

  handleChange(event) {
    this.setState({
      [event.target.name]: event.target.value
    })
  }

  handleSubmit(event) {
    const { event_name, event_date } = this.state
    const token = `Token ${this.props.token}`
    axios
      .post(
        API + 'api/events/',
        {
          event_name: event_name,
          event_date: event_date
        },
        {headers: {'Authorization': token}}
      )
      .then(response => {
        console.log("Add Event response: ", response)
        this.setState({
          event_name: "",
          event_date: ""
        });
        this.props.onAdd()
      })
      .catch(error => {
        console.log("Add Event error: ", error)
      });
      event.preventDefault();
  }

  render() {
    return (
      <div className="form">
        <form onSubmit={this.handleSubmit}>
          <fieldset>
            <legend>Add Event</legend>
            <input
              type="text"
              name="event_name"
              placeholder="Event Name"
              value={this.state.event_name}
              onChange={this.handleChange}
              required
            />
            <input
              type="date"
              name="event_date"
              placeholder="Event Date"
              value={this.state.event_date}
              onChange={this.handleChange}
              required
            />
            <button type="submit">Add Event</button>
          </fieldset>
        </form>
      </div>
    )
  }
}