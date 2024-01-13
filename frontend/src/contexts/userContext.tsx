"use client";
import Cookies from "js-cookie";
import { createContext, useContext, useEffect, useState } from "react";
import { authService } from "../services";
import { User } from "../types/user";

type UserContextType = {
    user: User | null;
    setUser: (user: User | null) => void;
    logOut : () => void;
    token: string | null;
    setToken: (token: string | null) => void;
};

export const UserContext = createContext<UserContextType>({
    user: null,
    setUser: () => {},
    logOut: () => {},
    token: null,
    setToken: () => {},
});

export const UserProvider = ({ children }: { children: React.ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(null);

    useEffect(() => {
        const token = Cookies.get('_token');
        if(!token) return;
        setToken(token)
        console.log(token);
    }, [])

    useEffect(() => {
        if(!token) return;
        Cookies.set('_token', token);
        const fetchUser = async () => {
            await authService.getMe(token!).then((user) => {
                if (!user)
                {
                    setToken(null);
                }
                setUser(user);
            })
        }
        fetchUser();
    }, [token])

    
    const session = {
        user,
        setUser,
        logOut: () => {
            setToken(null);
            setUser(null);
            Cookies.remove('_token');
            authService.logout();
        },
        token,
        setToken
    }

    return (
        <UserContext.Provider value={session}>
            {children}
        </UserContext.Provider>
    )
}
