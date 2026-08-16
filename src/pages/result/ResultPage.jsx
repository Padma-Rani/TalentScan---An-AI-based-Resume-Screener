import { Link } from "react-router-dom";
import Layout from "../../../Layout";
import ResultSummary from "./components/ResultSummary";

function ResultRoutePage() {
  return (
    <Layout>
      <div className="px-6 py-10">
        <div className="mx-auto max-w-5xl rounded-3xl border border-slate-200 bg-white p-8 shadow-2xl shadow-slate-200/60 dark:border-slate-800 dark:bg-slate-900 dark:shadow-black/30">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.3em] text-cyan-500">
                Result
              </p>
              <h1 className="mt-2 text-3xl font-semibold text-slate-900 dark:text-white">
                Candidate eligibility summary
              </h1>
            </div>
            <Link
              to="/"
              className="rounded-full border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
            >
              Back to dashboard
            </Link>
          </div>

          <ResultSummary />
        </div>
      </div>
    </Layout>
  );
}

export default ResultRoutePage;
