# Personalized Calendar App

This is a Streamlit-based calendar application that allows users to manage their routine and uncommon actions, and get AI-powered guidance based on their schedule.

## Setup

1. Clone this repository.
2. Install the required packages:
`pip install -r requirements.txt`


3. Set up your OpenAI API key in the `.env` file.

## Running the App

To run the app, use the following command:

`streamlit run app/main.py`


## Running Tests

To run the tests, use the following command:
`python -m unittest discover tests`


## Project Structure

- `app/`: Contains the main Streamlit application.
- `models/`: Contains the data models for the calendar and actions.
- `utils/`: Contains utility functions, including LLM integration.
- `tests/`: Contains unit tests for the application.

## Features

- Add routine and uncommon actions to your calendar.
- View scheduled actions for any given date.
- Get AI-powered guidance based on your calendar.

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.