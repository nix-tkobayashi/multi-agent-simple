import os
import json

def generate_config():
    """
    Dynamically generates the claude_config.json file by scanning
    the 'agents' directory for agent configurations.
    It reads server settings from 'agent.json' and the role prompt
    from 'CLAUDE.md' for each agent.
    """
    agents_dir = 'agents'
    config_data = {"mcpServers": {}}

    if not os.path.exists(agents_dir):
        print(f"Error: Directory '{agents_dir}' not found.")
        return

    for agent_name in os.listdir(agents_dir):
        agent_dir = os.path.join(agents_dir, agent_name)
        config_file = os.path.join(agent_dir, 'agent.json')
        role_file = os.path.join(agent_dir, 'CLAUDE.md')

        if os.path.isdir(agent_dir) and os.path.exists(config_file) and os.path.exists(role_file):
            try:
                # Read server config
                with open(config_file, 'r', encoding='utf-8') as f:
                    agent_config = json.load(f)

                # Read role definition
                with open(role_file, 'r', encoding='utf-8') as f:
                    claude_role = f.read()

                # Combine config
                # agent.json 側の cwd を優先し、なければデフォルトを設定
                agent_config['cwd'] = agent_config.get('cwd', f'./agents/{agent_name}')

                # 既存のenvがあればマージし、CLAUDE_ROLEのみ上書き
                existing_env = agent_config.get('env', {})
                agent_config['env'] = {**existing_env, 'CLAUDE_ROLE': claude_role}
                
                config_data["mcpServers"][agent_name] = agent_config
                print(f"Loaded config for agent: {agent_name}")

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {config_file}: {e}")
            except Exception as e:
                print(f"Error processing agent '{agent_name}': {e}")

    output_file = 'claude_config.json'
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        print(f"Successfully generated '{output_file}' with {len(config_data['mcpServers'])} agents.")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

if __name__ == "__main__":
    generate_config() 