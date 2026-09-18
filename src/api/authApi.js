import axiosClient from "./axiosClient";

export function signup({ fullName, email, password }) {
  return axiosClient
    .post("/auth/signup", { fullName, email, password })
    .then((res) => res.data);
}

export function login({ email, password }) {
  return axiosClient
    .post("/auth/login", { email, password })
    .then((res) => res.data);
}

export function logout() {
  return axiosClient.post("/auth/logout").then((res) => res.data);
}

export function me() {
  return axiosClient.get("/auth/me").then((res) => res.data);
}
