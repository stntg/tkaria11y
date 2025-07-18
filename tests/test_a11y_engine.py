# tests/test_a11y_engine.py

import time
from tkaria11y.a11y_engine import TTSEngine, speak, tts


def test_tts_engine_creation():
    """Test TTSEngine can be created with default parameters"""
    engine = TTSEngine()
    assert engine._rate == 150
    assert engine._volume == 1.0
    assert engine._voice_id is None
    assert not engine._started
    engine.shutdown()


def test_tts_engine_custom_parameters():
    """Test TTSEngine with custom parameters"""
    engine = TTSEngine(rate=200, volume=0.8, voice_id="test_voice")
    assert engine._rate == 200
    assert engine._volume == 0.8
    assert engine._voice_id == "test_voice"
    engine.shutdown()


def test_tts_engine_speak():
    """Test TTSEngine speak method"""
    engine = TTSEngine()

    # Should not raise an error
    engine.speak("Hello, world!")

    # Give it a moment to process
    time.sleep(0.1)

    engine.shutdown()


def test_tts_engine_settings():
    """Test TTSEngine settings methods"""
    engine = TTSEngine()

    engine.set_rate(180)
    assert engine._rate == 180

    engine.set_volume(0.5)
    assert engine._volume == 0.5

    engine.set_voice("test_voice")
    assert engine._voice_id == "test_voice"

    engine.shutdown()


def test_global_speak_function():
    """Test global speak function"""
    # Should not raise an error
    speak("Test message")

    # Give it a moment to process
    time.sleep(0.1)

    # Clean up to prevent warnings
    from tkaria11y.a11y_engine import shutdown_tts

    shutdown_tts()


def test_global_tts_instance():
    """Test global tts instance exists"""
    assert tts is not None
    assert isinstance(tts, TTSEngine)


def test_tts_engine_shutdown_before_start():
    """Test TTSEngine shutdown before thread is started"""
    engine = TTSEngine()
    # Should not raise an error even if thread never started
    engine.shutdown()
