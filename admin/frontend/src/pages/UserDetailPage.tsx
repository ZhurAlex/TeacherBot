import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { fetchUser, fetchUserMessages, setUserBlocked } from '../api/client'
import { StatusBadge } from '../components/StatusBadge'
import styles from './UserDetailPage.module.css'

export function UserDetailPage() {
  const { id } = useParams<{ id: string }>()
  const userId = Number(id)
  const queryClient = useQueryClient()

  const {
    data: user,
    isLoading: isUserLoading,
    isError: isUserError,
  } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  })

  const {
    data: messages,
    isLoading: isMessagesLoading,
    isError: isMessagesError,
  } = useQuery({
    queryKey: ['messages', userId],
    queryFn: () => fetchUserMessages(userId),
  })

  const blockMutation = useMutation({
    mutationFn: (blocked: boolean) => setUserBlocked(userId, blocked),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['user', userId] })
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })

  if (isUserLoading) return <p>Loading user...</p>
  if (isUserError || !user) return <p>Failed to load user.</p>

  const handleBlockToggle = () => {
    const action = user.is_blocked ? 'unblock' : 'block'
    if (!window.confirm(`Are you sure you want to ${action} this user?`)) return
    blockMutation.mutate(!user.is_blocked)
  }

  const fullName = [user.first_name, user.last_name].filter(Boolean).join(' ')

  return (
    <div className={styles.page}>
      <Link to="/users">← Back to users</Link>

      <h1>{fullName || `User #${user.id}`}</h1>

      <dl className={styles.details}>
        <dt>ID</dt>
        <dd>{user.id}</dd>

        <dt>Chat ID</dt>
        <dd>{user.chat_id}</dd>

        <dt>Username</dt>
        <dd>{user.username ?? '—'}</dd>

        <dt>Total Tokens</dt>
        <dd>{user.total_tokens ?? 0}</dd>

        <dt>First Seen</dt>
        <dd>{new Date(user.first_seen_at).toLocaleString()}</dd>

        <dt>Status</dt>
        <dd>
          <StatusBadge isBlocked={user.is_blocked} />
        </dd>
      </dl>

      <button onClick={handleBlockToggle} disabled={blockMutation.isPending}>
        {user.is_blocked ? 'Unblock' : 'Block'}
      </button>

      <h2 className={styles.messagesHeading}>Messages</h2>
      {isMessagesLoading && <p>Loading messages...</p>}
      {isMessagesError && <p>Failed to load messages.</p>}
      {messages && (
        <table className={styles.table}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Text</th>
              <th>Response</th>
              <th>Provider Used</th>
              <th>Tokens Used</th>
              <th>Created At</th>
            </tr>
          </thead>
          <tbody>
            {messages.map((message) => (
              <tr key={message.id}>
                <td>{message.id}</td>
                <td>{message.text}</td>
                <td>{message.response}</td>
                <td>{message.provider_used}</td>
                <td>{message.tokens_used ?? 0}</td>
                <td>{new Date(message.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
