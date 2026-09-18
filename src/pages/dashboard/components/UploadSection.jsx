import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { analyzeResume } from "../../../api/screeningApi";

const ALLOWED_TYPES = ["application/pdf", "image/jpeg", "image/png"];
const MAX_SIZE_BYTES = 10 * 1024 * 1024;

function validate(resumeFile, jobDescription) {
  if (!resumeFile) {
    return "Please select a resume file.";
  }
  if (!ALLOWED_TYPES.includes(resumeFile.type)) {
    return "Resume must be a PDF, JPEG, or PNG file.";
  }
  if (resumeFile.size > MAX_SIZE_BYTES) {
    return "Resume file must be under 10 MB.";
  }
  if (!jobDescription.trim()) {
    return "Please paste the job description.";
  }
  return "";
}

function UploadSection() {
  const navigate = useNavigate();

  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();

    const validationError = validate(resumeFile, jobDescription);
    if (validationError) {
      setError(validationError);
      return;
    }

    setError("");
    setIsSubmitting(true);
    try {
      const result = await analyzeResume({ resumeFile, jobDescription });
      navigate("/result", { state: result });
    } catch (err) {
      setError(
        err.response?.data?.message ||
          "Unable to analyze this resume. Please try again.",
      );
    } finally {
      setIsSubmitting(false);
    }
  };

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
      <form
        onSubmit={handleSubmit}
        className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 p-6"
      >
        {error && (
          <p className="mb-4 rounded-xl bg-red-50 px-4 py-3 text-sm text-red-600 dark:bg-red-950/40 dark:text-red-400">
            {error}
          </p>
        )}
        <label className="mb-2 block text-sm font-semibold text-cyan-700 dark:text-cyan-300">
          Upload resume
        </label>
        <input
          type="file"
          accept="application/pdf,image/jpeg,image/png"
          onChange={(e) => setResumeFile(e.target.files?.[0] ?? null)}
          className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-700 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        />
        <label className="mt-4 mb-2 block text-sm font-semibold text-cyan-700 dark:text-cyan-300">
          Job description
        </label>
        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          className="min-h-32 w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-700 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
          placeholder="Paste the employer requirements here..."
        />
        <button
          type="submit"
          disabled={isSubmitting}
          className="mt-4 inline-flex rounded-full bg-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isSubmitting ? "Analyzing…" : "Analyze resume"}
        </button>
      </form>
    </section>
  );
}

export default UploadSection;
