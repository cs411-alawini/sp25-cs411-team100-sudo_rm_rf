'use client';

import NavigationBar from "../components/NavigationBar";

export default function AccountPage() {
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

    return (
        <div>
            <NavigationBar />

            <button style = {{
                backgroundColor: 'red'
            }} onClick = {handleDelete}>Delete account</button>
        </div>
    )
}