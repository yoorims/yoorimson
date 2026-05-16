import { readFile } from "node:fs/promises";

const files = ["content/updates.json", "content/projects.json", "content/research.json"];
const profileFile = "content/profile.json";

async function checkJson(path) {
  const raw = await readFile(path, "utf8");
  const parsed = JSON.parse(raw);

  if (!Array.isArray(parsed)) {
    throw new Error(`${path} should contain an array.`);
  }

  if (parsed.length === 0) {
    throw new Error(`${path} should contain at least one item.`);
  }

  return parsed.length;
}

const counts = await Promise.all(files.map(checkJson));
const profile = JSON.parse(await readFile(profileFile, "utf8"));

["name", "initials", "tagline", "bio", "email"].forEach((key) => {
  if (!profile[key]) {
    throw new Error(`${profileFile} is missing "${key}".`);
  }
});

console.log("Content check passed:");
files.forEach((file, index) => {
  console.log(`- ${file}: ${counts[index]} items`);
});
console.log(`- ${profileFile}: ${profile.name}`);
