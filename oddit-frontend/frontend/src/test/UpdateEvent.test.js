import React from 'react';
import axios from 'axios'
import {render, waitForElement, screen, fireEvent} from '@testing-library/react'
import '@testing-library/jest-dom/extend-expect'
import UpdateEvent from '../components/UpdateEvent';
import { API } from '../Constants'

jest.mock('axios');
const event = {
    event_id: '1',
    event_name: "Event #1",
    event_date: "2020-11-10",
    user: 1
}

it('successfully displays with no selected event', async () => {
    render(<UpdateEvent/>);
    await waitForElement(() => screen.findByText("Update Event"))
    expect(
        screen.getByText("Select an event by clicking it on the event table")
    ).toBeInTheDocument()
})

it('successfully displays event editior', async () => {
  render(<UpdateEvent
    event = {event}
    onUpdate={()=>{}}
    token='pass123'
  />);
  await waitForElement(() => screen.getAllByRole('textbox'))
  const cells = screen.getAllByRole('cell')
  const rows = screen.getAllByRole('row')
  expect(cells).toHaveLength(3)
  expect(rows).toHaveLength(3)

  expect(cells[0].firstChild).toHaveValue(event.event_name)
  expect(cells[1].firstChild.getAttribute("value")).toBe(event.event_date)
})

it('successfully edits event name and date', async() => {
    //Setup Constants
    const updateFunc = jest.fn()
    const updatedEvent = {
        event_id: '1',
            event_name: "New Event Name",
        event_date: "2020-11-12",
        user: 1
    }
    axios.put.mockImplementation(() => Promise.resolve(updatedEvent));

    render(<UpdateEvent
        event = {event}
        onUpdate={updateFunc}
        token='pass123'
    />);
    await waitForElement(() => screen.getAllByRole('textbox'))

    //Set values
    const nameField = screen.getAllByRole("textbox")[0]
    const dateField = screen.getAllByRole("cell")[1].firstChild
    fireEvent.change(nameField, { target: { value: 'New Event Name' } })
    fireEvent.change(dateField, { target: { value: '2020-11-12' } })

    //Make request
    fireEvent.click(screen.getByText('Submit Changes'))

    //Assert on behavior
    await waitForElement(() => screen.getByText('Event successfully updated!'))
    expect(axios.put).toHaveBeenCalledWith(
        `${API}api/events/update/1/`, updatedEvent,
        { headers: {'Authorization':`Token pass123`} }
    );
    expect(updateFunc).toBeCalledTimes(1)
})

it('successfully displays error', async() => {
    const errorMessage = "Error message here"
    const updateFunc = jest.fn()
    axios.put.mockImplementationOnce(() =>
        Promise.reject(new Error(errorMessage)),
    );
    render(<UpdateEvent
        event = {event}
        onUpdate={updateFunc}
        token='pass123'
    />);
    await waitForElement(() => screen.getAllByRole('textbox'))
    fireEvent.click(screen.getByText('Submit Changes'))
    expect(updateFunc).toBeCalledTimes(0)
    await waitForElement(() => screen.getByText(errorMessage))
})

