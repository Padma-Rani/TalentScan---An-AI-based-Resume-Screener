import { Link } from "react-router-dom";
import { useTheme } from "../contexts/ThemeContext";

function Navbar() {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="border-b border-slate-300/70 bg-white/80 text-slate-900 shadow-sm backdrop-blur dark:border-slate-800 dark:bg-slate-900/80 dark:text-slate-100">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4 lg:px-8">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.3em] text-cyan-500">
            AI Resume Screener
          </p>
          <h1 className="text-xl font-semibold">Recruitment dashboard</h1>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={toggleTheme}
            className="rounded-full border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
          >
            {theme === "dark" ? "☀️ Light" : "🌙 Dark"}
          </button>
          <Link
            to="/history"
            className="rounded-full border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
          >
            View history
          </Link>
          <Link
            to="/login"
            className="rounded-full bg-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-cyan-400"
          >
            Logout
          </Link>
        </div>
      </div>
    </header>
  );
}

export default Navbar;
