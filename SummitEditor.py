from subprocess import Popen, PIPE, call

import os
import sublime_plugin


class SummitBuild(sublime_plugin.WindowCommand):

    def run(self, **kwargs):
        v = self.window.active_view()

        file_path = v.file_name()

        file_dir = os.path.abspath(os.path.join(file_path, '../'))
        print(file_dir)
        file_parent_dir = os.path.abspath(os.path.join(file_path, '../..'))

        print(os.path.exists(os.path.join(file_dir, 'main.lua')))
        print(os.path.exists(os.path.join(file_parent_dir, 'main.lua')))

        tar_process = Popen(
            ['tar', '--cz', '--exclude .git', '/home/tkells/dev/summit_apps/tjtest']
            , stdout=PIPE
        )
        ssh_process = Popen(
            ['ssh', '-q', 'summitdebug@lunaapp1.dev1.int.corvisacloud.com']
            , stdin=tar_process.stdout
            , stdout=PIPE
        )

        out, err = ssh_process.communicate()
        print(out, err)
        print(out, err)
