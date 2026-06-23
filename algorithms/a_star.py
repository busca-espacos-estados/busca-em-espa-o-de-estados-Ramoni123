import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan — heurística admissível para o 8-puzzle."""
        distance = 0
        for i, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            goal_i = tile - 1  # tile t pertence à posição t-1 no estado objetivo
            distance += abs(i // 3 - goal_i // 3) + abs(i % 3 - goal_i % 3)
        return distance

    def search(self, initial: State) -> SearchResult:
        counter = 0
        frontier = [(self.heuristic(initial), counter, initial)]
        explored = set()
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            _, _, node = heapq.heappop(frontier)

            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=node.cost,
                )

            if node in explored:
                continue

            explored.add(node)
            nodes_expanded += 1

            for neighbor in node.neighbors():
                nodes_generated += 1
                if neighbor not in explored:
                    counter += 1
                    f = neighbor.cost + self.heuristic(neighbor)
                    heapq.heappush(frontier, (f, counter, neighbor))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )
