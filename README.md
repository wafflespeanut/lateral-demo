## Lateral API demo

[![Build Status](https://api.travis-ci.org/wafflespeanut/lateral-demo.svg?branch=master)](https://travis-ci.org/wafflespeanut/lateral-demo)

A hobby project for demo'ing Lateral [news recommendation API](https://lateral.io/docs/news-recommender/reference/#news-similar-to-text-post). The frontend uses React and TypeScript whereas the backend uses Python's [Tornado](https://www.tornadoweb.org/en/stable/) through Nginx proxy. Everything's deployed and tested in an Ubuntu (18.04) server.

I'm new to both React and Tornado, but I've played with Vue and a number of web frameworks before, so I kinda have an idea of how they work. Here, I'll cover a brief summary of how I went around setting everything up, the decisions made along the way, why I preferred some choice over something else, etc.

> **NOTE:** I use `make` for building and testing locally before pushing (see `Makefile` in project root).

### Backend

I've used `pip` a number of times, but I personally like both [`pyenv`](https://github.com/pyenv/pyenv) (for toolchains) and [`pipenv`](https://github.com/pypa/pipenv/) (for packages). Pipenv is great - it offers a manifest for projects, helps with locking the deps for production deployment, allows dev/prod dependencies, constrains Python version and also respects pip's `requirements.txt`. In addition to that, I've used [`autopep8`](https://github.com/hhatto/autopep8/) for formatting and [`flake8`](https://github.com/pycqa/flake8) for linting.

The API itself has two endpoints:

 - `GET /`: Returns the (UTC) server time in a JSON message.
 - `POST /recommendations`: Accepts a JSON payload with some text in `text` parameter, sends it to Lateral API and proxies the returned documents to the client.

Tornado exports a `RequestHandler` object which should be inherited by handlers to handle requests, so the root handler is pretty straightforward. The recommendations handler however, needs to talk to Lateral API, so it needs a non-blocking HTTP client. Tornado supports async handlers and offers an async HTTP client out of the box.

That said, we cannot use the client directly, because we have to test the endpoints. So, we have an `ApiClient` base class which is inherited by both `LateralApiClient` and `TestApiClient` - the clients only expose async methods for the *business* requirements. We initialize the actual client with `API_KEY` from the environment. Tornado also supports initializing the handlers and also offers wrappers for them (inherited from `unittest.TestCase`), so it's now easy to test everything.

### Frontend

I've used [`nvm`](https://github.com/nvm-sh/nvm) for managing node versions and [ESLint](https://eslint.org/) for linting Typescript. I prefer using Typescript (personally) because of the rules it offers us to protect ourselves in Javascript realm. Python 3.x supports *some* typing, but I didn't go for it because it's way behind Typescript when it comes to type systems.

React has [`create-react-app`](https://github.com/facebook/create-react-app) (CRA) for setting up boilerplates easily - it saved time for me. CRA already offers [`jest`](https://jestjs.io/) for testing, but several articles suggested to use [`enzyme`](https://github.com/airbnb/enzyme) in addition to it, because of its simplicity in rendering and testing react DOM.

The application itself is simple enough (a form with an input and a button for user input, along with some divs for showing results), so I chose to stick with a single component (`App.*`). There's an `ApiClient` interface (similar to the one in Python) which is implemented for both `HttpApiClient` (backed by `fetch` API) and `TestApiClient` (with test data).

Now, unit tests can check whether the app has changed its state or called some function appropriately based on simulating events after rendering.

### Deployment

`deploy/setup.sh` script takes care of deploying the app in an Ubuntu server.

Nginx serves static assets and proxies Tornado API server. Since the root URL needs to serve the homepage, I've isolated the JSON API into `/api/` base path. I've used both Nginx and systemd in deployments before, but it's usually with docker. This time, I decided to go for the good ol' way of deploying everything.

The Ubuntu (18.04) server is really basic (1 GB RAM, 1 vCPU), and since we're not deploying the server for multiple domains (i.e., no need for `sites-available` and `sites-enabled`), our Nginx config is simple. I've enabled TLS because I'm deploying it to [lateral.waffles.space](https://lateral.waffles.space/) and the connection between Cloudflare and my server requires TLS.

Notable things:

- Pipenv doesn't require `requirements.txt`, but we're not using `pipenv` or `pyenv` in the server. Instead, we use the stable version with `pip` and `virtualenv`, for which we need the requirements.
- We use `nvm` for setting up the latest (LTS) version of `node`.
- We setup a virtual environment for an individual deployment of Tornado. New deployments remove old environments.
- Currently, we build the web app in the server, but they're already being built in Travis CI and we can upload it somewhere (I usually build and push to a docker registry from the CI, fetch the image from the server, spawn a container and get the assets).
- Nginx is already a systemd unit. The deployment script also sets up Tornado as a systemd unit. Whenever we re-deploy, the units are stopped, assets are updated and the units are started again.
