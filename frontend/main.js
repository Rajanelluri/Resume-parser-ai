console.log("✅ main.js loaded");

const API_URL = "http://127.0.0.1:8000/upload-resume";

// Grab elements safely
function el(id) {
  const node = document.getElementById(id);
  if (!node) throw new Error(`Missing element with id="${id}" in index.html`);
  return node;
}

const statusEl = el("status");
const scoreEl = el("score");
const roleOutEl = el("roleOut");
const skillsEl = el("skills");
const previewEl = el("preview");
const formEl = el("resume-form");
const btnEl = el("analyze-btn");

async function analyze() {
  console.log("🟦 Analyze clicked");

  const fileInput = el("resume-file");
  const roleSelect = el("job-role");
  const jdText = el("job-desc");

  const file = fileInput.files[0];
  const jobRole = roleSelect.value;
  const jobDesc = jdText.value;

  if (!file) {
    statusEl.textContent = "Please choose a resume file.";
    console.warn("⚠️ No file selected");
    return;
  }

  if (!jobDesc.trim()) {
    statusEl.textContent = "Please paste a job description.";
    console.warn("⚠️ Job description empty");
    return;
  }

  statusEl.textContent = "Analyzing...";
  console.log("📦 Sending:", { filename: file.name, jobRole, jdLen: jobDesc.length });

  const fd = new FormData();
  fd.append("file", file);
  fd.append("job_role", jobRole);
  fd.append("job_description", jobDesc);

  try {
    const res = await fetch(API_URL, { method: "POST", body: fd });

    console.log("🟩 Response status:", res.status);

    const text = await res.text(); // read raw first (best for debugging)
    console.log("📨 Raw response:", text);

    let data;
    try {
      data = JSON.parse(text);
    } catch {
      throw new Error("Backend did not return JSON. Check backend response in terminal.");
    }

    if (!res.ok) {
      throw new Error(data.detail || `Request failed (${res.status})`);
    }

    // Update UI
    scoreEl.textContent = `${data.score}/10`;
    roleOutEl.textContent = (data.job_role || "-").replaceAll("_", " ");
    skillsEl.textContent = (data.required_skills || []).join(", ") || "-";
    previewEl.textContent = data.resume_preview || "";

    statusEl.textContent = "Done ✅";
    console.log("✅ UI updated successfully");
  } catch (err) {
    console.error("❌ Analyze failed:", err);
    statusEl.textContent = "Error: " + err.message;
  }
}

// Button click
btnEl.addEventListener("click", analyze);

// Safety: prevent form submit refresh if user presses Enter
formEl.addEventListener("submit", (e) => {
  e.preventDefault();
  analyze();
});
