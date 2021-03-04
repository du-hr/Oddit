import React, {Component} from 'react'
import './UpdateEvent.css'
import axios from 'axios'
import { API } from '../Constants'
import AddLineItem from "./AddLineItem";
import ViewLineItems from "./ViewLineItems";
import RemoveLineItem from "./RemoveLineItem";

export default class UpdateEvent extends Component {

  constructor(props) {
    super(props)
    this.state = {
        currentEvent: {
          event_name: props.event?.event_name || "",
          event_date: props.event?.event_date || ""
        },
        message: "",
        selectedLineItem: null
    }
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.updateLineItems = this.updateLineItems.bind(this);
    this.selectLineItem = this.selectLineItem.bind(this);
    this.line_item_viewer = React.createRef();
  }

  componentDidUpdate(previousProps) {
    if (previousProps.event?.event_id !== this.props.event?.event_id) {
      this.setState({
        currentEvent: {
          event_name: this.props.event.event_name,
          event_date: this.props.event.event_date
        },
        selectedLineItem: null
      })
    }
  }

  handleChange(event) {
    let e = {...this.state.currentEvent}
    e[event.target.name] = event.target.value
    this.setState({ currentEvent: e })
  }

  selectLineItem(event) {
    console.log("RAN!")
    this.setState({ selectedLineItem: event })
  }

  handleSubmit(event) {
    const token = `Token ${this.props.token}`
    let newEvent = Object.assign(this.props.event, this.state.currentEvent)
    axios
      .put(
        API + "api/events/update/" + this.props.event.event_id + "/",
        newEvent,
        {headers: {'Authorization': token}}
      )
      .then(_ => {
        this.setState({
          message: <p>Event successfully updated!</p>
        })
        this.props.onUpdate()
      })
      .catch(error => {
        this.setState({
          message: (<p className="errorMessage"> {error.message}</p>)
        })
      })
    event.preventDefault();
  }

  updateLineItems() {
    this.line_item_viewer.current.getLineItems();
  }

  render() {
    if (!this.props.event) {
      return (
        <div>
          <h2>Update Event</h2>
          <p>Select an event by clicking it on the event table</p>
        </div>
      )
    }
    return(
      <div>
        <h2>Update Event</h2>
        <form id="event_attribute_form" onSubmit={this.handleSubmit}>
        <table><tbody>
          <tr>
            <th>Event Name</th>
            <th>Event Date</th>
          </tr>
          <tr>
            <td>
              <input
                type="text"
                name="event_name"
                value={this.state.currentEvent.event_name}
                onChange={this.handleChange}
                required
                form="event_attribute_form"
                placeholder="Event Name"
                />
            </td>
            <td>
            <input
              type="date"
              name="event_date"
              value={this.state.currentEvent.event_date}
              onChange={this.handleChange}
              required
              form="event_attribute_form"
              />
            </td>
          </tr>
          <tr>
            <td colSpan="2">
              <button form="event_attribute_form" type="submit">
                Submit Changes
              </button>
            </td>
          </tr>
        </tbody></table>
        </form>
        {this.state.message}
        <AddLineItem
            token = {this.props.token}
            event = {this.props.event}
            onAdd = {this.updateLineItems}
        />
        <ViewLineItems
            ref = {this.line_item_viewer}
            token = {this.props.token}
            event = {this.props.event}
            selectLineItem = {this.selectLineItem}
        />
        <RemoveLineItem
          token = {this.props.token}
          lineItem = {this.state.selectedLineItem}
          onRemove = {this.updateLineItems}
        />
      </div>
    )
  }
}
