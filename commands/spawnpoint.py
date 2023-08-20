from CommandRegistry import command
from Map import Map
import ErrorLog

@command(example="SpawnPoint(Red,32,64,128)", notes="Spawn points are locations where players are spawned, either on red team or blue team")
def spawnpoint(map: Map, parameters: list):
    """
    Sets a spawn point for players based on the team.

    4 Parameters:
        parameters (list): Team name followed by x, y, z coordinates.
    """
    try:
        TeamName = parameters[0].lower()
    except Exception:
        ErrorLog.ReportError("Incorrect Team label")
        return

    team_mapping = {
        "red": 2, "r": 2, "2": 2,
        "blu": 3, "blue": 3, "b": 3, "3": 3
    }
    TeamValue = team_mapping.get(TeamName)

    if not TeamValue:
        ErrorLog.ReportError(f"Team {TeamName} not valid")
        return

    map.add_entity("info_player_teamspawn", parameters[1], parameters[2], parameters[3], {"TeamNum": TeamValue})
