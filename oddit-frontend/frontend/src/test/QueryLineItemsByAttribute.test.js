import {fireEvent, render, screen, waitForElement} from "@testing-library/react";
import QueryLineItemsByAttribute from "../components/QueryLineItemsByAttribute";
import React from "react";
import axios from "axios";
import {API} from "../Constants";

jest.mock('axios');

function fillOutFields(id="", name="", event="") {
    const textFields = screen.getAllByRole("textbox");
    const idField = textFields[0]
    const nameField = textFields[1]
    const eventField = textFields[2]

    fireEvent.change(idField, { target: { value: id } })
    fireEvent.change(nameField, { target: { value: name } })
    fireEvent.change(eventField, { target: { value: event } })
}

async function basicTest(fields, expectedData, url, tableData=null) {
    if (!tableData) {
        tableData = expectedData;
    }
    axios.get.mockImplementation(() => Promise.resolve({
        "data":expectedData
    }));

    fillOutFields(fields.id || "", fields.name || "", fields.event || "")
    //send request
    fireEvent.click(screen.getByRole('button'))
    await waitForElement(() =>
        screen.findAllByText(
            (tableData.length === 1)? "Found 1 line item." : `Found ${tableData.length} line items.`
        )
    )

    //verify correct api call
    expect(axios.get).toHaveBeenCalledWith(
        `${API}${url}`,
        { headers: {'Authorization':`Token pass123`} }
    );

    //check table
    const cells = screen.getAllByRole('cell')
    const rows = screen.getAllByRole('row')
    expect(cells).toHaveLength(4 * tableData.length)
    expect(rows).toHaveLength(1 + tableData.length)
    for (let i = 0; i < tableData.length; i++) {
        expect(cells[4*i]).toHaveTextContent(tableData[i].name)
        expect(cells[4*i + 1]).toHaveTextContent(tableData[i].amount)
        expect(cells[4*i + 2]).toHaveTextContent(tableData[i].category)
        expect(cells[4*i + 3]).toHaveTextContent(tableData[i].event)
    }
}

beforeEach(async () => {
    render(<QueryLineItemsByAttribute token="pass123"/>);
    await waitForElement(() => screen.findAllByText("Search Line Items"))
})

it('successfully displays the Query Line Items by Attribute Component', async () => {
    const textboxes = screen.getAllByRole('textbox')
    expect(textboxes).toHaveLength(3)
    const button = screen.getAllByRole('button')
    expect(button).toHaveLength(1)
})

it ('successfully finds line item by id', async () => {
    await basicTest({id:"1"},
        [{"name":"example item", "amount":"500", "category":"1", "event":"uniqueId"}],
        "api/lineitems/queryId/1/")
})

it ('successfully finds line item by name', async () => {
    await basicTest({name:"example item"},
        [{"name":"example item", "amount":"500", "category":"1", "event":"uniqueId"}],
        "api/lineitems/queryName/example item/")
})

it ('successfully finds line item by event', async () => {
    await basicTest({event:"uniqueId"},
        [{"name":"example item", "amount":"500", "category":"1", "event":"uniqueId"}],
        "api/lineitems/uniqueId/")
})

it ('successfully finds line item by multiple fields', async () => {
    await basicTest({id:"1", name:"example item", event:"uniqueId"},
        [{"name":"example item", "amount":"500", "category":"1", "event":"uniqueId"}],
        "api/lineitems/uniqueId/")

    expect(axios.get).toHaveBeenCalledWith(
        `${API}api/lineitems/queryName/example item/`,
        { headers: {'Authorization':`Token pass123`} }
    );
    expect(axios.get).toHaveBeenCalledWith(
        `${API}api/lineitems/queryId/1/`,
        { headers: {'Authorization':`Token pass123`} }
    );
})

it ('handles api errors gracefully', async() => {
    const errorMessage = "Error message here"
    axios.get.mockImplementationOnce(() =>
        Promise.reject(new Error(errorMessage)),);
    fillOutFields("1")
    //Make request
    fireEvent.click(screen.getByRole('button'))

    await waitForElement(() =>
        screen.findAllByText("An error occurred while querying line items.")
    )
})

it ('warns user about invalid input', async() => {
    //Make request
    fireEvent.click(screen.getByRole('button'))

    await waitForElement(() =>
        screen.findAllByText("You need to specify either the line item ID, name, or Event ID.")
    )
})
