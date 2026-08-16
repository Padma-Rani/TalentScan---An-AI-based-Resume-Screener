import { Link } from "react-router-dom";
import Layout from "../../../Layout";
import UploadSection from "./components/UploadSection";

const recentAnalyses = [
  {
    id: 1,
    candidate: "Ava Patel",
    role: "Frontend Developer",
    match: "92%",
    status: "Strong Match",
  },
  {
    id: 2,
    candidate: "Marcus Lee",
    role: "Product Designer",
    match: "81%",
    status: "Good Match",
  },
  {
    id: 3,
    candidate: "Nina Gomez",
    role: "Data Analyst",
    match: "74%",
    status: "Potential Fit",
  },
  {
    id: 4,
    candidate: "Daniel Kim",
    role: "Backend Engineer",
    match: "68%",
    status: "Needs Review",
  },
  {
    id: 5,
    candidate: "Sara Chen",
    role: "DevOps Engineer",
    match: "57%",
    status: "Low Match",
  },
];

function DashboardRoutePage() {
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
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            {recentAnalyses.map((item) => (
              <article
                key={item.id}
                className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-900"
              >
                <div className="flex items-center justify-between">
                  <h4 className="font-semibold text-slate-900 dark:text-white">
                    {item.candidate}
                  </h4>
                  <span className="rounded-full bg-cyan-500/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.25em] text-cyan-600 dark:text-cyan-300">
                    {item.match}
                  </span>
                </div>
                <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
                  {item.role}
                </p>
                <p className="mt-4 text-sm text-slate-700 dark:text-slate-300">
                  {item.status}
                </p>
              </article>
            ))}
          </div>
        </section>
      </main>
    </Layout>
  );
}

export default DashboardRoutePage;
