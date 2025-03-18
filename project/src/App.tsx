import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./components/HomePage";
import Register from "./components/Register";
import Login from "./components/Login";
import AppointmentScheduler from "./components/AppointmentScheduler";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto py-4 px-4">
            <h1 className="text-3xl font-bold text-gray-900">
              Appointment Scheduler
            </h1>
          </div>
        </header>
        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path="/scheduler" element={<AppointmentScheduler />} />
          </Routes>
        </main>
        <footer className="bg-white border-t mt-8">
          <div className="max-w-7xl mx-auto py-4 px-4 text-center text-gray-600">
            © {new Date().getFullYear()} Appointment Scheduler. All rights
            reserved.
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;