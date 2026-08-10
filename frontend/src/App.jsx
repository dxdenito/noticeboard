import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Login from "./pages/Login";
import Feed from "./pages/Feed";
import NoticeDetail from "./pages/NoticeDetail";
import PostNotice from "./pages/PostNotice";
import ProtectedRoute from "./components/ProtectedRoute"

function App() {
  return (
    <AuthProvider>
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
      </Routes>
    </AuthProvider>
  );
}

export default App;