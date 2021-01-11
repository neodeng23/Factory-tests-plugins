# -*- coding=utf-8 -*-
import os

test_program_name = "Hyperion"
run_test_cmd = """
        osascript -e '
        tell application "System Events"
	        tell process "Hyperion"
		        click button "Start" of window 1 of application process "Hyperion" of application "System Events"
	        end tell
        end tell
        '
      """


os.system(run_test_cmd)
