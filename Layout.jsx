import Navbar from "./src/components/Navbar";

function Layout({ children }) {
  return (
    <div className="app-shell min-h-screen transition-colors duration-300">
      <Navbar />
      {children}
    </div>
  );
}

export default Layout;
