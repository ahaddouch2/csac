(() => {
    "use strict";
  
    async function updateSetting(el) {
      const isToggle = el.classList.contains("settings_toggle");
      const key = el.dataset.settings;
      const value = isToggle ? el.classList.contains("on") : parseInt(el.value);
  
      await chrome.storage.local.set({ [key]: value });
  
      if (isToggle) {
        el.classList.remove("on", "off");
        el.classList.add(value ? "on" : "off");
      }
    }
  
    function initialize() {
      const toggles = document.getElementsByClassName("settings_toggle");
      const texts = document.getElementsByClassName("settings_text");
  
      for (const el of toggles) {
        const key = el.dataset.settings;
  
        // ✅ Force toggle ON and store `true`
        el.classList.remove("on", "off");
        el.classList.add("on");
        chrome.storage.local.set({ [key]: true });
  
        // ✅ Optional: still allow clicking to toggle (you can disable this if needed)
        el.addEventListener("click", () => {
          el.classList.toggle("on");
          el.classList.toggle("off");
          updateSetting(el);
        });
      }
  
      for (const el of texts) {
        const key = el.dataset.settings;
        el.value = ""; // Clear or set to default
        el.addEventListener("input", () => updateSetting(el));
      }
    }
  
    document.addEventListener("DOMContentLoaded", initialize);
  })();
  