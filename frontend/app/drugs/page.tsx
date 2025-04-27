'use client'

import NavigationBar from "../components/NavigationBar";

import { useState, useEffect } from "react";

export default function DrugsPage() {

    const [drugsData, setDrugData] = useState([]);

    const fetchData = async () => {
        try {
            const response = await fetch("http://localhost:8000/api/conditions", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    user_id: localStorage.getItem("user_id"),
                }),
            });

            if (!response.ok) {
                throw new Error("Failed to fetch data");
            }

            const data = await response.json();
            setDrugData(data); // Update state with the fetched data
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    }

    useEffect(() => {
        fetchData();
    }, [])

    return (
        <div>
            <NavigationBar />
            <h1>Drugs</h1>
            <p>Drugs page</p>

            <br />

            <ul>
                {drugsData.map((drug, index) => (
                    <li key={index}>
                        <strong>Drug 1:</strong> {drug.drug_1_concept_name}, 
                        <strong> Drug 2:</strong> {drug.drug_2_concept_name}, 
                        <strong> Condition:</strong> {drug.condition_concept_name}
                    </li>
                ))}
            </ul>
        </div>
    )
}