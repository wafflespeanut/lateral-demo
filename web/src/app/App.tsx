import React from 'react';
import './App.css';
import Recommendation from '../api/models/recommendation';
import ApiClient, { HttpApiClient } from '../api/client';

interface AppState {
  text: string;
  disabled: boolean;
  datetime: string;
  results: Recommendation<Date>[];
}

export default class App extends React.Component {

  client: ApiClient = new HttpApiClient();

  state: AppState = {
    text: '',
    datetime: '',
    disabled: false,
    results: [],
  };

  /* React hooks */

  componentDidMount() {
    this.setServerTime();
  }

  render() {
    return (
      <div className="App">
        <div className="App-body">
          <form className="formInput" onSubmit={(e) => this.handleSubmit(e)}>
            <p>Enter keywords to get similar news recommendations.</p>
            <input disabled={this.state.disabled}
              onChange={(e) => this.handleChange(e)}
              value={this.state.text} />
            <button disabled={this.state.disabled || this.state.text === ""}>Suggest</button>
          </form>
          {this.state.datetime !== '' && <p>Server time: {this.state.datetime}</p>}
          <div>
            {this.state.results.length > 0 &&
              this.state.results.map((s, i) =>
                <div key={i} className="App-result">
                  <a href={s.url}><h3>{s.title}</h3></a>
                  <small>{s.published.toDateString()}</small>
                  <p>{s.summary}</p>
                </div>
              )
            }
          </div>
        </div>
      </div>
    );
  }

  /* Event listeners */

  /** Fetches and sets time from the server. */
  private setServerTime() {
    this.client.getServerTime().then(date => {
      this.setState({ datetime: date.toUTCString() });
    });
  }

  /**
   * Handles form submission by the user by getting the list of recommendations
   * from the API and rendering it in view.
   *
   * @param e Form submit event.
   */
  private handleSubmit(evt: React.FormEvent<HTMLFormElement>) {
    evt.preventDefault();
    this.setState({ disabled: true });
    this.client.getSimilarNews(this.state.text).then(results => {
      this.setState({ results, disabled: false });
    });
  }

  /**
   * Updates the state using the user's text input.
   *
   * @param evt Input element value change event.
   */
  private handleChange(evt: React.ChangeEvent<HTMLInputElement>) {
    this.setState({ text: evt.target.value });
  }
}
