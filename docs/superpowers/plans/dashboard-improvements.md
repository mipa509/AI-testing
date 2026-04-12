# Dashboard Improvement Backlog

> Collected after first visual review of `dashboard.html` — 2026-04-11

---

## ✅ 1. Row hover highlight contrast (Overview + Task Drill-Down)

**Problem:** The hover highlight colour (`.tr:hover td { background: #1e293b66; }`) is too similar to some score-cell background colours (e.g. `.s4 #15803d22`), making it hard to tell which row is active.

**Goal:** Hover highlight should be clearly visible on top of any score-cell colour without washing out the individual cell shading.

**Affected tabs:** Overview, Task Drill-Down

**Ideas:**
- Use a left-border indicator on `tr:hover` instead of (or in addition to) a full-row background tint
- Use a brighter/more opaque background on `tr:hover td` that has enough contrast against all five score classes
- Add a `z-index`/overlay approach so score-cell colour shows through but a thin accent is visible

---

## ✅ 2. Model Profiles radar chart — three improvements

### ✅ 2a. Bigger chart

**Problem:** The radar canvas is too small to read comfortably.

**Fix:** Increase `max-width` of the `.chart-wrap` and `height` on `<canvas id="radarChart">`. Target: fill more of the viewport (e.g. `max-width: 720px`, `height: 500`).

### ✅ 2b. Multi-select model comparison

**Problem:** The current dropdown only allows "All models" or one specific model. There is no way to compare an arbitrary subset.

**Goal:** Replace the single model `<select>` with a clickable model list where each model can be toggled on/off independently. Any combination should render on the radar simultaneously.

**Suggested UX:**
- Render a row of clickable chips/toggle buttons, one per model in the selected round
- Each chip shows the model's display name and its assigned colour dot
- Clicking a chip toggles it; selected chips are highlighted, deselected are dimmed
- "All" and "None" shortcut buttons
- Radar re-renders immediately on any toggle

### ✅ 2c. Radar gridlines

**Problem:** Without visible gridlines it is hard to judge absolute score values.

**Fix:** Enable Chart.js radar grid lines:
```js
scales: {
  r: {
    grid: { color: '#334155' },       // visible gridlines (was #1e293b — too dark)
    angleLines: { color: '#334155' }, // spoke lines
    ticks: { backdropColor: 'transparent', color: '#64748b' }
  }
}
```

---

## ✅ 3. Task Drill-Down — row hover highlight

Same issue as item 1. The winner row (`background: #0f2a1a88`) and hovered rows can look similar.

**Goal:** Same fix approach as Overview — ensure hover state is unambiguous on all row types including the winner row.

---

## Implementation notes

- All changes are in `dashboard/template.html` (CSS `<style>` block and the main `<script>` block)
- `dashboard/build.py` and `dashboard/parser.py` do not need changes
- After editing the template, regenerate with `python dashboard/build.py` and verify in browser
