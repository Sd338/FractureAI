import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './components/Home';
import ResultsDisplay from '../components/ResultsDisplay';
import Upload from './components/Upload';
import './styles/app.css'; // Ensure you have the correct path to your CSS file

const App = () => {
    return (
        <Router>
            <div className="App">
                <Switch>
                    <Route exact path="/" component={Home} />
                    <Route path="/upload" component={Upload} />
                    <Route path="/results" component={ResultsDisplay} />
                    {/* Add more routes as needed */}
                </Switch>
            </div>
        </Router>
    );
}

export default App;
