# Tournament Database

## Overview

This is a python code that connects to a PostgreSQL database to manage a Swiss Style Tournament.
You can add an unlimited number of players/teams to the tournament, and the database will manage
pairing opponents of equal skill based on the performance of each player/team in previous rounds.

## Running the Database

1. First you must connect to the database using the command `psql`

2. Once connected, simply run `\i tournament.sql` to create your database and all required tables

3. To check that everything is set up correctly, disconnect from the database with `\q` and then run they tournament testfile included 
using `python tournament_test.py`

4. If everything is setup correctly, you should see a checklist testing each of the functions below followed by 'Success!  All tests pass!'

## Using the Database

The following methods are available to manage your tournament:

- `registerPlayer(playerName)` Used to add players/teams to the tournament.  All players/teams should be 
added before rounds are started.

- `countPlayers()` Returns the number of registered players/teams so far.

- `playerStandings()` Returns a list of all registered players along with their ID number as well as the number of wins 
they have and the total number of matches they have played.

- `swissPairings()` Returns a list of matches that should take place based on performance in previous rounds.  
If it is the first round, players are randomly paired.  In subsequent rounds, matches are rearranged as needed to ensure 
two players/teams do not complete twice.

- `reportMatch(winnerID, loserID)` This method should be used to report the outcome of previous matches.  This should be done 
at the end of each round so that the information is available to use when generating opponents for the next round.

- `havePlayed(playerID, playerID)` This method can be used to see if to opponents have competed against each other already.

- `deletePlayers()` This method will delete all registered players.  This should only be used at the end of the tournament.

- `deleteMatches()` This method will delete all recorded match data.  This should only be used at the end of the tournament.
