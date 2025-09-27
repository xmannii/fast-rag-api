import { RAGService } from '../services/rag.service';
import { config } from '../config';

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  parts: Array<{
    type: 'text';
    text: string;
  }>;
}

export class RAGPipeline {
  /**
   * Prepare context for RAG-enabled chat
   */
  static async prepareContext(messages: ChatMessage[], getContext: boolean): Promise<string> {
    if (!getContext || messages.length === 0) {
      return '';
    }

    // Get the last user message
    const lastUserMessage = messages
      .filter(msg => msg.role === 'user')
      .pop();
    
    if (!lastUserMessage) {
      return '';
    }

    // Extract text from user message
    const userText = lastUserMessage.parts
      .filter(part => part.type === 'text')
      .map(part => part.text)
      .join(' ');
    
    if (!userText) {
      return '';
    }

    // Get relevant context from RAG service
    const relevantContext = await RAGService.getRelevantContext(userText);
    
    if (!relevantContext) {
      return '';
    }

    // Format context for system prompt using configurable template
    return `\n\n${config.ai.contextPromptTemplate.replace('{context}', relevantContext)}`;
  }
}
