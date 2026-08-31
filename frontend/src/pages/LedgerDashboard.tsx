import { useEffect, useState } from 'react'
import { getPayments } from '../services/api'
import { getAuditLogs } from '../services/auditApi'

type Payment = {
  event_id: string
  payment_id: string
  status: string
  failure_reason: string
  amount: number
  customer_name: string
  customer_email: string
  received_at: string
}

type AuditLog = {
  event_id: string
  payment_id: string
  intent: string
  confidence: number
  recovery_score: number
  systemic: boolean
  retry_count: number
  action: string
  reason: string
  created_at: string
}

const ACTION_STYLES: Record<string, string> = {
  SEND_PAYMENT_LINK: 'text-[#3FA796] border-[#3FA796]/35',

  SCHEDULE_PAYMENT_REMINDER: 'text-[#3FA796] border-[#3FA796]/35',

  UPDATE_PAYMENT_METHOD: 'text-[#C9A227] border-[#C9A227]/35',

  SEND_FAILURE_EXPLANATION: 'text-[#C9A227] border-[#C9A227]/35',

  NO_ACTION: 'text-[#7D8290] border-[#242B3A]',

  REVIEW: 'text-[#C9A227] border-[#C9A227]/35',

  PAUSE_AND_ESCALATE: 'text-[#D2543E] border-[#D2543E]/35',
}
function actionStyle(action: string) {
  return ACTION_STYLES[action] || 'text-[#7D8290] border-[#242B3A]'
}

function tapeVerdict(log: AuditLog, payment: Payment | undefined) {
  if (payment && payment.status !== 'failed') {
    return { label: 'RECOVERED', className: 'text-[#3FA796]' }
  }
  if (log.action === 'STOP') {
    return { label: 'STOPPED', className: 'text-[#7D8290]' }
  }
  if (log.systemic) {
    return { label: 'ESCALATED', className: 'text-[#D2543E]' }
  }
  return { label: 'HOLDING', className: 'text-[#C9A227]' }
}

