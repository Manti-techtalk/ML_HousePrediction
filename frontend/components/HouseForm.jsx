import React, { useState } from 'react';
import axios from 'axios';

const HouseForm = () => {
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
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setPrediction(null);

    try {
      const response = await axios.post('http://localhost:8000/predict', {
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
    <div className="max-w-xl mx-auto bg-white p-6 rounded shadow mt-10">
      <h2 className="text-2xl font-bold mb-4 text-center">House Price Predictor</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        {Object.keys(formData).map((key) => (
          <div key={key}>
            <label className="block text-gray-700 capitalize">{key.replace('_', ' ')}</label>
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
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
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
  );
};

export default HouseForm;
