# Hero Controls Click Fix

- **Intent:** Restore working clicks for the top-right navigation menu and the hero “Watch Live” button.
- **Why:** Both controls currently appear unresponsive, blocking navigation and live playback from the homepage.
- **Goals:** Find the shared or separate runtime cause; make the smallest reliable fix; preserve current layout, menu behavior, and player behavior.
- **Non-goals:** Redesigning the navbar or hero, changing channel selection, or changing playback/streaming logic unless the diagnosis shows it is the cause.
- **Anti-goals:** Adding broad overlays or global click handlers that could break other controls.
- **Constraints:** Reuse existing UI initialization and event-handling patterns. The hero layers are already configured to pass clicks through.
- **Approaches:** (1) Trace existing initialization, click handlers, and hit-testing, then patch only the failing point — selected and recommended because it minimizes behavioral risk. (2) Rebuild controls with delegated events — rejected as unnecessary without evidence that the existing handlers cannot work.
- **Implementation:** Diagnose in the current code; retain existing interactions and make only the verified fix. Validate JavaScript syntax and the affected UI behavior where available.
- **Open to the builder:** The exact root cause and the smallest code surface it requires.
