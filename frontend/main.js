console.log("✅ main.js loaded");

const API_UPLOAD = "http://127.0.0.1:8000/upload-resume";
const API_CHAT = "http://127.0.0.1:8000/chat";

// --------- elements ----------
const formEl = document.getElementById("resume-form");
const analyzeBtn = document.getElementById("analyze-btn");

const statusEl = document.getElementById("status");
const scoreEl = document.getElementById("score");
const roleOutEl = document.getElementById("roleOut");
const skillsEl = document.getElementById("skills");
const previewEl = document.getElementById("preview");

const chatLogEl = document.getElementById("chatLog");
const chatInputEl = document.getElementById("chatInput");
const sendChatBtn = document.getElementById("sendChat");

// track if analysis is done
let analyzedOnce = false;

function setStatus(text) {
  statusEl.textContent = text;
}

function appendChat(sender, text) {
  const wrap = document.createElement("div");
  wrap.style.marginBottom = "10px";

  const who = document.createElement("div");
  who.style.fontWeight = "700";
  who.style.marginBottom = "4px";
  who.textContent = sender;

  const msg = document.createElement("div");
  msg.style.whiteSpace = "pre-wrap";
  msg.textContent = text;

  wrap.appendChild(who);
  wrap.appendChild(msg);

  chatLogEl.appendChild(wrap);
  chatLogEl.scrollTop = chatLogEl.scrollHeight;
}

// prevent page reload if user presses Enter in the form
formEl.addEventListener("submit", (e) => {
  e.preventDefault();
});

async function analyzeResume() {
  const file = document.getElementById("resume-file").files[0];
  const jobRole = document.getElementById("job-role").value;
  const jobDesc = document.getElementById("job-desc").value;

  if (!file) {
    setStatus("Please choose a resume file.");
    return;
  }
  if (!jobDesc.trim()) {
    setStatus("Please paste the job description.");
    return;
  }

  setStatus("Analyzing...");

  const fd = new FormData();
  fd.append("file", file);
  fd.append("job_role", jobRole);
  fd.append("job_description", jobDesc);

  try {
    const res = await fetch(API_UPLOAD, {
      method: "POST",
      body: fd,
    });

    const contentType = res.headers.get("content-type") || "";
    const data = contentType.includes("application/json")
      ? await res.json()
      : { detail: await res.text() };

    if (!res.ok) throw new Error(data.detail || `Request failed (${res.status})`);

    // update UI
    scoreEl.textContent = `${data.score} / 10`;
    roleOutEl.textContent = (data.job_role || "-").replaceAll("_", " ");
    skillsEl.textContent = (data.required_skills || []).join(", ") || "-";
    previewEl.textContent = data.resume_preview || "";

    analyzedOnce = true;
    setStatus("Done ✅");

    // helpful chat hint
    chatLogEl.innerHTML = "";
    appendChat("System", "Analysis saved. Now you can ask questions in the chatbot.");
  } catch (err) {
    console.error(err);
    setStatus("Error: " + err.message);
  }
}

analyzeBtn.addEventListener("click", analyzeResume);

// --------- Chat ----------
async function sendChat() {
  const question = (chatInputEl.value || "").trim();

  if (!analyzedOnce) {
    appendChat("System", "Please click Analyze first, then ask questions.");
    return;
  }

  if (!question) return;

  appendChat("You", question);
  chatInputEl.value = "";

  const fd = new FormData();
  fd.append("message", question);

  try {
    sendChatBtn.disabled = true;

    const res = await fetch(API_CHAT, {
      method: "POST",
      body: fd
    });

    const contentType = res.headers.get("content-type") || "";
    const data = contentType.includes("application/json")
      ? await res.json()
      : { detail: await res.text() };

    if (!res.ok) throw new Error(data.detail || `Chat failed (${res.status})`);

    appendChat("Assistant", data.reply || "(no reply)");
  } catch (err) {
    console.error(err);
    appendChat("System", "Error: " + err.message);
  } finally {
    sendChatBtn.disabled = false;
  }
}

sendChatBtn.addEventListener("click", sendChat);

// allow Enter to send message
chatInputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    sendChat();
  }
});
