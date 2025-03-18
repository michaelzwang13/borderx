import { useNavigate } from "react-router-dom";

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-4xl font-bold mb-4">Welcome to Appointment Scheduler</h1>
      <p className="text-lg text-gray-700 mb-6 text-center">
        Easily schedule, manage, filter, and track your appointments with our seamless system.
        Stay organized and never miss an important event again.
      </p>
      <button
        onClick={() => navigate("/register")}
        className="bg-blue-600 text-white px-6 py-3 rounded-lg text-lg hover:bg-blue-700 transition duration-200"
      >
        Get Started
      </button>
    </div>
  );
};

export default HomePage;
