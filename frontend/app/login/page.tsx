'use client'

import { useState } from "react"
import Link from "next/link";

export default function LoginPage() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [errorMessage, setErrorMessage] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        console.log("Email:", email);
        console.log("Password:", password)

        // localStorage.setItem("email", email);

        // console.log("Email saved to local storage:", localStorage.getItem("email"));
        try {
            const response = await fetch("http://localhost:8000/api/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    email: email,
                    password: password,
                }),
            })

            const data = await response.json();

            if (response.status === 200) {
                localStorage.setItem("email", email);
                localStorage.setItem("user_id", data.user_id);
                window.location.href = "/";
            } else if (response.status === 401) {
                setErrorMessage("Invalid credentials. Please try again.");
            } else {
                console.log("Login failed")
            }
        } catch (error) {
            console.error("There has been an error:", error);
        }
    }

    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            height: '100vh',
        }}>
            <h1>Login</h1> <br />
            <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email"
                style={{
                    outline: '2px solid #3b82f6',
                    backgroundColor: 'transparent',
                    padding: '8px',
                    borderRadius: '4px',
                    marginBottom: '10px',
                    border: 'none'
                }}
            /> <br />
            <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                style={{
                    outline: '2px solid #3b82f6',
                    backgroundColor: 'transparent',
                    padding: '8px',
                    borderRadius: '4px',
                    marginBottom: '10px',
                    border: 'none'
                }}
            /> <br />
            <button type="submit" onClick={handleSubmit} style={{
                    backgroundColor: '#3b82f6',
                    color: 'white',
                    padding: '8px',
                    borderRadius: '4px',
                    marginBottom: '10px',
                    border: 'none'
                }}>Login</button>
                <p>No account? <Link href="/registration">Create one here</Link></p>
                {errorMessage && (
                <p style={{ color: 'red', marginBottom: '10px' }}>{errorMessage}</p>
            )}
        </div>
    )
}