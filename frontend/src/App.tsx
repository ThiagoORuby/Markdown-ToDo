import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
      <div className="text-center mx-10">
        <img src={logo} className="h-48 w-48 mx-auto" alt="logo" />
        <h1 className="text-4x1 text-red-500">Hello World!</h1>
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <button className="btn btn-wide btn-outline btn-secondary mt-4">Secondary</button>

      </div>
  );
}

export default App;
