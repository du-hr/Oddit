import React, { Component } from "react";
import axios from "axios";
import './auth/Registration.css'
import './ViewEvents.css'
import { API } from "../Constants";

export default class QueryLineItemsByAttribute extends Component {
  constructor(props) {
    super(props);
    this.state = {
      id: "",
      name: "",
      eventId: "",
      lineItems: [],
      message: "",
    };
    this.handleChange = this.handleChange.bind(this);
    this.getLineItemsByAttribute = this.getLineItemsByAttribute.bind(this);
    this.queryAttribute = this.queryAttribute.bind(this);
  }

  handleChange(event) {
    this.setState({
      [event.target.name]: event.target.value,
    });
  }

  getComparisonString(lineItem) {
    try {
      return lineItem.name + lineItem.amount + lineItem.category + lineItem.id;
    } catch {
      return ""
    }
  }

  getLineItemsByAttribute(value, endpoint) {
    if (endpoint && !endpoint.endsWith("/")) {
      endpoint+="/"
    }
    const token = `Token ${this.props.token}`;
    const url = API + "api/lineitems/" + endpoint + value + "/"
    axios
      .get(url, {
        headers: { Authorization: token, },
      })
      .then((response) => {
        let newLineItems = this.state.lineItems.concat(response.data);
        let lookup = newLineItems.map(x => this.getComparisonString(x))
        newLineItems = newLineItems.filter((item,index)=>{
          return(lookup.indexOf(this.getComparisonString(item)) === index)
        })
        this.setState({
          lineItems: newLineItems,
          message: this.formatMessage(newLineItems.length),
        });
      })
      .catch((error) => {
        this.setState({
          message: "An error occurred while querying line items.",
        });
        console.log(error);
      });
  }

  queryAttribute(event) {
    this.setState({
      lineItems: []
    });
    event.preventDefault();
    const lineItemId = this.state.id
    const lineItemName = this.state.name
    const eventId = this.state.eventId
    if (lineItemId) {
      //this is correct in the context of how the backend works
      this.getLineItemsByAttribute(lineItemId, "queryId");
    }
    if (lineItemName) {
      this.getLineItemsByAttribute(lineItemName, "queryName");
    }
    if (eventId) {
      this.getLineItemsByAttribute(eventId, "");
    }

    if (!(lineItemId + lineItemName + eventId)) {
      this.setState({
        message: "You need to specify either the line item ID, name, or Event ID.",
      });
    }
  }

  formatMessage(numberItems) {
    if (numberItems !== 1) return "Found " + numberItems + " line items.";
    else return "Found 1 line item.";
  }

  render() {
    const lineItems = this.state.lineItems;
    const line_item_titles =
      lineItems.length <= 0 ? null : (
        <tr>
          <th>Line Item Name</th>
          <th>Line Item Amount</th>
          <th>Line Item Category</th>
          <th>Event ID</th>
        </tr>
      );
    const line_item_rows = this.state.lineItems.map((e, i) => {
      return (
        <tr className="selectable" key={i}>
          <td>{e.name}</td>
          <td>{e.amount}</td>
          <td>{e.category}</td>
          <td>{e.event}</td>
        </tr>
      );
    });
    return (
      <div>
        <h2>Search Line Items</h2>
        <form id="queryLineItemByAttributeForm" onSubmit={this.queryAttribute}>
          <fieldset>
            <legend>Query</legend>
            <input
              type="text"
              name="id"
              placeholder="Line Item ID"
              form="queryLineItemByAttributeForm"
              value={this.state.id}
              onChange={this.handleChange}
            />
            <input
              type="text"
              name="name"
              placeholder="Line Item Name"
              form="queryLineItemByAttributeForm"
              value={this.state.name}
              onChange={this.handleChange}
            />
            <input
                type="text"
                name="eventId"
                placeholder="Associated Event ID"
                form="queryLineItemByAttributeForm"
                value={this.state.eventId}
                onChange={this.handleChange}
            />
            <button form="queryLineItemByAttributeForm" type="submit">Search</button>
          </fieldset>
        </form>
        <br />
        <p>{this.state.message}</p>
        <br />
        <table>
          <tbody>
            {line_item_titles}
            {line_item_rows}
          </tbody>
        </table>
      </div>
    );
  }
}