import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Login from "./pages/Login";
import Feed from "./pages/Feed";
import NoticeDetail from "./pages/NoticeDetail";
import PostNotice from "./pages/PostNotice";
import ProtectedRoute from "./components/ProtectedRoute"
import Register from "./pages/Register";
import Navbar from "./components/Navbar";

function App() {
  return (
    <AuthProvider>
      <Navbar />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Feed />} />
       
        <Route path="/notices/:id" element={<NoticeDetail />} />
        
        <Route
            path="/post-notice"
            element={
              <ProtectedRoute>
                <PostNotice />
              </ProtectedRoute>
            }
          />
        <Route path="/register" element={<Register />} />
      </Routes>
    </AuthProvider>
      );
}

export default App;