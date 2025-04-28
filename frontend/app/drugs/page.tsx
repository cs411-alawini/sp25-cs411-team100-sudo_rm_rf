'use client'

import NavigationBar from "../components/NavigationBar";

import { useState, useEffect } from "react";

export default function DrugsPage() {

    const [drugsData, setDrugData] = useState([]);
    const [rxcui, setRXCUI] = useState([]);

    const fetchDrugs = async () => {
        try {
            const response = await fetch("http://localhost:8000/api/user-drugs", {
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
            setRXCUI(data);

            console.log("Drugs data:", data);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    }

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
            setDrugData(data);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    }

    useEffect(() => {
        fetchData();
        fetchDrugs();
    }, [])

    return (
        <div>
            <NavigationBar />
            <p>Drugs page</p>
            <br />

            <h1>Drugs</h1>
            
            {/* <ul>
                {rxcui.map((drug, index) => (
                    <li key={index}>
                        <strong>Drug:</strong> {drug.RXCUI}
                ))} </li>
            </ul> */}
            <ul>
                {rxcui.map((drug, index) => (
                        <li key={index}>
                            Medication Set: {drug.result_id} : <strong>Drug:</strong> {drug.RXCUI}
                        </li>
                    ))
                }
            </ul>
            <br />

            <h1>Drug-Drug Interactions</h1>

            <ul>
                {drugsData.map((drug, index) => (
                    <li key={index}>
                        <strong>Drug 1:</strong> {drug.drug_1_concept_name}, 
                        <strong> Drug 2:</strong> {drug.drug_2_concept_name}, 
                        <strong> Maximum Probability of interaction:</strong> {drug.mean_reporting_frequency}
                    </li>
                ))}
            </ul>
        </div>
    )
}