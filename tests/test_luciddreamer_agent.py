"""
Tests for luciddreamer_agent.
"""

from datetime import date, datetime

import pytest

from luciddreamer_agent import (
    LucidDreamerAgent,
    DreamEntry,
    DreamMood,
    DreamMood,
    SleepQuality,
    SleepSession,
    TriggerType,
    LucidTrigger,
)


class TestDreamEntry:
    def test_record_dream_basic(self):
        agent = LucidDreamerAgent()
        dream = agent.record_dream(
            title="Test Dream",
            description="A simple test dream.",
        )
        assert dream.title == "Test Dream"
        assert dream.lucid is False
        assert dream.lucidity_level == 0

    def test_record_lucid_dream(self):
        agent = LucidDreamerAgent()
        dream = agent.record_dream(
            title="Flying Dream",
            description="I flew over mountains.",
            lucidity_level=2,
        )
        assert dream.lucid is True
        assert dream.lucidity_level == 2

    def test_dream_entry_to_from_dict(self):
        entry = DreamEntry(
            title="JSON Test",
            description="Testing serialization",
            mood=DreamMood.MYSTERIOUS,
        )
        data = entry.to_dict()
        restored = DreamEntry.from_dict(data)
        assert restored.title == entry.title
        assert restored.mood == entry.mood


class TestSleepSession:
    def test_record_sleep_session(self):
        agent = LucidDreamerAgent()
        session = agent.record_sleep(
            sleep_date=date(2024, 1, 15),
            quality=SleepQuality.AVERAGE,
        )
        assert session.date == date(2024, 1, 15)
        assert session.quality == SleepQuality.AVERAGE
        assert session.dream_count == 0

    def test_sleep_hours_calculation(self):
        agent = LucidDreamerAgent()
        session = agent.record_sleep(
            sleep_date=date(2024, 1, 15),
            bedtime=datetime(2024, 1, 15, 23, 0),
            wake_time=datetime(2024, 1, 16, 7, 0),
        )
        assert session.total_sleep_hours == 8.0


class TestTriggers:
    def test_register_trigger(self):
        agent = LucidDreamerAgent()
        trigger = agent.register_trigger(
            name="MILD",
            trigger_type=TriggerType.MILD,
            description="Mnemonic induction",
            default_effectiveness=0.5,
        )
        assert trigger.name == "MILD"
        assert trigger.trigger_type == TriggerType.MILD
        assert trigger.times_used == 0

    def test_record_trigger_attempt(self):
        agent = LucidDreamerAgent()
        agent.register_trigger("WBTB", TriggerType.WBTB)
        agent.record_trigger_attempt("WBTB", lucid_achieved=True)
        agent.record_trigger_attempt("WBTB", lucid_achieved=False)

        found = None
        for t in agent.triggers:
            if t.name == "WBTB":
                found = t
                break
        assert found is not None
        assert found.times_used == 2
        assert found.times_lucid == 1
        assert found.success_rate == 0.5

    def test_suggest_triggers(self):
        agent = LucidDreamerAgent()
        agent.register_trigger("WBTB", TriggerType.WBTB)
        agent.register_trigger("MILD", TriggerType.MILD)

        agent.record_trigger_attempt("WBTB", lucid_achieved=True)
        agent.record_trigger_attempt("WBTB", lucid_achieved=True)
        agent.record_trigger_attempt("WBTB", lucid_achieved=True)

        agent.record_trigger_attempt("MILD", lucid_achieved=True)

        suggested = agent.suggest_triggers()
        assert suggested[0].name == "WBTB"


class TestDreamSigns:
    def test_dream_sign_tracking(self):
        agent = LucidDreamerAgent()
        agent.record_dream(
            title="D1",
            description="...",
            dream_signs=["falling", "water"],
        )
        agent.record_dream(
            title="D2",
            description="...",
            dream_signs=["falling", "chase"],
        )
        top = agent.get_top_dream_signs()
        assert top[0] == ("falling", 2)
        assert top[1] == ("water", 1)


class TestStatistics:
    def test_statistics(self):
        agent = LucidDreamerAgent()
        agent.record_dream("D1", "Non-lucid dream.", lucidity_level=0)
        agent.record_dream("D2", "Lucid dream!", lucidity_level=2)
        agent.record_dream("D3", "Another lucid.", lucidity_level=1)

        stats = agent.get_statistics()
        assert stats["total_dreams"] == 3
        assert stats["total_lucid_dreams"] == 2
        assert stats["lucid_dream_rate"] == pytest.approx(2 / 3, rel=1e-2)


class TestExportImport:
    def test_export_import_json(self):
        agent = LucidDreamerAgent()
        agent.record_dream("Dream A", "Description A", mood=DreamMood.JOYFUL)
        agent.record_sleep(date(2024, 2, 1), quality=SleepQuality.RESTFUL)

        exported = agent.export_json()
        agent2 = LucidDreamerAgent()
        agent2.import_json(exported)

        assert agent2.sessions[0].date == date(2024, 2, 1)
        assert len(agent2.sessions[0].dreams) == 1
