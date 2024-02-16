import { Button, CssBaseline } from '@mui/joy';
import FormControl from '@mui/joy/FormControl';
import FormLabel from '@mui/joy/FormLabel';
import Input from '@mui/joy/Input';
import Sheet from '@mui/joy/Sheet';
import Typography from '@mui/joy/Typography';
import Link from 'next/link';


export default function Login(){


    return (
        <main>
        <CssBaseline />
        <Sheet
        sx={{
            width: 400,
            mx: 'auto', // margin left & right
            my: 5, // margin top & bottom
            py: 3, // padding top & bottom
            px: 4, // padding left & right
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
            <Typography level="body-sm">Sign in to continue.</Typography>
         </div>
        <FormControl>
            <FormLabel>Username</FormLabel>
            <Input
                // html input attribute
                name="username"
                type="email"
                placeholder="johndoe"
            />
        </FormControl>
        <FormControl>
            <FormLabel>Password</FormLabel>
            <Input
                // html input attribute
                name="password"
                type="password"
                placeholder="password"
            />
        </FormControl>
        <Button variant="solid" sx={{ mt: 1 /* margin top */ }}>Log in</Button>
        <Typography
            endDecorator={<Link href="/sign-up">Sign up</Link>}
            fontSize="sm"
            sx={{ alignSelf: 'center' }}
            >
            Don&apos;t have an account?
        </Typography>
        </Sheet>
        </main>
    )
}