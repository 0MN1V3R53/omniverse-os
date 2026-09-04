import webbrowser
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
montway_path = os.path.join(base_dir, 'montway_layout', 'index.html')
sherpa_path = os.path.join(base_dir, 'sherpa_layout', 'index.html')

print(f"Opening Montway Layout: {montway_path}")
webbrowser.open(f"file://{montway_path}")

print(f"Opening Sherpa Layout: {sherpa_path}")
webbrowser.open(f"file://{sherpa_path}")
