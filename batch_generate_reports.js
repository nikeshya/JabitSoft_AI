import fs from "fs";
import path from "path";
import { analyzeSession } from "./quality_checker.js";

const DATA_PATH = path.join("./clean_chat_history.json");

const MODEL_NAME = process.argv[2] || "mistral";
const SAFE_MODEL_NAME = MODEL_NAME.replace(":", "_");

const OUTPUT_PATH = path.join(`./quality_reports_${SAFE_MODEL_NAME}.json`);


const BATCH_SIZE = 10;
const TARGET_SESSION_IDS = [
  "session-1764309018004-cj65e6h",
  "session-1764308636158-277xtek",
  "session-1761525127868-vgm3g9c",
  "session-1763421553380-yxcpnid",
  "session-1763422040022-81orvrq",
  "session-1763422665024-j7zqjw2",
  "session-1763422905513-4f6pe7e",
  "session-1763423518396-exg9i4w",
  "session-1763423304974-4tjoofd",
  "session-1763423679567-lbwttom"
];


// ---------- Load Functions ----------

function loadSessions() {
  return JSON.parse(fs.readFileSync(DATA_PATH, "utf8"));
}

function loadExistingReports() {
  if (!fs.existsSync(OUTPUT_PATH)) return [];
  return JSON.parse(fs.readFileSync(OUTPUT_PATH, "utf8"));
}

function saveReports(reports) {
  fs.writeFileSync(
    OUTPUT_PATH,
    JSON.stringify(reports, null, 2),
    "utf8"
  );
}

// ---------- Main Batch Runner ----------

async function runBatch() {
  console.log("Starting batch analysis of chatbot sessions...\n");

  const sessions = loadSessions();
  let reports = loadExistingReports();

  const processedIds = new Set(
    reports.map(r => r.session_id)
  );

  const remainingSessions = sessions.filter(
  s =>
    TARGET_SESSION_IDS.includes(s.session_id) &&
    !processedIds.has(s.session_id)
);


  console.log(`Total sessions: ${sessions.length}`);
  console.log(`Already processed: ${processedIds.size}`);
  console.log(`Remaining: ${remainingSessions.length}\n`);

  for (let i = 0; i < remainingSessions.length; i += BATCH_SIZE) {
    const batch = remainingSessions.slice(i, i + BATCH_SIZE);

    console.log(
      `Processing batch ${Math.floor(i / BATCH_SIZE) + 1} (${batch.length} sessions)`
    );

    for (let j = 0; j < batch.length; j++) {
      const session = batch[j];
      const index = processedIds.size + 1;

      console.log(
        ` (${index}/${sessions.length}) Analyzing: ${session.session_id}`
      );

      try {
        const report = await analyzeSession(session, MODEL_NAME);

        reports.push({
          ...report,
          generated_at: new Date().toISOString()
        });

        processedIds.add(session.session_id);
      } catch (err) {
        console.error(
          ` Error processing ${session.session_id}:`,
          err.message
        );
      }
    }

    // Save after every 100 sessions
    saveReports(reports);

    console.log(
      `Batch saved (${processedIds.size}/${sessions.length} completed)\n`
    );
  }

  console.log("All sessions processed successfully!");
}

runBatch();
