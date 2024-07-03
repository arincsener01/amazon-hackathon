import { App } from "@slack/bolt";

import { config } from "./config";
import axios from "axios";
import { extractTextFromIssue } from "./util/extractTextFromIssue";

const app = new App({
  signingSecret: config.SIGNING_SECRET,
  appToken: config.APP_TOKEN,
  socketMode: true,
  token: config.OAUTH_TOKEN,
});

app.command("/question", async ({ ack, say, body, respond }) => {
  try {
    await ack();
    const { text, user_id } = body;
    await say(`Hello, <@${user_id}>, let me look at the codebase 👀`);
    const response = await axios.post("http://127.0.0.1:5000/chat", {
      question: text,
    });
    await respond({
      response_type: "in_channel",
      text: `Question: ${text}\n======\n${response.data.answer} \nRelated docs:\n${response.data.related_docs}`,
    });
  } catch (err) {
    await say(`Sorry I lost my node_modules folder 😢`);
  }
});

app.command("/jira", async ({ ack, say, body, respond }) => {
  try {
    await ack();
    const { text, user_id } = body;
    await say(
      `Hello, <@${user_id}>, let me look at the JIRA issue and codebase 👀`
    );
    const jiraResponse = await axios.get(
      `https://kontist.atlassian.net/rest/api/3/issue/${text}`,
      {
        headers: {
          Authorization: `Basic ${Buffer.from(
            `caglar.alkis@kontist.com:${config.JIRA_TOKEN}`
          ).toString("base64")}`,
          Accept: "application/json",
        },
      }
    );
    const { content } = jiraResponse.data.fields.description;
    const question = extractTextFromIssue(content);

    const aiResponse = await axios.post("http://127.0.0.1:5000/chat", {
      jira_description: question,
    });

    await respond({
      response_type: "in_channel",
      text: `Question: ${text}\n======\n${aiResponse.data.answer} \nRelated docs:\n${aiResponse.data.related_docs}`,
    });
  } catch (err) {
    console.error(err);
    await say(`Sorry I lost my node_modules folder 😢`);
  }
});

app.start(config.PORT);
