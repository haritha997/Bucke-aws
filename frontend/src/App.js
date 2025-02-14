import React, { useState } from "react";
import axios from "axios";

function App() {
  const [bucketName, setBucketName] = useState("");
  const [message, setMessage] = useState("");



  const handleCreateBucket = async () => {
    if (!bucketName) {
      setMessage("Bucket name cannot be empty.");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/create-bucket/", {
        bucket_name: bucketName,
      });

      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data?.detail || "Error creating bucket.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-6 rounded-xl shadow-lg w-96">
        <h2 className="text-xl font-semibold mb-4 text-center">Create S3 Bucket</h2>
        <input
          type="text"
          placeholder="Enter bucket name"
          value={bucketName}
          onChange={(e) => setBucketName(e.target.value)}
          className="w-full p-2 border rounded-md mb-4"
        />
        <button
          onClick={handleCreateBucket}
          className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600"
        >
          Create Bucket
        </button>
        {message && <p className="mt-4 text-center text-red-500">{message}</p>}
      </div>
    </div>
  );
}

export default App;