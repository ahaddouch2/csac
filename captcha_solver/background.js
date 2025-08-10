(() => {
    "use strict";
  
    // Default settings, now set to true by default
    const e = {
      recaptcha_auto_open: true,    // Always auto-open enabled by default
      recaptcha_auto_solve: true,   // Always auto-solve enabled by default
      recaptcha_click_delay_time: 300,
      recaptcha_solve_delay_time: 1000,
    };
  
    // On install: set default values if not already set
    chrome.runtime.onInstalled.addListener(async () => {
      // Loop through the default settings and set them in storage if not already set
      for (const [t, a] of Object.entries(e)) {
        const stored = await chrome.storage.local.get(t);
        console.log(stored);  // Debug log for current storage state
        if (stored[t] === undefined) {
          await chrome.storage.local.set({ [t]: a });
        }
      }
  
      // Handle first-time setup for Firefox (moz) case
      const t = chrome.runtime.getURL("").startsWith("moz"),
        a = await chrome.permissions.contains({
          origins: [
            "<all_urls>",
            "*://*.google.com/recaptcha/*",
            "*://*.recaptcha.net/recaptcha/*",
          ],
        });
      
      // If Firefox and permissions are not granted, show setup page
      if (t && !a) {
        chrome.tabs.create({ url: chrome.runtime.getURL("setup.html") });
      }
    });
  
    // Ensure defaults are always loaded on startup (if not set already)
    chrome.runtime.onStartup.addListener(async () => {
      await chrome.storage.local.set({
        recaptcha_auto_open: true,  // Force auto-open true on every startup
        recaptcha_auto_solve: true, // Force auto-solve true on every startup
      });
    });
  
    // Messaging system to store/retrieve custom values for each tab
    const t = {};
    chrome.runtime.onMessage.addListener(function ({ type, label }, c, s) {
      (async () => {
        if (type === "KV_SET") {
          if (label.tab_specific) {
            label.key = `${c.tab.id}_${label.key}`;
          }
          t[label.key] = label.value;
          s({ status: "success" });
        } else if (type === "KV_GET") {
          if (label.tab_specific) {
            label.key = `${c.tab.id}_${label.key}`;
          }
          s({ status: "success", value: t[label.key] });
        }
      })();
      return true;
    });
  })();
  