"""
Publish-Subscribe Event MessageBus with topic and tag-based filtering.
Enables decoupled, asynchronous communication between 80+ specialized agents.
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Set, Optional, Callable, Any
from core.bus.models import EventMessage


class Subscription:
    """Represents an agent's active filter and queue on the bus."""
    def __init__(self, agent_id: str, topics: Set[str], tags: Set[str], callback: Optional[Callable] = None):
        self.agent_id = agent_id
        self.topics = topics
        self.tags = tags
        self.callback = callback
        self.queue: asyncio.Queue = asyncio.Queue()

    def matches(self, message: EventMessage) -> bool:
        """Check if message matches topic, tags, or direct targeting."""
        # 1. Direct recipient check
        if message.target_agent_id:
            return message.target_agent_id == self.agent_id

        # 2. Topic wildcard match (e.g. "engineering.*" or "engineering.spec")
        topic_match = False
        if not self.topics or "*" in self.topics:
            topic_match = True
        else:
            for t in self.topics:
                if t == message.topic or (t.endswith(".*") and message.topic.startswith(t[:-2])):
                    topic_match = True
                    break

        # 3. Tag intersection match
        tag_match = True
        if self.tags:
            tag_match = bool(self.tags.intersection(message.tags))

        return topic_match and tag_match


class MessageBus:
    """
    Central Pub-Sub Message Bus for multi-agent events.
    """

    def __init__(self):
        self._subscriptions: Dict[str, Subscription] = {}
        self._history: List[EventMessage] = []
        self._lock = asyncio.Lock()

    def subscribe(
        self,
        agent_id: str,
        topics: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        callback: Optional[Callable] = None
    ) -> Subscription:
        """Register an agent subscription with specific topic and tag filters."""
        sub = Subscription(
            agent_id=agent_id,
            topics=set(topics or []),
            tags=set(tags or []),
            callback=callback
        )
        self._subscriptions[agent_id] = sub
        return sub

    def unsubscribe(self, agent_id: str) -> None:
        """Remove an agent subscription."""
        self._subscriptions.pop(agent_id, None)

    async def publish(self, message: EventMessage) -> int:
        """
        Broadcast an event message to all matching subscribers.
        Returns the number of subscribers that received the event.
        """
        async with self._lock:
            self._history.append(message)

        delivered_count = 0
        for sub in self._subscriptions.values():
            if sub.matches(message):
                await sub.queue.put(message)
                delivered_count += 1
                if sub.callback:
                    if asyncio.iscoroutinefunction(sub.callback):
                        asyncio.create_task(sub.callback(message))
                    else:
                        sub.callback(message)

        return delivered_count

    async def pull(self, agent_id: str, timeout: float = 5.0) -> Optional[EventMessage]:
        """Pull the next matching event from an agent's queue with timeout."""
        sub = self._subscriptions.get(agent_id)
        if not sub:
            return None
        try:
            return await asyncio.wait_for(sub.queue.get(), timeout=timeout)
        except asyncio.TimeoutError:
            return None

    def pull_nowait(self, agent_id: str) -> List[EventMessage]:
        """Drain and return all queued events for an agent without blocking."""
        sub = self._subscriptions.get(agent_id)
        if not sub:
            return []
        messages = []
        while not sub.queue.empty():
            messages.append(sub.queue.get_nowait())
        return messages

    def get_history(
        self,
        topic: Optional[str] = None,
        tag: Optional[str] = None,
        sender_id: Optional[str] = None
    ) -> List[EventMessage]:
        """Query historical event stream."""
        results = self._history
        if topic:
            results = [m for m in results if m.topic == topic]
        if tag:
            results = [m for m in results if tag in m.tags]
        if sender_id:
            results = [m for m in results if m.sender_id == sender_id]
        return results

    def clear(self) -> None:
        """Reset bus state and drained queues."""
        self._subscriptions.clear()
        self._history.clear()


# Global Singleton Message Bus
GLOBAL_MESSAGE_BUS = MessageBus()
