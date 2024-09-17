import React from 'react';
import { Switch, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer'
import Home from './pages/Home';
import Play from './pages/Play';
import Profile from './pages/Profile';
import About from './pages/About';
import './App.css';

function App() {
	return (
		<div className="App">
			<Header />
			<Switch>
				<Route path="/" exact component={Home} />
				<Route path="/play" exact component={Play} />
				<Route path="/profile" exact component={Profile} />
				<Route path="/about" exact component={About} />
			</Switch>
			<Footer />
		</div>
	);
}

export default App;
