(function () {
  // Keep in sync with hardware/keymap.md
  const KEYMAP = {
    ArrowRight: "next",
    ArrowLeft: "prev",
    PageUp: "aux1",
    PageDown: "aux2",
    Enter: "press",
    ArrowUp: "up",
    ArrowDown: "down",
  };

  // (3) Actions that must fire only once per press, even if the key is held.
  const NO_REPEAT = new Set(["press", "aux1", "aux2"]);

  // (1) Is the user typing into something right now?
  function isTyping(element) {
    if (!element) return false;
    if (element.isContentEditable) return true;
    const tag = element.tagName;
    if (tag === "TEXTAREA" || tag === "SELECT") return true;
    if (tag !== "INPUT") return false;
    const notText = ["button", "checkbox", "radio", "submit", "reset", "range"];
    return !notText.includes(element.type);
  }

  document.addEventListener("keydown", (event) => {
    // Ctrl/Alt/Shift/Cmd combos are shortcuts, not device presses.
    if (event.ctrlKey || event.altKey || event.shiftKey || event.metaKey) return;

    const action = KEYMAP[event.key];
    if (!action) return;
    if (event.repeat && NO_REPEAT.has(action)) return;   // (3)
    if (isTyping(event.target)) return;                  // (1)

    const deviceEvent = new CustomEvent("device:" + action, { cancelable: true });
    const handled = !document.dispatchEvent(deviceEvent);
    if (handled) event.preventDefault();                 // (2)
  });
})();