function LedgerDashboard() {
  const [payments, setPayments] = useState<Payment[]>([])
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([])
  const [now, setNow] = useState(new Date())
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    function load() {
      Promise.all([getPayments(), getAuditLogs()])
        .then(([paymentsRes, logsRes]) => {
          setPayments(paymentsRes)
          setAuditLogs(logsRes)
          setError(null)
        })
        .catch((err) => {
          console.error(err)
          setError('Could not reach the backend. Is it running on localhost:8000?')
        })
    }
    load()
    const poll = setInterval(load, 5000)
    return () => clearInterval(poll)
  }, [])

  useEffect(() => {
    const clock = setInterval(() => setNow(new Date()), 1000)
    return () => clearInterval(clock)
  }, [])

  const failedPayments = payments.filter((p) => p.status === 'failed')
  const resolvedPayments = payments.filter((p) => p.status !== 'failed')

  const systemicLogs = auditLogs.filter((log) => log.systemic)
  const systemicPaymentIds = new Set(systemicLogs.map((log) => log.payment_id))

  const revenueAtRisk = failedPayments.reduce((sum, p) => sum + p.amount, 0)
  const recoveredToday = resolvedPayments.reduce((sum, p) => sum + p.amount, 0)
  const recoveryRate =
    payments.length > 0
      ? Math.round((resolvedPayments.length / payments.length) * 1000) / 10
      : 0

  const logsByPaymentId = new Map(auditLogs.map((log) => [log.payment_id, log]))
  const paymentsByPaymentId = new Map(payments.map((p) => [p.payment_id, p]))

  const tapeLogs = [...auditLogs]
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 14)

  return (
    <div className="min-h-screen bg-[#0B0E14] text-[#EDEAE3]">
      <div className="mx-auto max-w-[1180px] px-5 pb-16 pt-7">

        {/* Status bar */}
        <div className="flex items-center justify-between border-b border-[#242B3A] pb-4">
          <div className="flex items-center gap-2.5">
            <span className="h-[9px] w-[9px] animate-pulse rounded-full bg-[#3FA796] shadow-[0_0_0_3px_rgba(63,167,150,0.18)]" />
            <div>
              <h1 className="text-sm font-semibold uppercase tracking-[0.14em]">
                Recovery Ledger
              </h1>
              <div className="font-ledger text-[11px] text-[#7D8290]">
                adaptive revenue recovery agent · merchant view
              </div>
            </div>
          </div>
          <div className="font-ledger text-xs text-[#7D8290]">
            {now.toLocaleString('en-IN', { hour12: false })}
          </div>
        </div>

        {error && (
          <div className="mt-6 rounded-sm border-l-2 border-[#D2543E] bg-[#D2543E]/10 px-4 py-3 text-sm text-[#D9B8B1]">
            {error}
          </div>
        )}

        {/* Systemic alert */}
        {systemicLogs.length > 0 && (
          <div className="mt-5 flex items-start gap-3 rounded-sm border-l-2 border-[#D2543E] bg-gradient-to-r from-[#D2543E]/10 to-transparent px-4 py-3.5">
            <span className="mt-1.5 h-[7px] w-[7px] shrink-0 animate-pulse rounded-full bg-[#D2543E]" />
            <p className="text-[13px] leading-relaxed text-[#D9B8B1]">
              <span className="mb-0.5 block font-ledger text-[10px] uppercase tracking-[0.08em] text-[#D2543E]">
                Systemic pattern detected
              </span>
              <strong className="text-[#EDEAE3]">
                {systemicLogs.length} decision{systemicLogs.length === 1 ? '' : 's'}
              </strong>{' '}
              Multiple customers are failing to complete payments. Automatic recovery is paused and the cases are escalated for investigation.
            </p>
          </div>
        )}

        {/* KPI strip */}
        <div className="mt-6 grid grid-cols-2 overflow-hidden rounded-sm border border-[#242B3A] md:grid-cols-4">
          <div className="border-r border-[#242B3A] px-[18px] py-4">
            <div className="text-[10px] uppercase tracking-[0.1em] text-[#7D8290]">
              Revenue at risk
            </div>
            <div className="font-ledger text-[22px] font-semibold">
              ₹{revenueAtRisk.toLocaleString('en-IN')}
            </div>
            <div className="mt-1 font-ledger text-[11px] text-[#3FA796]">
              {failedPayments.length} open cases
            </div>
          </div>
          <div className="border-r border-[#242B3A] px-[18px] py-4 md:border-r">
            <div className="text-[10px] uppercase tracking-[0.1em] text-[#7D8290]">
              Recovered
            </div>
            <div className="font-ledger text-[22px] font-semibold text-[#C9A227]">
              ₹{recoveredToday.toLocaleString('en-IN')}
            </div>
            <div className="mt-1 font-ledger text-[11px] text-[#3FA796]">
              {recoveryRate}% recovery rate
            </div>
          </div>
          <div className="border-r border-[#242B3A] px-[18px] py-4">
            <div className="text-[10px] uppercase tracking-[0.1em] text-[#7D8290]">
              Isolated cases
            </div>
            <div className="font-ledger text-[22px] font-semibold">
              {auditLogs.length - systemicLogs.length}
            </div>
            <div className="mt-1 font-ledger text-[11px] text-[#3FA796]">
              per-customer flow
            </div>
          </div>
          <div className="px-[18px] py-4">
            <div className="text-[10px] uppercase tracking-[0.1em] text-[#7D8290]">
              Systemic signals
            </div>
            <div
              className={`font-ledger text-[22px] font-semibold ${
                systemicLogs.length > 0 ? 'text-[#D2543E]' : ''
              }`}
            >
              {systemicLogs.length}
            </div>
            <div
              className={`mt-1 font-ledger text-[11px] ${
                systemicLogs.length > 0 ? 'text-[#D2543E]' : 'text-[#7D8290]'
              }`}
            >
              flagged segments
            </div>
          </div>
        </div>

        {/* Main grid */}
        <div className="mt-6 grid grid-cols-1 items-start gap-5 lg:grid-cols-[1.55fr_1fr]">

          {/* Recovery queue */}
          <div className="rounded-sm border border-[#242B3A] bg-[#131822]">
            <div className="flex items-baseline justify-between border-b border-[#242B3A] px-4 py-3.5">
              <h2 className="text-xs font-semibold uppercase tracking-[0.1em]">
                Recovery Queue
              </h2>
              <span className="font-ledger text-[11px] text-[#7D8290]">
                {failedPayments.length} open cases
              </span>
            </div>

            <div>
              {failedPayments.length === 0 && (
                <div className="px-4 py-8 text-center text-sm text-[#7D8290]">
                  No open cases — every failed payment has been resolved.
                </div>
              )}

              {failedPayments.map((payment) => {
                const log = logsByPaymentId.get(payment.payment_id)
                const systemic = systemicPaymentIds.has(payment.payment_id)
                return (
                  <div
                    key={payment.event_id}
                    className="grid grid-cols-[22px_1fr_auto_auto] items-center gap-3.5 border-b border-[#242B3A] px-4 py-3 last:border-b-0"
                  >
                    <span
                      className={`h-8 w-[3px] rounded-sm ${
                        systemic ? 'bg-[#D2543E]' : 'bg-[#3FA796]'
                      }`}
                    />
                    <div className="min-w-0">
                      <div className="font-ledger text-xs">{payment.payment_id}</div>
                      <div className="mt-0.5 truncate text-[11px] text-[#7D8290]">
                        {payment.failure_reason} · {payment.customer_name}
                        {systemic ? ' · flagged segment' : ''}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-ledger text-[13px] font-semibold text-[#C9A227]">
                        {log ? log.recovery_score.toFixed(2) : '—'}
                      </div>
                      <div className="text-[9px] uppercase tracking-[0.06em] text-[#7D8290]">
                        score
                      </div>
                    </div>
                    <span
                      className={`whitespace-nowrap rounded-sm border px-2 py-1 font-ledger text-[10px] tracking-[0.04em] ${actionStyle(
                        log?.action || ''
                      )}`}
                    >
                      {log?.action || 'PENDING'}
                    </span>
                  </div>
                )
              })}
            </div>
          </div>

          {/* Decision tape */}
          <div className="relative rounded-sm border border-[#242B3A] bg-[#131822]">
            <div className="flex items-baseline justify-between border-b border-[#242B3A] px-4 py-3.5">
              <h2 className="text-xs font-semibold uppercase tracking-[0.1em]">
                Decision Tape
              </h2>
              <span className="font-ledger text-[11px] text-[#7D8290]">live</span>
            </div>

            <div className="h-[420px] overflow-y-auto">
              {tapeLogs.length === 0 && (
                <div className="px-4 py-8 text-center text-sm text-[#7D8290]">
                  No decisions logged yet.
                </div>
              )}
              {tapeLogs.map((log) => {
                const verdict = tapeVerdict(log, paymentsByPaymentId.get(log.payment_id))
                return (
                <div
                  key={log.event_id}
                  className="border-b border-dashed border-[#242B3A] px-4 py-[7px] font-ledger text-[11px] leading-relaxed"
                >
                  <span className="text-[#7D8290]">
                    {new Date(log.created_at).toTimeString().slice(0, 8)}
                  </span>{' '}
                  <span>{log.payment_id}</span> →{' '}
                  <span className={`font-semibold ${verdict.className}`}>
                    {verdict.label}
                  </span>
                  <span className="mt-0.5 block text-[10px] text-[#7D8290]">
                    {log.reason}
                  </span>
                </div>
                )
              })}
            </div>

            <div className="border-t border-[#242B3A] px-4 py-3 font-ledger text-[10px] leading-relaxed text-[#7D8290]">
              score = <b className="text-[#C9A227]">w1</b>·success_rate −{' '}
              <b className="text-[#C9A227]">w2</b>·attempts +{' '}
              <b className="text-[#C9A227]">w3</b>·engagement −{' '}
              <b className="text-[#C9A227]">w4</b>·time_elapsed
              <br />
              stop if: captured · opted_out · attempts≥2 · action∉allowed
            </div>
          </div>
        </div>

        <footer className="mt-7 text-center font-ledger text-[10px] tracking-[0.04em] text-[#7D8290]">
          POLICY ENGINE ENFORCES ALL STOP CONDITIONS · AI RECOMMENDS, NEVER EXECUTES DIRECTLY
        </footer>
      </div>
    </div>
  )
}

export default LedgerDashboard
