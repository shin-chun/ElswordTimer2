from collections import defaultdict
from typing import Dict, Optional, Set

class GroupState:
    def __init__(self):
        self.locked_by: Optional[str] = None
        self.active_set: Set[str] = set()

class GroupStateManager:
    def __init__(self):
        self.groups: Dict[str, GroupState] = defaultdict(GroupState)

    def can_select(self, group: str, timer_id: str) -> bool:
        gs = self.groups[group]
        return gs.locked_by is None or gs.locked_by == timer_id

    def select(self, group: str, timer_id: str):
        gs = self.groups[group]
        if gs.locked_by == timer_id:
            gs.locked_by = None
            gs.active_set.discard(timer_id)
            print(f"[{group}] {timer_id} unlocked itself. Re-entering detection.")
            return
        if gs.locked_by is None:
            gs.locked_by = timer_id
            gs.active_set.add(timer_id)
            print(f"[{group}] {timer_id} locked the group.")
        else:
            print(f"[{group}] {timer_id} cannot select. Locked by {gs.locked_by}.")

    def release(self, group: str, timer_id: str):
        gs = self.groups[group]
        if gs.locked_by == timer_id:
            gs.locked_by = None
        gs.active_set.discard(timer_id)

    def is_idle(self, group: str, timer_id: str) -> bool:
        gs = self.groups[group]
        return gs.locked_by is not None and gs.locked_by != timer_id