import { configDotenv } from "dotenv";
import { AppConfig } from "./types";

configDotenv()

/* eslint-disable @typescript-eslint/no-non-null-assertion */
export const config: AppConfig = {
  APP_TOKEN: process.env.APP_TOKEN!,
  OAUTH_TOKEN: process.env.OAUTH_TOKEN!,
  SIGNING_SECRET: process.env.SIGNING_SECRET!,
  JIRA_TOKEN: process.env.JIRA_TOKEN!,
  PORT: Number(process.env.PORT)
}
