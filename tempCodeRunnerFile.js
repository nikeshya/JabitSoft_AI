import fs from "fs";
import path from "path";
import { analyzeSession } from "./quality_checker.js";

const DATA_PATH = path.join("./clean_chat_history.json");
const OUTPUT_PATH = path.join("./quality_reports.json");

function loadSessions() {
  return JSON.parse(fs.readFileSync(DATA_PATH, "utf8"));
}

function saveReports(reports) {
  fs.writeFileSync(
    OUTPUT_PATH,
    JSON.stringify(reports, null, 2)
  );
}

async function run() {

  console.log("Starting chat quality check...\n");

  const sessions = loadSessions().slice(0,2);
  const reports = [];

  for (const session of sessions) {

    console.log(`Checking: ${session.session_id}`);

    const result = await analyzeSession(session);

    reports.push(result);
  }

  saveReports(reports);

  console.log("\nDone.");
  console.log(`Saved ${reports.length} reports.`);
}

run();
