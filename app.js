// ---- Data you can edit ------------------------------------------------------

const recruits = [
  {
    name: 'Connor Lyons',
    classYear: 2026,
    position: 'SF',
    height: "6'8\"",
    weight: '—',
    status: 'committed', // 'target' | 'offered' | 'committed'
    hometown: 'Miller School (VA)',
    ranking: '2026 SF, Prep Hoops profile',
    tags: ['Knockdown shooter', 'Versatile forward', 'Guards 3–5'],
    notes:
      'Per Prep Hoops, Lyons is a 6-foot-8 forward, knockdown shooter and improved facilitator who can defend 3–5. See full profile for detailed ranking and context.',
  },
  {
    name: 'Elijah Hayeems',
    classYear: 2026,
    position: 'PG',
    height: "6'6\"",
    weight: '—',
    status: 'committed',
    hometown: 'Big Tyme Prep Academy (TX)',
    ranking: 'McDonald’s All-American nominee; Prep Hoops profile',
    tags: ['Elite positional size', 'Playmaking & scoring', 'Defensive versatility'],
    notes:
      "Per Prep Hoops, Hayeems’ McDonald’s All-American nomination is driven by rare positional size at point guard combined with functional skill, two-way versatility, and high-level feel for the game. See his profile for full evaluation.",
  },
];

const updates = [
  {
    date: '2026-01-05',
    type: 'offer',
    title: 'Bryant offers 2026 guard prospect (sample)',
    body: 'Use this timeline card to log offers, visits, and commitment announcements as they happen.',
    tag: 'Offer',
  },
  {
    date: '2025-12-10',
    type: 'visit',
    title: 'Unofficial visit scheduled (sample)',
    body: 'Track unofficial/official visits here so you can see recruiting momentum over time.',
    tag: 'Visit',
  },
  {
    date: '2025-11-02',
    type: 'commit',
    title: 'First 2026 commit goes public (sample)',
    body: 'When a prospect commits, add a new entry here and mark their status as "committed" above.',
    tag: 'Commit',
  },
];

const expertAnalysis = [
  {
    player: 'Connor Lyons',
    classYear: 2026,
    position: 'SF',
    source: 'Prep Hoops',
    sourceUrl: 'https://prephoops.com/player/connor-lyons/',
    author: 'Jaylen Fuller',
    date: '2026-03-10',
    snippet:
      'Prep Hoops describes Lyons as a 6-foot-8 forward and knockdown shooter who can also put the ball on the floor, facilitate, and defend multiple spots (3–5).',
    tags: ['Connor Lyons', 'Scouting report', 'Prep Hoops'],
  },
  {
    player: 'Elijah Hayeems',
    classYear: 2026,
    position: 'PG',
    source: 'Prep Hoops',
    sourceUrl: 'https://prephoops.com/player/elijah-hayeems/',
    author: 'Jay Frye',
    date: '2026-01-30',
    snippet:
      'Prep Hoops notes that Hayeems’ McDonald’s All-American nomination is driven by rare positional size at point guard combined with functional skill. He creates advantages as both a playmaker and scorer, finishes through contact, and defends multiple positions with plus court awareness.',
    tags: ['Elijah Hayeems', 'Scouting report', 'Prep Hoops'],
  },
];

// ---- Rendering logic ---------------------------------------------------------

const recruitsGrid = document.getElementById('recruits-grid');
const updatesTimeline = document.getElementById('updates-timeline');
const expertAnalysisList = document.getElementById('expert-analysis-list');
const bryantTimelineEl = document.getElementById('bryant-timeline');
const positionFilter = document.getElementById('position-filter');
const statusFilter = document.getElementById('status-filter');
const lastUpdatedEl = document.getElementById('last-updated');

