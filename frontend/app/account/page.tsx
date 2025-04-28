'use client';

import NavigationBar from "../components/NavigationBar";

import { useState } from "react"

export default function AccountPage() {
    const [password, setPassword] = useState("")

    const handleDelete = async (e: React.FormEvent) => {
        try {
            e.preventDefault();

            const response = await fetch("http://localhost:8000/api/users", {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    user_id: localStorage.getItem("user_id")
                }),
            })

            localStorage.removeItem("email");
            localStorage.removeItem("user_id");

            window.location.href = "/registration";
        } catch (error) {
            console.error("There has been an error:", error);
        }
    }

    const handleUpdate = async (e: React.FormEvent) => {
        try {
            e.preventDefault();

            const response = await fetch("http://localhost:8000/api/password", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    user_id: localStorage.getItem("user_id"),
                    password_hash: password
                }),
            })
        } catch (error) {
            console.error("There has been an error:", error);
        }
    }

    return (
        <div>
            <NavigationBar />

            <div className="border p-4 rounded width-50% w-1/2">
                    <h2 className="text-2xl font-semibold mb-4">Update password</h2>
                    <input
                        type="email"
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

                    <button onClick = {handleUpdate} className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Update password</button>
                </div>

            <button style = {{
                backgroundColor: 'red'
            }} onClick = {handleDelete}>Delete account</button>
        </div>
    )
}