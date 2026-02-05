export default function HandHistory({ hands }: { hands: string[] }) {
  return (
    <div className="space-y-3">
      {hands.map((hand, idx) => (
        <div key={idx} className="bg-white border border-slate-200 p-4 rounded-lg shadow-sm">
          <pre className="text-sm whitespace-pre-wrap text-slate-700">{hand}</pre>
        </div>
      ))}
    </div>
  );
}
