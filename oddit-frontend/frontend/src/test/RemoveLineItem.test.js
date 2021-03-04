import {fireEvent, render, screen, waitForElement} from "@testing-library/react";
import React from "react";
import axios from "axios";
import {API} from "../Constants";
import RemoveLineItem from "../components/RemoveLineItem";

jest.mock('axios');

it('successfully enables user to delete event', async () => {
    //given
    axios.delete.mockImplementation(() => Promise.resolve({}));
    const onRemoveFunc = jest.fn()

    render(<RemoveLineItem token={"pass123"} lineItem={{name: "item name", id: 25}} onRemove={onRemoveFunc}/>)
    await waitForElement(() => screen.findAllByText("Remove line item"))
    await waitForElement(() => screen.findAllByText("Selected line item: item name"))
    const button = screen.getAllByRole('button')
    expect(button).toHaveLength(1)
    expect(button[0].textContent).toEqual("REMOVE SELECTED ITEM")

    //when
    fireEvent.click(button[0])

    //then
    await waitForElement(() => screen.findAllByText("Line item successfully deleted!"))
    expect(axios.delete).toHaveBeenCalledWith(
        `${API}api/lineitems/queryId/25/`,
        { headers: {'Authorization':`Token pass123`} }
    );
    expect(onRemoveFunc).toBeCalledTimes(1)
})

it('renders correctly when no event is selected', async () => {
    render(<RemoveLineItem token={"pass123"} lineItem={null}/>);
    await waitForElement(() => screen.findAllByText("Remove line item"))
    await waitForElement(() =>
        screen.findAllByText("To remove a line item, first select on in the table above.")
    )
    const button = screen.queryByRole('button')
    expect(button).not.toBeInTheDocument()

})

it('correctly handles http errors', async () => {
    const errorMessage = "Error message here"
    axios.delete.mockImplementationOnce(() =>
        Promise.reject(new Error(errorMessage)),);
    render(<RemoveLineItem token={"pass123"} lineItem={{name: "item name", id: 25}}/>);
    await waitForElement(() => screen.findAllByText("Remove line item"))

    fireEvent.click(screen.getByRole("button"))

    await waitForElement(() => screen.findAllByText("Line Item could not be deleted: Error message here"))
})