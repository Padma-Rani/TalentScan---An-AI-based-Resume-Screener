import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Layout from "../../../Layout";
import UploadSection from "./components/UploadSection";
import { getHistory } from "../../api/screeningApi";

function DashboardRoutePage() {
  const [recentAnalyses, setRecentAnalyses] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getHistory()
      .then((items) => setRecentAnalyses(items.slice(0, 5)))
      .catch(() => setError("Unable to load recent analyses."))
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <Layout>
      <main className="mx-auto flex max-w-7xl flex-col gap-8 px-6 py-10 lg:px-8">
        <UploadSection />

        <section>
          <div className="mb-4 flex items-center justify-between">
            <h3 className="text-xl font-semibold text-slate-900 dark:text-white">
              Recent analysis history
            </h3>
            <Link
              to="/history"
              className="text-sm font-semibold text-cyan-500 hover:text-cyan-400"
            >
              View all →
            </Link>
          </div>
          {isLoading && (
            <p className="text-sm text-slate-500 dark:text-slate-400">
              Loading…
            </p>
          )}
          {!isLoading && error && (
            <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
          )}
          {!isLoading && !error && recentAnalyses.length === 0 && (
            <p className="text-sm text-slate-500 dark:text-slate-400">
              No screenings yet.
            </p>
          )}
          {!isLoading && !error && recentAnalyses.length > 0 && (
            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              {recentAnalyses.map((item) => (
                <article
                  key={item.id}
                  className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-900"
                >
                  <div className="flex items-center justify-between">
                    <h4 className="font-semibold text-slate-900 dark:text-white">
                      {item.candidateName}
                    </h4>
                    <span className="rounded-full bg-cyan-500/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.25em] text-cyan-600 dark:text-cyan-300">
                      {Math.round(item.matchScore)}%
                    </span>
                  </div>
                  <p className="mt-4 text-sm text-slate-700 dark:text-slate-300">
                    {item.eligible ? "Eligible" : "Not eligible"}
                  </p>
                </article>
              ))}
            </div>
          )}
        </section>
      </main>
    </Layout>
  );
}

export default DashboardRoutePage;
