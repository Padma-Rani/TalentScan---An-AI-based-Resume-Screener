import axiosClient from "./axiosClient";

export function analyzeResume({ resumeFile, jobDescription }) {
  const formData = new FormData();
  formData.append("resume", resumeFile);
  formData.append("jobDescription", jobDescription);

  return axiosClient
    .post("/screening/analyze", formData)
    .then((res) => res.data);
}

export function getHistory() {
  return axiosClient.get("/history").then((res) => res.data);
}
