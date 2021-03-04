import React from 'react';
import axios from 'axios'
import { render, fireEvent, waitForElement, screen } from '@testing-library/react'
import '@testing-library/jest-dom/extend-expect'
import ViewEvents from '../components/ViewEvents';
import { API } from '../Constants'

jest.mock('axios');

it('successfully displays events', async () => {
  const data = {data: [
    {
      event_id: '1',
      event_name: "Event #1",
      event_date: "10/10/2020"
    },
    {
      event_id: '2',
      event_name: "Event #2",
      event_date: "12/12/2020"
    }
  ]}
  axios.get.mockImplementation(() => Promise.resolve(data));

  render(<ViewEvents token='pass123'/>);
  fireEvent.click(screen.getByText('Query Events'))
  await waitForElement(() => screen.getAllByRole('columnheader'))
  const cells = screen.getAllByRole('cell')
  const rows = screen.getAllByRole('row')
  expect(cells).toHaveLength(4)
  expect(rows).toHaveLength(3)
  expect(cells[0]).toHaveTextContent('Event #1')
  expect(cells[1]).toHaveTextContent('10/10/2020')
  expect(cells[2]).toHaveTextContent('Event #2')
  expect(cells[3]).toHaveTextContent('12/12/2020')
  expect(axios.get).toHaveBeenCalledWith(
    `${API}api/events/`,
    { headers: {'Authorization':`Token pass123`} }
  );
})
