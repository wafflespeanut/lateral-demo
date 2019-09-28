import React from 'react';
import './App.css';

interface FormState {
  text: string;
  disabled: boolean;
  results: string[];
}

export default class App extends React.Component {

  state: FormState = {
    text: '',
    disabled: false,
    results: [],
  };

  render() {
    return (
      <div className="App">
        <div className="App-body">
          <form onSubmit={(e) => this.handleSubmit(e)}>
            <p>Add keywords to get similar recommendations.</p>
            <input disabled={this.state.disabled}
              onChange={(e) => this.handleChange(e)}
              value={this.state.text} />
            <button disabled={this.state.disabled}>Suggest</button>
          </form>
          <ul>
            {this.state.results.length > 0 &&
              this.state.results.map((s) =>
                <li>{s}</li>
              )
            }
          </ul>
        </div>
      </div>
    );
  }

  private handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    this.setState({ disabled: true });
  }

  private handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    this.setState({ text: e.target.value });
  }
}
