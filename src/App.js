import React from 'react';
import logo from './logo.png';
import './App.css';

class App extends React.Component {
	
	constructor() {
		super();
		this.flaskEndpoint = "http://localhost:5000"

		this.state = {
			integration: '',
			tel: '',
			email: '',
			password: '',
			message: ''
		}
	}
	
	submitClicked = (event) => {
		event.preventDefault();
		const requestBody = {
			integration: this.state.integration,
			tel: this.state.tel,
			email: this.state.email,
			password: this.state.password
		}
		console.log(requestBody)
		fetch(`${this.flaskEndpoint}/signup`, {
			method: 'POST',
			headers: {
			  'Content-Type': 'application/json',
			  'Access-Control-Request-Method': 'POST',
			  'Access-Control-Request-Headers': 'Content-Type',
			},
			body: JSON.stringify(requestBody)
		  }).then((response) => {
			console.log(response)
			response.json().then((data) => {
				// todo, update success msg
			  if (data.status === 200) {
				this.setState({     
				  integration: '',
				  tel: '',
				  email: '',
				  password: '',
				  message: 'Integration successfully added.'
				})
			  }
			  else {
				this.handleError(data.message);
			  }
			})
		  }).catch((err) => {
			const response = err.response;
			if (response) {
				this.handleError(response.data.message);
			}
			else {
				this.handleError('An error occured. Please try again later.');
			}
		  })
	}	

	handleError = (message) => {
		this.setState({ message: message })
	}

	setIntegration = (integration) => {
		this.setState({ integration: integration})
	}

	updateTel = (tel) => {
		this.setState({ tel: tel })
	}

	updateEmail = (email) => {
		this.setState({ email: email });
	}

	updatePassword = (password) => {
		this.setState({ password: password})
	}

	render = () => {
		return (
		  <div className="App">
			  <img src={logo} className="logo"></img>
			  <div className="container" id="container">
				  <div className="form-container add-int-container">
					  { this.state.message ? 
						  (<div className="status">{this.state.message}</div>)
						  : null
					  }
					  <h1>Add an Integration</h1>
					  <div className="social-container">
						  <div className={`social messenger ${this.state.integration == "messenger" ? 'selected' : ''}`} onClick={(e) => this.setIntegration("messenger")}><i className="fab fa-facebook-messenger"></i></div>
						  <div className={`social instagram ${this.state.integration == "instagram" ? 'selected' : ''}`} onClick={(e) => this.setIntegration("instagram")}><i className="fab fa-instagram"></i></div>
						  <div className={`social twitter ${this.state.integration == "twitter" ? 'selected' : ''}`} onClick={(e) => this.setIntegration("twitter")}><i className="fab fa-twitter"></i></div>
					  </div>
					  <input type="tel" placeholder="Phone Number" onChange={(e) => this.updateTel(e.target.value)}/>
					  <input type="email" placeholder="Email" onChange={(e) => this.updateEmail(e.target.value)}/>
					  <input type="password" placeholder="Password" onChange={(e) => this.updatePassword(e.target.value)}/>
					  <button onClick={this.submitClicked}>Add Integration</button>
				  </div>
				</div>
		  </div>
		);
	}

}

export default App;
