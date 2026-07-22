import styles from './StatusBadge.module.css'

interface StatusBadgeProps {
  isBlocked: boolean
}

export function StatusBadge({ isBlocked }: StatusBadgeProps) {
  return (
    <span className={styles.badge}>
      <span className={`${styles.dot} ${isBlocked ? styles.dotBlocked : styles.dotActive}`} />
      {isBlocked ? 'Blocked' : 'Active'}
    </span>
  )
}
