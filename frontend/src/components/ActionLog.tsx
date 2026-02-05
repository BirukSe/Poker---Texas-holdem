export default function ActionLog({ log }: { log: string[] }) {
  return (
    <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 mt-4 h-80 overflow-y-auto">
      <pre className="whitespace-pre-wrap text-sm text-slate-700">{log.join('\n')}</pre>
    </div>
  )
}
