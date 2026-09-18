import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Layout from "../../../Layout";
import HistoryTable from "./components/HistoryTable";
import { getHistory } from "../../api/screeningApi";

function HistoryRoutePage() {
  const [items, setItems] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getHistory()
      .then(setItems)
      .catch(() => setError("Unable to load screening history."))
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <Layout>
      <div className="px-6 py-10">
        <div className="mx-auto max-w-6xl">
          <div className="mb-8 flex flex-wrap items-center justify-between gap-4">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.3em] text-cyan-500">
                History
              </p>
              <h1 className="mt-2 text-3xl font-semibold text-slate-900 dark:text-white">
                All screening history
              </h1>
            </div>
            <Link
              to="/"
              className="rounded-full border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
            >
              Back to dashboard
            </Link>
          </div>

          <HistoryTable items={items} isLoading={isLoading} error={error} />
        </div>
      </div>
    </Layout>
  );
}

export default HistoryRoutePage;
