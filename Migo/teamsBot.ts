import * as ACData from "adaptivecards-templating";
import { ActivityTypes } from "@microsoft/agents-activity";
import {
  AgentApplication,
  AttachmentDownloader,
  MemoryStorage,
  MessageFactory,
  CardFactory,
  TurnContext,
  TurnState,
} from "@microsoft/agents-hosting";
import { version } from "@microsoft/agents-hosting/package.json";
import feedbackCard from "./adaptiveCards/feedback.json";
import tableCard from "./adaptiveCards/table.json";

interface ConversationState {
  count: number;
}
type ApplicationTurnState = TurnState<ConversationState>;

const downloader = new AttachmentDownloader();

// Define storage and application
const storage = new MemoryStorage();
export const teamsBot = new AgentApplication<ApplicationTurnState>({
  storage,
  fileDownloaders: [downloader],
});

// Listen for user to say '/reset' and then delete conversation state
teamsBot.message("/reset", async (context: TurnContext, state: ApplicationTurnState) => {
  state.deleteConversationState();
  await context.sendActivity("Ok I've deleted the current conversation state.");
});

teamsBot.message("/count", async (context: TurnContext, state: ApplicationTurnState) => {
  const count = state.conversation.count ?? 0;
  await context.sendActivity(`The count is ${count}`);
});

teamsBot.message("/diag", async (context: TurnContext, state: ApplicationTurnState) => {
  await state.load(context, storage);
  await context.sendActivity(JSON.stringify(context.activity));
});

teamsBot.message("/state", async (context: TurnContext, state: ApplicationTurnState) => {
  await state.load(context, storage);
  await context.sendActivity(JSON.stringify(state));
});

teamsBot.message("/runtime", async (context: TurnContext, state: ApplicationTurnState) => {
  const runtime = {
    nodeversion: process.version,
    sdkversion: version,
  };
  await context.sendActivity(JSON.stringify(runtime));
});

teamsBot.message("/typing", async (context: TurnContext, state: ApplicationTurnState) => {
  const activity = MessageFactory.text("typing...");
  activity.type = ActivityTypes.Typing;
  await context.sendActivity(activity);

  await new Promise((resolve) => setTimeout(resolve, 5000));
  await context.sendActivity(`and that's 5 sec typing...`);
});

teamsBot.message("/md1", async (context: TurnContext, state: ApplicationTurnState) => {
  const activity = MessageFactory.text(`
**bold text**

_italic text_

~strikethrough~

- Item 1
- Item 2
- Item 3

1. Green
2. Orange
3. Blue

[Hyperlink](https://www.microsoft.com)

| **Use Case**               | **Benefit of RAG**                                      |
|---------------------------|----------------------------------------------------------|
| Customer Support          | Answers grounded in company documentation                |
| Legal/Compliance Search   | Accurate retrieval from legal texts                      |
| Healthcare Q&A            | Contextual responses based on medical literature         |
| Enterprise Knowledge Base | Real-time access to internal documents                   |
| Research Assistants       | Summarizing and citing academic papers                   |

\`[code text]\`

> [block quote]

\`\`\`[code block]
`);

  await context.sendActivity(activity);
});

teamsBot.message("/md2", async (context: TurnContext, state: ApplicationTurnState) => {
  const info = `
**bold text**

_italic text_

~strikethrough~

- Item 1
- Item 2
- Item 3

1. Green
2. Orange
3. Blue

[Hyperlink](https://www.microsoft.com)

| **Use Case**               | **Benefit of RAG**                                      |
|---------------------------|----------------------------------------------------------|
| Customer Support          | Answers grounded in company documentation                |
| Legal/Compliance Search   | Accurate retrieval from legal texts                      |
| Healthcare Q&A            | Contextual responses based on medical literature         |
| Enterprise Knowledge Base | Real-time access to internal documents                   |
| Research Assistants       | Summarizing and citing academic papers                   |

\`[code text]\`

> [block quote]

\`\`\`[code block]
`;

  const cardJson = new ACData.Template(feedbackCard).expand({
    $root: {
      body: info,
    },
  });

  const activity = MessageFactory.attachment(CardFactory.adaptiveCard(cardJson));
  if (cardJson) {
    await context.sendActivity(activity);
  }
});

teamsBot.message("/table", async (context: TurnContext, state: ApplicationTurnState) => {
  const info = `
**bold text**

_italic text_

~strikethrough~

- Item 1
- Item 2
- Item 3

1. Green
2. Orange
3. Blue

[Hyperlink](https://www.microsoft.com)
`;

  const cardJson = new ACData.Template(tableCard).expand({
    $root: {
      body: info,
    },
  });

  const activity = MessageFactory.attachment(CardFactory.adaptiveCard(cardJson));
  if (cardJson) {
    await context.sendActivity(activity);
  }
});

