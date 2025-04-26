'use client'

import { useState } from "react"

export default function LoginPage() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")

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
            <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email"
                style={{
                    outline: '2px solid white',
                    backgroundColor: 'transparent',
                    color: 'white',
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
                    outline: '2px solid white',
                    backgroundColor: 'transparent',
                    color: 'white',
                    padding: '8px',
                    borderRadius: '4px',
                    marginBottom: '10px',
                    border: 'none'
                }}
            /> <br />
            <button type="submit" onClick={handleSubmit} style={{
                    outline: '2px solid white',
                    backgroundColor: 'transparent',
                    color: 'white',
                    padding: '8px',
                    borderRadius: '4px',
                    marginBottom: '10px',
                    border: 'none'
                }}>Login</button>
        </div>
    )
}