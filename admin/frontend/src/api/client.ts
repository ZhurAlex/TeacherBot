import type { Message, User } from './types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })

  if (!response.ok) {
    throw new Error(`Request to ${path} failed with status ${response.status}`)
  }

  return response.json() as Promise<T>
}

export function fetchUsers(): Promise<User[]> {
  return request<User[]>('/users')
}

export function fetchUser(id: number): Promise<User> {
  return request<User>(`/users/${id}`)
}

export function fetchUserMessages(id: number): Promise<Message[]> {
  return request<Message[]>(`/users/${id}/messages`)
}

export function setUserBlocked(id: number, blocked: boolean): Promise<{ id: number; is_blocked: boolean }> {
  return request(`/users/${id}/block`, {
    method: 'PATCH',
    body: JSON.stringify({ blocked }),
  })
}
