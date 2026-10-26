# Theater Auto-Hide and Sky Quick Surf Design

## Intent

Make the Watch Live theater easier to use by fixing native-playback auto-hide, adding a manual hide control, starting with Quick Channel Surf closed, and adding a Sky filter to the surf drawer. Improve Sky playback only through official or otherwise authorized sources.

## Why

The theater currently opens the channel drawer on every channel, auto-hide is disabled for mirror/embed playback, and the surf filters do not provide a single way to find all Sky channels. The current Sky playback fallback uses third-party pages; those are not an acceptable source for playback improvements.

## Goals

- Hide and reveal the theater's own header and bottom controls in both windowed and fullscreen theater during idle native playback; reveal them on pointer movement or another existing player interaction.
- Provide a clearly labeled manual hide control in the theater bottom control bar.
- Keep the theater controls visible during embedded playback, where pointer movement inside a cross-origin iframe cannot reliably be observed.
- Open the player with Quick Channel Surf collapsed, while retaining its toggle button and keyboard shortcut.
- Add a Sky quick-surf filter that includes Sky channels across their existing categories, including sports and news.
- Use only verified official/authorized Sky playback. When an official in-player stream is unavailable, offer a link to the relevant official provider page in a new tab.

## Non-goals

- Reworking the player's HLS buffering, stream token acquisition, or third-party stream scraping.
- Making claims about a channel stream being available or licensed when it cannot be verified.
- Redesigning the theater controls or the non-theater Sky Channels section.
- Hiding native browser or official-provider playback controls.

## Anti-goals

- Keep unauthorized third-party stream pages as a playback fallback.
- Hide controls during embedded playback when the page cannot reliably reveal them.
- Open the channel surf drawer automatically on each channel change.

## Constraints

- Theater interactions are implemented in `js/player.js`, with markup in `index.html` and transitions in `css/player.css`.
- Current auto-hide is controlled by `controls-hidden`; mirror/embed modes explicitly bypass it.
- Cross-origin iframe mouse events do not bubble to the parent document. Per user decision, embedded playback controls remain visible instead of adding an always-visible edge tab.
- Quick Surf categories are explicit HTML buttons filtered in `renderInPlayerSurfList`; Sky membership must match the existing data by channel name or ID, not just one display category.
- Sky channel records currently use third-party source-page/embed values; those must not be improved or promoted. Use verified official/authorized pages and external navigation if in-player playback is unavailable.
- Preserve unrelated worktree changes and existing player behavior outside the requested paths.

## Approaches

1. **Extend the existing theater state and surf filters (selected/recommended).** Keep `controls-hidden` and the existing drawer/category patterns; correct native auto-hide and reveal behavior, add the bottom hide action, start the drawer collapsed, add a Sky filter, and route unavailable Sky in-player playback to an official provider page. This is focused and preserves the current player architecture.
2. **Rebuild theater visibility and channel browsing as a new state system.** Could support more elaborate reveal behavior, but would touch many more controls and increase regression risk without being necessary for the requested behavior.

## Decisions

- Use approach 1.
- For native playback, the theater chrome auto-hides after idle in both windowed and fullscreen theater and returns on pointer movement; provide a manual hide button in the bottom bar.
- Keep the theater chrome visible during embedded playback; do not add an edge reveal tab.
- Start each newly opened channel with the Quick Channel Surf drawer collapsed. Keep the drawer toggle and `C` shortcut available.
- Add a Sky filter pill that includes any Sky channel across channel categories.
- Restrict Sky playback changes to official/authorized sources. Use an official provider page in a new tab as the fallback if verified in-player playback is unavailable. Do not use third-party extraction or embed URLs as a fallback.

## Builder calls

- Verify official provider URLs before wiring them. When no channel-specific official URL can be verified, use the official Sky/authorized provider landing page rather than inventing a deep link.
- Keep the hide action unavailable or inactive while embedded playback controls are intentionally pinned visible; retain the existing close/hide behavior for the surf drawer separately.
- Ensure manual and automatic visibility changes keep button labels, accessibility state, and drawer state synchronized.
