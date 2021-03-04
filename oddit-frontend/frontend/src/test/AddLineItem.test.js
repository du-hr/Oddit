import React from 'react';
import axios from 'axios'
import {render, waitForElement, screen, fireEvent} from '@testing-library/react'
import '@testing-library/jest-dom/extend-expect'
import AddLineItem from '../components/AddLineItem';
import { API } from '../Constants'

jest.mock('axios');
const event = {
    event_id: '1',
    event_name: "Event #1",
    event_date: "2020-11-10",
    user: 1
}

function fillOutFields() {
    const nameField = screen.getAllByRole("textbox")[0]
    const amountField = screen.getAllByRole("textbox")[1]
    fireEvent.change(nameField, { target: { value: 'Soda' } })
    fireEvent.change(amountField, { target: { value: '20' } })
    fireEvent.change(screen.getByTestId("select"), {
        target: { value: "3" },
    });
}

it('successfully displays the Add Line Item Component', async () => {
    render(<AddLineItem/>);
    await waitForElement(() => screen.findAllByText("Add Line Item"))
    expect(
        screen.getByText("Line Item Category")
    ).toBeInTheDocument()
    const textboxes = screen.getAllByRole('textbox')
    expect(textboxes).toHaveLength(2)
    const button = screen.getAllByRole('button')
    expect(button).toHaveLength(1)
})

it('successfully adds a line item to the event', async() => {
    //Setup Constants
    const lineItemFunc = jest.fn()
    const lineItem = {
        amount: "20",
        category: "3",
        event: "1",
        name: "Soda",
    }
    axios.post.mockImplementation(() => Promise.resolve(lineItem));

    render(<AddLineItem
        event={event}
        onAdd={lineItemFunc}
        token='pass123'
    />);
    await waitForElement(() => screen.getAllByRole('textbox'))

    //Set values
    fillOutFields();

    //Make request
    fireEvent.click(screen.getByRole('button'))

    //Assert on behavior
    await waitForElement(() => screen.getByText('Line item successfully added!'))
    expect(axios.post).toHaveBeenCalledWith(
        `${API}api/lineitems/`, lineItem,
        { headers: {'Authorization':`Token pass123`} }
    );
    expect(lineItemFunc).toBeCalledTimes(1);
})

it('successfully displays an error', async() => {
    //Setup Constants
    const lineItemFunc = jest.fn()
    const errorMessage = "Error message here"
    axios.post.mockImplementationOnce(() =>
    Promise.reject(new Error(errorMessage)),);
    render(<AddLineItem
        event={event}
        onAdd={lineItemFunc}
        token='pass123'
    />);
    await waitForElement(() => screen.getAllByRole('textbox'))
    fillOutFields();

    //Make request
    fireEvent.click(screen.getByRole('button'))

    //Assert on behavior
    await waitForElement(() => screen.getAllByRole('textbox'))
    expect(lineItemFunc).toBeCalledTimes(0)
    await waitForElement(() => screen.getByText(errorMessage))
})

