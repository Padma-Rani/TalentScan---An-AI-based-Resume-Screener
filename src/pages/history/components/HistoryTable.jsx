const historyItems = [
  {
    id: 1,
    candidate: "Ava Patel",
    role: "Frontend Developer",
    date: "2026-08-09",
    score: "92%",
    result: "Eligible",
  },
  {
    id: 2,
    candidate: "Marcus Lee",
    role: "Product Designer",
    date: "2026-08-08",
    score: "81%",
    result: "Eligible",
  },
  {
    id: 3,
    candidate: "Nina Gomez",
    role: "Data Analyst",
    date: "2026-08-08",
    score: "74%",
    result: "Review",
  },
  {
    id: 4,
    candidate: "Daniel Kim",
    role: "Backend Engineer",
    date: "2026-08-07",
    score: "68%",
    result: "Review",
  },
  {
    id: 5,
    candidate: "Sara Chen",
    role: "DevOps Engineer",
    date: "2026-08-07",
    score: "57%",
    result: "Not eligible",
  },
  {
    id: 6,
    candidate: "John Rivera",
    role: "Full Stack Engineer",
    date: "2026-08-06",
    score: "90%",
    result: "Eligible",
  },
];

function HistoryTable() {
  return (
    <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-2xl shadow-slate-200/60 dark:border-slate-800 dark:bg-slate-900 dark:shadow-black/30">
      <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-800">
        <thead className="bg-slate-50 dark:bg-slate-950/70">
          <tr>
            <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700 dark:text-slate-300">
              Candidate
            </th>
            <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700 dark:text-slate-300">
              Role
            </th>
            <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700 dark:text-slate-300">
              Date
            </th>
            <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700 dark:text-slate-300">
              Score
            </th>
            <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700 dark:text-slate-300">
              Result
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
          {historyItems.map((item) => (
            <tr
              key={item.id}
              className="hover:bg-slate-100 dark:hover:bg-slate-800/60"
            >
              <td className="px-6 py-4 text-sm text-slate-700 dark:text-slate-200">
                {item.candidate}
              </td>
              <td className="px-6 py-4 text-sm text-slate-600 dark:text-slate-300">
                {item.role}
              </td>
              <td className="px-6 py-4 text-sm text-slate-500 dark:text-slate-400">
                {item.date}
              </td>
              <td className="px-6 py-4 text-sm font-semibold text-cyan-600 dark:text-cyan-300">
                {item.score}
              </td>
              <td className="px-6 py-4 text-sm text-slate-600 dark:text-slate-300">
                {item.result}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default HistoryTable;
