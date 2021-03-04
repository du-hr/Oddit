import {fireEvent, render, screen, waitForElement} from "@testing-library/react";
import ViewLineItems from "../components/ViewLineItems.js";
import React from "react";
import axios from "axios";
import {API} from "../Constants";

jest.mock('axios');

beforeEach(async () => {
    render(<ViewLineItems event={{event_id: "uniqueEventID"}} token="pass123"/>);
    await waitForElement(() => screen.findAllByText("View Line Items"))
})

it('successfully displays the Query All Line Items component', async () => {
    const button = screen.getAllByRole('button')
    expect(button).toHaveLength(1)
    expect(button[0].textContent).toEqual("Query Line Items")
})

it('successfully displays list of events', async () => {
    const expectedData = [
        {
            id: 1,
            name: "First Item",
            amount: 50,
            category: 0
        },
        {
            id: 2,
            name: "Second Item",
            amount: -45,
            category: 2
        },
        {
            id: 3,
            name: "Third Item",
            amount: 0,
            category: 1
        }
    ]
    axios.get.mockImplementation(() => Promise.resolve({
        "data":expectedData
    }));

    //Run test
    fireEvent.click(screen.getByRole('button'))
    await waitForElement(() => screen.findAllByText("Line Item Name"))

    //verify correct api call
    expect(axios.get).toHaveBeenCalledWith(
        `${API}api/lineitems/uniqueEventID/`,
        { headers: {'Authorization':`Token pass123`} }
    );

    //check table
    const cells = screen.getAllByRole('cell')
    const rows = screen.getAllByRole('row')
    expect(cells).toHaveLength(3 * expectedData.length)
    expect(rows).toHaveLength(1 + expectedData.length)
    for (let i = 0; i < expectedData.length; i++) {
        expect(cells[3*i]).toHaveTextContent(expectedData[i].name)
        expect(cells[3*i + 1]).toHaveTextContent(expectedData[i].amount)
        expect(cells[3*i + 2]).toHaveTextContent(expectedData[i].category)
    }
})