"""Main entry point for MINA MVP-0 multi-agent reasoning system."""

import os
import sys
import argparse
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    # Try to import from Mina_Core for Google Drive integration
    from Mina_Core.drive_auth import get_drive_service
    from googleapiclient.http import MediaIoBaseDownload
    import io
    HAS_DRIVE = True
except ImportError:
    HAS_DRIVE = False
    print("Warning: Google Drive integration not available. Will use local persona files.")


from core import MinaCoreOrchestrator


def load_persona_from_drive(agent_name: str) -> str:
    """Load persona file from Google Drive."""
    if not HAS_DRIVE:
        raise RuntimeError("Google Drive not available")
    
    try:
        service = get_drive_service()
        query = f"name contains '{agent_name}_Setup.md' and trashed = false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get('files', [])
        
        if not files:
            raise FileNotFoundError(f"Persona file for {agent_name} not found on Drive")
        
        # Get first matching file
        file_id = files[0]['id']
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        
        return fh.getvalue().decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"Failed to load persona from Drive: {e}")


def load_persona_local(agent_name: str) -> str:
    """Load persona file from local agents directory."""
    agents_dir = Path(__file__).parent.parent.parent / "agents"
    persona_file = agents_dir / f"{agent_name.lower()}_agent.md"
    
    if not persona_file.exists():
        raise FileNotFoundError(f"Persona file not found: {persona_file}")
    
    return persona_file.read_text(encoding='utf-8')


def load_all_personas(use_drive: bool = False) -> dict:
    """Load all agent personas."""
    personas = {}
    agent_names = ["Mina", "Mila", "Misa", "Mita"]
    
    for agent_name in agent_names:
        try:
            if use_drive and HAS_DRIVE:
                personas[agent_name] = load_persona_from_drive(agent_name)
            else:
                personas[agent_name] = load_persona_local(agent_name)
            print(f"✓ Loaded persona for {agent_name}")
        except Exception as e:
            print(f"⚠ Warning: Could not load persona for {agent_name}: {e}")
            # Use default description
            personas[agent_name] = f"Agent {agent_name} - Default persona"
    
    return personas


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="MINA MVP-0 - Multi-agent reasoning system"
    )
    parser.add_argument(
        "--task",
        type=str,
        required=True,
        help="User task/question for agents to reason about"
    )
    parser.add_argument(
        "--memory-file",
        type=str,
        default="data/memory.jsonl",
        help="Path to memory storage file"
    )
    parser.add_argument(
        "--max-loops",
        type=int,
        default=5,
        help="Maximum reasoning loops"
    )
    parser.add_argument(
        "--use-drive",
        action="store_true",
        help="Load personas from Google Drive (requires credentials)"
    )
    parser.add_argument(
        "--user-mode",
        action="store_true",
        default=True,
        help="Yes-User mode (user actively participating)"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="Gemini API key (or set GEMINI_API_KEY env var)"
    )
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY not set. Set it via --api-key or environment variable.")
        sys.exit(1)
    
    print("=" * 60)
    print("MINA MVP-0 - Multi-Agent Reasoning System")
    print("=" * 60)
    print()
    
    # Load personas
    print("Loading agent personas...")
    personas = load_all_personas(use_drive=args.use_drive)
    print()
    
    # Initialize orchestrator
    print("Initializing MINA Core orchestrator...")
    orchestrator = MinaCoreOrchestrator(
        memory_file=args.memory_file,
        max_loops=args.max_loops,
        api_key=api_key
    )
    
    # Load personas into agents
    orchestrator.load_agent_personas(personas)
    print("✓ Orchestrator ready")
    print()
    
    # Start reasoning
    print(f"User task: {args.task}")
    print("-" * 60)
    print()
    
    result = orchestrator.reason(
        user_input=args.task,
        available_data={},  # Can be extended with actual data
        user_mode=args.user_mode
    )
    
    # Display results
    print("\n" + "=" * 60)
    print("REASONING RESULTS")
    print("=" * 60)
    print()
    
    # Show agent responses
    for i, resp in enumerate(result["responses"], 1):
        print(f"[{i}] {resp['agent_name']}:")
        print(f"    {resp['content']}")
        if resp.get('confidence'):
            print(f"    Confidence: {resp['confidence']:.2f}")
        print()
    
    # Show summary
    print("-" * 60)
    print("SUMMARY:")
    print(result["summary"])
    print()
    
    # Show loop detection
    loop_info = result["loop_detection"]
    if loop_info["is_loop"]:
        print("⚠️  LOOP DETECTED:")
        print(f"   Agents in loop: {', '.join(loop_info['loop_agents'])}")
        print(f"   Recommendation: {loop_info['recommendation']}")
        print()
    
    # Show if user input needed
    if result["requires_user_input"]:
        print("🔔 USER INPUT REQUIRED")
        print("   System needs human intervention to continue.")
        print()
    
    print(f"Total loops: {result['loop_count']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
