"use client";
import { UserContext } from "@/contexts/userContext";
import { authService } from "@/services";
import { Button } from "@mui/joy";
import { useRouter } from "next/navigation";
import { useContext } from "react";

const Home = () => {

    const session = useContext(UserContext);
    const router = useRouter();

    const handleSubmit = () => {
        session.logOut();
        router.push("/login");
    }

    return (
        <div>
            <h1>Home</h1>
            <p>{session.user?.username}</p>
            <p>{session.user?.email}</p>
            <p>{session.user?.id}</p>
            <br />
            <Button onClick={handleSubmit} >Logout</Button>
        </div>
    )
}

export default Home