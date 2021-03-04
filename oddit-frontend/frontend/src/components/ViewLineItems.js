import React, {Component} from 'react'
import axios from 'axios'
import './ViewEvents.css'
import { API } from '../Constants'

export default class ViewLineItems extends Component {
  constructor(props) {
    super(props)
    this.state = {
      LineItems: []
    }
    this.getLineItems = this.getLineItems.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    let value = event.target.value;
    this.setState({
      [event.target.name]: value
    })
  }

  getLineItems() {
    if (!this.props.event) {
      this.setState({
        LineItems: []
      })
      return;
    }
    const token = `Token ${this.props.token}`;
    axios
      .get(
        API + `api/lineitems/${this.props.event.event_id}/`,
        {headers: {'Authorization': token}}
      )
      .then(response => {
        this.setState({
          LineItems: response.data
        })
      })
      .catch(error => {
        console.log("query of all line items does not work")
        console.log(error)
      })
  }

  render() {
    const LineItems = this.state.LineItems
    const LineItems_table_titles =
    LineItems.length <= 0 ? null :
        (<tr>
          <th>Line Item Name</th>
          <th>Amount</th>
          <th>Category</th>
         </tr>)
    const LineItems_rows = this.state.LineItems.map((li) => {
      return this.LineItemRow(li)
    })
    return (
      <div>
        <h2>
          View Line Items
        </h2>
      <table><tbody>
        {LineItems_table_titles}
        {LineItems_rows}
      </tbody></table>
      <button onClick={this.getLineItems}>
        Query Line Items
      </button>
      </div>
    )
  }

  LineItemRow(lineItem) {
    return (
        <tr className="selectable" onClick={()=>this.props.selectLineItem(lineItem)}
            key={lineItem.id}>
          <td>{lineItem.name}</td>
          <td>{lineItem.amount}</td>
          <td>{lineItem.category}</td>
        </tr>
    )
  }
}