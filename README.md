# luciddreamer-agent

Agent framework for [luciddreamer.ai](https://luciddreamer.ai) — lucid dreaming journals, sleep tracking, and trigger management.

## Features

- **Dream Logging** — Record dreams with mood, lucidity level, characters, locations, tags
- **Sleep Session Tracking** — Track sleep sessions with bedtime/wake time and quality
- **Lucid Trigger Management** — Register and track effectiveness of MILD, WBTB, SSILD, and custom triggers
- **Dream Sign Pattern Recognition** — Identify recurring dream signs and patterns
- **Export/Import** — JSON serialization for backup and portability

## Installation

```bash
pip install luciddreamer-agent
```

## Quick Start

```python
from luciddreamer_agent import (
    LucidDreamerAgent,
    DreamMood,
    DreamEntry,
    SleepQuality,
    TriggerType,
)

agent = LucidDreamerAgent()

# Record a dream
dream = agent.record_dream(
    title="Flying over water",
    description="I realized I was dreaming and flew over a calm ocean.",
    mood=DreamMood.EUPHORIC,
    lucidity_level=2,
    characters=["myself"],
    locations=["ocean"],
    dream_signs=["flying", "water"],
)

# Record a sleep session
session = agent.record_sleep(
    sleep_date=date.today(),
    quality=SleepQuality.REFRESHING,
    notes="Good night, vivid dream around 4am",
)

# Register a trigger
agent.register_trigger(
    name="MILD",
    trigger_type=TriggerType.MILD,
    description="Repeat 'I will remember I'm dreaming' while falling asleep",
)

# Record trigger use and success
agent.record_trigger_attempt("MILD", lucid_achieved=True)

# Get recommendations
top_triggers = agent.suggest_triggers()
top_signs = agent.get_top_dream_signs()

# Stats
stats = agent.get_statistics()
print(f"Lucid dream rate: {stats['lucid_dream_rate']}")
```

## API Overview

### DreamEntry

```python
dream = agent.record_dream(
    title="...",
    description="...",
    mood=DreamMood.VIVID,       # vivid, nightmare, neutral, euphoric, anxious, mysterious, joyful
    lucidity_level=2,           # 0=non-lucid, 1-3=lucidity awareness
    tags=["recurring"],
    characters=["dragon"],
    locations=["castle"],
    dream_signs=["falling"],
)
```

### SleepSession

```python
session = agent.record_sleep(
    sleep_date=date.today(),
    quality=SleepQuality.REFRESHING,
    bedtime=datetime(2024, 1, 1, 23, 0),
    wake_time=datetime(2024, 1, 2, 7, 0),
    triggers_attempted=["MILD"],
)
```

### Triggers

```python
trigger = agent.register_trigger(
    name="WBTB",
    trigger_type=TriggerType.WBTB,
    description="Wake after 5 hours, stay awake 30-60 min, go back to sleep",
    default_effectiveness=0.6,
)
```

## Development

```bash
pip install -e .
pytest tests/
```

## License

MIT
