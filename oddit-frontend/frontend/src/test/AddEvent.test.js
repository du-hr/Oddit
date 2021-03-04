import React from 'react';
import ReactDOM from 'react-dom';
import AddEvent from '../components/AddEvent';

it('renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<AddEvent />, div);
});