import React, { Component } from 'react'
import './auth/Registration.css'
import CurrencyInput from 'react-currency-input-field'
import axios from 'axios'
import { API } from '../Constants'

export default class AddLineItem extends Component {
  constructor(props) {
    super(props);
    this.state = {
      name: "",
      amount: "",
      category: "1",
      message: ""
    }

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    let value = event.target.value;
    this.setState({
      [event.target.name]: value
    })
  }

  handleSubmit(event) {
    const { name, amount, category } = this.state
    const selectedEvent = this.props.event
    const token = `Token ${this.props.token}`
    axios
      .post(
        API + 'api/lineitems/',
        {
          name: name,
          amount: amount,
          category: category,
          event: selectedEvent.event_id,
        },
        {headers: {'Authorization': token}}
      )
      .then(response => {
        console.log("Add Line Item response: ", response)
        this.setState({
          message: <p>Line item successfully added!</p>
        })
        this.setState({
          name: "",
          amount: "",
          category: "1"
        });
        this.props.onAdd();
      })
      .catch(error => {
        console.log("Add Line Item error: ", error)
        this.setState({
          message: (<p className="errorMessage"> {error.message}</p>)
        })
      });
      event.preventDefault();
  }

  render() {
    return (
      <div className="form">
        <form onSubmit={this.handleSubmit}>
          <fieldset>
            <legend>Add Line Item</legend>
            <input
              type="text"
              name="name"
              placeholder="Line Item Name"
              value={this.state.name}
              onChange={this.handleChange}
              required
            />
            <CurrencyInput
              id="amount"
              name="amount"
              placeholder="Line Item Amount"
              value={this.state.amount}
              onChange={(value) => this.setState({"amount": value})}
              prefix="$"
              required
            />
        <label>Line Item Category:</label>
            <select
              data-testid="select"
              name="category"
              value={this.state.category}
              onChange={this.handleChange}
              required>
              <option disabled defaultValue value="">Line Item Category</option>
              <option value="1">Food</option>
              <option value="2">Recreation</option>
              <option value="3">TV</option>
              <option value="4">Sponsorship</option>
            </select>
            <button type="submit" name="submit">Add Line Item</button>
            {this.state.message}
          </fieldset>
        </form>
      </div>
    )
  }
}