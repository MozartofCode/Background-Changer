#!/usr/bin/env python
import sys
from background.crew import BackgroundCrew

def run():
    """
    Run the crew.
    """
    inputs = {
        'input': 'I wish I could be by a beautiful forest around big, green trees today',
        'folder_path': 'wallpapers'
    }
    BackgroundCrew().crew().kickoff(inputs=inputs)