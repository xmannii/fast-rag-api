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

// Mount routes under /api prefix
app.route('/api/chat', chat)
app.route('/api/embedding', embedding)
app.route('/api/context', context)

export default app
