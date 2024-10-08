# Betting Football Site

Simple betting site project made with flask

# Features
- User authentication(register and login)
- Integration with [FD](https://www.football-data.org)
- Filtering matches by days and competition
- View of individual competitions showing information about where they takes places,their emlem, matches, standings and top players
- Each match can be viewed separately, with information presentedabout the last matches of the two teams against each other and their ranking in the competition to which the match itself belongs
- Each team can be viewed, with information on which competitions they are in, who their coach is, stadium, their past and upcoming matches and players in the team
- Option to bet on matches
- Viewing bets
- Drawing 5 numbers from 1 to 35 once a week and each user can try to guess the next numbers
- Depositing and Withdrawing (it's not with real money, just a simulation)


# Instructions to run the application
- Download the source code/clone the repository
- Navigate to main project's directory
- Create a virtual environment in the main directory `python -m venv .venv` and activate it `.\venv\Scripts\Activate.ps1`(Optional)
- Install dependencies. Run `pip install -r requirements.txt`
- Run the application using `python app.py`