# genai-mash-game

A version of the MASH game using Python, React &amp; Generative AI to let users modify the theme and categories

## Quick Start

```bash
# Clone the repository
git clone https://github.com/your-username/genai-mash-game.git
cd genai-mash-game

# Install python dependencies
pip install -r requirements.txt

# Build the frontend
cd frontend
npm install
npm run build
cd ..

# Run the backend server
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
```

Other commands:

Stop the server (port 8000):

```bash
fuser -k 8000/tcp
```

Build the frontend after modification:

```bash
cd frontend && npm run build; cd ..
```

## LLM Access

The app allows you to use Groq or Huggingface models. Both require an API key.

You can do one of the following:

- Create a `.env` file in the project root containing your API key(s).
- Run this in the terminal: `export HUGGINGFACE_HUB_TOKEN=your_hf_token`
- Supply the API key in the UI.
  - **Note**: This is just for convenience and testing!! This app in its current state is intended for local use for testing purposes **ONLY**! Passing an API key to the endpoints would require HTTPS if hosted remotely!

A `.env` file should look something like this:

```bash
GROQ_API_KEY=gsk_x...
HUGGINGFACE_HUB_TOKEN=hf_F...
```

The models used are:

- Groq: `llama3-8b-8192`
- Huggingface: `microsoft/Phi-4-mini-instruct`

## Playing the Game

1. Select the LLM provider platform: Groq is usually faster, Huggingface runs on your local machine
   - **Note**: When running a huggingface model for the first time it will need to download the files, so there will be a delay of a few seconds or minutes, depending on your network speed. Subsequent use will be quicker.
1. Add API key if necessary (i.e. it's not in your `.env` file or exported directly)
1. Check the 'Classic Mode' option if you want to use the standard categories (Spuse, Number of kids, Job, Car), otherwise it will use the generative AI method.
1. *(If you did NOT check 'Classic Mode')* Enter a 'theme' for the game, e.g. Food, Superheroes, Health & Wellbeing.
1. Fill out all fields for each category.
1. Click on **"Get Magic Number"**: Your randomly chosen magic number will be shown.
1. Finally, click on **"Play Game"** to start the game and see your results!

Good luck!

## API Reference

The app provides the following 3 endpoints, required to run the game:

---

### /api/magic_number

Retrieves a randomly-generated magic number between 2-10

- **Request:**
  - `GET` method
  - No request body
- **Response:**

    ```json
    {
      "magic_number": 3,
    }
    ```

---

### /api/generate_options

- **Request:**
  - `POST` method

  ```json
  {
    "theme":"Animals",
    "platform":"groq",
    "api_key":"gps_xxx..."
  }
  ```

- **Response:**

    ```json
    {
        [
            "Habitat",
            "Diet",
            "Social Structure",
            "Adaptation"
        ]
    }
    ```

---

### /api/play

- **Request:**
  - `POST` method

  ```json
    {
        "categories": [
            {
                "name": "Constellation",
                "options": [
                    "Orion",
                    "Ursa Major",
                    "Cassiopeia"
                ]
            },
            {
                "name": "Galaxy",
                "options": [
                    "Andromeda",
                    "Milky Way",
                    "Triangulum"
                ]
            },
            {
                "name": "Star System",
                "options": [
                    "Alpha Centauri",
                    "Castor",
                    "Solar System"
                ]
            },
            {
                "name": "Black Hole",
                "options": [
                    "Cygnus x-1",
                    "Sagittarius A",
                    "Abell 1201"
                ]
            }
        ],
        "magic_number": 3
    }

  ```

- **Response:**

    ```json
    {
        "MASH": "Mansion",
        "Constellation": "Orion",
        "Galaxy": "Andromeda",
        "Star System": "Alpha Centauri",
        "Black Hole": "Cygnus x-1"
    }
    ```
