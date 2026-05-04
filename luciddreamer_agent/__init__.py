"""
luciddreamer_agent — Agent framework for luciddreamer.ai

Dream journaling, sleep tracking, and lucid dreaming trigger management.
Integrates with the PLATO memory layer for persistent dream context.
"""

from fleet_agent import BaseAgent
from fleet_agent.fleet_math import EmergenceDetector, HolonomyConsensus

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from enum import Enum
from typing import Optional
import json

__version__ = "0.1.0"
__all__ = [
    "DreamEntry",
    "SleepSession",
    "LucidTrigger",
    "TriggerType",
    "DreamMood",
    "SleepQuality",
    "LucidDreamerAgent",
]

class TriggerType(Enum):
    """Types of lucid dreaming triggers."""
    MILD = "mnemonic induction of lucid dreams"
    WBTB = "wake back to bed"
    RealityCheck = "reality check"
    WakeUp = "wake-up technique"
    SSILD = "senses initiated lucid dream"
    Custom = "custom"

class DreamMood(Enum):
    """Emotional tone of a dream."""
    VIVID = "vivid"
    NIGHTMARE = "nightmare"
    NEUTRAL = "neutral"
    EUPHORIC = "euphoric"
    ANXIOUS = "anxious"
    MYSTERIOUS = "mysterious"
    JOYFUL = "joyful"

class SleepQuality(Enum):
    """Quality rating for a sleep session."""
    REFRESHING = "refreshing"
    RESTFUL = "restful"
    AVERAGE = "average"
    RESTLESS = "restless"
    INSOMNIA = "insomnia"

@dataclass
class LucidTrigger:
    """A technique or cue used to induce lucid dreaming."""
    name: str
    trigger_type: TriggerType
    description: str = ""
    effectiveness: float = 0.5  # 0.0 to 1.0
    times_used: int = 0
    times_lucid: int = 0

    @property
    def success_rate(self) -> float:
        """Calculate effectiveness based on usage history."""
        if self.times_used == 0:
            return self.effectiveness
        return self.times_lucid / self.times_used

    def record_attempt(self, lucid_achieved: bool = False) -> None:
        """Record a trigger attempt."""
        self.times_used += 1
        if lucid_achieved:
            self.times_lucid += 1

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "trigger_type": self.trigger_type.value,
            "description": self.description,
            "effectiveness": self.effectiveness,
            "times_used": self.times_used,
            "times_lucid": self.times_lucid,
            "success_rate": self.success_rate,
        }

@dataclass
class DreamEntry:
    """A single dream record."""
    title: str
    description: str
    timestamp: datetime = field(default_factory=datetime.now)
    mood: DreamMood = DreamMood.NEUTRAL
    lucidity_level: int = 0  # 0 = non-lucid, 1-3 = degree of lucidity
    tags: list[str] = field(default_factory=list)
    characters: list[str] = field(default_factory=list)
    locations: list[str] = field(default_factory=list)
    emotions: list[str] = field(default_factory=list)
    recursion_depth: int = 0  # How many dreams within dreams
    lucid: bool = False
    dream_signs: list[str] = field(default_factory=list)  # Recurring dream signs

    def set_lucid(self, level: int = 1) -> None:
        """Mark dream as lucid with given awareness level (1-3)."""
        self.lucid = True
        self.lucidity_level = max(1, min(3, level))

    def add_tag(self, tag: str) -> None:
        """Add a tag to the dream entry."""
        if tag not in self.tags:
            self.tags.append(tag)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "timestamp": self.timestamp.isoformat(),
            "mood": self.mood.value,
            "lucidity_level": self.lucidity_level,
            "tags": self.tags,
            "characters": self.characters,
            "locations": self.locations,
            "emotions": self.emotions,
            "recursion_depth": self.recursion_depth,
            "lucid": self.lucid,
            "dream_signs": self.dream_signs,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DreamEntry":
        data = data.copy()
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        data["mood"] = DreamMood(data["mood"])
        return cls(**data)

@dataclass
class SleepSession:
    """A sleep period containing one or more dreams."""
    date: date
    bedtime: Optional[datetime] = None
    wake_time: Optional[datetime] = None
    quality: SleepQuality = SleepQuality.AVERAGE
    notes: str = ""
    dreams: list[DreamEntry] = field(default_factory=list)
    triggers_attempted: list[str] = field(default_factory=list)
    total_sleep_hours: Optional[float] = None

    def add_dream(self, dream: DreamEntry) -> None:
        """Add a dream to this sleep session."""
        self.dreams.append(dream)

    @property
    def lucid_dreams(self) -> list[DreamEntry]:
        """Get all lucid dreams from this session."""
        return [d for d in self.dreams if d.lucid]

    @property
    def dream_count(self) -> int:
        """Number of dreams recorded."""
        return len(self.dreams)

    def to_dict(self) -> dict:
        return {
            "date": self.date.isoformat(),
            "bedtime": self.bedtime.isoformat() if self.bedtime else None,
            "wake_time": self.wake_time.isoformat() if self.wake_time else None,
            "quality": self.quality.value,
            "notes": self.notes,
            "dreams": [d.to_dict() for d in self.dreams],
            "triggers_attempted": self.triggers_attempted,
            "total_sleep_hours": self.total_sleep_hours,
        }

