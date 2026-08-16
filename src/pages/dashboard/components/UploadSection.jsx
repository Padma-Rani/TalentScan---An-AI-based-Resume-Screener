import { Link } from "react-router-dom";

function UploadSection() {
  return (
    <section className="grid gap-6 rounded-3xl border border-slate-200 bg-white p-8 shadow-2xl shadow-slate-200/60 dark:border-slate-800 dark:bg-slate-900 dark:shadow-black/30 lg:grid-cols-[1.5fr_0.8fr]">
      <div className="space-y-4">
        <p className="text-sm font-medium uppercase tracking-[0.3em] text-cyan-500">
          Screen resumes with AI
        </p>
        <h2 className="text-3xl font-semibold text-slate-900 dark:text-white sm:text-4xl">
          Upload CVs and compare them to the role requirements in seconds.
        </h2>
        <p className="max-w-2xl text-base leading-7 text-slate-600 dark:text-slate-400">
          HR teams can upload PDF, JPEG, or PNG resumes, paste a job
          description, and receive a fast eligibility analysis powered by the
          backend AI pipeline.
        </p>
      </div>
      <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 p-6">
        <label className="mb-2 block text-sm font-semibold text-cyan-700 dark:text-cyan-300">
          Upload resume
        </label>
        <input
          type="file"
          className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-700 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        />
        <label className="mt-4 mb-2 block text-sm font-semibold text-cyan-700 dark:text-cyan-300">
          Job description
        </label>
        <textarea
          className="min-h-32 w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-700 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
          placeholder="Paste the employer requirements here..."
        />
        <Link
          to="/result"
          className="mt-4 inline-flex rounded-full bg-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-cyan-400"
        >
          Analyze resume
        </Link>
      </div>
    </section>
  );
}

export default UploadSection;