teamsBot.message("/stream1", async (context: TurnContext, state: ApplicationTurnState) => {
  const info = `Retrieval-Augmented Generation (RAG) is an AI architecture that enhances the capabilities of generative models by integrating a retrieval mechanism that fetches relevant external documents or data in response to a user query. This retrieved information is then used as context for the generative model to produce more accurate, relevant, and up-to-date responses. By grounding outputs in real-world data, RAG significantly reduces hallucinations and improves factual reliability, making it ideal for applications like customer support, legal research, healthcare Q&A, enterprise knowledge management, and academic summarization.`;
  
  // Send initial message
  const initialMessage = MessageFactory.text("typing...");
  const sentActivity = await context.sendActivity(initialMessage);
  
  // Loop through each word in the paragraph and update the sent message
  const words = info.split(/\s+/);
  let accumulatedText = "";
  
  for (const word of words) {
    accumulatedText += (accumulatedText ? " " : "") + word;
    
    const cardJson = new ACData.Template(feedbackCard).expand({
      $root: {
        body: accumulatedText,
      },
    });

    // Create updated activity with accumulated text
    const updatedActivity = MessageFactory.attachment(CardFactory.adaptiveCard(cardJson));
    updatedActivity.id = sentActivity.id;

    if (cardJson) {
      await context.updateActivity(updatedActivity);
    }
  }
});

teamsBot.message("/stream2", async (context: TurnContext, state: ApplicationTurnState) => {
  const info = `
**bold text**

_italic text_

~strikethrough~

- Item 1
- Item 2
- Item 3

1. Green
2. Orange
3. Blue

[Hyperlink](https://www.microsoft.com)

| **Use Case**               | **Benefit of RAG**                                      |
|---------------------------|----------------------------------------------------------|
| Customer Support          | Answers grounded in company documentation                |
| Legal/Compliance Search   | Accurate retrieval from legal texts                      |
| Healthcare Q&A            | Contextual responses based on medical literature         |
| Enterprise Knowledge Base | Real-time access to internal documents                   |
| Research Assistants       | Summarizing and citing academic papers                   |

\`[code text]\`

> [block quote]

\`\`\`[code block]
`;

  const info2 = `
**bold text**

_italic text_

~strikethrough~

- Item 1
- Item 2
- Item 3

1. Green
2. Orange
3. Blue

[Hyperlink](https://www.microsoft.com)
`;
  
  // Send initial message
  const initialMessage = MessageFactory.text("typing...");
  const sentActivity = await context.sendActivity(initialMessage);
  
  // Loop through each word in the paragraph and update the sent message
  const words = info.split(" ");
  let accumulatedText = "";
  
  for (const word of words) {
    accumulatedText += (accumulatedText ? " " : "") + word;
    
    const cardJson = new ACData.Template(feedbackCard).expand({
      $root: {
        body: accumulatedText,
      },
    });

    // Create updated activity with accumulated text
    const updatedActivity = MessageFactory.text(accumulatedText);
    updatedActivity.id = sentActivity.id;

    if (cardJson) {
      await context.updateActivity(updatedActivity);
      // add 100ms delay
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
  }

  // After the loop, send the final message with the full text and table
  const cardJson = new ACData.Template(tableCard).expand({
    $root: {
      body: info2,
    },
  });

  const updatedActivity = MessageFactory.attachment(CardFactory.adaptiveCard(cardJson));
  updatedActivity.id = sentActivity.id;

  if (cardJson) {
    await context.updateActivity(updatedActivity);
  }
});

teamsBot.conversationUpdate(
  "membersAdded",
  async (context: TurnContext, state: ApplicationTurnState) => {
    await context.sendActivity(
      `Hi there! I'm an echo bot running on Agents SDK version ${version} that will echo what you said to me.`
    );
  }
);

// Listen for ANY message to be received. MUST BE AFTER ANY OTHER MESSAGE HANDLERS
teamsBot.activity(
  ActivityTypes.Message,
  async (context: TurnContext, state: ApplicationTurnState) => {
    // Increment count state
    let count = state.conversation.count ?? 0;
    state.conversation.count = ++count;

    // Echo back users request
    await context.sendActivity(`[${count}] you said: ${context.activity.text}`);

    const cardJson = new ACData.Template(feedbackCard).expand({
      $root: {
        body: "Congratulations! Your hello world bot is running. Click the button below to trigger an action.",
      },
    });

    if (cardJson) {
      await context.sendActivity(MessageFactory.attachment(CardFactory.adaptiveCard(cardJson)));
    }
  }
);

teamsBot.activity(ActivityTypes.Invoke, async (context: TurnContext, state: ApplicationTurnState) => {
  const value = context.activity.value;

  if (value && value['action']['verb'] === 'user_like') {
      // You can store this in a database or trigger a backend process
      await context.sendActivity(`Your like feedback has been recorded.`);
  }

  if (value && value['action']['verb'] === 'user_dislike') {
      // You can store this in a database or trigger a backend process
      await context.sendActivity(`Your dislike feedback has been recorded.`);
  }
});

teamsBot.activity(/^message/, async (context: TurnContext, state: ApplicationTurnState) => {
  await context.sendActivity(`Matched with regex: ${context.activity.type}`);
});

teamsBot.activity(
  async (context: TurnContext) => Promise.resolve(context.activity.type === "message"),
  async (context, state) => {
    await context.sendActivity(`Matched function: ${context.activity.type}`);
  }
);
