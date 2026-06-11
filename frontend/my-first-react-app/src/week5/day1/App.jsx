import { BrowserRouter, Route, Routes } from "react-router";
import { ThemeProvider } from "../../contexts/ThemeContext";
import { TodoFilterProvider } from "../../contexts/TodoFilterContext";
import { UserProvider } from "../../contexts/UserContext";
import Chat from "../../w4d5/Chat";
import Home from "./Home";
import Layout from "./Layout";
import Settings from "./Settings";

function App() {
    return (
        <ThemeProvider>
            <UserProvider>
                <TodoFilterProvider>
                    <BrowserRouter>
                        <Routes>
                            {/* 父路由使用 Layout 组件，其中包含 Outlet */}
                            <Route element={<Layout />}>
                                <Route path="/" element={<Home />} />
                                <Route path="/chat" element={<Chat />} />
                                <Route path="/settings" element={<Settings />} />
                            </Route>
                        </Routes>
                    </BrowserRouter>
                </TodoFilterProvider>
            </UserProvider>
        </ThemeProvider>
    );
}

export default App;