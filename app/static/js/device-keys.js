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

  document.addEventListener("keydown", (event) => {
    const action = KEYMAP[event.key];
    if (!action) return;            // not one of our keys: ignore it

    console.log("device:" + action);
    document.dispatchEvent(new CustomEvent("device:" + action));
  });
})();