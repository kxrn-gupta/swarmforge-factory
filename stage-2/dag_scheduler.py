"""
Stage 2: Deterministic DAG Scheduler & Parallel Wave Dispatcher.
Organizes task nodes into execution waves where tasks with zero pending dependencies run in parallel.
"""
from typing import List, Dict, Set, Any
import collections

class DAGScheduler:
    def __init__(self, tasks: List[Dict[str, Any]]):
        self.tasks = {t["id"]: t for t in tasks}
        self.graph: Dict[str, Set[str]] = collections.defaultdict(set)
        self.in_degree: Dict[str, int] = {t["id"]: 0 for t in tasks}
        self._build_graph()

    def _build_graph(self):
        for task_id, task_data in self.tasks.items():
            for dep in task_data.get("dependencies", []):
                if dep in self.tasks:
                    self.graph[dep].add(task_id)
                    self.in_degree[task_id] += 1

    def compute_parallel_waves(self) -> List[List[str]]:
        """
        Computes wave groups using Kahn's topological sorting algorithm.
        Each wave contains task IDs that can execute concurrently without race conditions.
        """
        in_deg = dict(self.in_degree)
        current_wave = [t_id for t_id, deg in in_deg.items() if deg == 0]
        waves = []

        while current_wave:
            waves.append(sorted(current_wave))
            next_wave = []
            for node in current_wave:
                for neighbor in self.graph[node]:
                    in_deg[neighbor] -= 1
                    if in_deg[neighbor] == 0:
                        next_wave.append(neighbor)
            current_wave = next_wave

        total_scheduled = sum(len(w) for w in waves)
        if total_scheduled != len(self.tasks):
            raise ValueError("Cyclic dependency detected in task plan graph.")

        return waves

    def execute_mock_wave_simulation(self) -> Dict[str, Any]:
        """Simulates parallel wave execution with timing and seat assignment."""
        waves = self.compute_parallel_waves()
        execution_log = []
        
        for wave_idx, wave in enumerate(waves, start=1):
            wave_tasks = [self.tasks[tid] for tid in wave]
            execution_log.append({
                "wave_index": wave_idx,
                "parallel_tasks": len(wave),
                "tasks": [
                    {"id": t["id"], "name": t["name"], "seat": t["seat"], "status": "COMPLETED"}
                    for t in wave_tasks
                ]
            })

        return {
            "total_waves": len(waves),
            "total_tasks": len(self.tasks),
            "waves_executed": execution_log,
            "status": "SUCCESS"
        }
