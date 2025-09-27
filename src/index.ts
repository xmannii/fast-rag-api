import { Hono } from 'hono'
import { config } from 'dotenv'
import chat from './routes/chat/route'
import embedding from './routes/embedding/route'
import context from './routes/context/route'

config()

const app = new Hono()

app.get('/', (c) => {
  return c.text('Hello Hono! AI Chat, Embedding & Context Knowledge Base API is running.')
})

// Mount routes
app.route('/chat', chat)
app.route('/embedding', embedding)
app.route('/context', context)

export default app
