import React from 'react';
import ReactDOM from 'react-dom';
import Button from '../components/Button';
import Input from '../components/Input';

jest.mock('axios');

it('renders button without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<Button />, div);
});

it('renders input without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<Input />, div);
});
