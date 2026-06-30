import os
import sys
import argparse
import mimetypes
from pathlib import Path
from ringglabs.stt import Client

# Supported audio extensions
SUPPORTED_EXTENSIONS = {'.wav', '.mp3', '.m4a', '.flac', '.ogg', '.aac'}

def parse_arguments():
    parser = argparse.ArgumentParser(description="Batch transcribe audio files using Ringg Labs STT API.")
    parser.add_argument(
        "inputs",
        nargs="*",
        default=["path/to/your/audio/folder"],
        help="Paths to audio files or directories containing audio files. Defaults to 'path/to/your/audio/folder'."
    )
    parser.add_argument(
        "--api-key",
        "-k",
        default=os.environ.get("RINGG_API_KEY", "YOUR_API_KEY"),
        help="Ringg Labs API Key. Defaults to the RINGG_API_KEY environment variable."
    )
    parser.add_argument(
        "--language",
        "-l",
        default="en",
        help="Language code for transcription (default: en)."
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="path/to/your/text/folder",
        help="Directory to save transcription text files. Defaults to 'path/to/your/text/folder'."
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Do not save transcriptions to .txt files, only print to stdout."
    )
    return parser.parse_args()

def collect_files(inputs):
    files_to_process = []
    for path_str in inputs:
        path = Path(path_str)
        if not path.exists():
            print(f"Warning: Path does not exist: {path}", file=sys.stderr)
            continue
        
        if path.is_file():
            if path.suffix.lower() in SUPPORTED_EXTENSIONS:
                files_to_process.append(path)
            else:
                print(f"Warning: File extension '{path.suffix}' might not be supported, adding anyway: {path}", file=sys.stderr)
                files_to_process.append(path)
        elif path.is_dir():
            for child in path.rglob("*"):
                if child.is_file() and child.suffix.lower() in SUPPORTED_EXTENSIONS:
                    files_to_process.append(child)
                    
    return sorted(list(set(files_to_process)))

def main():
    args = parse_arguments()
    
    if not args.api_key or args.api_key == "YOUR_API_KEY":
        print("Error: API key is not set. Please set the RINGG_API_KEY environment variable or pass --api-key / -k.", file=sys.stderr)
        sys.exit(1)
        
    files = collect_files(args.inputs)
    if not files:
        print("No files found to process.", file=sys.stderr)
        sys.exit(0)
        
    print(f"Found {len(files)} file(s) to transcribe.")
    
    # Initialize output directory if saving is enabled
    if not args.no_save:
        output_path = Path(args.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = None

    try:
        with Client(api_key=args.api_key) as client:
            for idx, file_path in enumerate(files, 1):
                print(f"\n[{idx}/{len(files)}] Transcribing: {file_path.name}")
                try:
                    # Dynamically detect content type using mimetypes
                    mime_type, _ = mimetypes.guess_type(file_path)
                    content_type = mime_type or "audio/wav"
                    
                    result = client.transcribe(str(file_path), language=args.language, content_type=content_type)
                    transcription = result.transcription
                    
                    # Print results
                    print("-" * 40)
                    print(transcription)
                    print("-" * 40)
                    
                    # Save results
                    if not args.no_save and output_path:
                        save_path = output_path / f"{file_path.stem}.txt"
                        
                        # Handle potential filename collisions in the output directory
                        counter = 1
                        while save_path.exists():
                            save_path = output_path / f"{file_path.stem}_{counter}.txt"
                            counter += 1
                        
                        save_path.write_text(transcription, encoding="utf-8")
                        print(f"Saved transcript to: {save_path}")
                        
                except Exception as e:
                    print(f"Error transcribing {file_path.name}: {e}", file=sys.stderr)
                    
    except Exception as e:
        print(f"Failed to initialize client or connect: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()