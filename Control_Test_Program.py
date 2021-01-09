# -*- coding=utf-8 -*-
import os

test_program_name = "Hyperion"
run_test_cmd = """
        osascript -e '
        tell application "System Events"
	        tell process """ + str(test_program_name) + """
		        click button "Start" of window 1 of application process """ + str(test_program_name) + """ of application "System Events"
	        end tell
        end tell
        '
      """


os.system(run_test_cmd)
