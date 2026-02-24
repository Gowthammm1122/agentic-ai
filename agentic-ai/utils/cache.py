import hashlib
import json
import os

CACHE_DIR = ".agent_cache"

def get_cache_key(node_name, inputs):
    # Create a stable string representation of inputs
    input_str = json.dumps(inputs, sort_keys=True)
    combined = f"{node_name}:{input_str}"
    return hashlib.sha256(combined.encode()).hexdigest()

def get_cached_result(node_name, inputs):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    
    key = get_cache_key(node_name, inputs)
    cache_path = os.path.join(CACHE_DIR, f"{key}.json")
    
    if os.path.exists(cache_path):
        with open(cache_path, "r") as f:
            return json.load(f)
    return None

def set_cached_result(node_name, inputs, result):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    
    key = get_cache_key(node_name, inputs)
    cache_path = os.path.join(CACHE_DIR, f"{key}.json")
    
    with open(cache_path, "w") as f:
        json.dump(result, f)

def agent_cache(func):
    """Decorator to cache agent node outputs based on their specific input keys."""
    def wrapper(state):
        # We only cache based on titles and goals to avoid caching everything (like previous node outputs)
        # unless necessary. For nodes that depend on previous outputs, we include those in the signature.
        node_name = func.__name__
        
        # Decide which state keys matter for this node
        cache_context = {k: state.get(k) for k in ["title", "goals", "feedback", "purpose", "flow"]}
        
        cached = get_cached_result(node_name, cache_context)
        if cached:
            print(f"🔄 [Cache Hit] {node_name}")
            return cached
            
        print(f"🤖 [Agent Call] {node_name}")
        result = func(state)
        
        # Don't cache error/resting messages
        if isinstance(result, dict):
            # Check for resting message in dict values
            if any("The AI is currently resting" in str(v) for v in result.values()):
                return result
        elif "The AI is currently resting" in str(result):
            return result
            
        set_cached_result(node_name, cache_context, result)
        return result
    return wrapper
