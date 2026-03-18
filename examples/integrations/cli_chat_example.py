"""
CLI Chat integration example for fraq.

Interactive command-line chat with fraq data generation.
"""

from __future__ import annotations

import cmd
import json

from fraq import generate, stream, FraqSchema


class FraqChat(cmd.Cmd):
    """Interactive CLI for fraq operations."""
    
    intro = """
╔═══════════════════════════════════════════╗
║     🌀 Fraq Interactive Chat Shell        ║
╚═══════════════════════════════════════════╝

Type 'help' for commands or 'quit' to exit.
"""
    prompt = "fraq> "
    
    def __init__(self):
        super().__init__()
        self.current_schema = FraqSchema()
        self.last_results = []
    
    def do_generate(self, arg: str) -> None:
        """Generate data: generate <field:type> [count=N]"""
        args = arg.split()
        if not args:
            print("Usage: generate field1:type1 [field2:type2] [count=N]")
            print("Example: generate temp:float:0-100 hum:float count=50")
            return
        
        fields = {}
        count = 10
        
        for a in args:
            if a.startswith("count="):
                count = int(a.split("=")[1])
            elif ":" in a:
                name, type_spec = a.split(":", 1)
                fields[name] = type_spec
        
        if not fields:
            print("No fields specified")
            return
        
        print(f"Generating {count} records...")
        records = generate(fields, count=count, seed=42)
        self.last_results = records
        
        # Display first few
        for i, r in enumerate(records[:5]):
            print(f"  {i+1}: {r}")
        
        if len(records) > 5:
            print(f"  ... and {len(records) - 5} more")
    
    def do_stream(self, arg: str) -> None:
        """Stream data: stream [count=N] [interval=0.1]"""
        count = 10
        interval = 0.5
        
        for a in arg.split():
            if a.startswith("count="):
                count = int(a.split("=")[1])
            elif a.startswith("interval="):
                interval = float(a.split("=")[1])
        
        print(f"Streaming {count} records (interval={interval}s)...")
        
        for i, record in enumerate(stream({"value": "float"}, count=count, interval=interval)):
            print(f"  [{i+1}] {record}")
        
        print("Stream complete")
    
    def do_schema(self, arg: str) -> None:
        """Show current schema or add field: schema [field:type]"""
        if arg:
            if ":" in arg:
                name, type_spec = arg.split(":", 1)
                self.current_schema.add_field(name, type_spec)
                print(f"Added field: {name} ({type_spec})")
            else:
                print(f"Invalid format. Use: field:type")
        else:
            # Show schema
            if self.current_schema.fields:
                print("Current schema:")
                for f in self.current_schema.fields:
                    print(f"  - {f.name}: {f.type}")
            else:
                print("No fields in schema")
    
    def do_save(self, arg: str) -> None:
        """Save last results: save <filename>"""
        if not arg:
            print("Usage: save <filename>")
            return
        
        if not self.last_results:
            print("No results to save. Generate some data first.")
            return
        
        filename = arg if arg.endswith(".json") else f"{arg}.json"
        
        with open(filename, "w") as f:
            json.dump(self.last_results, f, indent=2)
        
        print(f"Saved {len(self.last_results)} records to {filename}")
    
    def do_stats(self, arg: str) -> None:
        """Show statistics for last results"""
        if not self.last_results:
            print("No results. Generate data first.")
            return
        
        # Simple stats
        if self.last_results:
            keys = self.last_results[0].keys()
            print(f"Records: {len(self.last_results)}")
            print(f"Fields: {', '.join(keys)}")
            
            # Numeric field stats
            for key in keys:
                values = [r.get(key) for r in self.last_results if isinstance(r.get(key), (int, float))]
                if values:
                    avg = sum(values) / len(values)
                    print(f"  {key}: min={min(values):.2f}, max={max(values):.2f}, avg={avg:.2f}")
    
    def do_quit(self, arg: str) -> bool:
        """Exit the shell"""
        print("Goodbye! 👋")
        return True
    
    def do_EOF(self, arg: str) -> bool:
        """Exit on Ctrl+D"""
        return self.do_quit(arg)
    
    def emptyline(self) -> None:
        """Do nothing on empty line"""
        pass


def main():
    """Run CLI chat."""
    FraqChat().cmdloop()


if __name__ == "__main__":
    main()
