import Layout from "../../../Layout";
import LoginForm from "./components/LoginForm";

function LoginRoutePage() {
  return (
    <Layout>
      <div className="flex min-h-screen items-center justify-center px-6 py-10">
        <LoginForm />
      </div>
    </Layout>
  );
}

export default LoginRoutePage;
