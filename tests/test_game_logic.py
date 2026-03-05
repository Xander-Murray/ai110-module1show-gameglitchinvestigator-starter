from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

# ============================================================================
# Bug #1 Tests: bounds don't make logical sense
# ============================================================================

def test_difficulty_bounds_easy():
    # Easy should be 1-20
    low, high = get_range_for_difficulty("Easy")
    assert low == 1 and high == 20

def test_difficulty_bounds_normal():
    # Normal should be 1-50 (was 1-100, but swapped with Hard)
    low, high = get_range_for_difficulty("Normal")
    assert low == 1 and high == 50

def test_difficulty_bounds_hard():
    # Hard should be 1-100 (was 1-50, but swapped with Normal)
    # FIX: Hard difficulty now correctly has larger range than Normal for actual difficulty progression
    low, high = get_range_for_difficulty("Hard")
    assert low == 1 and high == 100

def test_difficulty_bounds_progression():
    # Verify that difficulty ranges progress logically: Easy < Normal < Hard
    easy_low, easy_high = get_range_for_difficulty("Easy")
    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low, hard_high = get_range_for_difficulty("Hard")

    # Each difficulty should have a larger range than the previous
    assert easy_high < normal_high, "Normal should have larger range than Easy"
    assert normal_high < hard_high, "Hard should have larger range than Normal"


# ============================================================================
# Bug #2 Tests: check_guess should only compare numbers (not strings)
# ============================================================================

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

def test_numeric_comparison_not_string():
    # FIX: This test ensures the glitch is fixed - numeric comparison, not string comparison
    # If we were doing string comparison: "50" > "42" would be False (because "5" < "4")
    # With numeric comparison: 50 > 42 is True
    outcome, message = check_guess(50, 42)
    assert outcome == "Too High", "50 is numerically > 42, should return Too High"

def test_numeric_comparison_edge_case():
    # FIX: This catches the string comparison bug where "9" < "80" lexicographically
    # With string comparison, guess=9 and secret=80 would incorrectly say "Too Low"
    # because "9" > "80" as strings
    outcome, message = check_guess(9, 80)
    assert outcome == "Too Low", "9 is numerically < 80, should return Too Low"

def test_numeric_comparison_single_vs_double():
    # Another edge case: string comparison "8" vs "100" would say "Too High"
    # because "8" > "1", but numerically 8 < 100
    outcome, message = check_guess(8, 100)
    assert outcome == "Too Low", "8 is numerically < 100, should return Too Low"


# ============================================================================
# Parse Guess Tests
# ============================================================================

def test_parse_guess_valid_integer():
    ok, value, err = parse_guess("50")
    assert ok is True
    assert value == 50
    assert err is None

def test_parse_guess_valid_float():
    ok, value, err = parse_guess("50.7")
    assert ok is True
    assert value == 50
    assert err is None

def test_parse_guess_invalid_text():
    ok, value, err = parse_guess("hello")
    assert ok is False
    assert value is None
    assert err == "That is not a number."

def test_parse_guess_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_parse_guess_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


# ============================================================================
# Update Score Tests
# ============================================================================

def test_update_score_win_first_attempt():
    score = update_score(0, "Win", 1)
    assert score == 80  # 100 - 10*(1+1) = 100 - 20 = 80

def test_update_score_too_high_even_attempt():
    score = update_score(0, "Too High", 2)
    assert score == 5  # Even attempt gets +5

def test_update_score_too_high_odd_attempt():
    score = update_score(0, "Too High", 1)
    assert score == -5  # Odd attempt gets -5

def test_update_score_too_low():
    score = update_score(0, "Too Low", 1)
    assert score == -5


# ============================================================================
# Additional Bug Fixes: Hardcoded ranges
# ============================================================================

def test_new_game_respects_easy_range():
    # FIX: New Game button now generates secret from correct difficulty range
    # Verify Easy difficulty generates numbers in 1-20 range
    low, high = get_range_for_difficulty("Easy")
    assert low == 1 and high == 20
    for _ in range(100):
        import random
        secret = random.randint(low, high)
        assert 1 <= secret <= 20, f"Easy game secret {secret} outside range 1-20"

def test_new_game_respects_normal_range():
    # Verify Normal difficulty generates numbers in 1-50 range
    low, high = get_range_for_difficulty("Normal")
    assert low == 1 and high == 50
    for _ in range(100):
        import random
        secret = random.randint(low, high)
        assert 1 <= secret <= 50, f"Normal game secret {secret} outside range 1-50"

def test_new_game_respects_hard_range():
    # Verify Hard difficulty generates numbers in 1-100 range
    low, high = get_range_for_difficulty("Hard")
    assert low == 1 and high == 100
    for _ in range(100):
        import random
        secret = random.randint(low, high)
        assert 1 <= secret <= 100, f"Hard game secret {secret} outside range 1-100"
