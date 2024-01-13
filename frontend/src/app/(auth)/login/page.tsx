"use client"
import { UserContext } from "@/contexts/userContext";
import { authService } from "@/services";
import { Button, CssVarsProvider, FormControl, FormLabel, Input, Sheet, Typography } from "@mui/joy";
import { useRouter } from "next/navigation";
import { useContext, useEffect, useLayoutEffect, useState } from "react";


const Login = () => {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const session = useContext(UserContext);
    const router = useRouter();


    const handleSubmit = async () => {
        if(!username || !password) {
            alert("All fields are required");
        }
        else{
            await authService.login(username, password).then((res) => {
                if (res) {
                    session.setToken(res.access_token);
                    router.push("/home");
                }
            })
        }
    }

    return (
        <CssVarsProvider>
        <main>
        <Sheet
        sx={{
          width: 600,
          mx: 'auto', // margin left & right
          my: 4, // margin top & bottom
          py: 3, // padding top & bottom
          px: 2, // padding left & right
          display: 'flex',
          flexDirection: 'column',
          gap: 2,
          borderRadius: 'sm',
          boxShadow: 'md',
        }}
        variant="outlined"
         >
            <div>
            <Typography level="h4" component="h1">
              <b>Welcome!</b>
            </Typography>
            <Typography level="body-sm">Sign in to continue. session: {session.token}</Typography>
          </div>
          <FormControl>
            <FormLabel>Email</FormLabel>
            <Input
              // html input attribute
              name="email"
              type="email"
              placeholder="johndoe@email.com"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </FormControl>
          <FormControl>
            <FormLabel>Password</FormLabel>
            <Input
              // html input attribute
              name="password"
              type="password"
              placeholder="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </FormControl>

          <Button sx={{ mt: 1 /* margin top */ }} onClick = {handleSubmit} >Log in</Button>
      </Sheet>
      </main>
      </CssVarsProvider>
    )
}

export default Login;