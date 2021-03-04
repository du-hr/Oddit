import React, {Component} from 'react'
import ViewEvents from './ViewEvents.js'
import UpdateEvent from './UpdateEvent.js'
import AddEvent from "./AddEvent";
import QueryLineItemsByAttribute from "./QueryLineItemsByAttribute";

export default class UserHomepage extends Component {

  constructor(props) {
    super(props)
    this.state = {
        selectedEvent: null
    }
    this.selectEvent = this.selectEvent.bind(this);
    this.refreshEvents = this.refreshEvents.bind(this);
    this.events_viewer = React.createRef();
  }

  render() {
    return(
      <div>
          <AddEvent
              token={this.props.token}
              onAdd={this.refreshEvents}
          />
          <ViewEvents
              ref={this.events_viewer}
              selectEvent={this.selectEvent}
              token={this.props.token}
          />
          <UpdateEvent
              token={this.props.token}
              event={this.state.selectedEvent}
              onUpdate={this.refreshEvents}
          />
          <QueryLineItemsByAttribute
              token={this.props.token}
          />
      </div>
    )
  }

  refreshEvents() {
    this.events_viewer.current.getEvents();
  }

  selectEvent(e) {
    this.setState({
      selectedEvent: e
    })
  }
}
