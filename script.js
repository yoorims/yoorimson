const fallbackData = {
  profile: {
    name: "Yoorim Son",
    initials: "YS",
    role: "M.A. Student in Economics",
    tagline:
      "M.A. student in Economics interested in applied microeconomics, development economics, causal inference, spatial analysis, and GIS.",
    bio:
      "I am an M.A. student in Economics at Sogang University. My current working paper studies the economic impact of submarine cable arrival on local economic activity in South Africa.",
    affiliation: "M.A. in Economics, Sogang University",
    location: "Seoul, Korea",
    email: "hello@example.com",
    github: "https://github.com/",
    scholar: "https://scholar.google.com/"
  },
  updates: [
    {
      date: "2026-05-16",
      type: "news",
      title: "Researcher homepage draft",
      summary: "Created a public academic profile structure with About, Resume, Papers, Conferences, and Works pages.",
      tags: ["homepage", "public"]
    }
  ],
  projects: [
    {
      title: "Submarine Cable Arrival and Local Economic Activity",
      state: "Active",
      summary: "A district-level panel project on South Africa using satellite-based proxies and econometric methods.",
      tags: ["development", "south-africa"]
    }
  ],
  research: [
    {
      title: "Applied Microeconomics and Development Economics",
      status: "Primary field",
      cadence: "Research agenda",
      summary:
        "I am interested in empirical questions in development economics, especially how infrastructure and local conditions shape economic activity."
    }
  ]
};

async function getJson(path, key) {
  try {
    const response = await fetch(path, { cache: "no-store" });
    if (!response.ok) throw new Error(`Could not load ${path}`);
    return response.json();
  } catch {
    return fallbackData[key];
  }
}

const formatter = new Intl.DateTimeFormat("ko-KR", {
  year: "numeric",
  month: "short",
  day: "numeric"
});

function formatDate(dateString) {
  return formatter.format(new Date(`${dateString}T00:00:00`));
}

function sortByRecent(items) {
  return [...items].sort((a, b) => b.date.localeCompare(a.date));
}

function renderProfile(profile) {
  document.querySelectorAll("[data-profile]").forEach((element) => {
    const key = element.dataset.profile;
    if (profile[key]) element.textContent = profile[key];
  });

  document.querySelectorAll("[data-profile-link='email']").forEach((element) => {
    element.setAttribute("href", `mailto:${profile.email}`);
  });

  document.querySelectorAll("[data-profile-link='github']").forEach((element) => {
    element.setAttribute("href", profile.github);
  });

  document.querySelectorAll("[data-profile-link='scholar']").forEach((element) => {
    element.setAttribute("href", profile.scholar);
  });

  document.querySelectorAll("[data-profile-image]").forEach((image) => {
    const fallback = image.nextElementSibling;
    if (!profile.photo) {
      image.hidden = true;
      if (fallback) fallback.hidden = false;
      return;
    }

    image.src = profile.photo;
    image.hidden = false;
    if (fallback) fallback.hidden = true;
    image.addEventListener("error", () => {
      image.hidden = true;
      if (fallback) fallback.hidden = false;
    });
  });

  if (profile.name) {
    document.title = document.title.replace(/Yoorim Son|Yoori/g, profile.name);
  }
}

function renderStatus(updates) {
  const statusGrid = document.querySelector("#status-grid");
  if (!statusGrid) return;
  const latest = sortByRecent(updates).slice(0, 3);

  statusGrid.innerHTML = latest
    .map(
      (item) => `
        <article class="status-card">
          <div>
            <div class="status-top">
              <span class="status-label">${item.type}</span>
              <span class="status-date">${formatDate(item.date)}</span>
            </div>
            <h3>${item.title}</h3>
            <p>${item.summary}</p>
          </div>
          <div class="timeline-tags">
            ${item.tags.map((tag) => `<span>#${tag}</span>`).join("")}
          </div>
        </article>
      `
    )
    .join("");
}

function renderResearch(items) {
  const researchList = document.querySelector("#research-list");
  if (!researchList) return;

  researchList.innerHTML = items
    .map(
      (item) => `
        <article class="research-topic">
          <div>
            <h3>${item.title}</h3>
            <p>${item.summary}</p>
          </div>
          <div class="research-meta">
            <span>${item.status}</span>
            <span>${item.cadence}</span>
          </div>
        </article>
      `
    )
    .join("");
}

function renderProjects(items) {
  const projectList = document.querySelector("#project-list");
  if (!projectList) return;

  projectList.innerHTML = items
    .map(
      (item) => `
        <article class="project-card">
          <div>
            <span class="project-state">${item.state}</span>
            <h3>${item.title}</h3>
            <p>${item.summary}</p>
          </div>
          <footer>
            ${item.tags.map((tag) => `<span class="tag">${tag}</span>`).join("")}
          </footer>
        </article>
      `
    )
    .join("");
}

function renderTimeline(updates, filter = "all") {
  const timeline = document.querySelector("#timeline");
  if (!timeline) return;
  const filtered =
    filter === "all" ? updates : updates.filter((item) => item.type === filter || item.tags.includes(filter));

  timeline.innerHTML = sortByRecent(filtered)
    .map(
      (item) => `
        <article class="timeline-item">
          <time class="timeline-date" datetime="${item.date}">${formatDate(item.date)}</time>
          <div>
            <span class="status-label">${item.type}</span>
            <h3>${item.title}</h3>
            <p>${item.summary}</p>
            <div class="timeline-tags">
              ${item.tags.map((tag) => `<span>#${tag}</span>`).join("")}
            </div>
          </div>
        </article>
      `
    )
    .join("");
}

function bindFilters(updates) {
  const tabs = document.querySelectorAll(".filter-tab");

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((current) => current.classList.remove("is-active"));
      tab.classList.add("is-active");
      renderTimeline(updates, tab.dataset.filter);
    });
  });
}

function updateMetadata(updates) {
  const latest = sortByRecent(updates)[0];
  const year = document.querySelector("#year");
  const lastUpdated = document.querySelector("#last-updated");

  if (year) year.textContent = new Date().getFullYear();
  if (lastUpdated) lastUpdated.textContent = latest ? formatDate(latest.date) : "No updates yet";
}

async function init() {
  const [profile, updates, projects, research] = await Promise.all([
    getJson("./content/profile.json", "profile"),
    getJson("./content/updates.json", "updates"),
    getJson("./content/projects.json", "projects"),
    getJson("./content/research.json", "research")
  ]);

  renderProfile(profile);
  renderStatus(updates);
  renderResearch(research);
  renderProjects(projects);
  renderTimeline(updates);
  bindFilters(updates);
  updateMetadata(updates);
}

init();
