# luciddreamer-agent

A Python library for recording lucid dreaming journals, sleep sessions, and trigger techniques, with in-memory storage and JSON export/import. Data is held in process memory; persistence is via `export_json()` / `import_json()`.

## Features

- **Dream logging** — record dreams with mood, lucidity level, characters, locations, tags, and dream signs
- **Sleep session tracking** — track bedtime/wake time and quality per night
- **Trigger management** — register techniques (MILD, WBTB, SSILD, Reality Check, custom) and track success rates per attempt
- **Dream sign frequency** — count recurring dream signs and rank them by frequency
- **Statistics** — compute lucid dream rate, mood distribution, and per-trigger success rates
- **Export/import** — serialize and restore all data as JSON

## Installation

```bash
pip install luciddreamer-agent
```

## Quick Start

```python
from datetime import date

from luciddreamer_agent import (
    LucidDreamerAgent,
    DreamMood,
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

### `record_dream(...)`

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

Each dream is attached to a sleep session for the given date (created automatically if none exists). Dream signs are counted for frequency tracking.

### `record_sleep(...)`

```python
session = agent.record_sleep(
    sleep_date=date.today(),
    quality=SleepQuality.REFRESHING,
    bedtime=datetime(2024, 1, 1, 23, 0),
    wake_time=datetime(2024, 1, 2, 7, 0),
    triggers_attempted=["MILD"],
)
```

When both `bedtime` and `wake_time` are provided, `total_sleep_hours` is computed automatically.

### Triggers

```python
trigger = agent.register_trigger(
    name="WBTB",
    trigger_type=TriggerType.WBTB,
    description="Wake after 5 hours, stay awake 30-60 min, go back to sleep",
    default_effectiveness=0.6,
)
```

Each trigger's `success_rate` starts at `default_effectiveness` (before any attempts) and shifts to `times_lucid / times_used` once attempts are recorded. `suggest_triggers()` returns triggers sorted by success rate.

### `suggest_triggers()`

Returns triggers sorted by success rate (highest first). Before any attempts, the default effectiveness estimate is used.

### `get_top_dream_signs(limit=5)`

Returns `(sign, count)` tuples for the most frequently logged dream signs.

### `get_statistics()`

Returns a dict with `total_sessions`, `total_dreams`, `total_lucid_dreams`, `lucid_dream_rate`, `mood_distribution`, `trigger_statistics`, and `top_dream_signs`.

### Export / Import

```python
data = agent.export_json()   # returns JSON string
agent.import_json(data)      # restores all sessions, triggers, and dream signs
```

## Development

```bash
pip install -e .
pytest tests/
```

## License

MIT

## Related

- [luciddreamer.ai](https://luciddreamer.ai)
- [luciddreamer-ai-pages](https://github.com/SuperInstance/luciddreamer-ai-pages) — GitHub Pages source
