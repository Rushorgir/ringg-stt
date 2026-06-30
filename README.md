# STT Ringg Batch Transcriber

A production-grade Python script to batch transcribe audio files using the Ringg Labs Speech-to-Text (STT) API.

## Features

- **Batch Processing:** Transcribes files individually or recurses through entire directories.
- **Audio Formats:** Supports `.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg`, and `.aac`.
- **Automatic Output Handling:** Saves transcripts to text files with duplicate naming protection.
- **MIME Auto-detection:** Dynamically detects and sets audio content types.

## Installation

1. Clone or download this repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

To use the script, you need a Ringg Labs API Key. You can provide it in two ways:

1. **Environment Variable (Recommended):**
   Set the `RINGG_API_KEY` in your environment:
   ```bash
   export RINGG_API_KEY="your-api-key-here"
   ```

2. **Command Line Option:**
   Pass it via the `--api-key` or `-k` flag when running the script.

## Usage

Run the script with the path(s) to the audio files or directories you want to transcribe:

```bash
python STT_Ringg.py [inputs...] [options]
```

### Examples

- **Transcribing a directory (using env variable):**
  ```bash
  python STT_Ringg.py path/to/your/audio/folder
  ```

- **Transcribing a specific file and specifying the API key:**
  ```bash
  python STT_Ringg.py path/to/audio/file.mp3 --api-key YOUR_API_KEY
  ```

- **Saving results to a custom output directory:**
  ```bash
  python STT_Ringg.py path/to/your/audio/folder --output-dir path/to/your/text/folder
  ```

- **Transcribing without saving text files (stdout print only):**
  ```bash
  python STT_Ringg.py path/to/audio/file.mp3 --no-save
  ```

### CLI Options

| Option | Shorthand | Default | Description |
|---|---|---|---|
| `inputs` | | `["path/to/your/audio/folder"]` | Paths to files or directories containing audio. |
| `--api-key` | `-k` | `os.environ.get("RINGG_API_KEY")` | Ringg Labs API Key. |
| `--language` | `-l` | `"en"` | Language code for transcription. |
| `--output-dir`| `-o` | `"path/to/your/text/folder"` | Directory to save transcriptions. |
| `--no-save` | | `False` | Only print transcriptions to stdout, do not save files. |
