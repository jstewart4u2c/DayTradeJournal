**Steps for Deployment**
1. Install <a href="https://www.python.org/downloads/" target="_blank">Python 3.10+</a> and your Python IDE of choice (I recommend <a href="https://www.jetbrains.com/pycharm/download/?section=windows" target="_blank">PyCharm</a>)
2. Clone the repository and open the DayTradeJournal project in PyCharm (ensure you open the overall project folder that contains the .git, DayTradeJournal, node_modules, etc).
3. Enter the hotkey Alt+F12 to open terminal or click the terminal button on the bottom of the left side toolbar.
4. Within the terminal, enter "python -m venv env" to create a virtual environment. You should see a new env folder appear in the directory.
5. Activate the virtual environment by entering ".\env\Scripts\activate"
6. Install Django within the env by entering "pip install django"
7. Once Django installation is complete, enter "cd DayTradeJournal" and then enter "python manage.py runserver"
8. Click the local server in your terminal (should look like http://127.0.0.1:8000/ or similar) and the project should open in your default browser!
