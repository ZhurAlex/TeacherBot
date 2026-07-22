import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { fetchUsers } from '../api/client'
import { StatusBadge } from '../components/StatusBadge'
import styles from './UsersListPage.module.css'

export function UsersListPage() {
  const { data: users, isLoading, isError } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  })

  if (isLoading) return <p>Loading users...</p>
  if (isError) return <p>Failed to load users.</p>

  return (
    <div className={styles.page}>
      <h1>Users</h1>
      <table className={styles.table}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Chat ID</th>
            <th>Username</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Total Tokens</th>
            <th>Is Blocked</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {users?.map((user) => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.chat_id}</td>
              <td>{user.username ?? '—'}</td>
              <td>{user.first_name ?? '—'}</td>
              <td>{user.last_name ?? '—'}</td>
              <td>{user.total_tokens ?? 0}</td>
              <td>
                <StatusBadge isBlocked={user.is_blocked} />
              </td>
              <td>
                <Link to={`/users/${user.id}`}>View Details</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
