require("dotenv").config();
const express = require("express");
const axios   = require("axios");
const cors    = require("cors");
const path    = require("path");

const app  = express();
const PORT = parseInt(process.env.PORT || "3000", 10);

app.use(cors());
app.use(express.json({ limit: "1mb" }));
app.use(express.static(path.join(__dirname, "public")));

// ─── IBM IAM token cache ────────────────────────────────────────────────────
let cachedToken = null;
let tokenExpiry  = 0;

async function getIAMToken() {
  const now = Date.now();
  if (cachedToken && now < tokenExpiry) return cachedToken;

  const params = new URLSearchParams();
  params.append("grant_type", "urn:ibm:params:oauth:grant-type:apikey");
  params.append("apikey", process.env.WATSONX_API_KEY);

  const response = await axios.post(
    "https://iam.cloud.ibm.com/identity/token",
    params,
    {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      timeout: 15000,
    }
  );

  cachedToken = response.data.access_token;
  tokenExpiry  = now + (response.data.expires_in - 300) * 1000;
  console.log("✅ IBM IAM token refreshed successfully");
  return cachedToken;
}

// ─── System prompt ──────────────────────────────────────────────────────────
const SYSTEM_PROMPT = `You are Aria, an expert AI Travel Planner Agent powered by IBM Granite on watsonx.ai. You help users plan trips efficiently and intelligently.

Your capabilities:
- Destination recommendations based on preferences, travel style, budget, and constraints
- Detailed day-by-day itineraries with time slots, morning/afternoon/evening splits
- Transport advice: flights, trains, buses, car rentals with cost ranges
- Accommodation: hotels, hostels, Airbnb, resorts with price estimates
- Complete budget breakdowns: flights, accommodation, food, activities, transport, misc
- Weather guidance and best time to visit each destination
- Packing lists tailored to destination and season
- Visa and travel document requirements
- Local food recommendations: dishes, restaurants, street food
- Cultural tips, etiquette, safety advisories, and hidden gems

Response rules:
- Use markdown: headers (##), bullet points (-), bold (**text**)
- For itineraries use: Day 1: Title, Day 2: Title format
- For budgets use a clear table or structured list with USD estimates
- Always end with a helpful follow-up question
- If destination/duration/budget not specified, ask 2-3 clarifying questions first
- Be enthusiastic, warm, and highly specific — no generic advice`;

// ─── /api/chat ──────────────────────────────────────────────────────────────
app.post("/api/chat", async (req, res) => {
  const { messages } = req.body;

  if (!messages || !Array.isArray(messages) || messages.length === 0) {
    return res.status(400).json({ error: "messages array is required and must not be empty." });
  }

  if (!process.env.WATSONX_API_KEY) {
    return res.status(503).json({ error: "WATSONX_API_KEY is not set in .env file." });
  }
  if (!process.env.WATSONX_PROJECT_ID) {
    return res.status(503).json({ error: "WATSONX_PROJECT_ID is not set in .env file." });
  }

  try {
    console.log(`📨 /api/chat called — ${messages.length} message(s)`);

    const token = await getIAMToken();

    const payload = {
      model_id:   process.env.WATSONX_MODEL_ID || "ibm/granite-4-h-small",
      project_id: process.env.WATSONX_PROJECT_ID,
      messages: [
        { role: "system", content: SYSTEM_PROMPT },
        ...messages,
      ],
      parameters: {
        max_new_tokens:     2048,
        temperature:        0.7,
        top_p:              0.9,
        repetition_penalty: 1.05,
      },
    };

    const watsonxURL = process.env.WATSONX_URL ||
      "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29";

    console.log(`🤖 Calling watsonx: ${payload.model_id}`);

    const response = await axios.post(watsonxURL, payload, {
      headers: {
        Authorization:  `Bearer ${token}`,
        "Content-Type": "application/json",
        Accept:         "application/json",
      },
      timeout: 60000,
    });

    const reply =
      response.data?.choices?.[0]?.message?.content ||
      response.data?.results?.[0]?.generated_text ||
      "I'm sorry, I could not generate a response. Please try again.";

    console.log(`✅ Granite replied (${reply.length} chars)`);
    res.json({ reply });

  } catch (err) {
    const status  = err?.response?.status  || 500;
    const detail  =
      err?.response?.data?.errors?.[0]?.message ||
      err?.response?.data?.error                ||
      err?.response?.data?.message              ||
      err.message                               ||
      "Unknown error";

    console.error(`❌ watsonx error [${status}]:`, detail);
    console.error("Full error data:", JSON.stringify(err?.response?.data || {}, null, 2));

    // Return a user-friendly message + the real detail for debugging
    res.status(status).json({
      error:  `IBM Granite API error: ${detail}`,
      status: status,
      detail: err?.response?.data || null,
    });
  }
});

