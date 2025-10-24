import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import About from './pages/About';
import Mission from './pages/Mission';

// REQUIREMENT 1: When the user navigates to the URL, the system shall display the MyHealthPal landing page
// REQUIREMENT 22: When the user accesses the application on different devices, the system shall display a responsive interface
function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-grow">
          <Routes>
            {/* REQUIREMENT 1: Landing page route */}
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/mission" element={<Mission />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App; 