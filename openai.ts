import { AzureOpenAI } from "openai";

const endpoint = "https://r0bagents.cognitiveservices.azure.com/";
const modelName = "gpt-4.1-mini";
const deployment = "gpt-4.1-mini";

export async function* callAzureOpenAIStream(messages: { role: 'system' | 'user' | 'assistant'; content: string }[]): AsyncGenerator<string, void, unknown> {
  const apiKey = process.env.AZURE_OPENAI_API_KEY || "<your-azure-openai-api-key>";
  const apiVersion = "2024-04-01-preview";
  const options = { endpoint, apiKey, deployment, apiVersion };

  const client = new AzureOpenAI(options);

  try {
    const response = await client.chat.completions.create({
      messages: messages,
      stream: true,
      max_completion_tokens: 13107,
      temperature: 1,
      top_p: 1,
      frequency_penalty: 0,
      presence_penalty: 0,
      model: modelName
    });

    for await (const part of response) {
      const content = part.choices[0]?.delta?.content || '';
      if (content) {
        yield content;
      }
    }
  } catch (error) {
    console.error("Error calling Azure OpenAI streaming:", error);
    yield "Sorry, I encountered an error while processing your request.";
  }
}
