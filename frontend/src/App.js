import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [categories, setCategories] = useState([]);
  const [magicNumber, setMagicNumber] = useState(null);
  const [results, setResults] = useState(null);
  const [customTheme, setCustomTheme] = useState("");
  const [platform, setPlatform] = useState("huggingface");
  const [apiKey, setApiKey] = useState("");
  const [isClassicMode, setIsClassicMode] = useState(false);

  const classicCategories = [
    { name: "Spouse", options: ["", "", ""] },
    { name: "Number of kids", options: ["", "", ""] },
    { name: "Job", options: ["", "", ""] },
    { name: "Car", options: ["", "", ""] },
  ];

  useEffect(() => {
    if (isClassicMode) {
      // Original hard-coded categories
      setCategories(classicCategories);
    } else {
      // Clear categories when switching back to AI mode
      setCategories([]);
    }
  }, [isClassicMode]);

  const handleCategoryChange = (categoryIndex, optionIndex, value) => {
    const newCategories = [...categories];
    newCategories[categoryIndex].options[optionIndex] = value;
    setCategories(newCategories);
  };

  const getMagicNumber = async () => {
    const response = await fetch("/api/magic_number");
    const data = await response.json();
    setMagicNumber(data.magic_number);
  };

  const generateOptions = async () => {
    if (!customTheme) return;
    try {
      const response = await fetch("/api/generate_options", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          theme: customTheme,
          platform: platform,
          apiKey: apiKey,
        }),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to generate options");
      }
      const data = await response.json();
      const newCategories = data.options.map((categoryName) => ({
        name: categoryName,
        options: ["", "", ""], // Initialize with empty options for user input
      }));
      setCategories(newCategories);
      setCustomTheme(""); // Clear the input after generating
    } catch (error) {
      console.error("Error generating options:", error.message);
      alert(`Error: ${error.message}`);
    }
  };

  const playGame = async () => {
    const response = await fetch("/api/play", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ categories, magic_number: magicNumber }),
    });
    const data = await response.json();
    setResults(data);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>MASH</h1>
        <p>The game of Mansion, Apartment, Shack, House...</p>
        <h2>But with AI! 🤖</h2>
        <p>
          <a href="#game-container" class="play-button">
            Play
          </a>
        </p>
      </header>
      <div id="game-container" className="game-container">
        <div className="platform-selection">
          <h3>Select Platform</h3>
          <select value={platform} onChange={(e) => setPlatform(e.target.value)}>
            <option value="huggingface">Hugging Face</option>
            <option value="groq">Groq</option>
          </select>
        </div>
        <div className="api-key-input">
          <h3>API Key (if required)</h3>
          <input
            type="text"
            value={apiKey || ""}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="Enter API Key"
          />
        </div>
        <div id="mode-toggle" className="mode-toggle">
          <label>
            <input type="checkbox" checked={isClassicMode} onChange={(e) => setIsClassicMode(e.target.checked)} />
            Classic Mode
          </label>
        </div>
        {isClassicMode ? (
          <div className="categories">
            {categories.map((category, categoryIndex) => (
              <div key={categoryIndex} className="category">
                <h3>{category.name}</h3>
                {category.options.map((option, optionIndex) => (
                  <input
                    key={optionIndex}
                    type="text"
                    value={option}
                    onChange={(e) => handleCategoryChange(categoryIndex, optionIndex, e.target.value)}
                    placeholder={`Option ${optionIndex + 1}`}
                  />
                ))}
              </div>
            ))}
          </div>
        ) : (
          <div>
            <div className="custom-theme">
              <h3>Generate Categories from a Theme (LLM)</h3>
              <input
                type="text"
                value={customTheme}
                onChange={(e) => setCustomTheme(e.target.value)}
                placeholder="Enter a theme (e.g., Superheroes)"
              />
              <button onClick={generateOptions}>Generate Categories</button>
            </div>
            <div className="categories">
              {categories.map((category, categoryIndex) => (
                <div key={categoryIndex} className="category">
                  <h3>{category.name}</h3>
                  {category.options.map((option, optionIndex) => (
                    <input
                      key={optionIndex}
                      type="text"
                      value={option}
                      onChange={(e) => handleCategoryChange(categoryIndex, optionIndex, e.target.value)}
                      placeholder={`Option ${optionIndex + 1}`}
                    />
                  ))}
                </div>
              ))}
            </div>
          </div>
        )}

        <button onClick={getMagicNumber} disabled={magicNumber !== null}>
          Get Magic Number
        </button>
        {magicNumber && <p>Magic Number: {magicNumber}</p>}
        <button
          onClick={playGame}
          disabled={!magicNumber || categories.some((cat) => cat.options.some((opt) => opt === ""))}
        >
          Play Game
        </button>
        {results && (
          <div className="results">
            <h2>Your Future:</h2>
            {Object.entries(results).map(([category, option]) => (
              <p key={category}>
                <strong>{category}:</strong> {option}
              </p>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
