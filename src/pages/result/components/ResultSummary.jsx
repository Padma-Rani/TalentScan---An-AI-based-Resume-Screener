function SkillChips({ skills, tone }) {
  if (!skills || skills.length === 0) {
    return <p className="text-sm text-slate-500 dark:text-slate-400">None</p>;
  }

  const toneClasses =
    tone === "positive"
      ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-300"
      : "bg-amber-500/10 text-amber-600 dark:text-amber-300";

  return (
    <div className="flex flex-wrap gap-2">
      {skills.map((skill) => (
        <span
          key={skill}
          className={`rounded-full px-3 py-1 text-xs font-semibold ${toneClasses}`}
        >
          {skill}
        </span>
      ))}
    </div>
  );
}

function ResultSummary({ result }) {
  const {
    candidateName,
    matchScore,
    eligible,
    matchedSkills,
    missingSkills,
    summary,
  } = result;

  const verdictClasses = eligible
    ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-300"
    : "bg-red-500/10 text-red-600 dark:text-red-400";

  return (
    <div className="mt-8 grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
      <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 dark:border-slate-800 dark:bg-slate-950">
        <h2 className="text-xl font-semibold text-slate-900 dark:text-white">
          {candidateName || "Candidate"}
        </h2>
        <div
          className={`mt-4 inline-flex rounded-full px-4 py-2 text-sm font-semibold ${verdictClasses}`}
        >
          {eligible ? "Eligible for this role" : "Not eligible for this role"}
        </div>
        <p className="mt-4 text-sm leading-7 text-slate-600 dark:text-slate-400">
          {summary}
        </p>
      </div>
      <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 dark:border-slate-800 dark:bg-slate-950">
        <h3 className="text-lg font-semibold text-slate-900 dark:text-white">
          Match score
        </h3>
        <p className="mt-2 text-3xl font-semibold text-cyan-500">
          {Math.round(matchScore)}%
        </p>

        <h4 className="mt-6 text-sm font-semibold text-slate-700 dark:text-slate-300">
          Matched skills
        </h4>
        <div className="mt-2">
          <SkillChips skills={matchedSkills} tone="positive" />
        </div>

        <h4 className="mt-6 text-sm font-semibold text-slate-700 dark:text-slate-300">
          Missing skills
        </h4>
        <div className="mt-2">
          <SkillChips skills={missingSkills} tone="warning" />
        </div>
      </div>
    </div>
  );
}

export default ResultSummary;