function formatDate(dateStr) {
  const d = new Date(dateStr);
  if (Number.isNaN(d.getTime())) return dateStr;
  return d.toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

function computeLastUpdated() {
  if (!updates.length) return null;
  const latest = updates
    .map((u) => new Date(u.date))
    .filter((d) => !Number.isNaN(d.getTime()))
    .sort((a, b) => b - a)[0];
  return latest || null;
}

function setLastUpdatedText() {
  const latest = computeLastUpdated();
  if (!lastUpdatedEl) return;
  if (!latest) {
    lastUpdatedEl.textContent = 'No updates logged yet.';
    return;
  }
  lastUpdatedEl.textContent = `Last updated: ${latest.toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })}`;
}

function buildPositionFilterOptions() {
  if (!positionFilter) return;
  const uniquePositions = Array.from(
    new Set(recruits.map((r) => r.position).filter(Boolean)),
  ).sort();

  uniquePositions.forEach((pos) => {
    const opt = document.createElement('option');
    opt.value = pos;
    opt.textContent = pos;
    positionFilter.appendChild(opt);
  });
}

function renderRecruits() {
  if (!recruitsGrid) return;

  const positionValue = positionFilter?.value ?? 'all';
  const statusValue = statusFilter?.value ?? 'all';

  recruitsGrid.innerHTML = '';

  const filtered = recruits.filter((r) => {
    const posOk = positionValue === 'all' || r.position === positionValue;
    const statusOk = statusValue === 'all' || r.status === statusValue;
    return posOk && statusOk;
  });

  if (!filtered.length) {
    const empty = document.createElement('div');
    empty.style.fontSize = '0.86rem';
    empty.style.color = '#9ca3af';
    empty.textContent = 'No recruits match the current filters yet. Try widening them or add new data in app.js.';
    recruitsGrid.appendChild(empty);
    return;
  }

  filtered.forEach((r) => {
    const card = document.createElement('article');
    card.className = 'recruit-card';

    const statusClass =
      r.status === 'committed'
        ? 'status-committed'
        : r.status === 'offered'
          ? 'status-offered'
          : 'status-target';

    card.innerHTML = `
      <div class="recruit-header">
        <h3 class="recruit-name">${r.name}</h3>
        <span class="pill status-pill ${statusClass}">
          ${r.status === 'committed' ? 'Committed' : r.status === 'offered' ? 'Offer' : 'Target'}
        </span>
      </div>
      <div class="recruit-meta-row">
        <span class="pill"><span>${r.position || '—'}</span> • ${r.classYear || '2026'}</span>
        ${
          r.height || r.weight
            ? `<span class="pill">${r.height || ''}${r.height && r.weight ? ' • ' : ''}${r.weight || ''}</span>`
            : ''
        }
      </div>
      <div class="recruit-details">
        <span>${r.hometown ? `<strong>From:</strong> ${r.hometown}` : ''}</span>
        <span>${r.ranking ? `<strong>Rank:</strong> ${r.ranking}` : ''}</span>
      </div>
      ${
        r.tags && r.tags.length
          ? `<div class="recruit-tags">
              ${r.tags
                .map(
                  (t, i) =>
                    `<span class="tag ${i === 0 ? 'tag-keyword' : ''}">${t}</span>`,
                )
                .join('')}
            </div>`
          : ''
      }
      ${r.notes ? `<p class="notes">${r.notes}</p>` : ''}
    `;

    recruitsGrid.appendChild(card);
  });
}

function renderUpdates() {
  if (!updatesTimeline) return;
  updatesTimeline.innerHTML = '';

  if (!updates.length) {
    const empty = document.createElement('div');
    empty.style.fontSize = '0.86rem';
    empty.style.color = '#9ca3af';
    empty.textContent = 'No timeline events yet. Add your first offer, visit, or commit in app.js.';
    updatesTimeline.appendChild(empty);
    return;
  }

  const sorted = [...updates].sort(
    (a, b) => new Date(b.date) - new Date(a.date),
  );

  sorted.forEach((u) => {
    const item = document.createElement('article');
    item.className = 'timeline-item';

    item.innerHTML = `
      <div class="timeline-dot"></div>
      <div class="timeline-date">${formatDate(u.date)}</div>
      <div class="timeline-tag">${u.tag || 'Update'}</div>
      <div class="timeline-title">${u.title}</div>
      <div class="timeline-body">${u.body}</div>
    `;

    updatesTimeline.appendChild(item);
  });
}

function renderExpertAnalysis() {
  if (!expertAnalysisList) return;
  expertAnalysisList.innerHTML = '';

  if (!expertAnalysis.length) {
    const empty = document.createElement('div');
    empty.style.fontSize = '0.86rem';
    empty.style.color = '#9ca3af';
    empty.textContent =
      'No expert analysis logged yet. Add scouting blurbs for key targets in the expertAnalysis array in app.js.';
    expertAnalysisList.appendChild(empty);
    return;
  }

  const sorted = [...expertAnalysis].sort(
    (a, b) => new Date(b.date) - new Date(a.date),
  );

  sorted.forEach((e) => {
    const card = document.createElement('article');
    card.className = 'expert-card';

    const dateText = e.date ? formatDate(e.date) : '';
    const sourceLabel = e.source || 'External report';

    card.innerHTML = `
      <div class="expert-header-row">
        <div class="expert-player">
          ${e.player || 'Unnamed prospect'}${e.position ? ` • ${e.position}` : ''}${
            e.classYear ? ` • ${e.classYear}` : ''
          }
        </div>
        <div class="expert-meta">
          ${dateText ? `<span>${dateText}</span>` : ''}
          ${
            e.author
              ? `<span>${e.author}${sourceLabel ? ` • ${sourceLabel}` : ''}</span>`
              : sourceLabel
                ? `<span>${sourceLabel}</span>`
                : ''
          }
        </div>
      </div>
      <div class="expert-snippet">
        ${e.snippet || ''}
        ${
          e.sourceUrl
            ? `<span> <a href="${e.sourceUrl}" target="_blank" rel="noopener noreferrer">Full profile</a></span>`
            : ''
        }
      </div>
      ${
        e.tags && e.tags.length
          ? `<div class="expert-tags">
              ${e.tags
                .map(
                  (t) =>
                    `<span class="tag">${t}</span>`,
                )
                .join('')}
            </div>`
          : ''
      }
    `;

    expertAnalysisList.appendChild(card);
  });
}

function renderBryantTimeline() {
  if (!bryantTimelineEl) return;

  bryantTimelineEl.innerHTML = '';

  const item = document.createElement('article');
  item.className = 'timeline-item';
  item.innerHTML = `
    <div class="timeline-dot"></div>
    <div class="timeline-date">${formatDate(new Date().toISOString().slice(0, 10))}</div>
    <div class="timeline-tag">Verbal Commits</div>
    <div class="timeline-title">Check Bryant’s live recruiting / roster log</div>
    <div class="timeline-body">
      Open the Bryant page on Verbal Commits in a new tab to see the latest scholarship chart,
      transfer and commitment activity, then manually add any key notes you care about to this app.
      <a href="https://www.verbalcommits.com/schools/bryant" target="_blank" rel="noopener noreferrer">
        Go to Bryant on Verbal Commits
      </a>.
    </div>
  `;
  bryantTimelineEl.appendChild(item);
}

function initEvents() {
  positionFilter?.addEventListener('change', renderRecruits);
  statusFilter?.addEventListener('change', renderRecruits);
}

function init() {
  buildPositionFilterOptions();
  renderRecruits();
  renderUpdates();
  renderExpertAnalysis();
  renderBryantTimeline();
  setLastUpdatedText();
  initEvents();
}

document.addEventListener('DOMContentLoaded', init);
