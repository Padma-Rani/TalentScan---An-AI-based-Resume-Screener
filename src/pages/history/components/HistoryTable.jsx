function EligibleBadge({ eligible }) {
  const classes = eligible
    ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-300"
    : "bg-red-500/10 text-red-600 dark:text-red-400";

  return (
    <span className={`rounded-full px-3 py-1 text-xs font-semibold ${classes}`}>
      {eligible ? "Eligible" : "Not eligible"}
    </span>
  );
}

function HistoryTable({ items, isLoading, error }) {
  return (
    <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-2xl shadow-slate-200/60 dark:border-slate-800 dark:bg-slate-900 dark:shadow-black/30">
      <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-800">
        <thead className="bg-slate-50 dark:bg-slate-950/70">
          <tr>
            <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700 dark:text-slate-300">
              Candidate
            </th>
            <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700 dark:text-slate-300">
              Score
            </th>
            <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700 dark:text-slate-300">
              Eligible
            </th>
            <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700 dark:text-slate-300">
              Date
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
          {isLoading && (
            <tr>
              <td
                colSpan={4}
                className="px-6 py-6 text-center text-sm text-slate-500 dark:text-slate-400"
              >
                Loading…
              </td>
            </tr>
          )}
          {!isLoading && error && (
            <tr>
              <td
                colSpan={4}
                className="px-6 py-6 text-center text-sm text-red-600 dark:text-red-400"
              >
                {error}
              </td>
            </tr>
          )}
          {!isLoading && !error && items.length === 0 && (
            <tr>
              <td
                colSpan={4}
                className="px-6 py-6 text-center text-sm text-slate-500 dark:text-slate-400"
              >
                No screenings yet.
              </td>
            </tr>
          )}
          {!isLoading &&
            !error &&
            items.map((item) => (
              <tr
                key={item.id}
                className="hover:bg-slate-100 dark:hover:bg-slate-800/60"
              >
                <td className="px-6 py-4 text-sm text-slate-700 dark:text-slate-200">
                  {item.candidateName}
                </td>
                <td className="px-6 py-4 text-sm font-semibold text-cyan-600 dark:text-cyan-300">
                  {Math.round(item.matchScore)}%
                </td>
                <td className="px-6 py-4 text-sm">
                  <EligibleBadge eligible={item.eligible} />
                </td>
                <td className="px-6 py-4 text-sm text-slate-500 dark:text-slate-400">
                  {new Date(item.createdAt).toLocaleDateString()}
                </td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
}

export default HistoryTable;
