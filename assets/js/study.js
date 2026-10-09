(() => {
  "use strict";
  const key = "interview-practice:reading-place:v1";
  const steps = ["goal", "predict", "model", "practice", "verify", "recall"];
  const lesson = document.querySelector("[data-lesson-id]");
  const bookmarkStatus = document.querySelector("#bookmark-status");
  const resume = document.querySelector("[data-resume]");
  const resumeStatus = document.querySelector("[data-resume-status]");
  const say = (element, text) => {
    if (element) element.textContent = text;
  };
  document
    .querySelectorAll(
      "[data-copy-prompt], [data-close-answers], [data-clear-place]",
    )
    .forEach((button) => {
      button.disabled = false;
    });
  function readPlace() {
    try {
      const place = JSON.parse(localStorage.getItem(key));
      if (
        !place ||
        typeof place.lessonId !== "string" ||
        typeof place.path !== "string" ||
        !steps.includes(place.step)
      )
        return null;
      const url = new URL(place.path, location.origin);
      const allowed = Array.from(
        document.querySelectorAll("[data-public-lesson]"),
      ).some((link) => new URL(link.href).pathname === url.pathname);
      if (url.origin !== location.origin || !allowed) return null;
      return { ...place, path: url.pathname + "#" + place.step };
    } catch {
      return null;
    }
  }
  const place = readPlace();
  if (resume && place) {
    resume.href = place.path;
    say(
      resumeStatus,
      "This browser saved your place at “" +
        place.step +
        "”. This is a reading bookmark, not completion.",
    );
  }
  function saveStep(step) {
    if (!lesson || !steps.includes(step)) return;
    document.querySelectorAll("[data-step]").forEach((link) => {
      if (link.dataset.step === step) link.setAttribute("aria-current", "step");
      else link.removeAttribute("aria-current");
    });
    try {
      localStorage.setItem(
        key,
        JSON.stringify({
          lessonId: lesson.dataset.lessonId,
          path: lesson.dataset.lessonUrl,
          step,
          updatedAt: new Date().toISOString(),
        }),
      );
      say(
        bookmarkStatus,
        "Reading place saved in this browser only. Your repo agent records completion and review dates.",
      );
    } catch {
      say(
        bookmarkStatus,
        "Browser storage is unavailable. Step links still work; ask your repo agent to save session progress.",
      );
    }
  }
  if (lesson) {
    document
      .querySelectorAll('a[href^="#"]')
      .forEach((link) =>
        link.addEventListener("click", () => saveStep(link.hash.slice(1))),
      );
    if (steps.includes(location.hash.slice(1)))
      saveStep(location.hash.slice(1));
    window.addEventListener("hashchange", () =>
      saveStep(location.hash.slice(1)),
    );
  }
  document
    .querySelector("[data-clear-place]")
    ?.addEventListener("click", () => {
      try {
        localStorage.removeItem(key);
        say(
          bookmarkStatus,
          "Reading place cleared. Repository learning history is unchanged.",
        );
      } catch {
        say(
          bookmarkStatus,
          "Browser storage is unavailable; no repository data was changed.",
        );
      }
    });
  document.querySelectorAll("[data-copy-prompt]").forEach((button) =>
    button.addEventListener("click", async () => {
      const box = button.closest(".prompt-box");
      const prompt = box.querySelector("[data-prompt]").textContent.trim();
      const status = box.querySelector("[data-copy-status]");
      try {
        await navigator.clipboard.writeText(prompt);
        say(status, "Copied. Paste into your agent with this repository open.");
      } catch {
        say(
          status,
          "Copy is unavailable. Select the prompt above and paste it into your repo agent.",
        );
      }
    }),
  );
  document.querySelectorAll("[data-close-answers]").forEach((button) =>
    button.addEventListener("click", () => {
      document.querySelectorAll("details[data-answer]").forEach((answer) => {
        answer.open = false;
      });
      say(
        document.querySelector("#recall-status"),
        "Answers closed. Try the three recall questions without notes.",
      );
    }),
  );
})();
