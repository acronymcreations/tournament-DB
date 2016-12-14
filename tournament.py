#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect(f,*args):
    def new_connection(*args):
        db = psycopg2.connect("dbname=tournament")
        result = f(db,*args)
        db.commit()
        db.close()
        return result
    return new_connection


@connect
def deleteMatches(db):
    """Remove all the match records from the database."""
    c = db.cursor()
    c.execute("TRUNCATE matches")
    c.execute("Update players set wins = 0, matches = 0")


@connect
def deletePlayers(db):
    """Remove all the player records from the database."""
    c = db.cursor()
    c.execute("TRUNCATE players")


@connect
def countPlayers(db):
    """Returns the number of players currently registered."""
    c = db.cursor()
    c.execute("select count(*) from players")
    result = c.fetchone()
    return result[0]


@connect
def registerPlayer(db,name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    c = db.cursor()
    c.execute("Insert into players (name,wins,matches) Values (%s,0,0)",(bleach.clean(name),))


@connect
def playerStandings(db):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    c = db.cursor()
    c.execute("Select * from players order by wins desc")
    results = c.fetchall()
    return results


@connect
def reportMatch(db, winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    c = db.cursor()
    c.execute("Update players set wins = wins + 1, matches = matches + 1 where id = %s",(bleach.clean(winner),))
    c.execute("Update players set matches = matches + 1 where id = %s",(bleach.clean(loser),))

 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

# registerPlayer('John')
# registerPlayer('Jack')
# registerPlayer('Bill')
# registerPlayer('Matt')

# num = countPlayers()
# print 'from main ',num
# deletePlayers()
# countPlayers()
# reportMatch(14,15)
# reportMatch(16,17)
# reportMatch(14,16)
# reportMatch(15,17)
# playerStandings()






