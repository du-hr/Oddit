import React, {Component} from 'react'
import axios from 'axios'
import './ViewEvents.css'
import { API } from '../Constants'

export default class ViewEvents extends Component {
  constructor(props) {
    super(props)
    this.state = {
      events: []
    }
    this.getEvents = this.getEvents.bind(this);
  }

  componentDidMount() {
    this.getEvents();
  }

  getEvents() {
    const token = `Token ${this.props.token}`
    axios
      .get(
        API + 'api/events/',
        {headers: {'Authorization': token}}
      )
      .then(response => {
        this.setState({
          events: response.data
        })
      })
      .catch(error => {
        console.log("Error")
        console.log(error)
      })
  }

  render() {
    const events = this.state.events
    const event_table_titles =
      events.length <= 0 ? null :
        (<tr>
          <th>Event Name</th>
          <th>Event Date</th>
         </tr>)
    const event_rows = this.state.events.map((e, i) => {
      return (
        <tr className="selectable" onClick={()=>this.props.selectEvent(e)}
          key={e.event_id}>
        <td>{e.event_name}</td>
        <td>{e.event_date}</td>
        </tr>)
    })
    return (
      <div>
        <h2>
          View Events
        </h2>
      <table><tbody>
        {event_table_titles}
        {event_rows}
      </tbody></table>
      <button onClick={this.getEvents}>
        Query Events
      </button>
      </div>
    )
  }
}
