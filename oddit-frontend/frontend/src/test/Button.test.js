import React from 'react';
import ReactDOM from 'react-dom';
import DeleteEvent from '../Button'; 
it('renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<DeleteEvent />, div);
});
