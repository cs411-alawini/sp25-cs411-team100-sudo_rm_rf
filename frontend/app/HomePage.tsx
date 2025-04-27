'use client';

import { useState, useEffect } from 'react';

import NavigationBar from './components/NavigationBar';

// Define interfaces for the expected data structures from your backend endpoints
// These are examples and may need adjustment based on your actual backend responses.

// Interface for the original search endpoint (/search/) - based on your provided code and backend
interface OriginalSearchResult {
  rxcui: string;
  lat: string;
  ts: string | null;
  lui: string | null;
  stt: string | null;
  sui: string | null;
  ispref: string | null;
  rxaui: string;
  saui: string | null;
  scui: string | null;
  sdui: string | null;
  sab: string;
  tty: string;
  str: string;
  srl: string | null;
  suppress: string | null;
  cvf: string | null;
}


// Interfaces for the four new query endpoints (adjust based on your backend)
interface TopInteraction {
    avg_prr: number;
    interaction_count: number;
    drug_1_name: string;
    drug_2_name: string;
}

interface SubstanceConditions {
    drug_name: string;
    RXCUI: string;
    condition_count: number;
}

interface UserDrugs {
    RXCUI: string;
    // Add other drug details if your endpoint returns them
}

interface DrugInteractions {
    RXCUI2: string; // Or RXCUI1, depending on which is the interacting drug in the result
    interaction_count: number;
    // Add other details about the interacting drug if available
}