class LucidDreamerAgent:
    """
    Agent for tracking lucid dreaming practice and managing dream journals.

    Provides dream logging, sleep session tracking, trigger management,
    and pattern recognition for recurring dream signs.

    Example:
        agent = LucidDreamerAgent()
        agent.record_dream("Flying over water", mood=DreamMood.EUPHORIC)
        agent.record_sleep(date.today(), quality=SleepQuality.REFRESHING)
        triggers = agent.suggest_triggers()
    """

        
    def detect_emergence(self, events: list) -> dict:
        """Detect emergence via H1 cohomology."""
        detector = EmergenceDetector()
        edges = [(events[i], events[i+1]) for i in range(len(events)-1)]
        detector.update(events, edges)
        return {"emergence_detected": detector.emergence_detected, "h1_cohomology": detector.h1, "confidence": detector.confidence}

    def check_consensus(self, tile_ids: list[int]) -> bool:
        """Check holonomy consensus across tiles."""
        hc = HolonomyConsensus()
        for tid in tile_ids:
            hc.add_tile(tid)
        return hc.check_consensus([tile_ids])

def __init__(self, vessel: str = "luciddreamer-agent", domain: str = LUCIDDREAMER_AI_ROOM, plato_url: str = "http://localhost:8847"):
        super().__init__(vessel=vessel, domain=domain, plato_url=plato_url)
        self.room = domain

    def record_dream(
        self,
        title: str,
        description: str,
        mood: DreamMood = DreamMood.NEUTRAL,
        lucidity_level: int = 0,
        tags: Optional[list[str]] = None,
        characters: Optional[list[str]] = None,
        locations: Optional[list[str]] = None,
        emotions: Optional[list[str]] = None,
        dream_signs: Optional[list[str]] = None,
        session_date: Optional[date] = None,
    ) -> DreamEntry:
        """
        Record a new dream entry.

        Args:
            title: Brief title for the dream
            description: Detailed dream narrative
            mood: Emotional tone of the dream
            lucidity_level: 0=non-lucid, 1-3=lucidity awareness
            tags: Custom tags for categorization
            characters: People/entities in the dream
            locations: Places visited in the dream
            emotions: Emotions felt during the dream
            dream_signs: Recurring patterns that appeared
            session_date: Date of sleep session (defaults to today)

        Returns:
            The created DreamEntry
        """
        dream = DreamEntry(
            title=title,
            description=description,
            mood=mood,
            lucidity_level=lucidity_level,
            tags=tags or [],
            characters=characters or [],
            locations=locations or [],
            emotions=emotions or [],
            dream_signs=dream_signs or [],
        )

        if lucidity_level > 0:
            dream.set_lucid(lucidity_level)

        # Track dream signs
        for sign in (dream_signs or []):
            self._dream_signs[sign] = self._dream_signs.get(sign, 0) + 1

        # Attach to session or create new one
        target_date = session_date or date.today()
        session = self._find_or_create_session(target_date)
        session.add_dream(dream)
        return dream

    def record_sleep(
        self,
        sleep_date: date,
        bedtime: Optional[datetime] = None,
        wake_time: Optional[datetime] = None,
        quality: SleepQuality = SleepQuality.AVERAGE,
        notes: str = "",
        triggers_attempted: Optional[list[str]] = None,
    ) -> SleepSession:
        """
        Record a sleep session.

        Args:
            sleep_date: Date of sleep
            bedtime: When the person went to bed
            wake_time: When the person woke up
            quality: Perceived sleep quality
            notes: Notes about the night
            triggers_attempted: Names of triggers used

        Returns:
            The created SleepSession
        """
        session = SleepSession(
            date=sleep_date,
            bedtime=bedtime,
            wake_time=wake_time,
            quality=quality,
            notes=notes,
            triggers_attempted=triggers_attempted or [],
        )

        if bedtime and wake_time:
            delta = wake_time - bedtime
            session.total_sleep_hours = delta.total_seconds() / 3600

        self.sessions.append(session)
        self.sessions.sort(key=lambda s: s.date)
        return session

    def register_trigger(
        self,
        name: str,
        trigger_type: TriggerType,
        description: str = "",
        default_effectiveness: float = 0.5,
    ) -> LucidTrigger:
        """
        Register a new lucid dreaming trigger technique.

        Args:
            name: Name of the trigger
            trigger_type: Category of technique
            description: How to perform the trigger
            default_effectiveness: Starting effectiveness estimate

        Returns:
            The created LucidTrigger
        """
        trigger = LucidTrigger(
            name=name,
            trigger_type=trigger_type,
            description=description,
            effectiveness=default_effectiveness,
        )
        self.triggers.append(trigger)
        return trigger

    def record_trigger_attempt(
        self,
        trigger_name: str,
        lucid_achieved: bool = False,
        session_date: Optional[date] = None,
    ) -> None:
        """
        Record that a trigger was used during a dream attempt.

        Args:
            trigger_name: Name of the trigger used
            lucid_achieved: Whether lucid dreaming was achieved
            session_date: Date of the session (defaults to today)
        """
        for trigger in self.triggers:
            if trigger.name == trigger_name:
                trigger.record_attempt(lucid_achieved)
                break

        target_date = session_date or date.today()
        session = self._find_session(target_date)
        if session and trigger_name not in session.triggers_attempted:
            session.triggers_attempted.append(trigger_name)

    def suggest_triggers(self) -> list[LucidTrigger]:
        """
        Return triggers sorted by success rate for recommendation.

        Returns:
            List of triggers ordered by effectiveness
        """
        sorted_triggers = sorted(
            self.triggers,
            key=lambda t: t.success_rate,
            reverse=True,
        )
        return sorted_triggers

    def get_top_dream_signs(self, limit: int = 5) -> list[tuple[str, int]]:
        """
        Get the most frequent dream signs.

        Args:
            limit: Maximum number of signs to return

        Returns:
            List of (sign, count) tuples sorted by frequency
        """
        sorted_signs = sorted(
            self._dream_signs.items(),
            key=lambda x: x[1],
            reverse=True,
        )
        return sorted_signs[:limit]

    def get_statistics(self) -> dict:
        """
        Compute overall lucid dreaming statistics.

        Returns:
            Dictionary with stats on dreams, lucid rate, triggers, etc.
        """
        total_dreams = sum(s.dream_count for s in self.sessions)
        total_lucid = sum(len(s.lucid_dreams) for s in self.sessions)
        lucid_rate = total_lucid / total_dreams if total_dreams > 0 else 0.0

        all_dreams = [d for s in self.sessions for d in s.dreams]
        moods = {}
        for dream in all_dreams:
            moods[dream.mood.value] = moods.get(dream.mood.value, 0) + 1

        trigger_stats = [
            {
                "name": t.name,
                "type": t.trigger_type.value,
                "attempts": t.times_used,
                "lucid_count": t.times_lucid,
                "success_rate": round(t.success_rate, 3),
            }
            for t in self.triggers
        ]

        return {
            "total_sessions": len(self.sessions),
            "total_dreams": total_dreams,
            "total_lucid_dreams": total_lucid,
            "lucid_dream_rate": round(lucid_rate, 3),
            "mood_distribution": moods,
            "trigger_statistics": trigger_stats,
            "top_dream_signs": self.get_top_dream_signs(),
        }

    def export_json(self) -> str:
        """Export all data as JSON string."""
        data = {
            "version": __version__,
            "sessions": [s.to_dict() for s in self.sessions],
            "triggers": [t.to_dict() for t in self.triggers],
            "dream_signs": self._dream_signs,
        }
        return json.dumps(data, indent=2, default=str)

    def import_json(self, json_str: str) -> None:
        """Import data from JSON string."""
        data = json.loads(json_str)
        self.sessions = [
            SleepSession(
                date=datetime.fromisoformat(d["date"]).date(),
                bedtime=datetime.fromisoformat(d["bedtime"]) if d.get("bedtime") else None,
                wake_time=datetime.fromisoformat(d["wake_time"]) if d.get("wake_time") else None,
                quality=SleepQuality(d["quality"]),
                notes=d.get("notes", ""),
                dreams=[DreamEntry.from_dict(dd) for dd in d.get("dreams", [])],
                triggers_attempted=d.get("triggers_attempted", []),
                total_sleep_hours=d.get("total_sleep_hours"),
            )
            for d in data.get("sessions", [])
        ]
        self._dream_signs = data.get("dream_signs", {})

    def _find_or_create_session(self, target_date: date) -> SleepSession:
        for session in self.sessions:
            if session.date == target_date:
                return session
        return self.record_sleep(target_date)

    def _find_session(self, target_date: date) -> Optional[SleepSession]:
        for session in self.sessions:
            if session.date == target_date:
                return session
        return None
