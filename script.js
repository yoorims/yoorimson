const fallbackData = {
  profile: {
    "name": "Yoorim Son",
    "initials": "YS",
    "photo": "./assets/profile.png",
    "role": "M.A. Student in Economics",
    "tagline": "Development Economics and Digital Infrastructure",
    "bio": "I am an M.A. student in Economics at Sogang University, advised by Professor Hyunjoo Yang. My research interests lie in development economics and applied microeconomics, with a focus on digital infrastructure, local economic development, spatial inequality, and economic measurement using geospatial and satellite data. My current research, with Hyunjoo Yang, examines how mobile broadband upgrading during South Africa's 2021–2024 spectrum transition differs across municipalities by initial service quality, baseline poverty, and regulatory priority status. Using quarterly Ookla measurements, we track low-speed service, average performance, and high-speed expansion to distinguish local improvements from changes in gaps across places. I work as a Research Assistant to Hyunjoo Yang at the Sogang Spatial Economics & AI Lab and to BooKang Seol (LSE) on MIRACLE.",
    "affiliation": "M.A. in Economics, Sogang University",
    "location": "Seoul, Korea",
    "email": "yoorim0917@gmail.com",
    "scholar": "https://scholar.google.com/"
  },
  projects: [
    {
      "title": "Sogang Spatial Economics & AI Lab",
      "state": "Research Assistant to Hyunjoo Yang",
      "period": "Apr 2026–Present · Sogang University",
      "summary": "Led by Hyunjoo Yang, the lab brings together geospatial data, economics, and machine learning. My work focuses on agricultural prediction: constructing maize and rice ground-truth datasets, completing rice sampling, and building XGBoost features to predict cultivated area across Asian countries.",
      "url": "https://hy263.github.io/projects/",
      "linkLabel": "Lab website",
      "tags": [
        "remote sensing",
        "machine learning",
        "agriculture"
      ]
    },
    {
      "title": "MIRACLE — Subnational Economic Data for South Korea, 1960–1989",
      "state": "Research Assistant to BooKang Seol (LSE)",
      "period": "Nov 2025–Present",
      "summary": "MIRACLE is building a consistent township-year economic panel from municipal statistical yearbooks and other archival records. I completed administrative-region data collection and now work on OCR-based extraction and processing of historical statistical records.",
      "url": "https://miracle.bookangseol.com/",
      "linkLabel": "Project website",
      "tags": [
        "historical data",
        "OCR",
        "geographic harmonization"
      ]
    },
    {
      "title": "Satellite-Based Measurement of North Korean Economic Activity",
      "state": "Research Assistant to Hyunjoo Yang",
      "period": "Bank of Korea",
      "summary": "Uses daytime satellite imagery, atmospheric gas data, and AI to measure North Korean industrial production and economic activity. I contribute as a Research Assistant to Hyunjoo Yang.",
      "tags": [
        "economic measurement",
        "satellite data"
      ]
    }
  ],
  research: [
    {
      title: "Digital Infrastructure and Development",
      summary:
        "I am interested in how improvements in digital connectivity and other forms of infrastructure shape local economic development, particularly when the benefits of new infrastructure are distributed unevenly across space."
    },
    {
      title: "Spatial Development and Inequality",
      summary:
        "I study spatial differences in access to infrastructure and economic opportunities, and how these differences contribute to uneven patterns of local and regional development."
    },
    {
      title: "Remote Sensing and Economic Measurement",
      summary:
        "I am interested in combining conventional economic data with satellite imagery, geospatial information, and other nontraditional data sources to measure economic activity where standard administrative or survey data are limited."
    },
    {
      title: "African Development",
      summary:
        "My regional interests center on African economies, with particular attention to infrastructure, technological change, local development, and spatial inequality."
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

function renderProfile(profile) {
  document.querySelectorAll("[data-profile]").forEach((element) => {
    const key = element.dataset.profile;
    if (profile[key]) element.textContent = profile[key];
  });

  document.querySelectorAll("[data-profile-link='email']").forEach((element) => {
    element.setAttribute("href", `mailto:${profile.email}`);
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

function renderResearch(items) {
  const researchList = document.querySelector("#research-list");
  if (!researchList) return;

  researchList.innerHTML = items
    .map(
      (item) => `
        <article class="research-topic">
          <h3>${item.title}</h3>
          <p>${item.summary}</p>
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
            ${item.period ? `<p class="meta-line">${item.period}</p>` : ""}
            <p>${item.summary}</p>
            ${item.url ? `<p><a href="${item.url}">${item.linkLabel}</a></p>` : ""}
          </div>
          <footer>
            ${item.tags.map((tag) => `<span class="tag">${tag}</span>`).join("")}
          </footer>
        </article>
      `
    )
    .join("");
}

function updateYear() {
  const year = document.querySelector("#year");

  if (year) year.textContent = new Date().getFullYear();
}

async function init() {
  const [profile, projects, research] = await Promise.all([
    getJson("./content/profile.json", "profile"),
    getJson("./content/projects.json", "projects"),
    getJson("./content/research.json", "research")
  ]);

  renderProfile(profile);
  renderResearch(research);
  renderProjects(projects);
  updateYear();
}

init();
