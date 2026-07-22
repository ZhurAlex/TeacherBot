export interface User {
  id: number
  username: string | null
  first_name: string | null
  last_name: string | null
  chat_id: number
  is_blocked: boolean
  first_seen_at: string
  total_tokens: number | null
}

export interface Message {
  id: number
  user_id: number
  text: string
  response: string
  provider_used: string
  tokens_used: number | null
  created_at: string
}
