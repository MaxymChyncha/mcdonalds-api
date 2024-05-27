# McDonald's API 🍔🍟

This API helps you get the newest McDonald's Menu and check all the information about positions.

## Features
- **Parse up-to-date information**: Receive information about Menu directly from the official [site](https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html)
- **Save information with JSON**: Save all information in JSON format with possibility to change it in future very easy.
- **Asynchronous API**: Use fully asynchronous API to make user experience faster.
- **Easy Setup**: Make your project ready to start using only two commands.

## Tools and Technologies Used

* Programming language: `Python`
* Parsing tool: `Selenium`
* App framework: `FastAPI`
* Database: `SQLite`, `SQLAlchemy`

## Installation

To clone this project from GitHub, follow these steps:

1. **Open your terminal or command prompt.**
2. **Navigate to the directory where you want to clone the project.**
3. **Run the following commands:**
```shell
git clone https://github.com/MaxymChyncha/mcdonalds-api
python -m venv venv
source venv/bin/activate  #for Windows use: venv\Scripts\activate
```

4. **Install requirements:**

```shell
pip install -r requirements.txt
```

5. **Run Parser:**
```shell
python parser/main.py
```

6. **Run App:**
```shell
python app.py
```

## Files Structure

- `app.py`: module for running project
- `database/`: Package with Database settings
- `menu/`: Package with settings for FastAPI
- `parser/`: Package with settings for parsing and writing data
