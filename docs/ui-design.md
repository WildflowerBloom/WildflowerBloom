# UI/UX Blueprint

## Design Principles

- **Emotional safety first**: interface should feel like a soft landing, not a dashboard of guilt.
- **Low cognitive load**: minimal elements on screen; highlight next action over metrics.
- **Personal pace**: allow toggles between energetic “Fire Mode” and quiet “Gentle Mode”.
- **Accessibility**: large readable fonts, colour-safe palettes, audio optional.

## Primary Screens

### 1. Conversational Hub (Default View)

```
┌─────────────────────────────────────────────┐
│ Navi Copilot                                │
├────────────────────────────┬────────────────┤
│ Conversation Stream        │ Mode Indicator │
│ [User bubble]              │  ○ LowDopamine │
│ [Navi bubble + micro-step] │  Conf 0.72     │
│ ...                        │                │
├────────────────────────────┴────────────────┤
│ Quick Actions: [Spark] [Ground] [Quiet]     │
├─────────────────────────────────────────────┤
│ Textbox: “Tell Navi what’s happening…”      │
│ [Send] [Attach Memory]                      │
└─────────────────────────────────────────────┘
```

- **Conversation Stream**: alternating bubbles; Navi messages include tone tag chip (“Spark”, “Ground”).
- **Mode Indicator Card**: shows current mode, intensity bar, short explanation. Tapping reveals “Why this mode?” with trigger list.
- **Quick Actions**:
  - `Spark`: triggers high-energy prompt.
  - `Ground`: initiates calming mode.
  - `Quiet`: toggles minimal response style.

### 2. Micro-Action Drawer

Slide-up panel presenting 1-2 suggested actions with optional audio toggle.

```
┌─────────────────────────────┐
│ Try this spark?             │
│ 5-min dopamine challenge    │
│ • Tone: Playful             │
│ • Anchor: Ignite Chime  ⏯️  │
│ [Do It] [Too Much] [Swap]   │
└─────────────────────────────┘
```

- `Swap` cycles to another template if available.
- `Too Much` provides immediate feedback and reduces future intensity.

### 3. Memory & Insights (Beta)

```
┌───────────────────────────────┐
│ Today’s Rhythm                │
├───────────────────────────────┤
│ Mode Timeline: LowDopa → Reg │
│ Momentum Score: ★★★☆☆         │
│ Wins:                         │
│  - Reset studio (hopeful)     │
│  - Checked inbox (relieved)   │
├───────────────────────────────┤
│ Gentle Reminder queue         │
│  - Drink water in 5 min       │
│  - Nightly soften & stretch   │
└───────────────────────────────┘
```

Focus on narrative—not graphs. Use icons/emojis for emotional clarity.

## Interaction States

- **Mode Transition Glow**: subtle background gradient shift matching mode colour (e.g., warm orange for LowDopamine spark).
- **Quiet Mode**: reduces animations, switches to monochrome palette, short textual responses.
- **Emergency Pattern**: if user flags distress, UI locks to resource card with hotline info and optional friend contact.

## Tone Color Palette

| Mode | Colour | Usage |
|------|--------|-------|
| LowDopamine | Amber (#F7A046) | Buttons, background pulses |
| Overwhelm | Deep teal (#317C86) | Calming gradients |
| Hyperfocus | Indigo (#5C5FF0) | Focus outlines |
| Crash | Soft plum (#B966AA) | Gentle backgrounds |
| Regulated | Sage green (#6DBE85) | Success chips |

Ensure contrast ratio ≥ 4.5:1 for text.

## Component Library

- **Mode Badge**: pill with icon + label.
- **Emotion Tag**: small chip representing e.g., “hopeful,” “anxious.”
- **Micro-Action Card**: template for Task Translator suggestions.
- **Feedback Buttons**: `Done`, `Too Much`, `Later` (with microcopy).

## Animations

- 300ms fade for new responses.
- Micro-action acceptance triggers confetti spark at low opacity.
- Audio cues accompanied by subtle waveform pulsing to confirm trigger.

## Audio/Visual Settings Panel

Options:
- Sound on/off.
- Anchor type preference (sound, light, none).
- Mode intensity slider (Gentle ←→ Fire).
- Export data / Clear conversation controls.

## Mobile Considerations

- Bottom sheet for micro-actions to avoid covering chat.
- Swipe gesture to mark tasks “Done”.
- Haptic nudge when mode changes (if device supports).

## Empty States

- First launch: “Tell Navi how your day is landing. We’ll find a rhythm together.”
- No micro-actions: “Listening... let’s sit with this feeling for a moment.”

## Error Handling

- LLM offline: show banner “Navi’s offline brain needs a minute—switching to gentle script.”
- Database failure: “Your story didn’t save. Retry or export logs?” with backup instructions.

