import React, {Component} from 'react';
import axios from 'axios';
import { API } from '../Constants';

export default class RemoveLineItem extends Component {
    constructor(props) {
        super(props)
        this.state = {
            message: <p />
        }
        this.removeItem = this.removeItem.bind(this);
    }

    removeItem() {
        console.log("Removing " + this.props.lineItem.name)
        const token = `Token ${this.props.token}`
        axios.delete(`${API}api/lineitems/queryId/${this.props.lineItem.id}/`, {headers: {'Authorization': token}})
            .then(_ => {
                this.setState({
                    message: <p>Line item successfully deleted!</p>
                })
                this.props.onRemove()
            })
            .catch(error => {
                this.setState({
                    message: (<p className="errorMessage">Line Item could not be deleted: {error.message}</p>)
                })
            })
    }

    render() {
        if (!this.props.lineItem) {
            return (
                <div>
                    <h3>
                        Remove line item
                    </h3>
                    <p>
                        To remove a line item, first select on in the table above.
                    </p>
                    {this.state.message}
                </div>
            )
        }
        return (
            <div>
                <h3>Remove line item</h3>
                <p>
                    Selected line item: {this.props.lineItem.name}
                </p>
                <button onClick={this.removeItem}>
                    REMOVE SELECTED ITEM
                </button>
                    {this.state.message}
            </div>
        )
    }
}