'use client'

import { useState } from "react";
import Link from "next/link";

export default function RegistrationPage() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        console.log("Email:", email);
        console.log("Password:", password)

        try {
            const response = await fetch("http://localhost:8000/api/users", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    email: email,
                    password: password,
                }),
            })

            localStorage.setItem("email", email);

            window.location.href = "/";
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
            <h1>Registration</h1> <br />
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
            <button type="submit" onClick={handleSubmit}
                            style={{
                                outline: '2px solid white',
                                backgroundColor: 'transparent',
                                color: 'white',
                                padding: '8px',
                                borderRadius: '4px',
                                marginBottom: '10px',
                                border: 'none'
                            }}>
                                Register
            </button> <br />
            <p>Already have an account? <Link href="/login">Log in</Link></p>
        </div>
    )
}