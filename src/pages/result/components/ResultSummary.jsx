function ResultSummary() {
  return (
    <div className="mt-8 grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
      <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 dark:border-slate-800 dark:bg-slate-950">
        <h2 className="text-xl font-semibold text-slate-900 dark:text-white">
          Eligibility verdict
        </h2>
        <div className="mt-4 inline-flex rounded-full bg-emerald-500/10 px-4 py-2 text-sm font-semibold text-emerald-300">
          Eligible for this role
        </div>
        <p className="mt-4 text-sm leading-7 text-slate-600 dark:text-slate-400">
          The AI model reviewed the uploaded resume against the job description
          and found a strong alignment with the required frontend and
          collaboration experience.
        </p>
      </div>
      <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 dark:border-slate-800 dark:bg-slate-950">
        <h3 className="text-lg font-semibold text-slate-900 dark:text-white">
          Score breakdown
        </h3>
        <ul className="mt-4 space-y-3 text-sm text-slate-700 dark:text-slate-300">
          <li className="flex items-center justify-between">
            <span>Experience match</span>
            <span className="font-semibold text-cyan-300">92%</span>
          </li>
          <li className="flex items-center justify-between">
            <span>Skill alignment</span>
            <span className="font-semibold text-cyan-300">88%</span>
          </li>
          <li className="flex items-center justify-between">
            <span>Role fit</span>
            <span className="font-semibold text-cyan-300">84%</span>
          </li>
        </ul>
      </div>
    </div>
  );
}

export default ResultSummary;
