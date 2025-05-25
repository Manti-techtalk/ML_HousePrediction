'use client';

import React, { useState } from 'react';
import Head from 'next/head';
import axios from 'axios';

const Home = () => {
  const [formData, setFormData] = useState({
    latitude: '',
    longitude: '',
    total_rooms: '',
    population: '',
    households: '',
    median_income: ''
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setPrediction(null);

    try {
      const response = await axios.post('http://127.0.0.1:8000/predict', {
        latitude: parseFloat(formData.latitude),
        longitude: parseFloat(formData.longitude),
        total_rooms: parseFloat(formData.total_rooms),
        population: parseFloat(formData.population),
        households: parseFloat(formData.households),
        median_income: parseFloat(formData.median_income)
      });
      setPrediction(response.data.prediction);
    } catch (err) {
      console.error(err);
      alert('Prediction failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6 flex flex-col items-center justify-center">
      <Head>
        <title>House Price Predictor</title>
      </Head>
      <div className="max-w-xl w-full bg-white p-6 rounded shadow">
        <h2 className="text-2xl font-bold mb-4 text-center">House Price Predictor</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          {Object.keys(formData).map(key => (
            <div key={key}>
              <label className="block text-gray-700 capitalize mb-1">{key.replace('_', ' ')}</label>
              <input
                type="number"
                name={key}
                value={formData[key]}
                onChange={handleChange}
                required
                className="w-full border px-4 py-2 rounded"
              />
            </div>
          ))}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Predicting...' : 'Predict'}
          </button>
        </form>

        {prediction !== null && (
          <div className="mt-6 text-center">
            <p className="text-xl text-green-600 font-semibold">
              Predicted Price: ${prediction.toFixed(2)}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;
