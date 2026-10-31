# Manual Desktop & Mobile Walkthrough Checklists

The desktop/mobile testers are heuristic (stdlib-only, no GUI driver): they audit
layout metadata you supply and print a persona-flavored script. Use these
checklists against the real app, then record results as audit findings.

Generate the persona script any time:

```bash
python3 -m human_tester.cli test-desktop "MyApp" --persona tech_novice
python3 -m human_tester.cli test-mobile "MyApp" --persona rushed_commuter
```

## Desktop GUI checklist

- [ ] Keyboard-only pass: Tab/Shift+Tab reaches every control; focus always visible.
- [ ] Cancel/Submit gap ≥ 40px and Cancel de-emphasized (try as Sam, fatigued).
- [ ] Resize to 1024px → 800px mid-flow: primary action stays reachable.
- [ ] Dialog Cancel test: change 2 values → Cancel → zero changes applied.
- [ ] Top-3 app shortcuts: none fire an OS/browser default instead.
- [ ] Miss the drop zone by a few px: clear error appears (never silence).
- [ ] Stall test: click rapidly during a >2s hang — exactly one action fires.

## Mobile & touch checklist

- [ ] One-handed thumb pass (as Alex): primary action in the bottom half.
- [ ] Keyboard-open pass: submit + inline errors visible above the keyboard.
- [ ] Rotation pass: half-typed form → rotate → everything preserved.
- [ ] Deep-link pass: cold start from a shared link lands on the content.
- [ ] Permission pass: each prompt explains why; Deny keeps the flow usable.
- [ ] Rage-tap pass: 4 fast taps on the slowest button → exactly one request.

## Recording results

Feed observations back into the heuristic testers, e.g.:

```bash
# "Cancel sits 12px from Submit and 800px clips the button"
python3 -m human_tester.cli test-desktop "MyApp" --cancel-distance-px 12 --clipped-at 800

# "Keyboard covers submit; rotation wipes the form"
python3 -m human_tester.cli test-mobile "MyApp" --keyboard-covered --rotation-wipes
```
