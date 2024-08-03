"""source code file with code focusing on small-talk-like reflective and dynamic recursive introspection core data structure which demonstrates the properties of homoiconicity and nominative atomic python 3.12 standard lib forzen slotted dataclass with pub/sub pattern."""
from dataclasses import dataclass, field, fields
from typing import Any, Callable, Dict, List, Optional, Type

@dataclass(frozen=True, slots=True)
class ReflectiveNode:
    name: str
    value: Any = None
    children: List['ReflectiveNode'] = field(default_factory=list)
    subscribers: List[Callable[['ReflectiveNode'], None]] = field(default_factory=list, compare=False)

    def add_child(self, child: 'ReflectiveNode') -> 'ReflectiveNode':
        new_children = self.children + [child]
        new_node = self._replace(children=new_children)
        self._notify_subscribers(new_node)
        return new_node

    def update_value(self, new_value: Any) -> 'ReflectiveNode':
        new_node = self._replace(value=new_value)
        self._notify_subscribers(new_node)
        return new_node

    def subscribe(self, callback: Callable[['ReflectiveNode'], None]) -> 'ReflectiveNode':
        new_subscribers = self.subscribers + [callback]
        new_node = self._replace(subscribers=new_subscribers)
        return new_node

    def _replace(self, **changes) -> 'ReflectiveNode':
        field_dict = {f.name: getattr(self, f.name) for f in fields(self)}
        field_dict.update(changes)
        return ReflectiveNode(**field_dict)

    def _notify_subscribers(self, new_node: 'ReflectiveNode'):
        for subscriber in self.subscribers:
            subscriber(new_node)

    def introspect(self) -> Dict[str, Any]:
        return {f.name: getattr(self, f.name) for f in fields(self)}

# Example usage
def print_node(node: ReflectiveNode):
    print(f"Node {node.name} updated to value {node.value}")

root = ReflectiveNode(name="root")
root = root.subscribe(print_node)
child1 = ReflectiveNode(name="child1", value=42)
root = root.add_child(child1)
root = root.update_value("new_root_value")