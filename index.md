---
layout: home
title: Your Daily Learning Desk
---
{% assign published_lessons = site.pages | where_exp: "item", "item.lesson_id != nil" | sort: "created_at" %}
{% assign latest = published_lessons | last %}
<section class="hero" aria-labelledby="desk-title">
  <div><p class="eyebrow">YOUR DAILY LEARNING DESK</p><h1 id="desk-title">One idea.<br>Make it stick.</h1><p class="intro">Predict it. Build it. Explain why it works. A small session with something real to remember.</p></div>
  <div class="hero-note"><p class="eyebrow">A SIMPLE ROUTINE</p><ol><li>Choose one 30–45 minute session.</li><li>Try before opening the answer.</li><li>Close your notes and explain it back.</li></ol></div>
</section>
{% if latest %}
<section class="featured" aria-labelledby="featured-title">
  <div><p class="eyebrow">LATEST GUIDED LESSON · {{ latest.created_at | date: "%d %b %Y" }}</p><h2 id="featured-title">{{ latest.title | escape }}</h2><ul class="tag-row" aria-label="Session details"><li>{{ latest.duration_minutes | default: 40 }} minutes</li><li>{{ latest.level | capitalize }}</li><li>Practice first</li></ul><p>{{ latest.primary_objective | default: latest.objectives.first | escape }}</p></div>
  <a class="button" href="{{ latest.url | relative_url }}#goal" data-public-lesson>Start this lesson →</a>
</section>
{% endif %}
<div class="section-heading"><h2>What would help today?</h2><p class="muted">One clear next step.</p></div>
<section class="actions" aria-label="Daily learning actions">
  <article class="action-card"><span class="action-number" aria-hidden="true">01 / DISCOVER</span><h3>Learn something new</h3><p>Your repo agent chooses a fresh objective from your learning history.</p><a href="#new-session">Get the daily prompt →</a></article>
  <article class="action-card"><span class="action-number" aria-hidden="true">02 / CONTINUE</span><h3>Pick up where you left off</h3><p>Return to your reading place in this browser.</p><a href="{{ latest.url | relative_url }}#goal" data-resume>Continue reading →</a></article>
  <article class="action-card"><span class="action-number" aria-hidden="true">03 / RETRIEVE</span><h3>Recall without notes</h3><p>Ask your agent what is due, then test the mechanism from memory.</p><a href="{{ '/practice/review/' | relative_url }}">Start a review →</a></article>
  <article class="action-card"><span class="action-number" aria-hidden="true">04 / EXPLAIN</span><h3>Practice the interview</h3><p>Give a short answer, defend a failure case and discuss a trade-off.</p><a href="{{ '/practice/interview/' | relative_url }}">Practice speaking →</a></article>
</section>
<p class="resume-text" data-resume-status>No browser reading place saved yet. Continue opens the latest lesson; ask your repo agent “Tiếp tục bài đang học” to resume a saved coaching session.</p>
<section class="prompt-box" id="new-session" aria-labelledby="new-session-title">
  <h2 id="new-session-title">Ask for your next focused lesson</h2><p>Open this repository in your agent and send:</p><p><code data-prompt>Viết bài học hôm nay.</code></p><div class="prompt-actions"><button type="button" class="button secondary" data-copy-prompt disabled>Copy prompt</button><p class="prompt-status" role="status" data-copy-status aria-live="polite">The agent creates the lesson and saves its delivery record.</p></div>
</section>
<p class="scope-note">This public desk does not read your personal learning state or write to GitHub. Browser bookmarks save a reading place only. Your repo agent records attempts, completion and due reviews.</p>
<section aria-labelledby="library-title"><div class="section-heading"><h2 id="library-title">Your lesson library</h2><a href="{{ '/curriculum/' | relative_url }}">Explore the curriculum →</a></div><ul>{% for item in published_lessons reversed %}<li><a href="{{ item.url | relative_url }}" data-public-lesson>{{ item.title | escape }}</a> <span class="muted">· {{ item.created_at | date: "%d %b %Y" }}</span></li>{% endfor %}</ul></section>
