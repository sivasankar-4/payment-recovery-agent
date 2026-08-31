const API_URL = ''

export async function getAuditLogs() {
  const response = await fetch(`/api/audit-logs`)

  if (!response.ok) {
    throw new Error('Failed to fetch audit logs')
  }

  return response.json()
}