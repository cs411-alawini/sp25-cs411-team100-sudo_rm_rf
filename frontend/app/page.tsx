"use client"
import { useState, useEffect } from 'react';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);


  const handleSearch = async () => {
    const res = await fetch(`http://localhost:8000/search/?q=${query}`);
    const data = await res.json();
    setResults(data);
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Search Drug Concepts</h1>
      <input
        type="number"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="border p-2 w-full mb-4"
        placeholder="Search by RXCUI..."
      />
      <button
        onClick={handleSearch}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        Search
      </button>

      <ul className="mt-6">
        {results.map((item, index) => (
          <li key={index} className="border-b py-2">
            <strong>Atom name: {item.str}</strong>{"\n"} RXAUI: {item.rxaui}, Source vocabulary: {item.sab}
          </li>
        ))}
      </ul>
    </div>
  );
}
