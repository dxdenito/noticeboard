import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Login from "./pages/Login";
import Feed from "./pages/Feed";
import NoticeDetail from "./pages/NoticeDetail";
import PostNotice from "./pages/PostNotice";
import ProtectedRoute from "./components/ProtectedRoute"
import Register from "./pages/Register";
import Navbar from "./components/Navbar";
import MyNotices from "./pages/MyNotices";
import MyBookmarks from "./pages/MyBookmarks";
import ReviewQueue from "./pages/ReviewQueue";
import { ToastProvider } from "./context/ToastContext";
import ManageUsers from "./pages/admin/ManageUsers";
import AdminDashboard from "./pages/admin/AdminDashboard";
import AdminRoute from "./components/AdminRoutes";
import ManageDepartments from "./pages/admin/ManageDepartments";
import ManageClubs from "./pages/admin/ManageClubs";
import ManageCourses from "./pages/admin/ManageCourses";
import ManageCategories from "./pages/admin/ManageCategories";

function App() {
  return (
    <ToastProvider>
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
            <Route path="/my-notices" element={<ProtectedRoute><MyNotices/></ProtectedRoute>} />
            <Route path="/my-bookmarks" element={<ProtectedRoute><MyBookmarks/></ProtectedRoute>}/>
            <Route path="/review-queue" element={<ProtectedRoute><ReviewQueue/></ProtectedRoute>}/>  
            <Route path="/admin/manage-users" element={<AdminRoute><ManageUsers/></AdminRoute>}/>
            <Route path="/admin/dashboard" element={<AdminRoute><AdminDashboard/></AdminRoute>}/>
            <Route path="/admin/manage-departments" element={<AdminRoute><ManageDepartments/></AdminRoute>}/>
            <Route path="/admin/manage-clubs" element={<AdminRoute><ManageClubs/></AdminRoute> }/>
            <Route path="/admin/manage-courses" element={<AdminRoute><ManageCourses/></AdminRoute> }/>
            <Route path="/admin/manage-categories" element={<AdminRoute><ManageCategories/></AdminRoute> }/>




          <Route path="/register" element={<Register />} />
        </Routes>
      </AuthProvider>
    </ToastProvider>
      );
}

export default App;