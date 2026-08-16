import { Link } from "react-router-dom";

function SignupForm() {
  return (
    <div className="w-full max-w-md rounded-3xl border border-slate-200 bg-white p-8 shadow-2xl shadow-slate-200/60 dark:border-slate-800 dark:bg-slate-900 dark:shadow-black/30">
      <p className="text-sm font-semibold uppercase tracking-[0.3em] text-cyan-500">
        Join the platform
      </p>
      <h1 className="mt-2 text-3xl font-semibold text-slate-900 dark:text-white">
        Create an account
      </h1>
      <p className="mt-3 text-sm text-slate-600 dark:text-slate-400">
        Start screening resumes with your recruiting team.
      </p>

      <form className="mt-8 space-y-4">
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-300">
            Full name
          </label>
          <input
            type="text"
            className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-700 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100"
            placeholder="Alex Morgan"
          />
        </div>
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-300">
            Email
          </label>
          <input
            type="email"
            className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-700 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100"
            placeholder="alex@company.com"
          />
        </div>
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-300">
            Password
          </label>
          <input
            type="password"
            className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-700 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100"
            placeholder="••••••••"
          />
        </div>
        <Link
          to="/"
          className="flex justify-center rounded-full bg-cyan-500 px-4 py-3 text-sm font-semibold text-slate-950 hover:bg-cyan-400"
        >
          Create account
        </Link>
      </form>

      <p className="mt-6 text-center text-sm text-slate-600 dark:text-slate-400">
        Already have an account?{" "}
        <Link
          to="/login"
          className="font-semibold text-cyan-500 hover:text-cyan-400"
        >
          Sign in
        </Link>
      </p>
    </div>
  );
}

export default SignupForm;
