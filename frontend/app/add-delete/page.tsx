'use client'

import { useState, useEffect } from 'react';

export default function MedicationsPage() {
  const [medicationIdToAdd, setMedicationIdToAdd] = useState('');
  const [medicationIdToDelete, setMedicationIdToDelete] = useState('');
  const [resultSets, setResultSets] = useState([]);
  const [selectedResultId, setSelectedResultId] = useState('');

  // fetch result_ids on page load
  useEffect(() => {
    async function fetchResultSets() {
      try {
        const userId = localStorage.getItem('user_id');
        if (!userId) {
          console.error('No user_id found in localStorage');
          window.location.href = "/login"
          return;
        }
        const res = await fetch(`http://localhost:8000/api/result-sets?user_id=${userId}`)
        const data = await res.json();
        setResultSets(data); // Expecting [{id: 1, name: "Set 1"}, ...]
      } catch (error) {
        console.error('Error fetching result sets:', error);
      }
    }
    fetchResultSets();
  }, []);

  const handleAddMedication = async () => {
    if (!medicationIdToAdd || !selectedResultId) {console.log(medicationIdToAdd, selectedResultId); return;}
    try {
      const res = await fetch("http://localhost:8000/api/user-add-drugs", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          result_id: selectedResultId,
          rxcui: medicationIdToAdd,
        }),
      });
      if (res.ok) {
        alert('Medication added successfully');
        setMedicationIdToAdd('');
      } else {
        alert('Failed to add medication');
      }
    } catch (error) {
      console.error('Error adding medication:', error);
    }
  };

  const handleDeleteMedication = async () => {
    if (!medicationIdToDelete || !selectedResultId) return;
    try {
      const res = await fetch("http://localhost:8000/api/user-delete-drugs", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          result_id: selectedResultId,
          rxcui: medicationIdToDelete,
        }),
      });
      if (res.ok) {
        alert('Medication deleted successfully');
        setMedicationIdToDelete('');
      } else {
        alert('Failed to delete medication');
      }
    } catch (error) {
      console.error('Error deleting medication:', error);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8">
      <h1 className="text-3xl font-bold mb-6">Manage Medications</h1>

      <div className="mb-4">
        <label className="block mb-2 font-semibold">Select Medication Set:</label>
        <select
          className="border p-2 rounded"
          value={selectedResultId}
          onChange={(e) => setSelectedResultId(e.target.value)}
        >
          <option value="">Select a medication set</option>  {/* <--- Add this */}
          {resultSets.map((set) => (
            <option key={set["id"]} value={set["id"]}>
              {set["name"]}
            </option>
          ))}
        </select>
      </div>

      <div className="mb-6">
        <input
          type="number"
          placeholder="Medication ID to Add"
          className="border p-2 rounded mr-2"
          value={medicationIdToAdd}
          onChange={(e) => setMedicationIdToAdd(e.target.value)}
        />
        <button
          className="bg-blue-500 text-white p-2 rounded"
          onClick={handleAddMedication}
        >
          Add Medication
        </button>
      </div>

      <div>
        <input
          type="number"
          placeholder="Medication ID to Delete"
          className="border p-2 rounded mr-2"
          value={medicationIdToDelete}
          onChange={(e) => setMedicationIdToDelete(e.target.value)}
        />
        <button
          className="bg-red-500 text-white p-2 rounded"
          onClick={handleDeleteMedication}
        >
          Delete Medication
        </button>
      </div>
    </div>
  );
}