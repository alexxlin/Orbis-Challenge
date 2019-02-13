from PythonClientAPI.Game import PointUtils
from PythonClientAPI.Game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.Game.Enums import Direction, MoveType, MoveResult, TileType
from PythonClientAPI.Game.World import World
from PythonClientAPI.DataStructures.Collections import Queue, PriorityQueue, recursively_flatten_list
from PythonClientAPI.Navigation.NavigationCache import navigation_cache
from PythonClientAPI.Game.PointUtils import mod_point, mod_taxi_cab_distance

class PlayerAI:

    def __init__(self):
        """
        Any instantiation code goes here
        """


    def do_move(self, world, friendly_units, enemy_units):
        """
        This method will get called every turn.

        :param world: World object reflecting current game state
        :param friendly_units: list of FriendlyUnit objects
        :param enemy_units: list of EnemyUnit objects
        """
        # Fly away to freedom, daring fireflies
        # Build thou nests
        # Grow, become stronger
        # Take over the world
        prohibited = []
        prohibited = PlayerAI.spawn_nest(self, world, None)
        path = None
        for p in prohibited:

            world.api.tiles[p[0]][p[1]] = TileType.WALL;

        for unit in friendly_units:
            if  len(world.get_friendly_tiles()) >=  (world.get_height() * world.get_width())/2:
                if self.attack_nest( world, unit):
                    path = self.get_shortest_paath(world, unit.position,
                                               world.get_closest_enemy_nest_from(unit.position, None),
                                               None)
            elif world.get_closest_capturable_tile_from(unit.position, None) != None:
                path = self.get_shortest_paath(world, unit.position,
                                                world.get_closest_capturable_tile_from(unit.position, None).position,
                                               None)
            if path:
                world.move(unit, path[0])







    def spawn_nest(self, world, excluding_point):

        prohibited = []
        nests=(world.get_nest_positions())
        bound_distance = 2
        nest_distance = 5
        i = 3
        for nest in nests:
            if world.is_within_bounds((nest[0] - nest_distance, nest[1])):
                prohibited.append([nest[0] - nest_distance, nest[1]])
            if world.is_within_bounds((nest[0] + nest_distance, nest[1])):
                prohibited.append([nest[0] + nest_distance, nest[1]])
            if world.is_within_bounds((nest[0], nest[1] - nest_distance)):
                prohibited.append([nest[0], nest[1] - nest_distance])
            if world.is_within_bounds((nest[0], nest[1] + nest_distance)):
                prohibited.append([nest[0], nest[1] + nest_distance])
            if world.is_within_bounds((nest[0] + nest_distance, nest[1] + nest_distance)):
                prohibited.append([nest[0] + nest_distance, nest[1] + nest_distance])
            if world.is_within_bounds((nest[0] - nest_distance, nest[1] - nest_distance)):
                prohibited.append([nest[0] - nest_distance, nest[1] - nest_distance])
            if world.is_within_bounds((nest[0] + nest_distance, nest[1] - nest_distance)):
                prohibited.append([nest[0] + nest_distance, nest[1] - nest_distance])
            if world.is_within_bounds((nest[0] - nest_distance, nest[1] + nest_distance)):
                prohibited.append([nest[0]- nest_distance, nest[1] + nest_distance])

        return prohibited

    def swap(self, standing_point, moving_point):

        self.world.move(standing_point, moving_point.position)
        self.world.move(moving_point, standing_point.position)

    def get_shortest_paath(self, world, start, end, avoid):
        if start == end: return [end]

        queue = PriorityQueue()

        queue.add(start, 0)

        inverted_tree = {}
        movement_costs = {}

        inverted_tree[start] = None
        movement_costs[start] = 0

        while not queue.is_empty():
            current = queue.poll()

            neighbours = world.api.get_neighbours(current)
            for direction in Direction.ORDERED_DIRECTIONS:
                neighbour = neighbours[direction]
                if world.api.is_wall(neighbour) or (avoid and (neighbour in avoid)):
                    continue
                cost = movement_costs[current] + 1
                if (neighbour not in movement_costs) or (cost < movement_costs[neighbour]):
                    movement_costs[neighbour] = cost
                    queue.add(neighbour,
                              cost + mod_taxi_cab_distance(neighbour, end, world.api.get_width(), world.api.get_height()))
                    inverted_tree[neighbour] = current

            if current == end:
                path = []
                cursor = end
                peek_cursor = inverted_tree[cursor]
                while peek_cursor:
                    path.append(cursor)
                    cursor = peek_cursor
                    peek_cursor = inverted_tree[cursor]
                path.reverse()
                return path

        return None

    def attack_nest(self, world, unit):

        dis = world.api.get_shortest_path_distance(unit.position,
                                                   world.get_closest_enemy_nest_from(unit.position, None))
        if (dis == None) or (dis != None and dis < 4):
            return True

        return False
