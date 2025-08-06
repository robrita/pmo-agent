import {
  AuthConfiguration,
  authorizeJWT,
  CloudAdapter,
  loadAuthConfigFromEnv,
  Request,
  TurnContext,
} from "@microsoft/agents-hosting";
import express, { Response } from "express";

import { teamsBot } from "./teamsBot";

// Create authentication configuration
const authConfig: AuthConfiguration = loadAuthConfigFromEnv();

// Create adapter
const adapter = new CloudAdapter(authConfig);

// Catch-all for errors.
const onTurnErrorHandler = async (context: TurnContext, error: Error) => {
  // This check writes out errors to console log .vs. app insights.
  // NOTE: In production environment, you should consider logging this to Azure
  //       application insights.
  const timestamp = new Date().toISOString();
  const conversationId = context.activity.conversation?.id;
  const userId = context.activity.from?.id;
  
  console.error(`\n[${timestamp}] [onTurnError] Unhandled error in conversation ${conversationId} for user ${userId}`);
  console.error(`[${timestamp}] Error message: ${error.message}`);
  console.error(`[${timestamp}] Error stack: ${error.stack}`);
  console.error(`[${timestamp}] Activity type: ${context.activity.type}`);
  console.error(`[${timestamp}] Activity text: ${context.activity.text}`);

  // Only send error message for user messages, not for other message types so the bot doesn't spam a channel or chat.
  if (context.activity.type === "message") {
    // Send a trace activity
    await context.sendTraceActivity(
      "OnTurnError Trace",
      `${error}`,
      "https://www.botframework.com/schemas/error",
      "TurnError"
    );

    // Send a message to the user
    await context.sendActivity(`The bot encountered unhandled error:\n ${error.message}`);
    await context.sendActivity("To continue to run this bot, please fix the bot source code.");
  }
};

// Set the onTurnError for the singleton CloudAdapter.
adapter.onTurnError = onTurnErrorHandler;

// Create express application
const server = express();
server.use(express.json());
server.use(authorizeJWT(authConfig));

// Listen for incoming requests.
server.post("/api/messages", async (req: Request, res: Response) => {
  const startTime = Date.now();
  const requestId = `req-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

  try {
    // Enhanced incoming request logging
    console.log(`[${requestId}] Incoming request: ${JSON.stringify(req.body)}`);
    console.log(`[${requestId}] Headers: ${JSON.stringify(req.headers)}`);
    console.log(`[${requestId}] User-Agent: ${req.headers['user-agent']}`);

    await adapter.process(req, res, async (context) => {
      console.log(`[${requestId}] Processing with context - Activity Type: ${context.activity.type}, From: ${context.activity.from?.name || context.activity.from?.id}`);
      await teamsBot.run(context);
      console.log(`[${requestId}] Bot processing completed successfully`);
    });

    const duration = Date.now() - startTime;
    console.log(`[${requestId}] Request completed in ${duration}ms`);

  } catch (error) {
    const duration = Date.now() - startTime;
    console.error(`[${requestId}] Error processing message after ${duration}ms: ${error}`);
    console.error(`[${requestId}] Error stack: ${error.stack}`);
    
    // Send generic error message to user
    try {
      await adapter.process(req, res, async (context) => {
        await context.sendActivity("Sorry, I encountered an error while processing your message. Please try again.");
      });
    } catch (sendError) {
      console.error(`Error sending error message: ${sendError}`);
    }
    
    // Send 500 status code
    if (!res.headersSent) {
      res.status(500).send("Internal Server Error");
    }
  }
});

// Start the server
const port = process.env.PORT || 3978;
server
  .listen(port, () => {
    console.log(
      `Bot Started, listening to port ${port} for appId ${authConfig.clientId} debug ${process.env.DEBUG}`
    );
  })
  .on("error", (err) => {
    console.error(err);
    process.exit(1);
  });
