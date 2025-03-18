import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:5000/login", formData, {
        withCredentials: true,
      });
      alert("Login successful!");
      navigate("/scheduler");
    } catch (error) {
      console.error("Error logging in:", error);
      alert("Login failed.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h2 className="text-2xl font-bold mb-4">Login</h2>
      <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
        <input type="text" name="username" placeholder="Username" onChange={handleChange} className="border p-2" required />
        <input type="password" name="password" placeholder="Password" onChange={handleChange} className="border p-2" required />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          Login
        </button>
      </form>
      <p>Don't have an account?{" "}
        <button onClick={() => navigate("/register")} className="text-blue-600 hover:underline">
          Register
        </button>
      </p>
    </div>
  );
};

export default Login;
