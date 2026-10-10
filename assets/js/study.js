(() => {
  'use strict';
  const configNode = document.querySelector('#study-config');
  if (!configNode) return;
  let config;
  try { config = JSON.parse(configNode.textContent); } catch { return; }
  const key = 'interview-practice:reading-place:v1';
  const languageKey = 'interview-practice:language:v1';
  const steps = ['goal', 'predict', 'model', 'practice', 'verify', 'recall'];
  const lesson = document.querySelector('[data-lesson-id]');
  const bookmarkStatus = document.querySelector('#bookmark-status');
  const resume = document.querySelector('[data-resume]');
  const resumeStatus = document.querySelector('[data-resume-status]');
  const localeStatus = document.querySelector('#locale-status');
  const say = (element, value) => { if (element) element.textContent = value; };
  const message = name => config.messages[name];
  const knownLanguages = config.supportedLocales;
  const validLanguage = value => knownLanguages.includes(value);
  const routePath = value => {
    try {
      const url = new URL(value, location.origin);
      return url.origin === location.origin ? url.pathname : null;
    } catch { return null; }
  };
  let preferred = config.locale;
  let storageBlocked = false;
  try {
    const saved = localStorage.getItem(languageKey);
    if (validLanguage(saved)) preferred = saved;
  } catch { storageBlocked = true; }
  // Remember a deliberate choice. A direct URL never redirects automatically.
  // An offer preserves explicit links and browser back/forward behavior.
  if (preferred !== config.locale && config.routes[preferred]) {
    const offer = document.querySelector('[data-preference-link]');
    if (offer) {
      const updateOffer = () => { offer.href = config.routes[preferred] + location.hash; };
      updateOffer();
      window.addEventListener('hashchange', updateOffer);
      offer.textContent = message('locale_offer').replace('{language}', config.languageNames[preferred]);
      offer.closest('.preference-offer').hidden = false;
    }
  }
  if (storageBlocked) say(localeStatus, message('locale_blocked'));
  document.querySelectorAll('[data-copy-prompt], [data-close-answers], [data-clear-place]').forEach(button => { button.disabled = false; });
  document.querySelectorAll('[data-locale-link]').forEach(link => {
    const updateTarget = () => {
      if (!link.hasAttribute('data-locale-missing')) {
        const route = config.routes[link.dataset.localeLink];
        if (route) link.href = route + location.hash;
      }
    };
    updateTarget();
    window.addEventListener('hashchange', updateTarget);
    link.addEventListener('click', () => {
      const language = link.dataset.localeLink;
      if (!validLanguage(language)) return;
      try { localStorage.setItem(languageKey, language); say(localeStatus, message('locale_saved')); }
      catch { say(localeStatus, message('locale_blocked')); }
    });
  });
  function readPlace() {
    try {
      const place = JSON.parse(localStorage.getItem(key));
      if (!place || typeof place.lessonId !== 'string' || typeof place.path !== 'string' || !steps.includes(place.step)) return null;
      const logical = config.lessons.find(item => item.id === place.lessonId);
      if (!logical) return null;
      const existing = routePath(place.path);
      if (!existing || !Object.values(logical.routes).some(route => routePath(route) === existing)) return null;
      const target = logical.routes[preferred] || logical.routes.en;
      if (!target) return null;
      return { path: target + '#' + place.step, step: place.step, fallback: !logical.routes[preferred] };
    } catch { return null; }
  }
  const place = readPlace();
  if (resume && place) {
    resume.href = place.path;
    say(resumeStatus, place.fallback ? message('resume_fallback') : message('resume').replace('{step}', config.steps[place.step]));
  }
  function saveStep(step) {
    if (!lesson || !steps.includes(step)) return;
    document.querySelectorAll('[data-step]').forEach(link => {
      if (link.dataset.step === step) link.setAttribute('aria-current', 'step');
      else link.removeAttribute('aria-current');
    });
    try {
      localStorage.setItem(key, JSON.stringify({ lessonId: lesson.dataset.lessonId, path: lesson.dataset.lessonUrl, step, updatedAt: new Date().toISOString() }));
      say(bookmarkStatus, message('bookmark_saved'));
    } catch { say(bookmarkStatus, message('bookmark_blocked')); }
  }
  if (lesson) {
    document.querySelectorAll('a[href^="#"]').forEach(link => link.addEventListener('click', () => saveStep(link.hash.slice(1))));
    if (steps.includes(location.hash.slice(1))) saveStep(location.hash.slice(1));
    window.addEventListener('hashchange', () => saveStep(location.hash.slice(1)));
  }
  document.querySelector('[data-clear-place]')?.addEventListener('click', () => {
    try { localStorage.removeItem(key); say(bookmarkStatus, message('bookmark_cleared')); }
    catch { say(bookmarkStatus, message('clear_blocked')); }
  });
  document.querySelectorAll('[data-copy-prompt]').forEach(button => button.addEventListener('click', async () => {
    const box = button.closest('.prompt-box');
    const prompt = box.querySelector('[data-prompt]').textContent.trim();
    const status = box.querySelector('[data-copy-status]');
    try { await navigator.clipboard.writeText(prompt); say(status, message('copied')); }
    catch { say(status, message('copy_blocked')); }
  }));
  document.querySelectorAll('[data-close-answers]').forEach(button => button.addEventListener('click', () => {
    document.querySelectorAll('details[data-answer]').forEach(answer => { answer.open = false; });
    say(document.querySelector('#recall-status'), message('answers_closed'));
  }));
})();
