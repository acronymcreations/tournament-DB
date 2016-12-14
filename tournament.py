#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect(f, *args):
    def new_connection(*args):
        """Connects to the database and creates a cursor.  The coursor is
        then passed to the function it decorates.  After the function call,
        all changes are commited to the database and the connection is
        closed."""
        db = psycopg2.connect("dbname=tournament")
        c = db.cursor()
        result = f(c, *args)
        db.commit()
        db.close()
        return result
    return new_connection


@connect
def deleteMatches(c):
    """Remove all the match records from the database."""
    c.execute("TRUNCATE matches")
    c.execute("Update players set wins = 0, matches = 0")


@connect
def deletePlayers(c):
    """Remove all the player records from the database."""
    c.execute("TRUNCATE players")


@connect
def countPlayers(c):
    """Returns the number of players currently registered."""
    c.execute("select count(*) from players")
    result = c.fetchone()
    return result[0]


@connect
def registerPlayer(c, name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    c.execute("Insert into players (name,wins,matches) Values (%s,0,0)",
              (bleach.clean(name),))


@connect
def playerStandings(c):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    c.execute("Select * from players order by wins desc")
    results = c.fetchall()
    return results


@connect
def reportMatch(c, winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    c.execute("Update players set wins = wins + 1, ' \
              'matches = matches + 1 where id = %s",
              (bleach.clean(winner),))
    c.execute("Update players set matches = matches + 1 where id = %s",
              (bleach.clean(loser),))
    c.execute("Insert into matches (winner,loser) Values (%s,%s)",
              ((bleach.clean(winner),), (bleach.clean(loser),)))


@connect
def havePlayed(c, id1, id2):
    """Returns True if the two players have competed against eachother already,
    otherwise returns False.

    Args:
      id1: the id number of player 1
      id2: the id number of player 2

    Returns:
      True if player 1 and player 2 have competed against eachother,
      False if they have not.

    """
    command = "Select * from matches where winner = %s and ' \
              'loser = %s or winner = %s and loser = %s" % (id1, id2, id2, id1)
    c.execute(command)
    if c.fetchone():
        return True
    else:
        return False


@connect
def swissPairings(c):
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
    c.execute("Select * from players order by wins desc, matches desc, id asc")
    results = c.fetchall()
    black = []
    white = []
    for r in results[::2]:
        black.append(r)
    for r in results[1::2]:
        white.append(r)
    for i in range(0, len(black), 1):
        if havePlayed(black[i][0], white[i][0]):
            if i == len(black) - 1:
                white[i], white[i - 1] = white[i - 1], white[i]
            else:
                white[i], white[i + 1] = white[i + 1], white[i]
    zipped = zip([x[0] for x in black],
                 [x[1] for x in black],
                 [x[0] for x in white],
                 [x[1] for x in white])
    return zipped
