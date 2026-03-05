# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  - I could only play the normal difficulty when, sumbitting guesses for either the hard or easy mode nothing would happen no matter if the input changed.
  - The game would only hint that I needed to go lower despite getting to 1 which is the lower bound of the game, at least by the rules
  - Attempts allowed doesnt go down as you get to a harder mode

---

## 2. How did you use AI as a teammate?

I used Claude Code as my AI teammate throughout this project. It helped me explore the bugs, plan the fixes, and implement the solutions with tests.

**Example of a correct suggestion:** Claude suggested that the alternating string/int comparison in check_guess was the core issue—converting secret to a string on even attempts would cause lexicographic comparison instead of numeric comparison. For example, "9" > "80" as strings but 9 < 80 as numbers. I verified this by writing specific test cases like `test_numeric_comparison_edge_case()` that would immediately fail with the buggy code but pass with the fix. Running pytest confirmed all 22 tests passed after removing the TypeError handling and string conversion logic.

**Example of a misleading suggestion:** Claude initially suggested adding extra error handling and type validation to check_guess before removing the string comparison. However, I realized the simpler fix (just deleting the alternating conversion and TypeError block) was actually better—there was no need for the extra safety since we're always passing integers now. The tests proved that the minimal fix was correct, which taught me to trust simplicity over defensive programming when it's actually appropriate.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed by running `pytest` on a comprehensive test suite—if the tests passed, the fix worked; if they failed, I knew exactly what broke. For Bug #2 (the string comparison glitch), I ran this test:

```python
def test_numeric_comparison_not_string():
    outcome, message = check_guess(50, 42)
    assert outcome == "Too High"
```

With the buggy code, this would fail because it was sometimes doing string comparison ("50" > "42" is False). After removing the alternating string conversion, pytest showed 22/22 tests passing. I also discovered two additional bugs while testing—the info message and New Game button both hardcoded "1-100" instead of using the actual difficulty range—and added tests to catch those too. Claude helped me design edge-case tests like `test_numeric_comparison_edge_case()` that specifically target the string comparison bug by using numbers like 9 vs 80 where lexicographic order differs from numeric order.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
