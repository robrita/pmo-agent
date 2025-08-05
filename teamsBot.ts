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
import { callAzureOpenAIStream } from "./openai";

interface ChatMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

interface ConversationData {
  user_id: string;
  messages: ChatMessage[];
}

interface ConversationState {
  count: number;
  chatCache?: Record<string, ConversationData>;
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
  // Reinitialize the chatCache after clearing state
  state.conversation.chatCache = {};
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
  const activity = MessageFactory.text("Thinking...");
  activity.type = ActivityTypes.Typing;
  await context.sendActivity(activity);

  await new Promise((resolve) => setTimeout(resolve, 5000));
  await context.sendActivity(`and that's 5 sec Thinking...`);
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
  await context.sendActivity(activity);
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
  await context.sendActivity(activity);
});

teamsBot.message("/stream1", async (context: TurnContext, state: ApplicationTurnState) => {
  const info = `Retrieval-Augmented Generation (RAG) is an AI architecture that enhances the capabilities of generative models by integrating a retrieval mechanism that fetches relevant external documents or data in response to a user query. This retrieved information is then used as context for the generative model to produce more accurate, relevant, and up-to-date responses. By grounding outputs in real-world data, RAG significantly reduces hallucinations and improves factual reliability, making it ideal for applications like customer support, legal research, healthcare Q&A, enterprise knowledge management, and academic summarization.`;
  
  // Send initial message
  const initialMessage = MessageFactory.text("Thinking...");
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

    await context.updateActivity(updatedActivity);
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
  const initialMessage = MessageFactory.text("Thinking...");
  const sentActivity = await context.sendActivity(initialMessage);
  
  // Loop through each word in the paragraph and update the sent message
  const words = info.split(" ");
  let accumulatedText = "";
  
  for (const word of words) {
    accumulatedText += (accumulatedText ? " " : "") + word;

    // Create updated activity with accumulated text
    const updatedActivity = MessageFactory.text(accumulatedText);
    updatedActivity.id = sentActivity.id;

    await context.updateActivity(updatedActivity);
    // add 100ms delay
    await new Promise((resolve) => setTimeout(resolve, 100));
  }

  // After the loop, send the final message with the full text and table
  const cardJson = new ACData.Template(tableCard).expand({
    $root: {
      body: info2,
    },
  });

  const updatedActivity = MessageFactory.attachment(CardFactory.adaptiveCard(cardJson));
  updatedActivity.id = sentActivity.id;

  await context.updateActivity(updatedActivity);
});

teamsBot.message("/openai", async (context: TurnContext, state: ApplicationTurnState) => {
  // Extract user message from the activity text, removing the "/openai" command
  const userMessage = context.activity.text?.replace("/openai", "").trim() || "Hello, how can you help me?";

  // Initialize chatCache if it doesn't exist
  if (!state.conversation.chatCache) {
    state.conversation.chatCache = {};
  }

  // Fetch the current cached messages
  const conversationId = context.activity.conversation?.id || "default";
  const chatCache = state.conversation.chatCache[conversationId] || { 
    user_id: context.activity.from?.id || "unknown", 
    messages: [] 
  };
  
  const messages: ChatMessage[] = [{ role: "system", content: "You are a helpful assistant." }];

  // Append chatCache.messages
  messages.push(...chatCache.messages);
  messages.push({ role: "user", content: userMessage });

  try {
    // Send initial message
    const initialMessage = MessageFactory.text("Thinking...");
    const sentActivity = await context.sendActivity(initialMessage);
    
    let accumulatedText = "";
    
    // Stream the response from Azure OpenAI
    for await (const chunk of callAzureOpenAIStream(messages)) {
      accumulatedText += chunk;
      const cardJson = new ACData.Template(feedbackCard).expand({
        $root: {
          body: accumulatedText,
        },
      });

      // Update the message with the adaptive card
      const updatedActivity = MessageFactory.attachment(CardFactory.adaptiveCard(cardJson));
      updatedActivity.id = sentActivity.id;

      await context.updateActivity(updatedActivity);
    }

    // Update chat cache with assistant response
    const updatedMessages = [...chatCache.messages];
    updatedMessages.push({ role: "user", content: userMessage });
    updatedMessages.push({ role: "assistant", content: accumulatedText });
    
    // Trim the array to keep the last 10 messages (excluding system message)
    const trimmedMessages = updatedMessages.slice(-10);
    
    // Update the chat cache in state
    state.conversation.chatCache[conversationId] = {
      user_id: context.activity.from?.id || "unknown",
      messages: trimmedMessages
    };
    // console.log("Updated chat cache:", state.conversation.chatCache);

  } catch (error) {
    console.error("Error in /openai handler:", error);
    await context.sendActivity("Sorry, I encountered an error while processing your streaming OpenAI request.");
  }
});

teamsBot.conversationUpdate(
  "membersAdded",
  async (context: TurnContext, state: ApplicationTurnState) => {
    // Initialize conversation state if needed
    if (!state.conversation.chatCache) {
      state.conversation.chatCache = {};
    }
    
    await context.sendActivity(
      `Hi there! I'm an echo bot running on Agents SDK version ${version} that will echo what you said to me.`
    );
  }
);

// Listen for ANY message to be received. MUST BE AFTER ANY OTHER MESSAGE HANDLERS
teamsBot.activity(
  ActivityTypes.Message,
  async (context: TurnContext, state: ApplicationTurnState) => {
    // Initialize conversation state if needed
    if (!state.conversation.chatCache) {
      state.conversation.chatCache = {};
    }

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

    await context.sendActivity(MessageFactory.attachment(CardFactory.adaptiveCard(cardJson)));
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
