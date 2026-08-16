import Layout from "../../../Layout";
import SignupForm from "./components/SignupForm";

function SignupRoutePage() {
  return (
    <Layout>
      <div className="flex min-h-screen items-center justify-center px-6 py-10">
        <SignupForm />
      </div>
    </Layout>
  );
}

export default SignupRoutePage;
