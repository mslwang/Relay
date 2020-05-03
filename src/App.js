import React from 'react';
import logo from './logo.png';
import './App.css';
import { errorMessages } from './constants'

class App extends React.Component {
	
	constructor() {
		super();
		this.flaskEndpoint = ""

		this.state = {
			integration: '',
			tel: '',
			email: '',
			password: '',
			access_token: '',
			access_secret_token: '',
			api_key: '',
			api_secret_key: '',
			message: '',
			warning: false
		}
	}

	submitClicked = (event) => {
		event.preventDefault();
		let requestBody;

		if(this.state.integration == "twitter") {
			requestBody = {
				integration: this.state.integration,
				active: this.state.integration,
				tel: this.state.tel,
				access_token: this.state.access_token,
				access_secret_token: this.state.access_secret_token,
				api_key: this.state.api_key,
				api_secret_key: this.state.api_secret_key
			}
		} else {
			requestBody = {
				integration: this.state.integration,
				active: this.state.integration,
				tel: this.state.tel,
				email: this.state.email,
				password: this.state.password
			}
		}
			
		const checkFilled = new Promise((resolve, reject) => {
			if(requestBody.integration !== "messenger" && requestBody.integration !== "twitter"){
				reject('MISSING_INTEGRATION');
			} else if(requestBody.tel === ""){
				reject('MISSING_PHONE');
			} else if (requestBody.integration == "messenger") {
				if (requestBody.email === ""){
					reject('MISSING_EMAIL');
				} else if(requestBody.password === ""){
					reject('MISSING_PASSWORD');
				} else {
					resolve();
				}
			} else if (requestBody.integration == "twitter") {
				if (requestBody.access_token === ""){
					reject('MISSING_ACCESS_TOKEN');
				} else if (requestBody.access_token_secret === ""){
					reject('MISSING_ACCESS_TOKEN_SECRET');
				} else if (requestBody.api_key === "") {
					reject('MISSING_API_KEY');
				} else if (requestBody.api_secret_key === "") {
					reject('MISSING_API_KEY_SECRET');
				} else {
					resolve();
				}
			}
		})
		.then(fetch(`${this.flaskEndpoint}/signup`, {
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
					access_token: '',
					access_secret_token: '',
					api_key: '',
					api_secret_key: '',
					message: 'Integration successfully added.',
					warning: false
				})
			  }
			  else {
				this.handleError(data.message);
			  }
			})
		  }).catch((err) => {
			this.setState({warning: true});
		  }),
		  (val) => {
			  console.log(val)
			  this.handleError(errorMessages[val])
		  });
	}	

	handleError = (message) => {
		this.setState({ message: message})
	}

	setIntegration = (integration) => {
		this.setState({ integration: integration, message: '', warning: false })
	}

	updateTel = (tel) => {
		this.setState({ tel: tel, message: '', warning: false })
	}

	updateEmail = (email) => {
		this.setState({ email: email, message: '', warning: false });
	}

	updatePassword = (password) => {
		this.setState({ password: password, message: '', warning: false })
	}

	updateAccessToken = (accessToken) => {
		this.setState({ access_token: accessToken, message: '', warning: false })
	}

	updateAccessTokenSecret = (accessTokenSecret) => {
		this.setState({ access_secret_token: accessTokenSecret, message: '', warning: false })
	}

	updateAPIKey = (accessAPIKey) => {
		this.setState({ api_key: accessAPIKey, message: '', warning: false })
	}

	updateAPIKeySecret = (accessAPIKeySecret) => {
		this.setState({ api_secret_key: accessAPIKeySecret, message: '', warning: false })
	}

	renderMessengerForm = () => {
		return (
			<div className="messengerForm">
				<input type="tel" placeholder="Phone Number" onChange={(e) => this.updateTel(e.target.value)}/>
				<input type="email" placeholder="Email" onChange={(e) => this.updateEmail(e.target.value)}/>
				<input type="password" placeholder="Password" onChange={(e) => this.updatePassword(e.target.value)}/>
			</div>
		)
	}

	renderTwitterForm = () => {
		return (
			<div className="twitterForm">
				<input type="tel" placeholder="Phone Number" onChange={(e) => this.updateTel(e.target.value)}/>
				<input type="text" placeholder="Access Token" onChange={(e) => this.updateAccessToken(e.target.value)}/>
				<input type="text" placeholder="Access Token Secret" onChange={(e) => this.updateAccessTokenSecret(e.target.value)}/>
				<input type="text" placeholder="API Key" onChange={(e) => this.updateAPIKey(e.target.value)}/>
				<input type="text" placeholder="API Secret Key" onChange={(e) => this.updateAPIKeySecret(e.target.value)}/>
			</div>
		)
	}

	render = () => {
		return (
		  <div className="App">
			  <img src={logo} className="logo"></img>
			  <div className="container" id="container">
				  <div className="form-container add-int-container">
					  { this.state.message ? 
						  (<div className="status" style={{backgroundColor: this.state.warning ? "#ff726f" : "#4ee45e"}}>{this.state.message}</div>)
						  : null
					  }
					  <h1>Add an Integration</h1>
					  <div className="social-container">
						  <div className={`social messenger ${this.state.integration == "messenger" ? 'selected' : ''}`} onClick={(e) => this.setIntegration("messenger")}><i className="fab fa-facebook-messenger"></i></div>
						  <div className={`social twitter ${this.state.integration == "twitter" ? 'selected' : ''}`} onClick={(e) => this.setIntegration("twitter")}><i className="fab fa-twitter"></i></div>
					  </div>
					  { (this.state.integration && this.state.integration == "twitter") ?
						  this.renderTwitterForm() :
						  this.renderMessengerForm()
					  }
					  <button onClick={this.submitClicked}>Add Integration</button>
				  </div>
				</div>
		  </div>
		);
	}

}

export default App;