// ─── /api/test  (diagnose connection without a chat message) ────────────────
app.get("/api/test", async (req, res) => {
  const results = { env: {}, iam: null, watsonx: null };

  results.env = {
    WATSONX_API_KEY:    process.env.WATSONX_API_KEY    ? "SET ✅" : "MISSING ❌",
    WATSONX_PROJECT_ID: process.env.WATSONX_PROJECT_ID ? "SET ✅" : "MISSING ❌",
    WATSONX_MODEL_ID:   process.env.WATSONX_MODEL_ID   || "ibm/granite-4-h-small (default)",
    WATSONX_URL:        process.env.WATSONX_URL        || "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29 (default)",
  };

  // Step 1: IBM IAM token
  try {
    await getIAMToken();
    results.iam = "Token obtained ✅";
  } catch (e) {
    results.iam = `FAILED ❌: ${e?.response?.data?.errorMessage || e.message}`;
    return res.status(500).json(results);
  }

  // Step 2: Quick watsonx ping
  try {
    const token = await getIAMToken();
    const payload = {
      model_id:   process.env.WATSONX_MODEL_ID || "ibm/granite-4-h-small",
      project_id: process.env.WATSONX_PROJECT_ID,
      messages: [
        { role: "system",  content: "You are a helpful assistant. Reply very briefly." },
        { role: "user",    content: "Say OK in one word." },
      ],
      parameters: { max_new_tokens: 10, temperature: 0.1 },
    };
    const url = process.env.WATSONX_URL ||
      "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29";
    const r = await axios.post(url, payload, {
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json", Accept: "application/json" },
      timeout: 20000,
    });
    const text = r.data?.choices?.[0]?.message?.content || JSON.stringify(r.data);
    results.watsonx = `IBM Granite responded ✅: "${text.trim()}"`;
  } catch (e) {
    const detail = e?.response?.data?.errors?.[0]?.message || e?.response?.data?.error || e.message;
    results.watsonx = `FAILED ❌: ${detail}`;
    console.error("Test endpoint watsonx error:", e?.response?.data || e.message);
    return res.status(500).json(results);
  }

  res.json(results);
});

// ─── /api/health ────────────────────────────────────────────────────────────
app.get("/api/health", (req, res) => {
  res.json({
    status: "ok",
    model:  process.env.WATSONX_MODEL_ID || "ibm/granite-4-h-small",
    configured: {
      apiKey:    !!process.env.WATSONX_API_KEY,
      projectId: !!process.env.WATSONX_PROJECT_ID,
    },
  });
});

// ─── Catch-all → frontend ───────────────────────────────────────────────────
app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// ─── Start server with port-conflict handling ───────────────────────────────
const server = app.listen(PORT, () => {
  console.log("\n╔══════════════════════════════════════════════╗");
  console.log("║   ✈  Aria — AI Travel Planner Agent          ║");
  console.log("╚══════════════════════════════════════════════╝");
  console.log(`\n🌐 App:     http://localhost:${PORT}`);
  console.log(`🔬 Test:    http://localhost:${PORT}/api/test`);
  console.log(`❤️  Health:  http://localhost:${PORT}/api/health`);
  console.log(`🤖 Model:   ${process.env.WATSONX_MODEL_ID || "ibm/granite-4-h-small"}`);
  console.log(`🔑 API Key: ${process.env.WATSONX_API_KEY ? "✅ Configured" : "❌ MISSING"}`);
  console.log(`📁 Project: ${process.env.WATSONX_PROJECT_ID ? "✅ Configured" : "❌ MISSING"}`);
  console.log("\nPress Ctrl+C to stop.\n");
});

server.on("error", (err) => {
  if (err.code === "EADDRINUSE") {
    console.error(`\n❌ Port ${PORT} is already in use!`);
    console.error("   Run this command to free it:");
    console.error(`   Stop-Process -Id (netstat -ano | Select-String ':${PORT}' | ForEach-Object { ($_ -split '\\s+')[-1] } | Select-Object -First 1) -Force\n`);
    process.exit(1);
  } else {
    console.error("Server error:", err);
    process.exit(1);
  }
});