export default function Home() {
    // Original State for the initial search
    const [originalQuery, setOriginalQuery] = useState('');
    const [originalSearchResults, setOriginalSearchResults] = useState<OriginalSearchResult[]>([]);
    const [loadingOriginalSearch, setLoadingOriginalSearch] = useState(false);
    const [errorOriginalSearch, setErrorOriginalSearch] = useState<string | null>(null);


    // State for Query 1: Top Interactions by PRR
    const [topInteractions, setTopInteractions] = useState<TopInteraction[]>([]);
    const [loadingTopInteractions, setLoadingTopInteractions] = useState(false);
    const [errorTopInteractions, setErrorTopInteractions] = useState<string | null>(null);

    // State for Query 2: Substances Invoking Most Conditions
    const [substanceConditions, setSubstanceConditions] = useState<SubstanceConditions[]>([]);
    const [loadingSubstanceConditions, setLoadingSubstanceConditions] = useState(false);
    const [errorSubstanceConditions, setErrorSubstanceConditions] = useState<string | null>(null);

    // State for Query 3: User's Drugs
    const [userId, setUserId] = useState('');
    const [userDrugs, setUserDrugs] = useState<UserDrugs[]>([]);
    const [loadingUserDrugs, setLoadingUserDrugs] = useState(false);
    const [errorUserDrugs, setErrorUserDrugs] = useState<string | null>(null);

    // State for Query 4: Drugs Interacting Most with a Given Drug
    const [drugRxcui, setDrugRxcui] = useState('');
    const [drugInteractions, setDrugInteractions] = useState<DrugInteractions[]>([]);
    const [loadingDrugInteractions, setLoadingDrugInteractions] = useState(false);
    const [errorDrugInteractions, setErrorDrugInteractions] = useState<string | null>(null);

    const [isClient, setIsClient] = useState(false);

    useEffect(() => {
        setIsClient(true);
    }, []);

    useEffect(() => {
        if (localStorage.getItem('email') === null) {
            window.location.href = '/login';
        }
    }, [])

     // Original Handler for the initial search
     const handleOriginalSearch = async () => {
        if (!originalQuery) {
            setOriginalSearchResults([]);
            return;
        }
        setLoadingOriginalSearch(true);
        setErrorOriginalSearch(null);
        try {
            // Original API endpoint for the initial search
            const res = await fetch(`http://localhost:8000/search/?q=${originalQuery}`);
            if (!res.ok) {
                 throw new Error(`HTTP error! status: ${res.status}`);
            }
            const data: OriginalSearchResult[] = await res.json();
            setOriginalSearchResults(data);
        } catch (error: any) {
            setErrorOriginalSearch(error.message);
        } finally {
            setLoadingOriginalSearch(false);
        }
     };


    // Handler for Query 1: Fetch Top Interactions
    const fetchTopInteractions = async () => {
        setLoadingTopInteractions(true);
        setErrorTopInteractions(null);
        try {
            // Replace with your actual API endpoint for Query 1
            const res = await fetch('http://localhost:8000/api/top-interactions-by-prr');
            if (!res.ok) {
                 throw new Error(`HTTP error! status: ${res.status}`);
            }
            const data: TopInteraction[] = await res.json();
            setTopInteractions(data);
        } catch (error: any) {
            setErrorTopInteractions(error.message);
        } finally {
            setLoadingTopInteractions(false);
        }
    };

    // Handler for Query 2: Fetch Substances Invoking Most Conditions
    const fetchSubstanceConditions = async () => {
        setLoadingSubstanceConditions(true);
        setErrorSubstanceConditions(null);
        try {
            // Replace with your actual API endpoint for Query 2
            const res = await fetch('http://localhost:8000/api/top-drugs-by-conditions');
             if (!res.ok) {
                 throw new Error(`HTTP error! status: ${res.status}`);
            }
            const data: SubstanceConditions[] = await res.json();
            setSubstanceConditions(data);
        } catch (error: any) {
            setErrorSubstanceConditions(error.message);
        } finally {
            setLoadingSubstanceConditions(false);
        }
    };

    // Handler for Query 3: Fetch User's Drugs by User ID
    const fetchUserDrugs = async () => {
        if (!userId) {
            setUserDrugs([]);
            return;
        }
        setLoadingUserDrugs(true);
        setErrorUserDrugs(null);
        try {
            // Replace with your actual API endpoint for Query 3, using userId as a query parameter
            const res = await fetch(`YOUR_BACKEND_API_ENDPOINT/user-drugs/?userId=${userId}`);
             if (!res.ok) {
                 throw new Error(`HTTP error! status: ${res.status}`);
            }
            const data: UserDrugs[] = await res.json();
            setUserDrugs(data);
        } catch (error: any) {
            setErrorUserDrugs(error.message);
        } finally {
            setLoadingUserDrugs(false);
        }
    };

    // Handler for Query 4: Fetch Drugs Interacting Most with a Given Drug
    const fetchDrugInteractions = async () => {
         if (!drugRxcui) {
            setDrugInteractions([]);
            return;
        }
        setLoadingDrugInteractions(true);
        setErrorDrugInteractions(null);
        try {
            // Replace with your actual API endpoint for Query 4, using drugRxcui as a query parameter
            const res = await fetch(`http://localhost:8000/api/interacting-drugs/${drugRxcui}`);
             if (!res.ok) {
                 throw new Error(`HTTP error! status: ${res.status}`);
            }
            const data: DrugInteractions[] = await res.json();
            setDrugInteractions(data);
        } catch (error: any) {
            setErrorDrugInteractions(error.message);
        } finally {
            setLoadingDrugInteractions(false);
        }
    };


    return (
        <div>
            <NavigationBar />

            <div className="p-4 max-w-4xl mx-auto space-y-8">
                <h1 className="text-3xl font-bold text-center mb-8">MedWise Application Entry Point</h1>

                {/* Original Search Section */}
                <div className="border p-4 rounded shadow">
                    <h2 className="text-2xl font-semibold mb-4">Search Drug Concepts (Original)</h2>
                    <input
                        type="text" // Changed from number to text based on previous discussion
                        value={originalQuery}
                        onChange={(e) => setOriginalQuery(e.target.value)}
                        className="border p-2 w-full mb-4 rounded"
                        placeholder="Search by RXCUI or name..."
                    />
                    <button
                        onClick={handleOriginalSearch}
                        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                    >
                        Search
                    </button>

                    {loadingOriginalSearch && <p className="mt-2">Loading original search results...</p>}
                    {errorOriginalSearch && <p className="mt-2 text-red-500">Error: {errorOriginalSearch}</p>}
                    {!loadingOriginalSearch && !errorOriginalSearch && originalSearchResults.length > 0 && (
                        <ul className="mt-4 space-y-2">
                            {originalSearchResults.map((item, index) => (
                            // Assuming RXAUI is unique for the key based on the original search result structure
                            <li key={item.rxaui || index} className="border-b py-2">
                                    <strong>Atom name: {item.str}</strong>{"\n"}
                                    RXCUI: {item.rxcui},
                                    RXAUI: {item.rxaui},
                                    Source vocabulary: {item.sab},
                                    Term Type: {item.tty}
                                </li>
                            ))}
                        </ul>
                    )}
                    {!loadingOriginalSearch && !errorOriginalSearch && originalSearchResults.length === 0 && originalQuery && (
                        <p className="mt-2">No results found for "{originalQuery}".</p>
                    )}
                    {!loadingOriginalSearch && !errorOriginalSearch && originalSearchResults.length === 0 && !originalQuery && (
                        <p className="mt-2">Enter a query in the search box above.</p>
                    )}
                </div>


                {/* Section for Query 1: Top Interactions by PRR */}
                <div className="border p-4 rounded shadow">
                    <h2 className="text-2xl font-semibold mb-4">Top 15 Interactions by PRR</h2>
                    <button
                        onClick={fetchTopInteractions}
                        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                    >
                        Fetch Top Interactions
                    </button>

                    {loadingTopInteractions && <p className="mt-2">Loading top interactions...</p>}
                    {errorTopInteractions && <p className="mt-2 text-red-500">Error: {errorTopInteractions}</p>}
                    {!loadingTopInteractions && !errorTopInteractions && topInteractions.length > 0 && (
                        <ul className="mt-4 space-y-2">
                            {topInteractions.map((item, index) => (
                                <li key={index} className="border-b py-2">
                                    <p><strong>Drug 1:</strong> {item.drug_1_name}</p>
                                    <p><strong>Drug 2:</strong> {item.drug_2_name}</p>
                                    <p><strong>Average PRR:</strong> {item.avg_prr}</p>
                                    <p><strong>Interaction Count:</strong> {item.interaction_count}</p>
                                </li>
                            ))}
                        </ul>
                    )}
                    {!loadingTopInteractions && !errorTopInteractions && topInteractions.length === 0 && (
                        <p className="mt-2">No top interactions found.</p>
                    )}
                </div>

                {/* Section for Query 2: Substances Invoking Most Conditions */}
                <div className="border p-4 rounded shadow">
                    <h2 className="text-2xl font-semibold mb-4">Substances Invoking Most Conditions</h2>
                    <button
                        onClick={fetchSubstanceConditions}
                        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                    >
                        Fetch Substances
                    </button>
                    {loadingSubstanceConditions && <p className="mt-2">Loading substance conditions...</p>}
                    {errorSubstanceConditions && <p className="mt-2 text-red-500">Error: {errorSubstanceConditions}</p>}
                    {!loadingSubstanceConditions && !errorSubstanceConditions && substanceConditions.length > 0 && (
                        <ul className="mt-4 space-y-2">
                            {substanceConditions.map((item, index) => (
                                <li key={index} className="border-b py-2">
                                    <p><strong>Drug Name:</strong> {item.drug_name}</p>
                                    <p><strong>RXCUI:</strong> {item.RXCUI}</p>
                                    <p><strong>Condition Count:</strong> {item.condition_count}</p>
                                </li>
                            ))}
                        </ul>
                    )}
                    {!loadingSubstanceConditions && !errorSubstanceConditions && substanceConditions.length === 0 && (
                        <p className="mt-2">No substance conditions found.</p>
                    )}
                </div>

                {/* Section for Query 3: User's Drugs */}
                <div className="border p-4 rounded shadow">
                    <h2 className="text-2xl font-semibold mb-4">List Drugs for a User</h2>
                    <input
                        type="text" // Use text type for potential non-numeric user IDs or flexibility
                        value={userId}
                        onChange={(e) => setUserId(e.target.value)}
                        className="border p-2 w-full mb-4 rounded"
                        placeholder="Enter User ID"
                    />
                    <button
                        onClick={fetchUserDrugs}
                        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                    >
                        Fetch User's Drugs
                    </button>
                    {loadingUserDrugs && <p className="mt-2">Loading user's drugs...</p>}
                    {errorUserDrugs && <p className="mt-2 text-red-500">Error: {errorUserDrugs}</p>}
                    {!loadingUserDrugs && !errorUserDrugs && userDrugs.length > 0 && (
                        <ul className="mt-4 space-y-2">
                            {userDrugs.map((item, index) => (
                                <li key={index} className="border-b py-2">
                                    <p><strong>Drug RXCUI:</strong> {item.RXCUI}</p>
                                    {/* Display other drug details if available */}
                                </li>
                            ))}
                        </ul>
                    )}
                    {!loadingUserDrugs && !errorUserDrugs && userDrugs.length === 0 && userId && (
                        <p className="mt-2">No drugs found for User ID "{userId}".</p>
                    )}
                    {!loadingUserDrugs && !errorUserDrugs && userDrugs.length === 0 && !userId && (
                        <p className="mt-2">Enter a User ID to search for drugs.</p>
                    )}
                </div>

                {/* Section for Query 4: Drugs Interacting Most with a Given Drug */}
                <div className="border p-4 rounded shadow">
                    <h2 className="text-2xl font-semibold mb-4">Drugs Interacting Most with a Given Drug</h2>
                    <input
                        type="text" // Use text type for potential non-numeric RXCUIs or flexibility
                        value={drugRxcui}
                        onChange={(e) => setDrugRxcui(e.target.value)}
                        className="border p-2 w-full mb-4 rounded"
                        placeholder="Enter Drug RXCUI"
                    />
                    <button
                        onClick={fetchDrugInteractions}
                        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                    >
                        Fetch Interactions
                    </button>
                    {loadingDrugInteractions && <p className="mt-2">Loading drug interactions...</p>}
                    {errorDrugInteractions && <p className="mt-2 text-red-500">Error: {errorDrugInteractions}</p>}
                    {!loadingDrugInteractions && !errorDrugInteractions && drugInteractions.length > 0 && (
                        <ul className="mt-4 space-y-2">
                            {drugInteractions.map((item, index) => (
                                <li key={index} className="border-b py-2">
                                    <p><strong>Interacting Drug RXCUI:</strong> {item.RXCUI2}</p> {/* Adjust field name based on your backend response */}
                                    <p><strong>Interaction Count:</strong> {item.interaction_count}</p>
                                    {/* Display other interacting drug details if available */}
                                </li>
                            ))}
                        </ul>
                    )}
                    {!loadingDrugInteractions && !errorDrugInteractions && drugInteractions.length === 0 && drugRxcui && (
                        <p className="mt-2">No interactions found for drug RXCUI "{drugRxcui}".</p>
                    )}
                    {!loadingDrugInteractions && !errorDrugInteractions && drugInteractions.length === 0 && !drugRxcui && (
                        <p className="mt-2">Enter a Drug RXCUI to search for interactions.</p>
                    )}
                </div>

            </div>
        </div>
    );
}