import React, {Component} from 'react';
import './App.css';
import Registration from './components/auth/Registration'
import Login from './components/auth/Login'
import UserHomepage from './components/UserHomepage'

export default class App extends Component {

  constructor(props) {
    super(props)
    this.state = {
      current_user_token: null,
      current_username: null
    }
    this.onLogin = this.onLogin.bind(this);
    this.logOut = this.logOut.bind(this);
  }

  onLogin(token, username) {
    this.setState({
      current_user_token: token,
      current_username: username
    })
  }

  logOut() {
    this.setState({
      current_user_token: null,
      current_username: null
    })
  }

  render() {
    if (this.state.current_user_token === null) {
      return (
        <div>
        <Login onSuccess={this.onLogin}/>
        <Registration/>
        </div>
      );
    }
    return (
      <div>
        <h1>Welcome, {this.state.current_username}</h1>
        <UserHomepage token={this.state.current_user_token} />
        <button onClick={this.logOut}>Logout</button>
    </div>
    )
  }
}
